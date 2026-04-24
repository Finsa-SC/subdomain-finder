import requests

def fetch_hackertarget(domain: str):
    subdomains = set()
    try:
        url = f"https://api.hackertarget.com/hostsearch/?q={domain}"
        response = requests.get(url=url)

        if "error" in response.text.lower() or response.status_code != 200:
            print(f"[x] Error occurred: {response.text}")
            return subdomains

        raw_data = response.text
        if not raw_data:
            return subdomains

        lines = raw_data.strip().split("\n")
        for line in lines:
            sub = line.split(",")[0].lower().strip()
            if sub:
                subdomains.add(sub)
    except:
        ...
    finally:
        return subdomains