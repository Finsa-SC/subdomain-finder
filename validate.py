from output import sign, show_output, show_quiet
from request import http_request, https_request
from save_file import save_file_healthy, save_file_problem, check_result_dir, save_file_as_json
from scan_config import ScanConfig
from summary import ReconStats

from concurrent.futures import ThreadPoolExecutor
import os
import tldextract
import socket
import requests


stats = ReconStats()

def validate_subdomain(sub, config: ScanConfig, wildcard_baseline):
    try:
        try:
            ip_address = socket.gethostbyname(sub)
        except socket.gaierror:
            ip_address = "No IP"

        dict_http = http_request(sub, config.timeout)
        dict_https = https_request(sub, config.timeout)

        h = dict_http if dict_http else {}
        s = dict_https if dict_https else {}

        timestamp = h.get("timestamp") or s.get("timestamp")

        http_status = h.get("http_status")
        http_server = h.get("http_server", "Unknown")
        http_latency = h.get("http_latency")
        http_content = h.get("length", b"")
        http_redir = h.get("location", "-")

        https_status = s.get("https_status")
        https_server = s.get("https_server", "Unknown")
        https_latency = s.get("https_latency")
        https_content = s.get("length", b"")
        https_redir = s.get("location", "-")


        ##Validate Wildcard
        baselines = wildcard_baseline
        is_wildcard = False
        if baselines["http"]:
            if baselines["http"]["status"] == 200 and baselines["http"]["size"] == http_content:
                is_wildcard = True
        if is_wildcard and config.no_wildcard:
            return None, None, None



        signing = sign(http_status, https_status, is_wildcard)

        server = http_server if http_status != None else https_server

        sub_info = {
            "server": server,
            "signing": signing,
            "subdomain": sub,
            "http_status": http_status,
            "https_status": https_status,
            "ip_address": ip_address,
            "http_latency": http_latency,
            "https_latency": https_latency,
            "show_available": config.available,
            "show_verbose": config.verbose,
            "show_redir": config.redirect,
            "http_redir": http_redir,
            "https_redir": https_redir
        }
        dict_info = {
            "timestamp": timestamp,
            "subdomain": sub,
            "ip_address": ip_address,
            "status": {
                "http": http_status,
                "https": https_status
            },
            "server": server,
            "latency": {
                "http": http_latency,
                "https": https_latency
            },
            "redirect": {
                "http": http_redir,
                "https": https_redir
            },
            "size": {
                "http": len(http_content) if http_content else 0,
                "https": len(https_content) if https_content else 0
            },
            "posible_wildcard": is_wildcard
        }

        status_ok = 200 in [http_status, https_status]
        if config.quiet:
            show_quiet(is_okay=status_ok, sub=sub, ip=ip_address, show_ip=config.quiet_ip)
        else:
            show_output(sub_info)
        stats.log(http_status, https_status)
        return status_ok, ip_address, dict_info

    except requests.exceptions.RequestException:
        return False, "No IP", None
    except Exception as e:
        print(f"Error: {sub} -> {e}")
        return False, "No IP", None


def check_subdomain(domain: str, config: ScanConfig):
    healthy_ip = set()
    problem_ip = set()

    print("validate as file")
    if os.path.isfile(domain):
        with open(domain, "r")as f:
            raw_data = f.read()
    elif "." in domain and not domain.endswith(".txt"):
        print(f"Search for subdomain for {domain}")
        url = f"https://api.hackertarget.com/hostsearch/?q={domain}"
        response = requests.get(url=url)

        if "error" in response.text.lower():
            print(f"[x] Error occurred: {response.text}")
            exit(1)
        if response.status_code != 200:
            print("[x] Failed to access Hacker Target API")
            exit(1)
        raw_data = response.text
    else:
        print("[x] Invalid Domain")
        exit(0)

    lines = raw_data.strip().split("\n")

    subdomain = [line.split(",")[0] for line in lines]

    print(f"[*]Found {len(subdomain)} potential hosts, starting validation\n")

    wildcard_baseline = check_wildcard(get_domain_root(subdomain[0]))

    try:
        with ThreadPoolExecutor(max_workers=config.thread) as executor:
            futures = [executor.submit(validate_subdomain, s, config, wildcard_baseline) for s in subdomain]

        sub_list = []
        for future in futures:
            is_ok, ip, dict_sub = future.result()
            if ip != "No IP":
                if is_ok:
                    healthy_ip.add(ip)
                else:
                    problem_ip.add(ip)
            if dict_sub:
                sub_list.append(dict_sub)

        if config.save_file_plain:
            root = get_domain_root(subdomain[0])
            check_result_dir()
            save_file_healthy(root, healthy_ip)
            save_file_problem(root, problem_ip)
        if config.save_file_json:
            check_result_dir()
            root = get_domain_root(subdomain[0])
            save_file_as_json(root, sub_list)

        stats.summary()

    except KeyboardInterrupt:
        print("\n[!]Process stop by user...")
        exit(0)


def get_domain_root(full_domain: str):
    root = tldextract.extract(full_domain)
    return f"{root.domain}.{root.suffix}"

def check_wildcard(domain: str):
    wild_sub = f"{os.urandom(2).hex()}.{domain}"
    baselines = {"http": None, "https": None}
    try:
        res = requests.get(f"http://{wild_sub}", timeout=5, allow_redirects=False)
        wild_status = res.status_code
        wild_size = len(res.content)
        baselines["http"] = {"status": wild_status, "size": wild_size}
    except:
        ...
    try:
        res = requests.get(f"https://{wild_sub}", allow_redirects=False, timeout=5, verify=False)
        wild_status = res.status_code
        wild_size = len(res.content)
        baselines["https"] = {"status": wild_status, "size": wild_size}
    except:
        ...
    return baselines