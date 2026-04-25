from pathlib import Path
from typing import Any, Mapping
from urllib.parse import urlparse
from utils import is_cloudflare
from models import scan_config


# ANSI Colors (Soft/Standard)
RESET = "\033[0m"
LIME = "\033[38;5;112m"
YELLOW = "\033[33m"
WHITE = "\033[37m"
CYAN   = "\033[36m"
DIM = "\033[2m"

def colorize(text: Any, color_code: str):
    return f"{color_code}{text}{RESET}"

def print_legend():
    print(f"""
        [ LEGEND ]
        {colorize("[+]", LIME)} : Host is UP (HTTP/HTTPS 200)
        {colorize("[!]", YELLOW)} : Access Forbidden (403)
        {colorize("[?]", CYAN)} : Wildcard Subdomain Detected
        {colorize("[-]", WHITE)} : Host is Down / Other Status
        """)

def sign(http_status, https_status, is_wildcard) -> str:
    config = scan_config.current
    if is_wildcard:
        return colorize("[?]", CYAN if config.color else WHITE)
    elif http_status == 200 or https_status == 200:
        return colorize("[+]", LIME if config.color else WHITE)
    elif http_status == 403 or https_status == 403:
        return colorize("[!]", YELLOW if config.color else WHITE)
    else:
        return colorize("[-]", WHITE)

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
    config = scan_config.current
    server = sub_info["server"]
    sub = sub_info["subdomain"]
    http_status = sub_info["http_status"]
    https_status = sub_info["https_status"]
    http_title = sub_info["http_title"]
    https_title = sub_info["https_title"]
    is_wildcard = sub_info["is_wildcard"]
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


    # Set Color
    if not config.color:
        color = WHITE
    elif is_wildcard:
        color = CYAN
    elif 200 in [http_status, https_status]:
        color = LIME
    elif 403 in [http_status, https_status]:
        color = YELLOW
    else:
        color = WHITE

    h_out = http_status if isinstance(http_status, int) else "-"
    s_out = https_status if isinstance(https_status, int) else "-"

    status = show_verbose(http_status, https_status, show_redir, http_redir, https_redir, is_verbose)

    output_line = (f"{sub: <40} | {ip_address: <15} | {server: <15} | "
              f"HTTP: {str(h_out): <3} ({f'{http_latency}ms)' if http_latency else 'N/A)': <7} | "
              f"HTTPS: {str(s_out): <3} ({f'{https_latency}ms)' if https_latency else 'N/A)': <7} {status}")

    if server == None:
        return
    elif http_status == 200 or sub_info["https_status"] == 200:
        print(f"{sub_info['signing']} {colorize(output_line, color)}")

        if show_title:
            print_title(http_title, https_title, color)
        if show_tech:
            print_tech(http_tech, https_tech, color)
        return True, ip_address
    elif not show_available:
        print(f"{sub_info['signing']} {colorize(output_line, color)}")

        if show_title:
            print_title(http_title, https_title, color)
        if show_tech:
            print_tech(http_tech, https_tech, color)
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

def print_title(http_title: str, https_title: str, color):
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
        print(colorize(f"        |_title: [{h}]", color))
    else:
        if h:
            print(colorize(f"        |_http title : [{h}]", color))
        if s:
            print(colorize(f"        |_https title: {s}", color))

def print_tech(http_header, https_header, color):
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
        print(colorize(f"        |_Tech      : {h_tech}", color))
    else:
        if h_tech:
            print(colorize(f"        |_http Tech : {h_tech}", color))
        elif s_tech:
            print(colorize(f"        |_https Tech: {s_tech}", color))

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

def print_banner():
    base_path = Path(__file__).resolve().parent.parent.parent
    banner_path = base_path / "assets" / "banner.txt"
    try:
        with open(banner_path, "r") as f:
            print(f.read())
    except FileNotFoundError:
        print("Banner file not found!!")