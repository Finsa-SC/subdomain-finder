# subdomain-finder

![Python](https://img.shields.io/badge/Python-3.10+-blue?style=flat-square)
![uv](https://img.shields.io/badge/env-uv-purple?style=flat-square)
![License](https://img.shields.io/badge/License-MIT-green?style=flat-square)
![Security](https://img.shields.io/badge/Use-Ethical%20Only-red?style=flat-square)
![Status](https://img.shields.io/badge/Status-Active-brightgreen?style=flat-square)

A lightweight CLI tool for **subdomain enumeration** and **HTTP/HTTPS validation** — supports direct domain input or file input, with multi-source discovery, wildcard DNS detection, latency measurement, Cloudflare IP filtering, and JSON output.

> 🟡 **Recon Type: Hybrid (Passive + Active)**
> Subdomain *discovery* is done passively via external APIs (no direct contact with the target).
> However, the *validation* phase sends real HTTP/HTTPS requests to each discovered subdomain — meaning your traffic **will be logged** by the target server and may trigger IDS/WAF alerts.
> Only use this tool on domains you **own** or have **explicit written permission** to test.

---

## Features

- Multi-source subdomain discovery — HackerTarget, crt.sh, RapidDNS, AlienVault OTX
- Select a specific source (`-s`) or run all of them at once (`-all`)
- Input from domain (`-d`) or file (`-dL`) — flexible format, subdomain just needs to be the first value per line
- HTTP **and** HTTPS validation simultaneously — with IP resolution, Server header detection, and latency measurement
- Wildcard DNS detection — skip subdomains that are likely false positives (`-nW`)
- Filter to show only live hosts (`-A`)
- Verbose mode with redirect info (`-v`, `-r`)
- Quiet mode for clean output (`-q`) — optionally show IPs instead of subdomains (`--ip`)
- Page title extraction per subdomain (`-T`)
- Technology detection from response headers (`-x`)
- Configurable request delay between threads (`--delay`)
- Automatic Cloudflare IP filtering on saved results
- Save results as plain IP list (`-o`) or detailed JSON (`-oJ`)
- Scan summary at the end — breakdown of OK, Forbidden, SSL Error, Server Error, No Response
- Concurrent validation via ThreadPoolExecutor (configurable via `-th`)
- Full CLI support via `argparse` — no interactive prompts
- Default configuration via `.env`

---

## Requirements

- Python 3.10+
- [uv](https://github.com/astral-sh/uv)

---

## Getting Started

```bash
# Clone
git clone --depth 1 https://github.com/Finsa-SC/subdomain-finder.git
cd subdomain-finder

# Create virtual environment
uv venv --python 3.10
source .venv/bin/activate        # Linux / macOS
.venv\Scripts\activate           # Windows

# Install dependencies
uv sync

# (Optional) Configure defaults
cp .env.example .env
```

---

## Usage

```bash
python main.py [-h] [-V] (-d DOMAIN | -dL FILE) [options]
```

### Flags

| Flag | Long | Description |
|------|------|-------------|
| `-d` | `--domain` | Target domain to enumerate |
| `-dL` | `--domain-list` | Path to file containing subdomains to validate |
| `-s` | `--source` | Select a specific discovery source (e.g. `hackertarget`, `crtsh`, `rapiddns`, `alienvault`) |
| `-all` | | Use all available discovery sources |
| `-t` | `--timeout` | Request timeout in seconds *(default: from `.env` or `3.0`)* |
| `-th` | `--thread` | Number of concurrent threads *(default: from `.env` or `10`)* |
| `--delay` | | Delay between requests in seconds *(default: `0.0`)* |
| `-A` | `--available` | Only show hosts with status `200 OK` |
| `-v` | `--verbose` | Show detailed protocol and header information |
| `-r` | `--redirect` | Show redirect targets *(requires `-v`)* |
| `-nW` | `--no-wildcard` | Skip subdomains detected as wildcard DNS |
| `-q` | `--quiet` | Clean output — only show subdomains with HTTP/HTTPS 200 |
| `--ip` | | Show IPs instead of subdomains *(requires `-q`)* |
| `-T` | `--title` | Print the page title below each subdomain |
| `-x` | `--header-tech` | Show technology stack detected from response headers |
| `-o` | `--output` | Save results as plain IP list |
| `-oJ` | `--output-json` | Save results as JSON with full details |
| `-V` | `--version` | Print tool version |

> `-d` and `-dL` are mutually exclusive. `-r` requires `-v`. `--ip` requires `-q`.

---

## Examples

```bash
# Basic scan
python main.py -d example.com

# Use all discovery sources
python main.py -d example.com -all

# Use a specific source
python main.py -d example.com -s crtsh

# Only show live hosts (HTTP 200)
python main.py -d example.com -A

# Verbose with redirect info
python main.py -d example.com -v -r

# Clean output with page titles and tech detection
python main.py -d example.com -q -T -x

# Scan from file, custom timeout and threads
python main.py -dL hosts.txt -t 5.0 -th 20

# Skip wildcard DNS + save as JSON
python main.py -d example.com -nW -oJ

# Slow scan with delay between requests
python main.py -d example.com --delay 0.5 -th 5

# Full combo
python main.py -dL hosts.txt -A -nW -o -oJ -th 20 -t 5
```

---

## Example Output

```
[*] sub.example.com      | 93.184.216.34   | Apache          | HTTP: 200 (250ms)  | HTTPS: 200 (310ms)  [ (OK) ]
[!] admin.example.com    | 93.184.216.35   | nginx           | HTTP: 403 (80ms)   | HTTPS: 403 (90ms)   [ [!Forbidden] ]
[-] old.example.com      | 93.184.216.36   | Unknown         | HTTP: 404 (120ms)  | HTTPS: -   (N/A)


Summary:
Host Up      : 1
Forbidden    : 1
SSL Error    : 0
Server Error : 0
No Response  : 0
```

| Prefix | Meaning |
|--------|---------|
| `[*]` | Host is alive and accessible (200 OK) |
| `[!]` | Host exists but access is denied (403 Forbidden) |
| `[?]` | Possible wildcard DNS match |
| `[-]` | Host found with another status code |

---

## Discovery Sources

| Source | Flag | Notes |
|--------|------|-------|
| HackerTarget | `hackertarget` | Default source. Free, no API key required. |
| crt.sh | `crtsh` | Certificate transparency logs. No API key required. |
| RapidDNS | `rapiddns` | Scrapes subdomain data from rapiddns.io. |
| AlienVault OTX | `alienvault` | Passive DNS data. Requires an API key. |

Use `-s <source>` to pick one, or `-all` to run all sources and merge results.

---

## File Input Format (`-dL`)

The format is flexible — the tool takes the **first value per line** (split by `,`). HackerTarget-style output works out of the box, but so does a plain subdomain list:

```
# HackerTarget format (works)
sub.example.com,93.184.216.34

# Plain list (also works)
sub.example.com
admin.example.com
```

---

## Environment Variables

Configurable via `.env` (copy from `.env.example`). CLI flags will **override** these values at runtime.

| Variable | Default | Description |
|----------|---------|-------------|
| `TIMEOUT` | `3.0` | HTTP request timeout in seconds |
| `THREAD` | `10` | Number of concurrent threads |
| `DELAY` | `0.0` | Delay between requests in seconds |
| `DEBUG` | `False` | When `True`, skips CLI and runs directly against `hosts.txt` |

---

## Output Files

Results are saved in the `recon_result/` directory. Cloudflare IPs are automatically filtered from saved output.

| File | Contents |
|------|----------|
| `recon_result/<domain>_healthy_ip.txt` | IPs that returned 200 OK |
| `recon_result/<domain>_problem_ip.txt` | IPs with non-200 responses |
| `recon_result/<domain>.json` | Full details of all subdomains (via `-oJ`) |

---

## Project Structure

```
subdomain-finder/
├── main.py             # Entry point — argparse CLI
├── validate.py         # Orchestration: fetch, threading, wildcard check
├── output.py           # Output formatting and sign classification
├── request.py          # HTTP/HTTPS request helpers with latency measurement
├── save_file.py        # File saving logic with Cloudflare IP filtering
├── scan_config.py      # Scan configuration dataclass
├── summary.py          # ReconStats — scan result tracker and summary printer
├── sources/
│   ├── handler.py      # Source dispatcher — routes to the right fetcher
│   ├── hackertarget.py # HackerTarget API source
│   ├── crtsh.py        # crt.sh certificate transparency source
│   ├── rapiddns.py     # RapidDNS scraper source
│   └── alienvault.py   # AlienVault OTX passive DNS source
├── assets/
│   └── banner.txt      # ASCII banner
├── .env.example        # Configuration template
└── pyproject.toml      # Project metadata and dependencies
```

---

## Disclaimer

> **Use responsibly.**
>
> This tool performs **active reconnaissance** — during the validation phase, HTTP/HTTPS requests are sent directly to each discovered subdomain. Your activity **will be logged** by the target server and may trigger IDS/WAF alerts.
>
> This tool is intended **only** for domains you **own** or have **explicit written permission** to test. Unauthorized use against third-party domains may violate applicable laws and regulations (e.g. UU ITE in Indonesia, CFAA in the US).
>
> The author is not responsible for any misuse or damage caused by this tool.

---

## License

Distributed under the [MIT License](LICENSE).

---

<p align="center">Made with ❤️ using Python & multiple OSINT sources</p>
