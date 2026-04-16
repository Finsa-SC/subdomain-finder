from save_file import save_file_healthy, save_file_problem, check_result_dir
from request import http_request, https_request

from dotenv import load_dotenv
import os
import socket
import requests
from concurrent.futures import ThreadPoolExecutor


### Init env
load_dotenv()
TIMEOUT = float(os.getenv("TIMEOUT", 3.0))
THREAD = int(os.getenv("THREAD", 10))
DEBUG = bool(os.getenv("DEBUG"))

healthy_ip = set()
problem_ip = set()


def sign(http_status, https_status) -> str:
    if http_status == 200 or https_status == 200:
        return "[*]"
    elif http_status == 403 or https_status == 403:
        return "[!]"
    else:
        return "[-]"


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

        if show_verbose:
            status = "[ "
            if http_status == 200 and https_status != 200:
                status += "HTTP ONLY, "
            if https_status == 200 and http_status != 200:
                status += "HTTPS ONLY, "
            if https_status == 200 and http_status == 200:
                status += "HTTP and HTTPS, "
            if http_status == 403:
                status += "HTTP FORBIDDEN, "
            if https_status == 403:
                status += "HTTPS FORBIDDEN"
            if show_redir:
                if "-" != http_redir:
                    status += f"HTTP REDIR: {http_redir}"
                if "-" != https_redir:
                    status += f"HTTPS REDIR: {https_redir}"
            status += " ]"
        else:
            status = "(OK)" if http_status == 200 or https_status == 200 else "[!Forbidden]" if http_status == 403 or https_status == 403 else ""

        if server == None:
            return 0
        elif http_status == 200 or https_status == 200:
            print(f"{signing} {sub: <40} | {ip_address: <15} | {server: <15} | "
                  f"HTTP: {str(http_status or '-'): <3} ({f'{http_latency}ms)' if http_latency else 'N/A)': <7} | "
                  f"HTTPS: {str(https_status or '-'): <3} ({f'{https_latency}ms)' if https_latency else 'N/A)': <7} {status}")
            healthy_ip.add(ip_address)
            return 1
        elif not show_available:
            print(f"{signing} {sub: <40} | {ip_address: <15} | {server: <15} | "
                  f"HTTP: {str(http_status or '-'): <3} ({f'{http_latency}ms)' if http_latency else 'N/A)': <7} | "
                  f"HTTPS: {str(https_status or '-'): <3} ({f'{https_latency}ms)' if https_latency else 'N/A)': <7} {status}")
            problem_ip.add(ip_address)
            return 0
        return 0
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
            result = list(executor.map(lambda s: validate_subdomain(s, time_out, show_available, show_verbose, show_redir), subdomain))
            host_up_count = sum(result)
    except KeyboardInterrupt:
        print("\n[!]Process stop by user...")
        exit(0)

    print(f"{host_up_count} Host UP (↑)")


if __name__ == "__main__":
    if DEBUG:
        check_subdomain("hosts.txt", 3.0, False, True)
        exit(1)

    with open("assets/banner.txt", "r") as file:
        print(file.read())

    domain_name = input("\n\nDomain name input or TXT: ").strip()
    if not domain_name:
        print("Domain name required!")
        exit(1)

    timeout_input = input("Timeout: ").strip()
    show_available_host = input("Show only available host? [y/N]: ").lower().strip()
    show_verbose_output = input("Enable verbose output? (Show detailed headers / protocols)[y/N]: ").lower().strip()

    try:
        timeout = float(timeout_input) if timeout_input else TIMEOUT
    except ValueError:
        print("Invalid Timeout; Using default 3.0")
        timeout = TIMEOUT

    show_available = show_available_host == "y"
    show_verbose = show_verbose_output == "y"

    show_redir_input = False
    if show_verbose:
        show_redir_input = input("Show redirect? targets? [y/N]: ").strip().lower()
    show_redir = show_redir_input == "y"

    check_subdomain(domain_name, timeout, show_available, show_verbose, show_redir)

    write_file = input("Did you want to save the result? [y/N]: ")
    if write_file.lower().strip() == "y":
        check_result_dir()
        save_file_healthy(domain_name, healthy_ip)
        save_file_problem(domain_name, problem_ip)
