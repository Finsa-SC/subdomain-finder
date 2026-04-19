import requests
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def http_request(sub, time_out):
    try:
        sub_url = f"http://{sub}"
        res = requests.get(url=sub_url, timeout=time_out, allow_redirects=False, verify=False)
        http_dict = {
            "http_status": res.status_code,
            "http_server": res.headers.get('Server', 'Unknown'),
            "location": res.headers.get("Location", "-"),
            "http_latency": int(res.elapsed.total_seconds() * 1000),
            "length": res.content,
            "timestamp": res.headers.get('Date')
        }
        return http_dict
    except requests.exceptions.RequestException:
        return None

def https_request(sub, time_out):
    try:
        sub_url = f"https://{sub}"
        res = requests.get(url=sub_url, timeout=time_out, allow_redirects=False, verify=False)
        https_dict = {
            "https_status": res.status_code,
            "https_server": res.headers.get('Server', 'Unknown'),
            "location": res.headers.get("Location", "-"),
            "https_latency": int(res.elapsed.total_seconds() * 1000),
            "length": res.content,
            "timestamp": res.headers.get('Date')
        }
        return https_dict

    except requests.exceptions.RequestException:
        return None