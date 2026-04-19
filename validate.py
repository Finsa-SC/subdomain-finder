from output import sign, show_output
from concurrent.futures import ThreadPoolExecutor
import os
import tldextract

import socket
from request import http_request, https_request
import requests

from save_file import save_file_healthy, save_file_problem, check_result_dir
from scan_config import ScanConfig


def validate_subdomain(sub, config: ScanConfig, wildcard_baseline):
    try:
        try:
            ip_address = socket.gethostbyname(sub)
        except socket.gaierror:
            ip_address = "No IP"

        http_status, http_server, http_redir, http_latency, http_content = http_request(sub, config.timeout)
        https_status, https_server, https_redir, https_latency, https_content = https_request(sub, config.timeout)

        ##Validate Wildcard
        baselines = wildcard_baseline
        is_wildcard = False
        if baselines["http"]:
            if baselines["http"]["status"] == 200 and baselines["http"]["size"] == http_content:
                is_wildcard = True
        if is_wildcard and config.no_wildcard:
            return None, None



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

        show_output(sub_info)
        return 200 in [http_status, https_status], ip_address

    except requests.exceptions.RequestException:
        return False, "No IP"
    except Exception as e:
        print(f"Error: {sub} -> {e}")
        return False, "No IP"


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

        for future in futures:
            is_ok, ip = future.result()
            if ip != "No IP":
                if is_ok:
                    healthy_ip.add(ip)
                else:
                    problem_ip.add(ip)

        if config.save_file:
            root = get_domain_root(subdomain[0])
            check_result_dir()
            save_file_healthy(root, healthy_ip)
            save_file_problem(root, problem_ip)

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