import requests
import socket
from concurrent.futures import ThreadPoolExecutor

def validate_subdomain(sub, time_out, show_available):

    try:
        try:
            ip_address = socket.gethostbyname(sub)
        except socket.gaierror:
            ip_address = "No IP"
        sub_url = f"http://{sub}"
        res = requests.get(url=sub_url, timeout=time_out)

        status = res.status_code
        server = res.headers.get('Server', 'Unknown')
        if status == 200:
            print(f"[+] {sub: <40} | {ip_address: <15} | {server} | Status: {status} (OK)")
            return 1
        elif not show_available:
            if status == 403 and not show_available:
                print(f"[!] {sub: <40} | {ip_address: <15} | {server} | Status: {status} Forbidden")
            else:
                print(f"[-] {sub: <40} | {ip_address: <15} | {server} | Status: {status}")
        return 0
    except requests.exceptions.RequestException:
        return 0




def check_subdomain(domain, time_out:float, show_available: bool = False):
    print(f"Search for subdomain for {domain}")

    url = f"https://api.hackertarget.com/hostsearch/?q={domain}"
    response = requests.get(url=url)

    if response.status_code != 200:
        print("[!] Failed to access Hacker Target API")
        return

    lines = response.text.strip().split("\n")
    subdomain = [line.split(",")[0] for line in lines]

    print(f"[*]Found {len(subdomain)} potential hosts, starting validation\n")

    host_up_count = 0

    try:
        with ThreadPoolExecutor(max_workers=10) as executor:
            result = list(executor.map(lambda s: validate_subdomain(s, time_out, show_available), subdomain))
            host_up_count = sum(result)
    except KeyboardInterrupt:
        print("\n[!]Process stop by user...")
        exit(0)

    print(f"{host_up_count} Host UP (↑)")


if __name__ == "__main__":
    with open("assets/banner.txt", "r") as file:
        print(file.read())

    domain_name = input("\n\nDomain name input: ").strip()
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