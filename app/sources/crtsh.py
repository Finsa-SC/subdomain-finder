import requests

def fetch_crtsh(domain: str):
    subdomains = set()
    url = f"https://crt.sh/?q={domain}&output=json"
    try:
        res = requests.get(url, timeout=10)
        if res.status_code == 200:
            data = res.json()
            for entry in data:
                name = entry['name_value'].lower()
                if "\n" in name:
                    for n in name.split("\n"):
                        subdomains.add(n.replace("*.", ""))
                else:
                    subdomains.add(name.replace("*.", ""))
    except:
        ...
    finally:
        return subdomains