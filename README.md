<div align="center">

```
 ██╗   ██╗███╗   ██╗██████╗ ██╗██╗   ██╗ █████╗ ██╗     ███████╗██████╗
 ██║   ██║████╗  ██║██╔══██╗██║██║   ██║██╔══██╗██║     ██╔════╝██╔══██╗
 ██║   ██║██╔██╗ ██║██████╔╝██║██║   ██║███████║██║     █████╗  ██║  ██║
 ██║   ██║██║╚██╗██║██╔══██╗██║╚██╗ ██╔╝██╔══██║██║     ██╔══╝  ██║  ██║
 ╚██████╔╝██║ ╚████║██║  ██║██║ ╚████╔╝ ██║  ██║███████╗███████╗██████╔╝
  ╚═════╝ ╚═╝  ╚═══╝╚═╝  ╚═╝╚═╝  ╚═══╝  ╚═╝  ╚═╝╚══════╝╚══════╝╚═════╝
```

**Instagram · Gmail · Yahoo · Outlook Account Checker**

Coded by [@meaz0x8](https://github.com/dvdzzy)

![Python](https://img.shields.io/badge/Python-3.8+-blue?style=flat-square&logo=python)
![Platform](https://img.shields.io/badge/Platform-Linux%20%7C%20Termux-green?style=flat-square)
![TLS](https://img.shields.io/badge/TLS-Chrome120_Fingerprint-purple?style=flat-square)

</div>

---

## Features

- **Chrome TLS Fingerprint** via `curl_cffi` — bypasses Python `requests`/`httpx` detection
- **Smart domain detection** — uses Instagram recovery API to identify email domain before checking
- **Multi-platform email check** — Gmail, Yahoo, Outlook/Live
- **Proxy rotation** — load proxies from `proxies.txt`
- **Dual Instagram check methods** — `check_email` endpoint + `login/ajax` fallback
- **Random timing jitter** — human-like request intervals to avoid behavioral detection
- **Year-based targeting** — account ID ranges matched to registration year (2012–2020)
- **Termux & Linux compatible**

---

## Installation

### Linux / Termux

```bash
git clone https://github.com/meaz0x8/unrivaled
cd unrivaled
pip install -r requirements.txt
python unrivaled.py
```

### Termux (Android) — first time setup

```bash
pkg update && pkg upgrade
pkg install python git
git clone https://github.com/meaz0x8/unrivaled](https://github.com/dvdzzy/instahunt.git
cd unrivaled
pip install -r requirements.txt
python unrivaled.py
```

---

## Requirements

```
curl_cffi
h2
rich
requests
user_agent
httpx
httpx[http2]
faker
beautifulsoup4
```

Install all at once:

```bash
pip install -r requirements.txt
```

---

## Proxy Support

Create a `proxies.txt` file in the same directory. One proxy per line:

```
1.2.3.4:8080
user:pass@5.6.7.8:3128
http://9.10.11.12:8080
```

If `proxies.txt` is not found, the tool runs without proxies.

---

## Usage

```
python unrivaled.py
```

Select a year range (1–9), press Enter, the tool starts scanning automatically.

Results are saved to `hits.txt`.

---

## How It Works

```
1. Enumerate Instagram user IDs in year-specific ranges
2. Query Instagram GraphQL API to resolve username
3. Call Instagram recovery API → get masked email (e.g. j***@gmail.com)
4. Parse domain from masked email
5. Check target email on correct platform (Gmail / Yahoo / Outlook)
6. Save hits to hits.txt
```

---



---

<div align="center">
Coded by <b>@meaz0x8</b>
</div>
