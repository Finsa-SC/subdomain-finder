import html
import requests
import urllib3
import re

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def http_request(sub, time_out):
    try:
        sub_url = f"http://{sub}"
        res = requests.get(url=sub_url, timeout=time_out, allow_redirects=False, verify=False)
        http_dict = {
            "http_title": get_html_title(res),
            "http_status": res.status_code,
            "http_server": res.headers.get('Server', 'Unknown'),
            "location": res.headers.get("Location", "-"),
            "http_latency": int(res.elapsed.total_seconds() * 1000),
            "length": len(res.content),
            "timestamp": res.headers.get('Date'),
            "header": res.headers
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
            "https_title": get_html_title(res),
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

def get_html_title(res):
    res.encoding = res.apparent_encoding
    try:
        title_search = re.search(r'<title>(.*?)</title>', res.text, re.IGNORECASE | re.DOTALL)
        if title_search:
            title = html.unescape(title_search.group(1).strip())
            return title.replace('\n', ' ').replace('\r', '')
        return "-"
    except:
        return "-"
