# 🔍 Subdomain Finder

![Python](https://img.shields.io/badge/Python-3.10-blue?style=flat-square)
![uv](https://img.shields.io/badge/env-uv-purple?style=flat-square)
![Requests](https://img.shields.io/badge/Library-requests-orange?style=flat-square)
![License](https://img.shields.io/badge/License-MIT-green?style=flat-square)
![Security](https://img.shields.io/badge/Use-Ethical%20Only-red?style=flat-square)

A lightweight Python tool for **subdomain enumeration** using the [HackerTarget API](https://hackertarget.com/), with live HTTP status validation for each discovered host.

---

## ✨ Features

- 🔎 Automatic subdomain discovery via HackerTarget API
- ✅ Live HTTP status validation for each found subdomain
- 🎨 Classified output based on status (`200 OK`, `403 Forbidden`, etc.)
- ⏱️ Configurable request timeout
- 🪶 Lightweight, no heavy dependencies

---

## 📋 Requirements

- Python 3.10
- [uv](https://github.com/astral-sh/uv) (package & environment manager)

---

## 🚀 Getting Started

### 1. Clone the repository

```bash
git clone https://github.com/yourusername/subdomain-finder.git
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
uv pip install requests
```

### 4. Run

```bash
python main.py
```

You will be prompted to enter:

| Input | Description | Example |
|-------|-------------|---------|
| `Domain name` | Target domain to enumerate | `example.com` |
| `Timeout` | Request timeout in seconds | `3.0` *(default)* |

---

## 📊 Example Output

```
Search for subdomain for example.com
[*] Finding 3 potential hosts, starting validation

[+] sub.example.com                      | Status: 200 (OK)
[!] admin.example.com                    | Status: 403 Forbidden
[-] old.example.com                      | Status: 404
```

| Prefix | Meaning |
|--------|---------|
| `[+]` | Host is alive and accessible (200) |
| `[!]` | Host exists but access is denied (403) |
| `[-]` | Host found with another status code |

---

## 📁 Project Structure

```
subdomain-finder/
│
└── main.py        # Main script
```

---

## ⚠️ Disclaimer

> **Use responsibly.**
>
> This tool is intended **only** for domains you **own** or have **explicit written permission** to test. Unauthorized use against third-party domains may violate applicable laws and regulations.
>
> The author is not responsible for any misuse or damage caused by this tool.

---

## 📜 License

Distributed under the [MIT License](LICENSE).

---

<p align="center">Made with ❤️ using Python & HackerTarget API</p>
