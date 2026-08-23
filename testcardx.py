#!/usr/bin/env python3
import os
import sys
import random
import json
import csv
import time
import logging
import argparse
from typing import Dict, List, Tuple, Optional, Union, Any
from dataclasses import dataclass, asdict
from datetime import datetime, timedelta
from enum import Enum
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor, as_completed
import re

class Colors:
    RESET = "\033[0m"
    BOLD = "\033[1m"
    DIM = "\033[2m"
    ITALIC = "\033[3m"
    UNDERLINE = "\033[4m"
    BLINK = "\033[5m"
    REVERSE = "\033[7m"
    HIDDEN = "\033[8m"

    BLACK = "\033[30m"
    RED = "\033[31m"
    GREEN = "\033[32m"
    YELLOW = "\033[33m"
    BLUE = "\033[34m"
    MAGENTA = "\033[35m"
    CYAN = "\033[36m"
    WHITE = "\033[37m"
    BRIGHT_BLACK = "\033[90m"
    BRIGHT_RED = "\033[91m"
    BRIGHT_GREEN = "\033[92m"
    BRIGHT_YELLOW = "\033[93m"
    BRIGHT_BLUE = "\033[94m"
    BRIGHT_MAGENTA = "\033[95m"
    BRIGHT_CYAN = "\033[96m"
    BRIGHT_WHITE = "\033[97m"

    BG_BLACK = "\033[40m"
    BG_RED = "\033[41m"
    BG_GREEN = "\033[42m"
    BG_YELLOW = "\033[43m"
    BG_BLUE = "\033[44m"
    BG_MAGENTA = "\033[45m"
    BG_CYAN = "\033[46m"
    BG_WHITE = "\033[47m"
    BG_BRIGHT_BLACK = "\033[100m"
    BG_BRIGHT_RED = "\033[101m"
    BG_BRIGHT_GREEN = "\033[102m"
    BG_BRIGHT_YELLOW = "\033[103m"
    BG_BRIGHT_BLUE = "\033[104m"
    BG_BRIGHT_MAGENTA = "\033[105m"
    BG_BRIGHT_CYAN = "\033[106m"
    BG_BRIGHT_WHITE = "\033[107m"

    @staticmethod
    def gradient(text: str, color1: str = CYAN, color2: str = MAGENTA) -> str:
        chars = list(text)
        result = []
        for i, char in enumerate(chars):
            if i % 2 == 0:
                result.append(f"{color1}{char}")
            else:
                result.append(f"{color2}{char}")
        return "".join(result) + Colors.RESET

def clear_screen() -> None:
    os.system('cls' if os.name == 'nt' else 'clear')

