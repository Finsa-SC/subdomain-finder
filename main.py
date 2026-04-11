from xxlimited_35 import Null

import requests
import socket

def check_subdomain(domain, time_out:float, show_available: bool = False):
    print(f"Search for subdomain for {domain}")

    url = f"https://api.hackertarget.com/hostsearch/?q={domain}"
    response = requests.get(url=url)

    if response.status_code != 200:
        print("[!] Failed to access Hacker Target API")
        return

    lines = response.text.strip().split("\n")
    subdomain = [line.split(",")[0] for line in lines]

    print(f"[*]Finding {len(subdomain)} potential hosts, starting validation\n")

    host_up = 0
    for sub in subdomain:
        try:
            try:
                ip_address = socket.gethostbyname(sub)
            except socket.gaierror:
                ip_address = "No IP"

            sub_url = f"http://{sub}"
            res = requests.get(url=sub_url, timeout=time_out)

            status = res.status_code
            if status == 200:
                print(f"[+] {sub: <40} | {ip_address: <15} | Status: {status} (OK)")
                host_up+=1
            elif not show_available:
                if status == 403 and not show_available:
                    print(f"[!] {sub: <40} | {ip_address: <15} | Status: {status} Forbidden")
                else:
                    print(f"[-] {sub: <40} | {ip_address: <15} | Status: {status}")
        except requests.exceptions.RequestException:
            pass

    print(f"{host_up} Host UP (↑)")

if __name__ == "__main__":
    domain_name = input("Domain name input: ").strip()
    if not domain_name:
        print("Domain name required!")
        exit(1)
    timeout_input = input("Timeout: ").strip()
    show_available_host = input("Show only available host? [y/N]: ").lower().strip()
    try:
        timeout = float(timeout_input) if timeout_input else 3.0
    except ValueError:
        print("Invalid Timeout; Using default 3.0")
        timeout = 3.0

    show_available = show_available_host == "y"
    check_subdomain(domain_name, timeout, show_available)
