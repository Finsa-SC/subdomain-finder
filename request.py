import requests
import urllib3
import re

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def http_request(sub, time_out):
    try:
        sub_url = f"http://{sub}"
        res = requests.get(url=sub_url, timeout=time_out, allow_redirects=False, verify=False)
        http_dict = {
            "http_title": get_html_title(res.text),
            "http_status": res.status_code,
            "http_server": res.headers.get('Server', 'Unknown'),
            "location": res.headers.get("Location", "-"),
            "http_latency": int(res.elapsed.total_seconds() * 1000),
            "length": len(res.content),
            "timestamp": res.headers.get('Date')
        }
        return http_dict
    except requests.exceptions.SSLError:
        return {"http_status": "SSL_ERR"}
    except requests.exceptions.RequestException:
        return {"http_status": "CONN_ERR"}

def https_request(sub, time_out):
    try:
        sub_url = f"https://{sub}"
        res = requests.get(url=sub_url, timeout=time_out, allow_redirects=False, verify=False)
        https_dict = {
            "https_title": get_html_title(res.text),
            "https_status": res.status_code,
            "https_server": res.headers.get('Server', 'Unknown'),
            "location": res.headers.get("Location", "-"),
            "https_latency": int(res.elapsed.total_seconds() * 1000),
            "length": len(res.content),
            "timestamp": res.headers.get('Date')
        }
        return https_dict
    except requests.exceptions.SSLError:
        return {"http_status": "SSL_ERR"}
    except requests.exceptions.RequestException:
        return {"http_status": "CONN_ERR"}

def get_html_title(html_content):
    try:
        title = re.search(r'<title>(.*?)</title>', html_content, re.IGNORECASE)
        return title.group(1).strip() if title else "-"
    except:
        return "-"
