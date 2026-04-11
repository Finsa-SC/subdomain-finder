from logging import NullHandler

import requests

def check_subdomain(domain, time_out:float):
    print(f"Search for subdomain for {domain}")

    url = f"https://api.hackertarget.com/hostsearch/?q={domain}"
    response = requests.get(url=url)

    if response.status_code != 200:
        print("[!] Failel to access Hacker Target API")
        return

    lines = response.text.strip().split("\n")
    subdomain = [line.split(",")[0] for line in lines]

    print(f"[*]Finding {len(subdomain)} potential hosts, starting validation\n")

    for sub in subdomain:
        try:
            sub_url = f"http://{sub}"
            res = requests.get(url=sub_url, timeout=time_out)

            status = res.status_code
            if status == 200:
                print(f"[+] {sub: <40} | Status: {status} (OK)")
            elif status == 403:
                print(f"[!] {sub: <40} | Status: {status} Forbidden")
            else:
                print(f"[-] {sub: <40} | Status: {status}")
        except requests.exceptions.RequestException:
            pass

if __name__ == "__main__":
    domain_name = input("Domain name input: ")
    timeout_input = input("Timeout: ")
    try:
        timeout = float(timeout_input) if timeout_input else 3.0
    except ValueError:
        print("Invalid Timeout; Using default 3.0")
        timeout = 3.0
    check_subdomain(domain_name, timeout)