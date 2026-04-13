def save_file_healty(domain: str, ip_sets: set[str]):
    with open(f"{domain}_healty_ip.txt", "w") as file:
        for ip in ip_sets:
            file.write(f"{ip}\n")

def save_file_problem(domain: str, ip_sets: set[str]):
    with open(f"{domain}_problem_ip.txt", "w") as file:
        for ip in ip_sets:
            file.write(f"{ip}\n")