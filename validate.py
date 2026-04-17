from output import sign, show_output
from concurrent.futures import ThreadPoolExecutor
from main import THREAD

import socket
from request import http_request, https_request
import requests

healthy_ip = set()
problem_ip = set()

def validate_subdomain(sub, time_out, show_available, show_verbose, show_redir):
    try:
        try:
            ip_address = socket.gethostbyname(sub)
        except socket.gaierror:
            ip_address = "No IP"

        http_status, http_server, http_redir, http_latency = http_request(sub, time_out)
        https_status, https_server, https_redir, https_latency = https_request(sub, time_out)

        signing = sign(http_status, https_status)

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
            "show_available": show_available,
            "show_verbose": show_verbose,
            "show_redir": show_redir,
            "http_redir": http_redir,
            "https_redir": https_redir,
        }

        show_output(sub_info)


    except requests.exceptions.RequestException:
        return 0


def check_subdomain(domain, time_out:float, show_available: bool = False, show_verbose: bool = False, show_redir: bool = False):
    if ".txt" not in domain:
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
        with open(domain, "r")as f:
            raw_data = f.read()

    lines = raw_data.strip().split("\n")

    subdomain = [line.split(",")[0] for line in lines]

    print(f"[*]Found {len(subdomain)} potential hosts, starting validation\n")

    host_up_count = 0

    try:
        with ThreadPoolExecutor(max_workers=THREAD) as executor:
            executor.map(lambda s: validate_subdomain(s, time_out, show_available, show_verbose, show_redir), subdomain)

    except KeyboardInterrupt:
        print("\n[!]Process stop by user...")
        exit(0)

    print(f"{host_up_count} Host UP (↑)")
