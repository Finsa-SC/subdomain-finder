import socket
from request import http_request, https_request
import requests


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