def print_centered(text: str, width: int = 80) -> None:
    lines = text.split('\n')
    for line in lines:
        padding = max(0, (width - len(line)) // 2)
        print(' ' * padding + line)

def print_header(title: str, subtitle: str = "") -> None:
    width = 80
    border = "═" * width
    print(f"{Colors.BRIGHT_CYAN}{border}{Colors.RESET}")
    print(f"{Colors.BRIGHT_MAGENTA}{Colors.BOLD}║{Colors.RESET}{Colors.BRIGHT_YELLOW} {title.center(width-4)} {Colors.RESET}{Colors.BRIGHT_MAGENTA}{Colors.BOLD}║{Colors.RESET}")
    if subtitle:
        print(f"{Colors.BRIGHT_MAGENTA}{Colors.BOLD}║{Colors.RESET}{Colors.DIM} {subtitle.center(width-4)} {Colors.RESET}{Colors.BRIGHT_MAGENTA}{Colors.BOLD}║{Colors.RESET}")
    print(f"{Colors.BRIGHT_CYAN}{border}{Colors.RESET}")

def print_footer() -> None:
    width = 80
    border = "═" * width
    print(f"{Colors.BRIGHT_CYAN}{border}{Colors.RESET}")
    print(f"{Colors.DIM}{'TestCardX v3.0 | Author: SYLHETYHACKVENGER (THE-ERROR808)'.center(width)}{Colors.RESET}")
    print(f"{Colors.BRIGHT_CYAN}{border}{Colors.RESET}")

class AnimatedBanner:

    @staticmethod
    def get_credit_card_ascii() -> str:
        return """
  .......,:i1i1t111;:..,,:;1tttt11iiiii:,,.,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,::,::,,,,,,,,,:::::::,,
 .........,:i1ttii;:::;itfLCCCLLLLfffffftti,.,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,:;::;;:,,,,,,,,,,::::;;::
...........,::;i;:;ifLLLLCCGCLLfffffffttfLLt:,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,:;::;;:,,,,,,,,,,::,::;;;
............,::;iiifCCLfLCG0CLfffffLffffttfLt,,,,.,,,,,,,,,,,,,,,,,,,,,,,,,:;::;::,,,,,,,,,,,,:::i;;
 ..........,:itt11tCCLLLLffffffffLLLLLLffftfLi,,,,.,,,,,,,,,,,,,,,,,,,,,,,,:;::;:,,,,,,,,,,,,,,,:iii
..........,:;1t1itLCCCLftttffffLLLLLLCLfffftff;,,;:,,,,,,,,,,,,,,,,,,,,,,,,:;::::,,,,,,,,,,,,,,,,:;;
 .........::;;ii1LCLLLfft1tttffLLLLLCCLLLfftttt1ii1i,,,,,,,,,,,,,,,,,,,,,,,,,,,.:,,,,,,,,,,,,,,,,,:;
 .........,:;1fttLLffftt111tffLLLLLLLLft1iiii11t1;;:,,,,,,,,,,,,,,,,,,,,,,,,.,:,:,,,,,,,,,,,,,,,,,,:
 ..........,,:;iitLfttt11i1tttt1i;i11ft1fffffftti::,,,,,,,,,,,,,,,,,,,,,,,,,,::,:,,,,,,,,,,,,,,,,,,,
............,,::;ifftt11ii111ii11ttt11tfLLCLLftft:,,,,,,,,,,,,,,,,,,,,,,,,,,,:,,:,,,,,,,,,,,,,,,,,,,
.........,.,:ii111LCft11i;ii1tLCCCLLtt1tffffLftt1:,,,,,,,,,,,,,,,,,,,,,,,,,,,:,,:,,,,,,,,,,,,,,,,,,,
 .......,,,:;111ttfft11t1iii1tfffLLLft1tLLttttt1;,,,,,,,,,,,,,,,,,,,,,,,,,,,,::,:,,,,,,,,,,,,,,,,,,,
 .........,:;1t111tt111tttii111tffft11ii1tfLLft1:,,,,,,,,,,,,,,,,,,,,,,,,,,,,:,,:,,,,,,,,,,,,,,,,,,,
........,,,,:1tt1111i1111t1ii11ttffffttttt11tfft:,,,,,,,,,,,,,,,,,,,,,,,,,,,,:,::,,,,,,,,,,,,,,,,,,,
......,,,,,,,::;:::,,;ii11i;i111tftt111ttf11ttft,,,,,,,,,,,,,,,,,,,,,,,,,,,,,:,::,,,,,,,,,,,,,,,,,,,
 ....,,,,,,,,,,::,,,,,;11ii;;i11tft111ttffftfff1,,,,,,,,,,,,,,,,,,,,,,,,,,,,,:,::,,,,,,,,,,,,,,,,,,,
 ....,,,,,,,,,,;;:,,,,;tf1i;iiit1tfftttfLfffft1:,,,,,,,,,,,,,,,,,,,,,,,,,,,,,:,::,,,,,,,,,,,,,,,,,,,
 ....,,,,,,,,,,::,,,,,,;ii1i;iiitt1ttffffffttt;,,,,,,.,,,,,,,,::,,,,,,,,,,,,,::::,,,,,,,,,,,,,,,,,,,
 ....,,,,,,,,,,,,,,,,,,.:tfLti;;i11111tt1111itftttt111ii;;::,,,,,,,,,,,,,,,,,::::,,,,,,,,,,,,,,,,,,,
.....,,,,,,,,,,,,,,,,,:1LCLCGCf1;;iiiiiii;i1ifCLLLCCCCCCCCLLft1i;,,,,,,,,,,,,::::,,,,,,,,,,,,,,,,,,,
.....,,,,,,,,,,,,,,:;tLCCLLLCGGGCf1i;;;iii11L0GCLffLLLLLLLCCCCCCCt,,,,,,,,,,,:::,,,,,,,,,,,,,,,,,,,,
.....,,,,,,,,,,;itfLCCCLLLLffLGGGGGCLt1111tG800CLLfLCGGGCLLLLLLLLCi,,,,,,,,,,:::,,,,,,,,,,,,,,,,,,,,
..,,,,,,,:;i1fLCGGCCCCCCLLLLLLCGG00080LfffLCC00GCCCG0000GLLLLLLLLLf,,,,,,,,,,:::,,,,,,,,,,,,,,,,,,,:
 .,,,,;tLCCGGGCCCCLCLLCCCCCLLLLC0000GttffffftC0000GGGGGGGGLLLLLLLLLi,,,,,,,,,:::,,,,,,,,,,,,,,,,,,,:
...:1fCGGCCCCCCCCCCCLLCCCCCCLLLLG000LiitfLLLG0GGGGGCG00000GCLLLLLLLf;,,,,,,,,:::,,,,,,,,,,,,,,,,,,,:
  :fffLLCCCCCCCLCLLLCLLLLLLLLLLLLC000C1;tfCGGGGGGCGGGGGGGGGGLLLLLLLft:,,,,,,,:::,,,,,,,,,,,,,,,,,,;t
.;1ttttffLCCCCCCCCLLLCLLLLLLLLLLLLC000C1ii1GGGGGGGGGGGGGGCLLLLLLLLLff1,,,,,,,:::,,,,,,,,,,,,,,,,:;fC
.,ii1tffffLLLCCCCCLLLLLCCCCCCCCLLLLC00GtiftLGCGCCGGGGCCCLLLLLLLLLfLfff;,,,,,,:::,,,,,,,,,,,,,,,,ifLL
 .:;;i1ffffLLLLCCCCLLLLLLCCCCCCCLLLLC0GtfLLfLLLffLLLLLLLLLLCLCLLLffLLft:,,,,,:::,,,,,,,,,,,,,,,:1LLL
 ,1ff1ii1fffLLLLLLLLLLLffLCCCCCCCLLCLLLffttfffftttfLLLLLLLLLLLLLLfffftf;,,,,,:::,,,,,,,,,,,,,,,;fLLL
..;tfCLf11tLLLLLLffLLLLCLtLCCCCCLLLfffffffffLLLLLffLLLLLLLLLCLLLffftfff1,,,,,:::,,,,,,,,,,,,,::ifLLC
 :;;11tfftttfLLLCCtfLLLCCLtfCCCCCCCttLfffftfffffttttfffLLLLLLLLffttffff1,,,,,:::,,,,,,,,,,,,:,:tLLLL
 :::1tt1ttfffffffLLtLLLLLCLffCCCCCCtitffffffffffft1tfffffLLLLLfftttfttf1,,,,,:::,,,:,,,,,,,,,,:1LLLL
 ,,;t1tfffffffffLff1tLLLLCCCffLCCCCt;;tffLLffffft1itffffffffLfftttfftft1;,,,,::,,,,:,,,,,,,,,,;1LLLL
.:,iLti1ttffLLLLLLLf1fLLLLLLCLffLCL1;:;1fLfffLLft1;tfffffffffftt1tffttt1i,,,,::,,,,,,,,,,,,,::iffLLL
.,,,itttfffLLLLLLfft1tLLLLLLLLLLLLti;:::ittftt1it1;tffffLLfffftt1ttttt111;,,,::,,,,,,,,,,,,,:;1ffLLL
 ,,.,;i11111ttfLLfff11fLLLLLLLLLLL1i;::::;1ttii1f1;1ffLLLLffftt1itttt1111i,,,::,,,,,,,,,,,,,:1ffffLL
        """

    @staticmethod
    def animate_banner(frames: int = 5, delay: float = 0.1) -> None:
        ascii_art = AnimatedBanner.get_credit_card_ascii()
        colors = [Colors.BRIGHT_CYAN, Colors.BRIGHT_MAGENTA, Colors.BRIGHT_YELLOW, Colors.BRIGHT_GREEN, Colors.BRIGHT_BLUE]

        for _ in range(frames):
            clear_screen()
            color = random.choice(colors)
            colored_art = "\n".join([f"{color}{line}{Colors.RESET}" for line in ascii_art.split('\n')])
            print_centered(colored_art)
            time.sleep(delay)
            shimmer = random.choice(["░", "▒", "▓", "█"])
            print(f"{Colors.DIM}{shimmer * 40}{Colors.RESET}")

class CardIssuer(Enum):
    VISA = "Visa"
    MASTERCARD = "Mastercard"
    AMEX = "Amex"
    DISCOVER = "Discover"
    DINERS = "Diners"
    RUPay = "RuPay"
    MAESTRO = "Maestro"
    LOCAL = "Local"
    UNKNOWN = "Unknown"

@dataclass
class CardData:
    card_number: str
    expiry_month: str
    expiry_year: str
    cvv: str
    issuer: CardIssuer
    bank: str
    country: str
    currency: str
    zip_code: Optional[str] = None
    phone: Optional[str] = None
    generated_at: str = None

    def __post_init__(self):
        if self.generated_at is None:
            self.generated_at = datetime.now().isoformat()

    def to_pipe(self) -> str:
        return f"{self.card_number}|{self.expiry_month}|{self.expiry_year}|{self.cvv}"

    def to_json(self) -> Dict:
        return asdict(self)

    def to_csv_row(self) -> List[str]:
        return [
            self.card_number,
            self.expiry_month,
            self.expiry_year,
            self.cvv,
            self.issuer.value,
            self.bank,
            self.country,
            self.currency,
            self.zip_code or "",
            self.phone or "",
            self.generated_at
        ]

@dataclass
class ValidationResult:
    valid: bool
    card_number: str
    issuer: CardIssuer
    country: str
    bank: str
    errors: List[str]
    warnings: List[str]

class BINDatabase:

    COUNTRY_DATA = {
        "Bangladesh": {
            "prefixes": {
                CardIssuer.VISA: ["491141", "491145", "491158", "491162", "491177"],
                CardIssuer.MASTERCARD: ["525094", "529996", "539301", "540688"],
                CardIssuer.AMEX: ["370079", "370088", "376965"],
                CardIssuer.LOCAL: ["603792", "603750", "603771"]
            },
            "bank_mapping": {
                "491141": "DBBL (Dutch-Bangla Bank)",
                "491145": "BRAC Bank",
                "525094": "City Bank",
                "603792": "Eastern Bank",
                "603750": "NCC Bank"
            },
            "lengths": {CardIssuer.VISA: 16, CardIssuer.MASTERCARD: 16, CardIssuer.AMEX: 15, CardIssuer.LOCAL: 16},
            "issuers": [CardIssuer.VISA, CardIssuer.MASTERCARD, CardIssuer.AMEX, CardIssuer.LOCAL],
            "currency": "BDT",
            "country_code": "880",
            "zip_pattern": r"^\d{4}$"
        },
        "India": {
            "prefixes": {
                CardIssuer.VISA: ["431447", "432037", "460579", "462040", "463430"],
                CardIssuer.MASTERCARD: ["521422", "525724", "529447", "533508", "540303"],
                CardIssuer.AMEX: ["371016", "371288", "371316", "376974"],
                CardIssuer.RUPay: ["356527", "356528", "356529", "356530", "356531"],
                CardIssuer.MAESTRO: ["589431", "589441", "589442", "589443"]
            },
            "bank_mapping": {
                "431447": "State Bank of India",
                "432037": "HDFC Bank",
                "460579": "ICICI Bank",
                "521422": "Axis Bank",
                "525724": "Kotak Mahindra",
                "356527": "RuPay (NPCI)"
            },
            "lengths": {CardIssuer.VISA: 16, CardIssuer.MASTERCARD: 16, CardIssuer.AMEX: 15, CardIssuer.RUPay: 16, CardIssuer.MAESTRO: 19},
            "issuers": [CardIssuer.VISA, CardIssuer.MASTERCARD, CardIssuer.AMEX, CardIssuer.RUPay, CardIssuer.MAESTRO],
            "currency": "INR",
            "country_code": "91",
            "zip_pattern": r"^\d{6}$"
        },
        "Pakistan": {
            "prefixes": {
                CardIssuer.VISA: ["431337", "431700", "431771", "462416", "462779"],
                CardIssuer.MASTERCARD: ["527089", "527200", "529595", "530362", "542142"],
                CardIssuer.AMEX: ["370083", "370086", "370089"],
                CardIssuer.LOCAL: ["603600", "603601", "603602", "603603"]
            },
            "bank_mapping": {
                "431337": "Habib Bank Limited",
                "431700": "MCB Bank",
                "462416": "United Bank Limited",
                "527089": "Allied Bank",
                "529595": "Standard Chartered",
                "603600": "1Link Pakistan"
            },
            "lengths": {CardIssuer.VISA: 16, CardIssuer.MASTERCARD: 16, CardIssuer.AMEX: 15, CardIssuer.LOCAL: 16},
            "issuers": [CardIssuer.VISA, CardIssuer.MASTERCARD, CardIssuer.AMEX, CardIssuer.LOCAL],
            "currency": "PKR",
            "country_code": "92",
            "zip_pattern": r"^\d{5}$"
        },
        "Indonesia": {
            "prefixes": {
                CardIssuer.VISA: ["414138", "414148", "414153", "414177", "414187"],
                CardIssuer.MASTERCARD: ["515293", "525751", "529326", "530085", "540127"],
                CardIssuer.AMEX: ["371177", "371480", "371598"],
                CardIssuer.LOCAL: ["635473", "635474", "635475", "635476"]
            },
            "bank_mapping": {
                "414138": "Bank Mandiri",
                "414153": "BCA (Bank Central Asia)",
                "515293": "Bank Rakyat Indonesia",
                "525751": "Bank Negara Indonesia",
                "530085": "Bank Danamon",
                "635473": "BCA"
            },
            "lengths": {CardIssuer.VISA: 16, CardIssuer.MASTERCARD: 16, CardIssuer.AMEX: 15, CardIssuer.LOCAL: 16},
            "issuers": [CardIssuer.VISA, CardIssuer.MASTERCARD, CardIssuer.AMEX, CardIssuer.LOCAL],
            "currency": "IDR",
            "country_code": "62",
            "zip_pattern": r"^\d{5}$"
        },
        "UK": {
            "prefixes": {
                CardIssuer.VISA: ["414571", "419542", "420848", "429489", "432152"],
                CardIssuer.MASTERCARD: ["525950", "526408", "529662", "535240", "541590"],
                CardIssuer.AMEX: ["370091", "370092", "370093", "370094"],
                CardIssuer.LOCAL: ["675900", "675910", "675920"]
            },
            "bank_mapping": {
                "414571": "Barclays",
                "419542": "HSBC",
                "420848": "Lloyds",
                "525950": "NatWest",
                "526408": "Royal Bank of Scotland",
                "675900": "UK Domestic"
            },
            "lengths": {CardIssuer.VISA: 16, CardIssuer.MASTERCARD: 16, CardIssuer.AMEX: 15, CardIssuer.LOCAL: 16},
            "issuers": [CardIssuer.VISA, CardIssuer.MASTERCARD, CardIssuer.AMEX, CardIssuer.LOCAL],
            "currency": "GBP",
            "country_code": "44",
            "zip_pattern": r"^[A-Z]{1,2}\d[A-Z\d]? \d[A-Z]{2}$"
        },
        "USA": {
            "prefixes": {
                CardIssuer.VISA: ["401288", "411111", "431112", "441111", "451111"],
                CardIssuer.MASTERCARD: ["511111", "515111", "525111", "535111", "545111"],
                CardIssuer.AMEX: ["340000", "370000", "371111", "378282"],
                CardIssuer.DISCOVER: ["601100", "601111", "601128", "601155"],
                CardIssuer.DINERS: ["300000", "301111", "302111", "303111", "304111"]
            },
            "bank_mapping": {
                "401288": "Chase Bank",
                "411111": "Bank of America",
                "511111": "Citibank",
                "515111": "Wells Fargo",
                "601100": "Discover",
                "340000": "American Express"
            },
            "lengths": {CardIssuer.VISA: 16, CardIssuer.MASTERCARD: 16, CardIssuer.AMEX: 15, CardIssuer.DISCOVER: 16, CardIssuer.DINERS: 14},
            "issuers": [CardIssuer.VISA, CardIssuer.MASTERCARD, CardIssuer.AMEX, CardIssuer.DISCOVER, CardIssuer.DINERS],
            "currency": "USD",
            "country_code": "1",
            "zip_pattern": r"^\d{5}(-\d{4})?$"
        },
        "Canada": {
            "prefixes": {
                CardIssuer.VISA: ["413590", "419877", "431945", "443557", "450015"],
                CardIssuer.MASTERCARD: ["528604", "533207", "540181", "544403", "548436"],
                CardIssuer.AMEX: ["370167", "370170", "370172"],
                CardIssuer.LOCAL: ["605622", "605630", "605640"]
            },
            "bank_mapping": {
                "413590": "RBC Royal Bank",
                "419877": "TD Canada Trust",
                "431945": "Scotiabank",
                "528604": "BMO Bank of Montreal",
                "533207": "CIBC",
                "605622": "Canadian Domestic"
            },
            "lengths": {CardIssuer.VISA: 16, CardIssuer.MASTERCARD: 16, CardIssuer.AMEX: 15, CardIssuer.LOCAL: 16},
            "issuers": [CardIssuer.VISA, CardIssuer.MASTERCARD, CardIssuer.AMEX, CardIssuer.LOCAL],
            "currency": "CAD",
            "country_code": "1",
            "zip_pattern": r"^[A-Z]\d[A-Z] \d[A-Z]\d$"
        }
    }

    @classmethod
    def get_countries(cls) -> List[str]:
        return list(cls.COUNTRY_DATA.keys())

    @classmethod
    def get_country_data(cls, country: str) -> Dict:
        return cls.COUNTRY_DATA.get(country, cls.COUNTRY_DATA["USA"])

    @classmethod
    def detect_issuer(cls, card_number: str) -> Tuple[CardIssuer, str, str]:
        for country, data in cls.COUNTRY_DATA.items():
            for issuer, prefixes in data["prefixes"].items():
                for prefix in prefixes:
                    if card_number.startswith(prefix):
                        bank = data["bank_mapping"].get(prefix, "Unknown Bank")
                        return issuer, country, bank
        return CardIssuer.UNKNOWN, "Unknown", "Unknown Bank"

class CardGenerator:

    def __init__(self, country: str = "USA"):
        self.country = country
        self.country_data = BINDatabase.get_country_data(country)
        self.logger = logging.getLogger(__name__)

    def luhn_checksum(self, partial: str) -> int:
        digits = [int(d) for d in partial]
        for i in range(len(digits) - 1, -1, -2):
            digits[i] *= 2
            if digits[i] > 9:
                digits[i] -= 9
        total = sum(digits)
        return (10 - (total % 10)) % 10

    def generate_card_number(self, bin_prefix: str, length: int) -> str:
        remaining = length - len(bin_prefix) - 1
        if remaining < 0:
            bin_prefix = bin_prefix[:length - 1]
            remaining = 0

        random_part = ''.join(str(random.randint(0, 9)) for _ in range(remaining))
        partial = bin_prefix + random_part
        checksum = self.luhn_checksum(partial)
        return partial + str(checksum)

    def generate_expiry(self, months_ahead: int = 60) -> Tuple[str, str]:
        now = datetime.now()
        future = now + timedelta(days=random.randint(30, months_ahead * 30))
        return f"{future.month:02d}", str(future.year)

    def generate_cvv(self, issuer: CardIssuer) -> str:
        length = 4 if issuer == CardIssuer.AMEX else 3
        return ''.join(str(random.randint(0, 9)) for _ in range(length))

    def generate_zip_code(self) -> str:
        patterns = {
            "Bangladesh": lambda: f"{random.randint(1000, 9999)}",
            "India": lambda: f"{random.randint(110001, 999999):06d}",
            "Pakistan": lambda: f"{random.randint(10000, 99999)}",
            "Indonesia": lambda: f"{random.randint(10000, 99999)}",
            "UK": lambda: f"{random.choice(['AB','AL','B','BA','BB','BD','BH','BL','BN','BR','BS','BT','CA','CB','CF','CH','CM','CO','CR','CT','CV','CW','DA','DD','DE','DG','DH','DL','DN','DT','DY','E','EC','EH','EN','EX','FK','FY','G','GL','GU','HA','HD','HG','HP','HR','HS','HU','HX','IG','IP','IV','KA','KT','KW','KY','L','LA','LD','LE','LL','LN','LS','LU','M','ME','MK','ML','N','NE','NG','NN','NR','NW','OL','OX','PA','PE','PH','PL','PO','PR','RG','RH','RM','S','SA','SE','SG','SK','SL','SM','SN','SO','SP','SR','SS','ST','SW','SY','TA','TD','TF','TN','TQ','TR','TS','TW','UB','W','WA','WC','WD','WF','WN','WR','WS','WV','YO'])}{random.randint(0,9)}{random.choice(['','A','B','C','D','E','F','G','H','J','K','L','M','N','P','Q','R','S','T','U','V','W','X','Y','Z'])}{random.randint(0,9)}{random.choice(['','A','B','C','D','E','F','G','H','J','K','L','M','N','P','Q','R','S','T','U','V','W','X','Y','Z'])}{random.randint(0,9)}",
            "USA": lambda: f"{random.randint(10000, 99999)}",
            "Canada": lambda: f"{random.choice(['A','B','C','E','G','H','J','K','L','M','N','P','R','S','T','V','X','Y'])}{random.randint(0,9)}{random.choice(['A','B','C','E','G','H','J','K','L','M','N','P','R','S','T','V','X','Y'])} {random.randint(0,9)}{random.choice(['A','B','C','E','G','H','J','K','L','M','N','P','R','S','T','V','X','Y'])}{random.randint(0,9)}"
        }
        return patterns.get(self.country, lambda: "00000")()

    def generate_phone(self) -> str:
        country_code = self.country_data["country_code"]
        if self.country in ["USA", "Canada"]:
            return f"+{country_code}{random.randint(200, 999):03d}{random.randint(200, 999):03d}{random.randint(1000, 9999):04d}"
        elif self.country == "UK":
            return f"+{country_code}{random.randint(70, 79):02d}{random.randint(1000, 9999):04d}"
        elif self.country == "India":
            return f"+{country_code}{random.randint(7000000000, 9999999999):010d}"
        else:
            return f"+{country_code}{random.randint(10000000, 99999999):08d}"

    def generate_single(self, issuer: Optional[CardIssuer] = None, include_details: bool = False) -> CardData:
        if issuer and issuer in self.country_data["prefixes"]:
            prefixes = self.country_data["prefixes"][issuer]
        else:
            issuer = random.choice(self.country_data["issuers"])
            prefixes = self.country_data["prefixes"].get(issuer, ["411111"])

        bin_prefix = random.choice(prefixes)
        length = self.country_data["lengths"].get(issuer, 16)
        card_number = self.generate_card_number(bin_prefix, length)
        month, year = self.generate_expiry()
        cvv = self.generate_cvv(issuer)
        bank = self.country_data["bank_mapping"].get(bin_prefix[:6], "Unknown Bank")

        return CardData(
            card_number=card_number,
            expiry_month=month,
            expiry_year=year,
            cvv=cvv,
            issuer=issuer,
            bank=bank,
            country=self.country,
            currency=self.country_data["currency"],
            zip_code=self.generate_zip_code() if include_details else None,
            phone=self.generate_phone() if include_details else None
        )

    def generate_batch(self, count: int = 10, issuer: Optional[CardIssuer] = None,
                       include_details: bool = False, parallel: bool = False) -> List[CardData]:
        if parallel and count > 10:
            with ThreadPoolExecutor(max_workers=min(4, count)) as executor:
                futures = [executor.submit(self.generate_single, issuer, include_details) for _ in range(count)]
                return [f.result() for f in as_completed(futures)]
        else:
            return [self.generate_single(issuer, include_details) for _ in range(count)]

class CardValidator:

    @staticmethod
    def validate_luhn(card_number: str) -> bool:
        digits = [int(d) for d in str(card_number)][::-1]
        total = 0
        for i, digit in enumerate(digits):
            if i % 2 == 1:
                doubled = digit * 2
                total += doubled - 9 if doubled > 9 else doubled
            else:
                total += digit
        return total % 10 == 0

    @staticmethod
    def validate_length(card_number: str) -> bool:
        return 14 <= len(card_number) <= 19

    @staticmethod
    def validate_expiry(month: str, year: str) -> Tuple[bool, str]:
        try:
            exp_month = int(month)
            exp_year = int(year)
            if not (1 <= exp_month <= 12):
                return False, "Invalid month"
            now = datetime.now()
            exp_date = datetime(exp_year, exp_month, 1)
            if exp_date < now:
                return False, "Card has expired"
            return True, "Valid"
        except ValueError:
            return False, "Invalid date format"

    @classmethod
    def validate_full(cls, card_data: CardData) -> ValidationResult:
        errors = []
        warnings = []

        if not cls.validate_luhn(card_data.card_number):
            errors.append("Failed Luhn check")

        if not cls.validate_length(card_data.card_number):
            errors.append("Invalid length")

        detected_issuer, country, bank = BINDatabase.detect_issuer(card_data.card_number)
        if detected_issuer == CardIssuer.UNKNOWN:
            warnings.append("Unknown issuer detected")

        valid_expiry, expiry_msg = cls.validate_expiry(card_data.expiry_month, card_data.expiry_year)
        if not valid_expiry:
            errors.append(f"Expiry invalid: {expiry_msg}")

        if not card_data.cvv.isdigit() or not (3 <= len(card_data.cvv) <= 4):
            errors.append("Invalid CVV format")

        return ValidationResult(
            valid=len(errors) == 0,
            card_number=card_data.card_number,
            issuer=detected_issuer,
            country=country,
            bank=bank,
            errors=errors,
            warnings=warnings
        )

class ExportEngine:

    @staticmethod
    def to_json(cards: List[CardData], filename: str) -> None:
        data = [c.to_json() for c in cards]
        with open(filename, 'w') as f:
            json.dump(data, f, indent=2)

    @staticmethod
    def to_csv(cards: List[CardData], filename: str) -> None:
        if not cards:
            return
        headers = ["Card Number", "Expiry Month", "Expiry Year", "CVV", "Issuer", "Bank", "Country", "Currency", "ZIP", "Phone", "Generated At"]
        with open(filename, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(headers)
            for card in cards:
                writer.writerow(card.to_csv_row())

    @staticmethod
    def to_pipe(cards: List[CardData]) -> str:
        return "\n".join(c.to_pipe() for c in cards)

    @staticmethod
    def to_sql(cards: List[CardData], table_name: str = "cards") -> str:
        sql = f"INSERT INTO {table_name} (card_number, expiry_month, expiry_year, cvv, issuer, bank, country, currency) VALUES\n"
        values = []
        for card in cards:
            values.append(f"  ('{card.card_number}', '{card.expiry_month}', '{card.expiry_year}', '{card.cvv}', '{card.issuer.value}', '{card.bank}', '{card.country}', '{card.currency}')")
        return sql + ",\n".join(values) + ";"

class TestCardXTUI:

    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.setup_logging()
        self.country = "USA"
        self.generator = CardGenerator(self.country)
        self.last_generated: List[CardData] = []
        self.running = True

    def setup_logging(self):
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler('testcardx.log'),
                logging.StreamHandler()
            ]
        )

    def display_banner(self):
        clear_screen()
        AnimatedBanner.animate_banner(frames=3, delay=0.15)
        print("\n")
        print_header("TESTCARD-X", "Credit Card Testing Utility")
        print(f"\n{Colors.BRIGHT_CYAN}╭────────────────────────────────────────────────────────────────────────────╮{Colors.RESET}")
        print(f"{Colors.BRIGHT_CYAN}│{Colors.RESET} {Colors.GREEN}Author:{Colors.RESET} SYLHETYHACKVENGER (THE-ERROR808)                         {Colors.BRIGHT_CYAN}│{Colors.RESET}")
        print(f"{Colors.BRIGHT_CYAN}│{Colors.RESET} {Colors.GREEN}Type:{Colors.RESET} MAYBE IT CAN GENERATE REAL CC DO NOT MISUSE THIS TOOL              {Colors.BRIGHT_CYAN}│{Colors.RESET}")
        print(f"{Colors.BRIGHT_CYAN}│{Colors.RESET} {Colors.GREEN}Features:{Colors.RESET} Generate, Validate, Export, Batch Process, and More      {Colors.BRIGHT_CYAN}│{Colors.RESET}")
        print(f"{Colors.BRIGHT_CYAN}╰────────────────────────────────────────────────────────────────────────────╯{Colors.RESET}")
        print("\n")

    def display_menu(self):
        print(f"\n{Colors.BRIGHT_YELLOW}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━{Colors.RESET}")
        print(f"{Colors.BRIGHT_MAGENTA}  MAIN MENU{Colors.RESET}")
        print(f"{Colors.BRIGHT_YELLOW}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━{Colors.RESET}")
        print(f"{Colors.BRIGHT_CYAN}  [1]{Colors.RESET} Generate Single Card")
        print(f"{Colors.BRIGHT_CYAN}  [2]{Colors.RESET} Generate Batch Cards")
        print(f"{Colors.BRIGHT_CYAN}  [3]{Colors.RESET} Validate a Card")
        print(f"{Colors.BRIGHT_CYAN}  [4]{Colors.RESET} Validate Batch")
        print(f"{Colors.BRIGHT_CYAN}  [5]{Colors.RESET} Export Cards")
        print(f"{Colors.BRIGHT_CYAN}  [6]{Colors.RESET} Change Country")
        print(f"{Colors.BRIGHT_CYAN}  [7]{Colors.RESET} View Statistics")
        print(f"{Colors.BRIGHT_CYAN}  [8]{Colors.RESET} Display Banner")
        print(f"{Colors.BRIGHT_CYAN}  [9]{Colors.RESET} Clear Screen")
        print(f"{Colors.BRIGHT_RED}  [0]{Colors.RESET} Exit")
        print(f"{Colors.BRIGHT_YELLOW}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━{Colors.RESET}")

    def generate_single_flow(self):
        clear_screen()
        print_header("GENERATE SINGLE CARD", f"Country: {self.country}")
        print(f"\n{Colors.DIM}Available issuers: {', '.join([i.value for i in self.generator.country_data['issuers']])}{Colors.RESET}")

        issuer_input = input(f"\n{Colors.BRIGHT_GREEN}Enter issuer (or press Enter for random): {Colors.RESET}").strip().upper()
        issuer = None
        if issuer_input:
            try:
                issuer = CardIssuer[issuer_input.upper()]
            except KeyError:
                print(f"{Colors.RED}Invalid issuer. Using random.{Colors.RESET}")

        include_details = input(f"{Colors.BRIGHT_GREEN}Include full details? (y/n): {Colors.RESET}").strip().lower() == 'y'

        print(f"\n{Colors.BRIGHT_CYAN}Generating...{Colors.RESET}")
        card = self.generator.generate_single(issuer, include_details)

        print(f"\n{Colors.BRIGHT_GREEN}✓ Card Generated Successfully!{Colors.RESET}")
        print(f"{Colors.BRIGHT_YELLOW}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━{Colors.RESET}")
        print(f"{Colors.BRIGHT_CYAN}Card Number:{Colors.RESET} {card.card_number}")
        print(f"{Colors.BRIGHT_CYAN}Expiry:{Colors.RESET} {card.expiry_month}/{card.expiry_year}")
        print(f"{Colors.BRIGHT_CYAN}CVV:{Colors.RESET} {card.cvv}")
        print(f"{Colors.BRIGHT_CYAN}Issuer:{Colors.RESET} {card.issuer.value}")
        print(f"{Colors.BRIGHT_CYAN}Bank:{Colors.RESET} {card.bank}")
        print(f"{Colors.BRIGHT_CYAN}Country:{Colors.RESET} {card.country}")
        print(f"{Colors.BRIGHT_CYAN}Currency:{Colors.RESET} {card.currency}")
        if include_details:
            print(f"{Colors.BRIGHT_CYAN}ZIP Code:{Colors.RESET} {card.zip_code}")
            print(f"{Colors.BRIGHT_CYAN}Phone:{Colors.RESET} {card.phone}")
        print(f"{Colors.BRIGHT_YELLOW}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━{Colors.RESET}")

        self.last_generated = [card]
        input(f"\n{Colors.DIM}Press Enter to continue...{Colors.RESET}")

    def generate_batch_flow(self):
        clear_screen()
        print_header("GENERATE BATCH CARDS", f"Country: {self.country}")

        try:
            count = int(input(f"{Colors.BRIGHT_GREEN}Number of cards: {Colors.RESET}").strip() or "10")
            count = max(1, min(10000, count))
        except ValueError:
            count = 10
            print(f"{Colors.YELLOW}Using default count: 10{Colors.RESET}")

        print(f"\n{Colors.DIM}Available issuers: {', '.join([i.value for i in self.generator.country_data['issuers']])}{Colors.RESET}")
        issuer_input = input(f"{Colors.BRIGHT_GREEN}Enter issuer (or press Enter for random): {Colors.RESET}").strip().upper()
        issuer = None
        if issuer_input:
            try:
                issuer = CardIssuer[issuer_input.upper()]
            except KeyError:
                print(f"{Colors.RED}Invalid issuer. Using random.{Colors.RESET}")

        include_details = input(f"{Colors.BRIGHT_GREEN}Include full details? (y/n): {Colors.RESET}").strip().lower() == 'y'
        parallel = input(f"{Colors.BRIGHT_GREEN}Use parallel processing? (y/n): {Colors.RESET}").strip().lower() == 'y'

        print(f"\n{Colors.BRIGHT_CYAN}Generating {count} cards...{Colors.RESET}")
        start_time = time.time()
        cards = self.generator.generate_batch(count, issuer, include_details, parallel)
        elapsed = time.time() - start_time

        self.last_generated = cards

        print(f"\n{Colors.BRIGHT_GREEN}✓ Generated {len(cards)} cards in {elapsed:.2f}s{Colors.RESET}")
        print(f"{Colors.BRIGHT_YELLOW}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━{Colors.RESET}")
        preview_count = min(5, len(cards))
        for i in range(preview_count):
            card = cards[i]
            print(f"{i+1}. {card.card_number}|{card.expiry_month}|{card.expiry_year}|{card.cvv}")
        if len(cards) > preview_count:
            print(f"... and {len(cards) - preview_count} more")
        print(f"{Colors.BRIGHT_YELLOW}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━{Colors.RESET}")

        input(f"\n{Colors.DIM}Press Enter to continue...{Colors.RESET}")

    def validate_card_flow(self):
        clear_screen()
        print_header("VALIDATE A CARD")

        card_number = input(f"{Colors.BRIGHT_GREEN}Enter card number to validate: {Colors.RESET}").strip()
        if not card_number:
            print(f"{Colors.RED}No card number provided.{Colors.RESET}")
            input(f"{Colors.DIM}Press Enter to continue...{Colors.RESET}")
            return

        card_data = None
        for c in self.last_generated:
            if c.card_number == card_number:
                card_data = c
                break

        if card_data:
            result = CardValidator.validate_full(card_data)
        else:
            detected_issuer, country, bank = BINDatabase.detect_issuer(card_number)
            card_data = CardData(
                card_number=card_number,
                expiry_month="12",
                expiry_year="2030",
                cvv="123",
                issuer=detected_issuer,
                bank=bank,
                country=country,
                currency="USD"
            )
            result = CardValidator.validate_full(card_data)

        print(f"\n{Colors.BRIGHT_YELLOW}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━{Colors.RESET}")
        print(f"{Colors.BRIGHT_CYAN}Validation Results for: {card_number}{Colors.RESET}")
        print(f"Status: {Colors.BRIGHT_GREEN}✓ VALID{Colors.RESET}" if result.valid else f"{Colors.BRIGHT_RED}✗ INVALID{Colors.RESET}")
        print(f"Issuer: {result.issuer.value}")
        print(f"Country: {result.country}")
        print(f"Bank: {result.bank}")
        if result.errors:
            print(f"{Colors.RED}Errors:{Colors.RESET}")
            for error in result.errors:
                print(f"  ✗ {error}")
        if result.warnings:
            print(f"{Colors.YELLOW}Warnings:{Colors.RESET}")
            for warning in result.warnings:
                print(f"  ⚠ {warning}")
        print(f"{Colors.BRIGHT_YELLOW}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━{Colors.RESET}")

        input(f"\n{Colors.DIM}Press Enter to continue...{Colors.RESET}")

    def validate_batch_flow(self):
        clear_screen()
        print_header("VALIDATE BATCH")

        if not self.last_generated:
            print(f"{Colors.RED}No cards to validate. Generate some first.{Colors.RESET}")
            input(f"{Colors.DIM}Press Enter to continue...{Colors.RESET}")
            return

        print(f"\n{Colors.BRIGHT_CYAN}Validating {len(self.last_generated)} cards...{Colors.RESET}")
        valid_count = 0
        invalid_count = 0
        errors_summary = {}

        for card in self.last_generated:
            result = CardValidator.validate_full(card)
            if result.valid:
                valid_count += 1
            else:
                invalid_count += 1
                for error in result.errors:
                    errors_summary[error] = errors_summary.get(error, 0) + 1

        print(f"\n{Colors.BRIGHT_YELLOW}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━{Colors.RESET}")
        print(f"{Colors.BRIGHT_CYAN}Batch Validation Summary{Colors.RESET}")
        print(f"Total Cards: {len(self.last_generated)}")
        print(f"{Colors.BRIGHT_GREEN}Valid: {valid_count}{Colors.RESET}")
        print(f"{Colors.BRIGHT_RED}Invalid: {invalid_count}{Colors.RESET}")
        if errors_summary:
            print(f"\n{Colors.YELLOW}Error Distribution:{Colors.RESET}")
            for error, count in errors_summary.items():
                print(f"  {error}: {count}")
        print(f"{Colors.BRIGHT_YELLOW}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━{Colors.RESET}")

        input(f"\n{Colors.DIM}Press Enter to continue...{Colors.RESET}")

    def export_flow(self):
        clear_screen()
        print_header("EXPORT CARDS")

        if not self.last_generated:
            print(f"{Colors.RED}No cards to export. Generate some first.{Colors.RESET}")
            input(f"{Colors.DIM}Press Enter to continue...{Colors.RESET}")
            return

        print(f"\n{Colors.BRIGHT_CYAN}Export Formats:{Colors.RESET}")
        print(f"  [1] JSON")
        print(f"  [2] CSV")
        print(f"  [3] Pipe-separated (.txt)")
        print(f"  [4] SQL Insert")
        print(f"  [5] Display in terminal")

        format_choice = input(f"\n{Colors.BRIGHT_GREEN}Select format: {Colors.RESET}").strip()

        if format_choice == "5":
            print(f"\n{Colors.BRIGHT_YELLOW}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━{Colors.RESET}")
            print(ExportEngine.to_pipe(self.last_generated))
            print(f"{Colors.BRIGHT_YELLOW}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━{Colors.RESET}")
            input(f"\n{Colors.DIM}Press Enter to continue...{Colors.RESET}")
            return

        filename = input(f"{Colors.BRIGHT_GREEN}Enter filename (without extension): {Colors.RESET}").strip() or "cards"

        try:
            if format_choice == "1":
                ExportEngine.to_json(self.last_generated, f"{filename}.json")
                print(f"{Colors.GREEN}✓ Exported to {filename}.json{Colors.RESET}")
            elif format_choice == "2":
                ExportEngine.to_csv(self.last_generated, f"{filename}.csv")
                print(f"{Colors.GREEN}✓ Exported to {filename}.csv{Colors.RESET}")
            elif format_choice == "3":
                with open(f"{filename}.txt", 'w') as f:
                    f.write(ExportEngine.to_pipe(self.last_generated))
                print(f"{Colors.GREEN}✓ Exported to {filename}.txt{Colors.RESET}")
            elif format_choice == "4":
                with open(f"{filename}.sql", 'w') as f:
                    f.write(ExportEngine.to_sql(self.last_generated))
                print(f"{Colors.GREEN}✓ Exported to {filename}.sql{Colors.RESET}")
            else:
                print(f"{Colors.RED}Invalid format.{Colors.RESET}")
        except Exception as e:
            print(f"{Colors.RED}Error exporting: {e}{Colors.RESET}")

        input(f"\n{Colors.DIM}Press Enter to continue...{Colors.RESET}")

    def change_country_flow(self):
        clear_screen()
        print_header("CHANGE COUNTRY")

        countries = BINDatabase.get_countries()
        print(f"\n{Colors.BRIGHT_CYAN}Available Countries:{Colors.RESET}")
        for i, country in enumerate(countries, 1):
            print(f"  [{i}] {country}")

        choice = input(f"\n{Colors.BRIGHT_GREEN}Select country (number): {Colors.RESET}").strip()
        try:
            idx = int(choice) - 1
            if 0 <= idx < len(countries):
                self.country = countries[idx]
                self.generator = CardGenerator(self.country)
                print(f"{Colors.GREEN}✓ Country changed to: {self.country}{Colors.RESET}")
            else:
                print(f"{Colors.RED}Invalid selection.{Colors.RESET}")
        except ValueError:
            print(f"{Colors.RED}Invalid input.{Colors.RESET}")

        input(f"\n{Colors.DIM}Press Enter to continue...{Colors.RESET}")

    def view_statistics_flow(self):
        clear_screen()
        print_header("STATISTICS")

        if not self.last_generated:
            print(f"{Colors.RED}No cards to analyze. Generate some first.{Colors.RESET}")
            input(f"{Colors.DIM}Press Enter to continue...{Colors.RESET}")
            return

        total = len(self.last_generated)
        issuers = {}
        countries = {}
        banks = {}
        valid_count = 0

        for card in self.last_generated:
            issuers[card.issuer.value] = issuers.get(card.issuer.value, 0) + 1
            countries[card.country] = countries.get(card.country, 0) + 1
            banks[card.bank] = banks.get(card.bank, 0) + 1

            result = CardValidator.validate_full(card)
            if result.valid:
                valid_count += 1

        print(f"\n{Colors.BRIGHT_YELLOW}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━{Colors.RESET}")
        print(f"{Colors.BRIGHT_CYAN}Card Statistics{Colors.RESET}")
        print(f"Total Cards: {total}")
        print(f"{Colors.BRIGHT_GREEN}Valid Cards: {valid_count} ({valid_count/total*100:.1f}%){Colors.RESET}")
        print(f"{Colors.BRIGHT_RED}Invalid Cards: {total - valid_count} ({(total-valid_count)/total*100:.1f}%){Colors.RESET}")

        print(f"\n{Colors.BRIGHT_CYAN}Issuer Distribution:{Colors.RESET}")
        for issuer, count in sorted(issuers.items(), key=lambda x: -x[1]):
            print(f"  {issuer}: {count} ({count/total*100:.1f}%)")

        print(f"\n{Colors.BRIGHT_CYAN}Country Distribution:{Colors.RESET}")
        for country, count in sorted(countries.items(), key=lambda x: -x[1]):
            print(f"  {country}: {count} ({count/total*100:.1f}%)")

        if len(banks) <= 10:
            print(f"\n{Colors.BRIGHT_CYAN}Bank Distribution:{Colors.RESET}")
            for bank, count in sorted(banks.items(), key=lambda x: -x[1])[:5]:
                print(f"  {bank}: {count} ({count/total*100:.1f}%)")
        print(f"{Colors.BRIGHT_YELLOW}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━{Colors.RESET}")

        input(f"\n{Colors.DIM}Press Enter to continue...{Colors.RESET}")

    def run(self):
        try:
            while self.running:
                self.display_banner()
                self.display_menu()

                choice = input(f"\n{Colors.BRIGHT_GREEN}Enter your choice: {Colors.RESET}").strip()

                if choice == "1":
                    self.generate_single_flow()
                elif choice == "2":
                    self.generate_batch_flow()
                elif choice == "3":
                    self.validate_card_flow()
                elif choice == "4":
                    self.validate_batch_flow()
                elif choice == "5":
                    self.export_flow()
                elif choice == "6":
                    self.change_country_flow()
                elif choice == "7":
                    self.view_statistics_flow()
                elif choice == "8":
                    clear_screen()
                    AnimatedBanner.animate_banner(frames=5, delay=0.15)
                    input(f"\n{Colors.DIM}Press Enter to continue...{Colors.RESET}")
                elif choice == "9":
                    clear_screen()
                elif choice == "0":
                    print(f"\n{Colors.BRIGHT_CYAN}Exiting TestCardX...{Colors.RESET}")
                    print_footer()
                    self.running = False
                else:
                    print(f"{Colors.RED}Invalid choice. Please try again.{Colors.RESET}")
                    time.sleep(1)

        except KeyboardInterrupt:
            print(f"\n\n{Colors.YELLOW}Interrupted. Exiting...{Colors.RESET}")
        except Exception as e:
            print(f"\n{Colors.RED}Error: {e}{Colors.RESET}")
            self.logger.error(f"Runtime error: {e}", exc_info=True)

