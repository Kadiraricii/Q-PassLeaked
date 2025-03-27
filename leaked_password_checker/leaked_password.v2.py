import hashlib
import requests
import json
import time
import os
import random
import string
import logging
import asyncio
import aiohttp
import math
import certifi
import ssl
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from colorama import init, Fore, Style  # Renkli terminal için

# Colorama’yı başlat
init(autoreset=True)

# Fontları kaydet (yolları fonts/ dizinine göre güncelle)
pdfmetrics.registerFont(TTFont('DejaVuSans', 'fonts/DejaVuSans.ttf'))
pdfmetrics.registerFont(TTFont('DejaVuSans-Bold', 'fonts/DejaVuSans-Bold.ttf'))

logging.basicConfig(filename='password_checker.log', level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')

OPEN_SOURCE_PASSWORDS = {
    "123456", "password", "12345678", "qwerty", "123456789", "12345", "1234", "111111", "1234567", "dragon",
    "123123", "baseball", "abc123", "football", "monkey", "letmein", "696969", "shadow", "master", "666666",
    "qwertyuiop", "123321", "mustang", "1234567890", "michael", "654321", "pussy", "superman", "1qaz2wsx", "7777777",
    "fuckyou", "121212", "000000", "qazwsx", "123qwe", "killer", "trustno1", "jordan", "jennifer", "zxcvbnm",
    "asdfgh", "hunter", "buster", "soccer", "harley", "batman", "andrew", "tigger", "sunshine", "iloveu",
    "fuckme", "2000", "charlie", "robert", "thomas", "hockey", "ranger", "daniel", "starwars", "klaster",
    "112233", "george", "asshole", "computer", "michelle", "jessica", "pepper", "1111", "zxcvbn", "555555",
    "11111111", "131313", "freedom", "777777", "pass", "fuck", "maggie", "159753", "aaaaaa", "ginger",
    "princess", "joshua", "cheese", "amanda", "summer", "love", "ashley", "6969", "nicole", "chelsea",
    "biteme", "matthew", "access", "yankees", "987654321", "dallas", "austin", "thunder", "taylor", "matrix"
}


async def check_pwned_password_async(password, session, retries=3):
    sha1_hash = hashlib.sha1(password.encode('utf-8')).hexdigest().upper()
    prefix, suffix = sha1_hash[:5], sha1_hash[5:]
    url = f"https://api.pwnedpasswords.com/range/{prefix}"

    for attempt in range(retries):
        try:
            async with session.get(url, timeout=aiohttp.ClientTimeout(total=5)) as response:
                if response.status == 200:
                    text = await response.text()
                    for line in text.splitlines():
                        if line.startswith(suffix):
                            count = int(line.split(':')[1])
                            logging.info(f"HIBP: {password[:2]}... sızdırılmış, {count} kez")
                            return {"is_leaked": True, "breach_count": count, "source": "HIBP"}
                    return {"is_leaked": False, "breach_count": 0, "source": "HIBP"}
                logging.warning(f"HIBP: {response.status}")
                return {"is_leaked": None, "breach_count": 0, "source": "HIBP",
                        "error": f"Durum kodu: {response.status}"}
        except Exception as e:
            logging.error(f"HIBP deneme {attempt + 1} başarısız: {str(e)}")
            if attempt == retries - 1:
                return {"is_leaked": None, "breach_count": 0, "source": "HIBP", "error": "Ağ hatası, tekrar denendi"}
            await asyncio.sleep(1)


async def check_leakcheck_async(password, session):
    api_key = "9d2dd7d51952ef5a0163b407171f6e4c6187f7ab"
    url = f"https://leakcheck.io/api/public?key={api_key}&check={password}"
    try:
        async with session.get(url) as response:
            if response.status == 200:
                data = await response.json()
                logging.info(f"LeakCheck: {password[:2]}... {'sızdırılmış' if data['success'] else 'temiz'}")
                return {"is_leaked": data["success"], "sources": data.get("sources", []), "source": "LeakCheck"}
            elif response.status == 429:
                logging.warning("LeakCheck kota limiti aşıldı")
                return {"is_leaked": None, "sources": [], "source": "LeakCheck", "error": "Ücretsiz hakkın bitti"}
            return {"is_leaked": None, "sources": [], "source": "LeakCheck", "error": f"Durum kodu: {response.status}"}
    except Exception as e:
        logging.error(f"LeakCheck hatası: {str(e)}")
        return {"is_leaked": None, "sources": [], "source": "LeakCheck", "error": str(e)}


def check_open_source_list(password):
    if password in OPEN_SOURCE_PASSWORDS:
        logging.info(f"Açık Kaynak: {password[:2]}... sızdırılmış")
        return {"is_leaked": True, "source": "Açık Kaynak Listesi"}
    return {"is_leaked": False, "source": "Açık Kaynak Listesi"}


def get_breach_details(password, source_result):
    if not source_result["is_leaked"]:
        return {"site_name": "Yok", "site_url": "Yok", "breach_date": "Yok", "used_in": "Yok",
                "breach_source": source_result["source"]}

    sim_details = {
        "123456": {"site_name": "Adobe", "site_url": "https://adobe.com", "breach_date": "2013-10-04",
                   "used_in": "E-posta", "breach_source": "Adobe ihlali"},
        "password": {"site_name": "LinkedIn", "site_url": "https://linkedin.com", "breach_date": "2012-06-05",
                     "used_in": "LinkedIn", "breach_source": "LinkedIn ihlali"},
        "admin": {"site_name": "Dropbox", "site_url": "https://dropbox.com", "breach_date": "2016-08-31",
                  "used_in": "Dropbox", "breach_source": "Dropbox ihlali"},
        "qwerty": {"site_name": "MySpace", "site_url": "https://myspace.com", "breach_date": "2008-07-01",
                   "used_in": "MySpace", "breach_source": "MySpace ihlali"},
        "123456789": {"site_name": "RockYou", "site_url": "https://rockyou.com", "breach_date": "2009-12-14",
                      "used_in": "Oyun", "breach_source": "RockYou ihlali"},
        "letmein": {"site_name": "Twitter", "site_url": "https://twitter.com", "breach_date": "2018-05-03",
                    "used_in": "Twitter", "breach_source": "Twitter ihlali"},
        "monkey": {"site_name": "Yahoo", "site_url": "https://yahoo.com", "breach_date": "2013-08-01",
                   "used_in": "E-posta", "breach_source": "Yahoo ihlali"},
        "football": {"site_name": "Ashley Madison", "site_url": "https://ashleymadison.com",
                     "breach_date": "2015-07-15", "used_in": "Hesap", "breach_source": "Ashley Madison ihlali"}
    }
    return sim_details.get(password, {"site_name": "Bilinmeyen", "site_url": "Bilinmeyen", "breach_date": "Bilinmeyen",
                                      "used_in": "Bilinmeyen", "breach_source": source_result["source"]})


def estimate_crack_time(password):
    charset_size = 0
    if any(c.islower() for c in password): charset_size += 26
    if any(c.isupper() for c in password): charset_size += 26
    if any(c.isdigit() for c in password): charset_size += 10
    if any(c in string.punctuation for c in password): charset_size += 32

    combinations = charset_size ** len(password) if charset_size > 0 else 1
    guesses_per_second = 1_000_000_000
    seconds = combinations / guesses_per_second

    if seconds < 1:
        return f"{seconds * 1_000_000:.2f} mikrosaniye"
    elif seconds < 60:
        return f"{seconds:.2f} saniye"
    elif seconds < 3600:
        return f"{seconds / 60:.2f} dakika"
    elif seconds < 86400:
        return f"{seconds / 3600:.2f} saat"
    elif seconds < 31536000:
        return f"{seconds / 86400:.2f} gün"
    else:
        return f"{seconds / 31536000:.2f} yıl"


def analyze_password_strength_advanced(password):
    score = 0
    entropy = len(set(password)) * math.log2(len(password)) if password else 0
    common_passwords = OPEN_SOURCE_PASSWORDS

    if password in common_passwords: score -= 2
    if len(password) >= 12:
        score += 2
    elif len(password) >= 8:
        score += 1
    if any(c.isupper() for c in password): score += 1
    if any(c.islower() for c in password): score += 1
    if any(c.isdigit() for c in password): score += 1
    if any(c in string.punctuation for c in password): score += 1
    if entropy > 30: score += 1
    if len(set(password)) < len(password) / 2: score -= 1

    level = "Zayıf" if score < 3 else "Orta" if score < 5 else "Güçlü"
    funny_warnings = [
        "RUHİ1234 OLABİLİR Mİ?"
        "GÖRMEDİM SAY!"
        "BEN 3 DEN GERİYE SAYANA KADAR SEN BU ŞİFREYİ BENİM ÖNERDİĞİM ŞİFRE İLE DEĞİŞTİR 3.........2........."
        "Aman dikkat, bu şifreyle kapıyı çalmadan girerler!",
        "Kedi bile bu şifreyi patisiyle çözer!",
        "Hackerlar bunu görünce parti vermeye başladı!",
        "Bu şifre mi, yoksa şaka mı anlamadım?",
        "Bunu yazarken güvenlik alarmı çaldı!",
        "Şifren zayıf, ama cesaretin büyük!",
        "123456 yazsaydın da olurdu, ne fark eder ki?"
    ]
    funny_warning = random.choice(funny_warnings) if score < 3 else ""
    return {"score": min(max(score, 0), 6), "level": level, "entropy": entropy, "warning": funny_warning}


def suggest_strong_password():
    while True:
        pwd = ''.join(random.choice(string.ascii_letters + string.digits + string.punctuation) for _ in range(16))
        strength = analyze_password_strength_advanced(pwd)
        if strength["level"] == "Güçlü":
            return pwd


def report_event(password, hibp_result, leakcheck_result, opensource_result, strength_result):
    timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
    crack_time = estimate_crack_time(password)
    report = ("OLAY RAPORU\n"
              f"ZAMAN: {timestamp}\n"
              f"ŞİFRE: {password}\n"
              f"ŞİFRE GÜCÜ: {strength_result['level']} (Puan: {strength_result['score']}/6, Entropi: {strength_result['entropy']:.2f})\n"
              f"TAHMİNİ KIRILMA SÜRESİ: {crack_time}\n")

    if strength_result["warning"]:
        report += f"ŞAKA MI BU?: {strength_result['warning']}\n"

    report += "HIBP SONUCU: "
    if hibp_result.get("error"):
        report += f"Hata: {hibp_result['error']}\n"
    else:
        report += f"Sızdırılmış: {'Evet' if hibp_result['is_leaked'] else 'Hayır'}, Kaç kez: {hibp_result['breach_count']}\n"
        if hibp_result["is_leaked"]:
            details = get_breach_details(password, hibp_result)
            report += f"  Site: {details['site_name']}, Tarih: {details['breach_date']}\n"

    report += "LEAKCHECK SONUCU: "
    if leakcheck_result.get("error"):
        report += f"Hata: {leakcheck_result['error']}\n"
    else:
        report += f"Sızdırılmış: {'Evet' if leakcheck_result['is_leaked'] else 'Hayır'}, Kaynaklar: Diğer sayfada verilmiştir\n"

    report += f"AÇIK KAYNAK SONUCU: Sızdırılmış: {'Evet' if opensource_result['is_leaked'] else 'Hayır'}\n"

    if strength_result["level"] in ["Zayıf", "Orta"]:
        suggested_pwd = suggest_strong_password()
        suggested_crack_time = estimate_crack_time(suggested_pwd)
        report += (f"ÖNERİLEN GÜÇLÜ ŞİFRE: {suggested_pwd}\n"
                   f"ÖNERİLEN ŞİFRENİN KIRILMA SÜRESİ: {suggested_crack_time}\n")

    # Terminal için kısa rapor
    short_report = ("OLAY RAPORU\n"
                    f"ZAMAN: {timestamp}\n"
                    f"ŞİFRE: {password}\n"
                    f"ŞİFRE GÜCÜ: {strength_result['level']}\n"
                    f"TAHMİNİ KIRILMA SÜRESİ: {crack_time}\n\n"
                    "DİĞER BİLGİLER İÇİN LÜTFEN PDF’YE BAKINIZ")

    return report, leakcheck_result.get("sources", []), timestamp, password, short_report


def save_as_pdf_enhanced(password, report, strength_score, leakcheck_sources, timestamp, original_password):
    date_str = time.strftime("%Y-%m-%d")
    filename = f"PasswordReport_{password[:3]}_{date_str}.pdf"
    c = canvas.Canvas(filename, pagesize=letter)

    # Arka planı daha açık gri yap (RGB: 0.85, 0.85, 0.85)
    c.setFillColorRGB(0.85, 0.85, 0.85)
    c.rect(0, 0, letter[0], letter[1], fill=1)

    c.setFont("DejaVuSans", 11)
    c.setFillColorRGB(0, 0, 0)
    c.setTitle(f"Şifre Raporu - {password[:3]}")

    # Başlık
    c.setFont("DejaVuSans-Bold", 14)
    c.drawString(50, 750, "ŞİFRE GÜVENLİK RAPORU")

    # Metni yaz, satır aralarına boşluk ekle
    y = 720
    c.setFont("DejaVuSans-Bold", 11)
    for line in report.split("\n"):
        if ":" not in line or line.startswith("  "):
            c.setFont("DejaVuSans", 11)
            c.drawString(50, y, line)
        else:
            c.setFont("DejaVuSans-Bold", 11)
            c.drawString(50, y, line.upper())
        y -= 25

        if y < 50:
            c.showPage()
            c.setFillColorRGB(0.85, 0.85, 0.85)
            c.rect(0, 0, letter[0], letter[1], fill=1)
            c.setFillColorRGB(0, 0, 0)
            c.setFont("DejaVuSans-Bold", 11)
            y = 750

    # Şifre gücü kısmı
    strength_level = "ZAYIF" if strength_score < 3 else "ORTA" if strength_score < 5 else "GÜÇLÜ"
    c.setFont("DejaVuSans-Bold", 11)
    strength_text = f"ŞİFRE GÜCÜ=({strength_score}/6)"
    c.drawString(50, y - 25, strength_text)

    # Metnin genişliğini hesapla
    text_width = c.stringWidth(strength_text, "DejaVuSans-Bold", 11)
    bar_x = 50 + text_width + 10

    # Grafik
    c.setFillColorRGB(0, 0.5 if strength_score >= 3 else 1, 0)
    bar_width = strength_score * 40
    c.rect(bar_x, y - 30, bar_width, 15, fill=1)

    # Seviye metni
    c.setFillColorRGB(0, 0, 0)
    c.setFont("DejaVuSans", 11)
    level_x = bar_x + bar_width + 10
    c.drawString(level_x, y - 25, f"({strength_level})")

    # İkinci sayfa: LeakCheck kaynakları
    c.showPage()
    c.setFillColorRGB(0.85, 0.85, 0.85)
    c.rect(0, 0, letter[0], letter[1], fill=1)
    c.setFillColorRGB(0, 0, 0)

    # İkinci sayfa başlıkları
    y = 750
    c.setFont("DejaVuSans-Bold", 14)
    c.drawString(50, y, "ŞİFRE GÜVENLİK RAPORU")
    y -= 25

    c.setFont("DejaVuSans-Bold", 11)
    c.drawString(50, y, "OLAY RAPORU")
    y -= 25

    c.drawString(50, y, f"ZAMAN: {timestamp}")
    y -= 25

    c.drawString(50, y, f"ŞİFRE: {original_password}")
    y -= 25

    c.drawString(50, y, "LEAKCHECK SONUCU KAYNAKLARI:")
    y -= 25

    # Kaynakları alt alta yaz
    c.setFont("DejaVuSans", 11)
    for source in leakcheck_sources:
        c.drawString(50, y, str(source))
        y -= 25
        if y < 50:
            c.showPage()
            c.setFillColorRGB(0.85, 0.85, 0.85)
            c.rect(0, 0, letter[0], letter[1], fill=1)
            c.setFillColorRGB(0, 0, 0)
            c.setFont("DejaVuSans", 11)
            y = 750

    c.save()
    logging.info(f"PDF oluşturuldu: {filename}")
    return filename


async def main_async(passwords):
    ssl_context = ssl.create_default_context(cafile=certifi.where())
    async with aiohttp.ClientSession(connector=aiohttp.TCPConnector(ssl=ssl_context)) as session:
        hibp_tasks = [check_pwned_password_async(pwd, session) for pwd in passwords]
        leakcheck_tasks = [check_leakcheck_async(pwd, session) for pwd in passwords]
        hibp_results = await asyncio.gather(*hibp_tasks)
        leakcheck_results = await asyncio.gather(*leakcheck_tasks)

        for pwd, hibp_res, leak_res in zip(passwords, hibp_results, leakcheck_results):
            opensource_res = check_open_source_list(pwd)
            strength = analyze_password_strength_advanced(pwd)
            report, leakcheck_sources, timestamp, original_password, short_report = report_event(pwd, hibp_res,
                                                                                                 leak_res,
                                                                                                 opensource_res,
                                                                                                 strength)
            pdf_file = save_as_pdf_enhanced(pwd, report, strength["score"], leakcheck_sources, timestamp,
                                            original_password)

            # Terminalde kısa raporu yazdır
            lines = short_report.split("\n")
            for i, line in enumerate(lines):
                if line == "DİĞER BİLGİLER İÇİN LÜTFEN PDF’YE BAKINIZ":
                    print(Fore.GREEN + line)  # Yeşil renkte
                else:
                    print(Fore.YELLOW + line)  # Turuncu renkte
            # PDF dosya yolunu turuncu renkte yazdır
            print(Fore.YELLOW + f"PDF: {os.path.abspath(pdf_file)}")
            print(Fore.YELLOW + '-' * 50)


def interactive_mode():
    # Giriş mesajlarını kırmızı renkte yazdır
    print(Fore.RED + "Şifre Kontrol Aracına Hoş Geldiniz!")
    print(Fore.RED + "Birden fazla şifre için virgülle ayırın (örn: 123456,şifre), çıkmak için 'q'")
    while True:
        try:
            print(Fore.RED + "\nŞifre(ler)i girin: ", end="")
            pwd_input = input()
            if pwd_input.lower() == 'q':
                print(Fore.RED + "Çıkılıyor...")
                break
            passwords = [p.strip() for p in pwd_input.split(",")]
            asyncio.run(main_async(passwords))
        except KeyboardInterrupt:
            print(Fore.RED + "\nProgramdan çıkılıyor...")
            break


if __name__ == "__main__":
    interactive_mode()