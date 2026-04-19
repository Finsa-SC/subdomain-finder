import requests
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def http_request(sub, time_out):
    try:
        sub_url = f"http://{sub}"
        res = requests.get(url=sub_url, timeout=time_out, allow_redirects=False, verify=False)
        status_code = res.status_code
        server = res.headers.get('Server', 'Unknown')
        location = res.headers.get("Location", "-")
        latency = int(res.elapsed.total_seconds() * 1000)
        length = res.content
        return status_code, server, location, latency, length
    except requests.exceptions.RequestException:
        return None, None, None, None, None

def https_request(sub, time_out):
    try:
        sub_url = f"https://{sub}"
        res = requests.get(url=sub_url, timeout=time_out, allow_redirects=False, verify=False)
        status_code = res.status_code
        server = res.headers.get('Server', 'Unknown')
        location = res.headers.get("Location", "-")
        latency = int(res.elapsed.total_seconds() * 1000)
        length = res.content
        return status_code, server, location, latency, length

    except requests.exceptions.RequestException:
        return None, None, None, None, None