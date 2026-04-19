from Tools.scripts.mkreal import join
from typing import Any, Mapping

def sign(http_status, https_status, is_wildcard) -> str:
    if is_wildcard:
        return "[?]"
    elif http_status == 200 or https_status == 200:
        return "[*]"
    elif http_status == 403 or https_status == 403:
        return "[!]"
    else:
        return "[-]"

def show_verbose(http_status, https_status, show_redir=False, http_redir=None, https_redir=None, is_verbose: bool = False) -> str:
    if is_verbose:
        status = []
        if http_status == 200 and https_status != 200:
            status.append("HTTP ONLY")
        if https_status == 200 and http_status != 200:
            status.append("HTTPS ONLY")
        if https_status == 200 and http_status == 200:
            status.append("HTTP and HTTPS")
        if http_status == 403:
            status.append("HTTP FORBIDDEN")
        if https_status == 403:
            status.append("HTTPS FORBIDDEN")
        if show_redir:
            if http_redir and http_redir not in ["-", "None"]:
                status.append(f"HTTP REDIR: {http_redir}")
            if https_redir and https_redir not in ["-", "None"]:
                status.append(f"HTTPS REDIR: {https_redir}")

    else:
        status = "(OK)" if http_status == 200 or https_status == 200 else "[!Forbidden]" if http_status == 403 or https_status == 403 else ""
    if status:
        return f"[ {', '.join(status)} "
    return ""

def show_output(sub_info: Mapping[str, Any]):
    server = sub_info["server"]
    sub = sub_info["subdomain"]
    http_status = sub_info["http_status"]
    https_status = sub_info["https_status"]
    signing = sub_info["signing"]
    http_latency = sub_info["http_latency"]
    https_latency = sub_info["http_latency"]
    ip_address = sub_info["ip_address"]
    show_available = sub_info["show_available"]

    is_verbose = sub_info["show_verbose"]
    show_redir = sub_info["show_redir"]
    http_redir = sub_info["http_redir"]
    https_redir = sub_info["https_redir"]

    status = show_verbose(http_status, https_status, show_redir, http_redir, https_redir, is_verbose)


    if server == None:
        return
    elif http_status == 200 or sub_info["https_status"] == 200:
        print(f"{sub_info['signing']} {sub: <40} | {sub_info['ip_address']: <15} | {sub_info['server']: <15} | "
              f"HTTP: {str(http_status or '-'): <3} ({f'{http_latency}ms)' if http_latency else 'N/A)': <7} | "
              f"HTTPS: {str(https_status or '-'): <3} ({f'{https_latency}ms)' if https_latency else 'N/A)': <7} {status}")
        return True, ip_address

    elif not show_available:
        print(f"{signing} {sub: <40} | {ip_address: <15} | {server: <15} | "
              f"HTTP: {str(http_status or '-'): <3} ({f'{http_latency}ms)' if http_latency else 'N/A)': <7} | "
              f"HTTPS: {str(https_status or '-'): <3} ({f'{https_latency}ms)' if https_latency else 'N/A)': <7} {status}")
        return False, ip_address
    return