def main():
    parser = argparse.ArgumentParser(description="TestCardX - Credit Card Testing Utility")
    parser.add_argument("--country", default="USA", help="Default country for generation")
    parser.add_argument("--generate", type=int, help="Generate N cards and exit")
    parser.add_argument("--export", help="Export format: json, csv, pipe, sql")
    parser.add_argument("--output", help="Output filename")
    parser.add_argument("--validate", help="Validate a card number")
    parser.add_argument("--banner", action="store_true", help="Display animated banner")
    parser.add_argument("--batch", type=int, help="Batch generation with parallel processing")

    args = parser.parse_args()

    if args.banner:
        clear_screen()
        AnimatedBanner.animate_banner(frames=5, delay=0.15)
        return

    if args.validate:
        card_number = args.validate
        detected_issuer, country, bank = BINDatabase.detect_issuer(card_number)
        card = CardData(
            card_number=card_number,
            expiry_month="12",
            expiry_year="2030",
            cvv="123",
            issuer=detected_issuer,
            bank=bank,
            country=country,
            currency="USD"
        )
        result = CardValidator.validate_full(card)
        print(json.dumps(asdict(result), indent=2))
        return

    if args.generate:
        generator = CardGenerator(args.country)
        cards = generator.generate_batch(args.generate, parallel=True)
        print(f"Generated {len(cards)} cards for {args.country}")

        if args.export and args.output:
            if args.export == "json":
                ExportEngine.to_json(cards, args.output)
            elif args.export == "csv":
                ExportEngine.to_csv(cards, args.output)
            elif args.export == "pipe":
                with open(args.output, 'w') as f:
                    f.write(ExportEngine.to_pipe(cards))
            elif args.export == "sql":
                with open(args.output, 'w') as f:
                    f.write(ExportEngine.to_sql(cards))
            print(f"Exported to {args.output}")
        else:
            print(ExportEngine.to_pipe(cards))
        return

    app = TestCardXTUI()
    app.run()

if __name__ == "__main__":
    main()
