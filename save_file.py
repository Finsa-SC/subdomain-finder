import ipaddress
import os
import json

CLOUDFLARE_IPS = [
    "173.245.48.0/20", "103.21.244.0/22", "103.22.200.0/22",
    "103.31.4.0/22", "141.101.64.0/18", "108.162.192.0/18",
    "190.93.240.0/20", "188.114.96.0/20", "197.234.240.0/22",
    "198.41.128.0/17", "162.158.0.0/15", "104.16.0.0/13",
    "104.24.0.0/14", "172.64.0.0/13", "131.0.72.0/22"
]

def check_result_dir():
    if not os.path.exists("recon_result"):
        os.makedirs("recon_result")

def is_cloudflare(ip):
    ip_obj = ipaddress.ip_address(ip)
    for network in CLOUDFLARE_IPS:
        if ip_obj in ipaddress.ip_network(network):
            return True
    return False

def save_file_healthy(domain: str, ip_sets: set[str]):
    file_name = f"recon_result/{domain}_healthy_ip.txt"
    with open(file_name, "w") as file:
        for ip in ip_sets:
            if not is_cloudflare(ip):
                file.write(f"{ip}\n")
    print(f"Success save healthy ip as {file_name}")

def save_file_problem(domain: str, ip_sets: set[str]):
    file_name = f"recon_result/{domain}_problem_ip.txt"
    with open(file_name, "w") as file:
        for ip in ip_sets:
            if not is_cloudflare(ip):
                file.write(f"{ip}\n")
    print(f"Success save problem ip as {file_name}")

def save_file_as_json(domain: str ,dict_sub):
    file_name = f"recon_result/{domain}.json"
    with open(file_name, "w")as file:
        json.dump(dict_sub, file, indent=4)
    print(f"Success save JSON result as {file_name}")
