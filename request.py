import requests
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def http_request(sub, time_out):
    try:
        sub_url = f"http://{sub}"
        res = requests.get(url=sub_url, timeout=time_out, allow_redirects=False, verify=False)
        return res.status_code, res.headers.get('Server', 'Unknown')
    except requests.exceptions.RequestException:
        return None, None

def https_request(sub, time_out):
    try:
        sub_url = f"https://{sub}"
        res = requests.get(url=sub_url, timeout=time_out, allow_redirects=False, verify=False)
        return res.status_code, res.headers.get('Server', 'Unknown')
    except requests.exceptions.RequestException:
        return None, None