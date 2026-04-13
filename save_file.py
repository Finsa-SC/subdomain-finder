import ipaddress

CLOUDFLARE_IPS = [
    "173.245.48.0/20", "103.21.244.0/22", "103.22.200.0/22",
    "103.31.4.0/22", "141.101.64.0/18", "108.162.192.0/18",
    "190.93.240.0/20", "188.114.96.0/20", "197.234.240.0/22",
    "198.41.128.0/17", "162.158.0.0/15", "104.16.0.0/13",
    "104.24.0.0/14", "172.64.0.0/13", "131.0.72.0/22"
]

def is_cloudflare(ips):
    ip_obj = ipaddress.ip_address(ips)
    for network in CLOUDFLARE_IPS:
        if ip_obj in ipaddress.ip_network(network):
            return True
    return False

def save_file_healthy(domain: str, ip_sets: set[str]):
    with open(f"recon_result/{domain}_healthy_ip.txt", "w") as file:
        for ip in ip_sets:
            if not is_cloudflare(ip):
                file.write(f"{ip}\n")

def save_file_problem(domain: str, ip_sets: set[str]):
    with open(f"recon_result/{domain}_problem_ip.txt", "w") as file:
        for ip in ip_sets:
            if not is_cloudflare(ip):
                file.write(f"{ip}\n")