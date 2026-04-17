# 🔍 Subdomain Finder

![Python](https://img.shields.io/badge/Python-3.10-blue?style=flat-square)
![uv](https://img.shields.io/badge/env-uv-purple?style=flat-square)
![Requests](https://img.shields.io/badge/Library-requests-orange?style=flat-square)
![License](https://img.shields.io/badge/License-MIT-green?style=flat-square)
![Security](https://img.shields.io/badge/Use-Ethical%20Only-red?style=flat-square)

A lightweight Python tool for **subdomain enumeration** using the [HackerTarget API](https://hackertarget.com/), with live HTTP/HTTPS status validation, latency measurement, IP resolution, server detection, and scan summary reporting.

> 🟡 **Recon Type: Hybrid (Passive + Active)**
> Subdomain *discovery* is done passively via HackerTarget API (no direct contact with the target).
> However, the *validation* phase sends real HTTP/HTTPS requests to each discovered subdomain — making this **active reconnaissance**. The target's server **will** see your traffic. Only use this tool on targets you own or have explicit written permission to test.

---

## ✨ Features

- 🔎 Automatic subdomain discovery via HackerTarget API
- 📄 Support input from domain name **or** a `.txt` file
- ✅ Live HTTP **and** HTTPS validation with **IP resolution**, **Server header detection**, and **latency measurement**
- 🎨 Classified output based on status (`200 OK`, `403 Forbidden`, `404`, etc.)
- 🔍 Optional filter to **show only available (200) hosts**
- 📊 **Scan summary** — breakdown of OK, Forbidden, SSL Error, and Server Error counts
- 💾 Save results to file, with **automatic Cloudflare IP filtering**
- ⚡ Concurrent validation using **ThreadPoolExecutor** (configurable workers)
- ⏱️ Configurable request timeout
- 🐛 Debug mode via `.env` for quick local testing
- 🪶 Lightweight, no heavy dependencies

---

## 📋 Requirements

- Python 3.10+
- [uv](https://github.com/astral-sh/uv) (package & environment manager)

---

## 🚀 Getting Started

### 1. Clone the repository

```bash
git clone --depth 1 https://github.com/Finsa-SC/subdomain-finder.git
cd subdomain-finder
```

### 2. Create virtual environment with uv

```bash
uv venv --python 3.10
source .venv/bin/activate        # Linux / macOS
.venv\Scripts\activate           # Windows
```

### 3. Install dependencies

```bash
uv sync
```

### 4. Configure environment (optional)

```bash
cp .env.example .env
# Edit .env to customize TIMEOUT, THREAD, and DEBUG
```

### 5. Run

```bash
uv run main.py
```

You will be prompted to enter:

| Input | Description | Example |
|-------|-------------|---------|
| `Domain name or TXT` | Target domain or path to `.txt` file | `example.com` or `hosts.txt` |
| `Timeout` | Request timeout in seconds | `3.0` *(default)* |
| `Show only available host?` | Filter output to 200 OK only | `y` / `N` *(default)* |
| `Enable verbose output?` | Show HTTP/HTTPS protocol detail and redirect info | `y` / `N` *(default)* |
| `Show redirect targets?` | Show `Location` header value *(verbose only)* | `y` / `N` *(default)* |

---

## 📊 Example Output

```
Search for subdomain for example.com
[*] Found 3 potential hosts, starting validation

[*] sub.example.com      | 93.184.216.34   | Apache          | HTTP: 200 (250ms)  | HTTPS: 200 (310ms)  (OK)
[!] admin.example.com    | 93.184.216.35   | nginx           | HTTP: 403 (80ms)   | HTTPS: 403 (90ms)   [!Forbidden]
[-] old.example.com      | 93.184.216.36   | Unknown         | HTTP: 404 (120ms)  | HTTPS: -   (N/A)

3 Host UP (↑)

Summary:
Host Up      : 1
Forbidden    : 1
SSL Error    : 0
Server Error : 0

Did you want to save the result? [y/N]:
```

| Prefix | Meaning |
|--------|---------|
| `[*]` | Host is alive and accessible (200 OK) |
| `[!]` | Host exists but access is denied (403 Forbidden) |
| `[ ]` | Host not found (404) |
| `[-]` | Host found with another status code |

---

## ⚙️ Environment Variables

Configurable via `.env` file (copy from `.env.example`):

| Variable | Default | Description |
|----------|---------|-------------|
| `TIMEOUT` | `3.0` | HTTP request timeout in seconds |
| `THREAD` | `10` | Number of concurrent validation threads |
| `DEBUG` | `False` | When `True`, skips prompts and runs against `hosts.txt` directly |

---

## 💾 Saving Results

After scanning, you can save the results. Output files are stored in the `recon_result/` directory:

| File | Contents |
|------|----------|
| `recon_result/<domain>_healthy_ip.txt` | IPs that returned 200 OK |
| `recon_result/<domain>_problem_ip.txt` | IPs with non-200 responses |

> **Note:** Cloudflare IPs are automatically excluded from saved results to reduce noise and focus on origin servers.

---

## 📄 Using a TXT File as Input

Instead of querying the HackerTarget API, you can pass a `.txt` file directly.
The file should follow the same format returned by HackerTarget:

```
sub.example.com,93.184.216.34
admin.example.com,93.184.216.35
```

Just enter the file path when prompted:

```
Domain name input or TXT: hosts.txt
```

---

## 📁 Project Structure

```
subdomain-finder/
│
├── main.py           # Main script — input, scanning, and orchestration
├── request.py        # HTTP/HTTPS request helpers with latency measurement
├── save_file.py      # File saving logic with Cloudflare IP filtering
├── summary.py        # ReconStats — scan result tracker and summary printer
├── assets/
│   └── banner.txt    # ASCII banner displayed on startup
└── pyproject.toml    # Project metadata and dependencies
```

---

## 🗺️ Roadmap

| # | Feature | Status |
|---|---------|--------|
| #1 | Option to stop at passive recon (skip validation) | 🔲 Open |
| #5 | Smarter, more compact redirect output | 🔲 Open |
| #6 | Status code grouping in summary | ✅ Done |
| #7 | Wildcard DNS detection | 🔲 Open |
| #12 | Build recon report output | 🔲 Open |
| #13 | Refactor to use `argparse` (CLI flags) | 🔲 Open |
| #14 | Split outputs to separate files per category | 🔲 Open |
| #15 | Fix SSL error summary count | 🐛 Open |

---

## ⚠️ Disclaimer

> **Use responsibly.**
>
> This tool performs **active reconnaissance** — during the validation phase, HTTP/HTTPS requests are sent directly to each discovered subdomain. This means your activity **will be logged** by the target server and may trigger IDS/WAF alerts.
>
> This tool is intended **only** for domains you **own** or have **explicit written permission** to test. Unauthorized use against third-party domains may violate applicable laws and regulations (e.g. UU ITE in Indonesia, CFAA in the US).
>
> The author is not responsible for any misuse or damage caused by this tool.

---

## 📜 License

Distributed under the [MIT License](LICENSE).

---

<p align="center">Made with ❤️ using Python & HackerTarget API</p>
