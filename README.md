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
- 📄 Support input from **domain name** (`-d`) or **file** (`-dL`) — file format is flexible, subdomain just needs to be the first value per line
- ✅ Live HTTP **and** HTTPS validation with **IP resolution**, **Server header detection**, and **latency measurement**
- 🎨 Classified output based on status (`200 OK`, `403 Forbidden`, `404`, etc.)
- 🔍 Optional filter to show only available (`200`) hosts with `-A`
- 📊 **Scan summary** — breakdown of OK, Forbidden, SSL Error, and Server Error counts
- 💾 Save results to file, with **automatic Cloudflare IP filtering**
- ⚡ Concurrent validation via **ThreadPoolExecutor** (configurable with `-th`)
- ⏱️ Configurable request timeout with `-t`
- 🖥️ Full **CLI support** via `argparse` — no interactive prompts
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

---

## 🖥️ Usage

```bash
uv run main.py [-h] [-V] (-d DOMAIN | -dL DOMAIN_LIST) [options]
```

### Flags

| Flag | Long | Description |
|------|------|-------------|
| `-d` | `--domain` | Target domain to enumerate |
| `-dL` | `--domain-list` | Path to file containing subdomains to validate |
| `-t` | `--timeout` | Request timeout in seconds *(default: `.env` or `3.0`)* |
| `-th` | `--thread` | Number of concurrent threads *(default: `.env` or `10`)* |
| `-A` | `--available` | Only show hosts with status `200 OK` |
| `-v` | `--verbose` | Show detailed protocol and header information |
| `-r` | `--redirect` | Show redirect targets *(requires `-v`)* |
| `-o` | `--output` | Save results to file |
| `-V` | `--version` | Print tool version |

> `-d` and `-dL` are mutually exclusive. `-r` requires `-v`.

---

## 📊 Examples

```bash
# Basic scan
uv run main.py -d example.com

# Only show live hosts
uv run main.py -d example.com -A

# Verbose with redirect info
uv run main.py -d example.com -v -r

# Scan from file, custom timeout and threads
uv run main.py -dL hosts.txt -t 5.0 -th 20

# Save results
uv run main.py -d example.com -o result.txt
```

---

## 📊 Example Output

```
Search for subdomain for example.com
[*] Found 3 potential hosts, starting validation

[*] sub.example.com      | 93.184.216.34   | Apache          | HTTP: 200 (250ms)  | HTTPS: 200 (310ms)  (OK)
[!] admin.example.com    | 93.184.216.35   | nginx           | HTTP: 403 (80ms)   | HTTPS: 403 (90ms)   [!Forbidden]
[-] old.example.com      | 93.184.216.36   | Unknown         | HTTP: 404 (120ms)  | HTTPS: -   (N/A)

Summary:
Host Up      : 1
Forbidden    : 1
SSL Error    : 0
Server Error : 0
```

| Prefix | Meaning |
|--------|---------|
| `[*]` | Host is alive and accessible (200 OK) |
| `[!]` | Host exists but access is denied (403 Forbidden) |
| `[ ]` | Host not found (404) |
| `[-]` | Host found with another status code |

---

## 📄 Using a File as Input (`-dL`)

The file format is flexible — the tool takes the **first value per line** (split by `,`). HackerTarget-style output works out of the box, but so does a plain subdomain list:

```
# HackerTarget format (works)
sub.example.com,93.184.216.34

# Plain list (also works)
sub.example.com
admin.example.com
```

```bash
uv run main.py -dL hosts.txt
```

---

## ⚙️ Environment Variables

Configurable via `.env` (copy from `.env.example`). CLI flags override these values at runtime.

| Variable | Default | Description |
|----------|---------|-------------|
| `TIMEOUT` | `3.0` | HTTP request timeout in seconds |
| `THREAD` | `10` | Number of concurrent validation threads |
| `DEBUG` | `False` | When `True`, skips CLI and runs directly against `hosts.txt` |

---

## 💾 Saving Results

Results are saved via `-o`. IP lists are also stored in the `recon_result/` directory:

| File | Contents |
|------|----------|
| `recon_result/<domain>_healthy_ip.txt` | IPs that returned 200 OK |
| `recon_result/<domain>_problem_ip.txt` | IPs with non-200 responses |

> **Note:** Cloudflare IPs are automatically excluded from saved results to focus on origin servers.

---

## 📁 Project Structure

```
subdomain-finder/
│
├── main.py           # Entry point — argparse CLI and argument routing
├── validate.py       # Subdomain fetching, threading, and scan orchestration
├── output.py         # Output formatting, sign classification, verbose display
├── request.py        # HTTP/HTTPS request helpers with latency measurement
├── save_file.py      # File saving logic with Cloudflare IP filtering
├── summary.py        # ReconStats — scan result tracker and summary printer
├── assets/
│   └── banner.txt    # ASCII banner displayed on startup
└── pyproject.toml    # Project metadata and dependencies
```

---

## 🗺️ Roadmap

| Issue | Feature | Status |
|-------|---------|--------|
| #1 | Option to stop at passive recon (skip validation) | 🔲 Open |
| #5 | Smarter, more compact redirect output | 🔲 Open |
| #6 | Status code grouping in summary | ✅ Done |
| #7 | Wildcard DNS detection | 🔲 Open |
| #12 | Build recon report output | 🔲 Open |
| #13 | Refactor to use `argparse` | ✅ Done |
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
