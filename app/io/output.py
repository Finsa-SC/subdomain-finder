from typing import Any, Mapping
from urllib.parse import urlparse
from save_file import is_cloudflare

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
    status = []
    if is_verbose:
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
                status.append(f"HTTP REDIR: {clean_redirect(http_redir)}")
            if https_redir and https_redir not in ["-", "None"]:
                status.append(f"HTTPS REDIR: {clean_redirect(https_redir)}")

    else:
        status.append("(OK)" if http_status == 200 or https_status == 200 else "[!Forbidden]" if http_status == 403 or https_status == 403 else "")
    if status:
        return f"[ {', '.join(status)} ]"
    return ""

def show_output(sub_info: Mapping[str, Any]):
    server = sub_info["server"]
    sub = sub_info["subdomain"]
    http_status = sub_info["http_status"]
    https_status = sub_info["https_status"]
    http_title = sub_info["http_title"]
    https_title = sub_info["https_title"]
    signing = sub_info["signing"]
    http_latency = sub_info["http_latency"]
    https_latency = sub_info["https_latency"]
    ip_address = sub_info["ip_address"]
    show_available = sub_info["show_available"]
    show_title = sub_info["show_title"]
    http_tech = sub_info["http_tech"]
    https_tech = sub_info["https_tech"]
    show_tech = sub_info["show_tech"]

    is_verbose = sub_info["show_verbose"]
    show_redir = sub_info["show_redir"]
    http_redir = sub_info["http_redir"]
    https_redir = sub_info["https_redir"]

    status = show_verbose(http_status, https_status, show_redir, http_redir, https_redir, is_verbose)


    h_out = http_status if isinstance(http_status, int) else "-"
    s_out = https_status if isinstance(https_status, int) else "-"

    if server == None:
        return
    elif http_status == 200 or sub_info["https_status"] == 200:
        print(f"{sub_info['signing']} {sub: <40} | {sub_info['ip_address']: <15} | {sub_info['server']: <15} | "
              f"HTTP: {str(h_out): <3} ({f'{http_latency}ms)' if http_latency else 'N/A)': <7} | "
              f"HTTPS: {str(h_out): <3} ({f'{https_latency}ms)' if https_latency else 'N/A)': <7} {status}")

        if show_title:
            print_title(http_title, https_title)
        if show_tech:
            print_tech(http_tech, https_tech)
        return True, ip_address
    elif not show_available:
        print(f"{signing} {sub: <40} | {ip_address: <15} | {server: <15} | "
              f"HTTP: {str(s_out): <3} ({f'{http_latency}ms)' if http_latency else 'N/A)': <7} | "
              f"HTTPS: {str(s_out): <3} ({f'{https_latency}ms)' if https_latency else 'N/A)': <7} {status}")

        if show_title:
            print_title(http_title, https_title)
        if show_tech:
            print_tech(http_tech, https_tech)
        return False, ip_address
    return False, "No IP"


print_ip = []
def show_quiet(is_okay: int, sub: str = None, ip: str= None, show_ip: bool = False):
    if is_okay:
        if show_ip:
            is_reverse = is_cloudflare(ip)
            if ip not in print_ip and not is_reverse:
                print(ip)
                print_ip.append(ip)
        else:
            print(sub)

def print_title(http_title: str, https_title: str):
    ignore_list = ["301 moved permanently", "302 found", "object moved", "welcome to nginx!", "welcome to openresty"]

    def is_valid(title: str):
        if not title and title.strip() in ["-", ""]:
            return False
        if title.lower() in ignore_list or title.lower() in ignore_list:
            return False
        return True

    h = http_title if is_valid(http_title) else None
    s = https_title if is_valid(https_title) else None

    if h == s and h:
        print(f"        |_title: [{h}]")
    else:
        if h:
            print(f"        |_http title : [{h}]")
        if s:
            print(f"        |_https title: {s}")

def print_tech(http_header, https_header):
    target_headers = ["X-Powered-By", "X-Generator", "Server"]

    def get_tech(header):
        found = []
        for h in target_headers:
            val = header.get(h)
            if val and val.strip() not in ["-", "None", ""]:
                found.append(val)
        return ", ".join(found) if found else None

    h_tech = get_tech(http_header)
    s_tech = get_tech(https_header)

    if h_tech == s_tech and h_tech:
        print(f"        |_Tech      : {h_tech}")
    else:
        if h_tech:
            print(f"        |_http Tech : {h_tech}")
        elif s_tech:
            print(f"        |_https Tech: {s_tech}")

def clean_redirect(url, max_len: int = 30):
    if not url or url in ["-", "None"]:
        return None
    parsed = urlparse(url)
    target = parsed.netloc if parsed.netloc else parsed.path

    if not parsed.netloc and parsed.path:
        target = parsed.path

    if len(target) > max_len:
        return target[:max_len-3] + "..."
    return target