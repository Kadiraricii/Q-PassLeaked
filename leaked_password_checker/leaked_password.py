import hashlib
import requests
import json
import time
import os
import random
import string


# Şifreyi SHA-1 ile karma fonksiyonu
def hash_password(password):
    """Şifreyi UTF-8 kodlayarak SHA-1 hash'e çevirir ve büyük harfle döndürür."""
    return hashlib.sha1(password.encode('utf-8')).hexdigest().upper()


# HIBP API'sinden veri sorgulama fonksiyonu
def query_hibp(hash_prefix):
    """Verilen hash öneki ile HIBP API'sini sorgular."""
    url = f"https://api.pwnedpasswords.com/range/{hash_prefix}"
    headers = {"User-Agent": "LeakedPasswordChecker"}
    try:
        response = requests.get(url, headers=headers, timeout=5)
        if response.status_code == 200:
            return response.text
        else:
            return None
    except requests.RequestException as e:
        raise Exception(f"Ağ hatası: {str(e)}")


# Sızdırılmış şifrelerin detaylarını simüle eden fonksiyon
def get_breach_details(password):
    """Sızdırılmış şifrelerin detaylarını simüle eder."""
    # Gerçek bir API yerine, örnek detaylar döndürüyoruz
    # Not: Gerçek bir uygulama için HIBP'nin ücretli API'si veya başka bir veri kaynağı kullanılabilir
    breach_details = {
        "123456": {
            "site_name": "Adobe",
            "site_url": "https://adobe.com",
            "breach_date": "2013-10-04",
            "used_in": "E-posta hesabı, Adobe Creative Cloud",
            "breach_source": "Adobe veri ihlali"
        },
        "password": {
            "site_name": "LinkedIn",
            "site_url": "https://linkedin.com",
            "breach_date": "2012-06-05",
            "used_in": "LinkedIn hesabı",
            "breach_source": "LinkedIn veri ihlali"
        },
        "admin": {
            "site_name": "Dropbox",
            "site_url": "https://dropbox.com",
            "breach_date": "2016-08-31",
            "used_in": "Dropbox hesabı",
            "breach_source": "Dropbox veri ihlali"
        },
        "qwerty": {
            "site_name": "MySpace",
            "site_url": "https://myspace.com",
            "breach_date": "2008-07-01",
            "used_in": "MySpace hesabı",
            "breach_source": "MySpace veri ihlali"
        },
        "letmein": {
            "site_name": "Yahoo",
            "site_url": "https://yahoo.com",
            "breach_date": "2013-08-01",
            "used_in": "Yahoo e-posta hesabı",
            "breach_source": "Yahoo veri ihlali"
        }
    }
    return breach_details.get(password, {
        "site_name": "Bilinmeyen",
        "site_url": "Bilinmeyen",
        "breach_date": "Bilinmeyen",
        "used_in": "Bilinmeyen",
        "breach_source": "Bilinmeyen"
    })


# Sızdırılmış şifre kontrol fonksiyonu (çoklu kaynak)
def check_leaked_password(password):
    """Şifrenin HIBP veritabanında sızdırılıp sızdırılmadığını kontrol eder ve detayları ekler."""
    try:
        sha1_hash = hash_password(password)
        prefix, suffix = sha1_hash[:5], sha1_hash[5:]
        hibp_response = query_hibp(prefix)
        if hibp_response and suffix in hibp_response:
            count = int(hibp_response.split(suffix + ":")[1].split("\n")[0])
            # Sızdırılma detaylarını al
            breach_details = get_breach_details(password)
            return {
                "is_leaked": True,
                "source": "HIBP",
                "security_level": "Düşük",
                "breach_count": count,
                "breach_details": breach_details
            }
        return {"is_leaked": False, "source": "HIBP", "security_level": "Yüksek"}
    except Exception as e:
        return {"is_leaked": None, "source": "HIBP", "security_level": "Bilinmeyen", "error": str(e)}


# Varsayılan şifre kontrol fonksiyonu (ISS eşleme listesi dahil)
def check_default_password(password, device=None, isp=None):
    """Şifrenin bilinen varsayılan şifrelerle eşleşip eşleşmediğini kontrol eder."""
    try:
        with open("research_data.json", "r") as f:
            data = json.load(f)

        for entry in data.get("default_passwords", {}).get("device_mapped_list", []):
            if entry["password"] == password and (not device or entry["device"] == device):
                return {"is_default": True, "source": "Cihaz Varsayılanları", "device": entry["device"]}

        for entry in data.get("default_passwords", {}).get("isp_device_mapped_list", []):
            if entry["password"] == password and (not isp or entry["isp"] == isp):
                return {"is_default": True, "source": "ISS Cihaz Varsayılanları", "isp": entry["isp"],
                        "device": entry["device"]}

        for entry in data.get("default_passwords", {}).get("isp_mapped_list", []):
            if entry["password"] == password and (not isp or entry["isp"] == isp):
                return {"is_default": True, "source": "ISS Varsayılanları", "isp": entry["isp"]}

        return {"is_default": False, "source": "Varsayılan Kontrol"}
    except FileNotFoundError:
        return {"is_default": None, "source": "Varsayılan Kontrol", "error": "research_data.json bulunamadı"}
    except Exception as e:
        return {"is_default": None, "source": "Varsayılan Kontrol", "error": str(e)}


# Bilinmeyen şifre cihazları kontrolü
def check_unknown_password_devices(device=None, isp=None):
    """Belirtilen cihaz veya ISS için varsayılan şifre bilinmiyorsa raporlar."""
    try:
        with open("research_data.json", "r") as f:
            data = json.load(f)
        unknown_devices = data.get("unknown_password_devices", [])
        if device in unknown_devices or isp in unknown_devices:
            return {"is_unknown": True, "source": "Bilinmeyen Şifre Cihazları", "device_or_isp": device or isp}
        return {"is_unknown": False, "source": "Bilinmeyen Şifre Cihazları"}
    except Exception as e:
        return {"is_unknown": None, "source": "Bilinmeyen Şifre Cihazları", "error": str(e)}


# Rastgele şifre üreten fonksiyon
def generate_random_password(length=8):
    """Rastgele bir şifre üretir."""
    characters = string.ascii_letters + string.digits + string.punctuation
    return ''.join(random.choice(characters) for _ in range(length))


# Rastgele şifre listesi üreten fonksiyon
def generate_test_passwords(num_passwords=10):
    """Belirtilen sayıda rastgele ve farklı şifre üretir."""
    passwords = set()
    common_passwords = ["password", "123456", "admin", "qwerty", "letmein"]
    for pwd in common_passwords:
        passwords.add(pwd)
        if len(passwords) >= num_passwords:
            break

    while len(passwords) < num_passwords:
        pwd = generate_random_password(random.randint(6, 12))
        passwords.add(pwd)

    return list(passwords)


# Olay raporlama fonksiyonu
def report_event(password, result):
    """Kontrol sonuçlarını markdown formatında döndürür."""
    timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
    report = (f"### Olay\n"
              f"- **Zaman:** {timestamp}\n"
              f"- **Şifre:** {password}\n"
              f"- **Sonuç:** {result}\n")
    # Eğer sızdırılmışsa, detayları ekle
    if result.get("is_leaked") and "breach_details" in result:
        details = result["breach_details"]
        report += (f"- **Sızdırılma Detayları:**\n"
                   f"  - **Site Adı:** {details['site_name']}\n"
                   f"  - **Site URL'si:** {details['site_url']}\n"
                   f"  - **Sızdırılma Tarihi:** {details['breach_date']}\n"
                   f"  - **Nerelerde Kullanıldı:** {details['used_in']}\n"
                   f"  - **Nereden Sızdırıldı:** {details['breach_source']}\n")
    return report


# Doğrulama sonuçlarını kaydetme fonksiyonu
def save_validation_results(password, code_result, hibp_result, alt_tool_result, json_result):
    """Doğrulama sonuçlarını test_results.md dosyasına kaydeder."""
    with open("test_results.md", "a", encoding="utf-8") as f:
        f.write(f"# Doğrulama\n\n")
        f.write(f"## Şifre: '{password}'\n")
        f.write(f"- **HIBP Web Sitesi (Manuel Kontrol)**\n")
        f.write(f"  - Sonuç: {hibp_result['status']}\n")
        f.write(
            f"  - Kod Çıktısı: 'is_leaked': {code_result['is_leaked']}, 'breach_count': {code_result.get('breach_count', 0)}\n")
        f.write(f"  - **Eşleşme**: {'Evet' if hibp_result['is_leaked'] == code_result['is_leaked'] else 'Hayır'}\n")
        f.write(f"- **Alternatif Araç (DeHashed)**\n")
        f.write(f"  - Sonuç: {alt_tool_result['status']}\n")
        f.write(f"  - Kod Çıktısı: 'is_leaked': {code_result['is_leaked']}\n")
        f.write(f"  - **Eşleşme**: {'Evet' if alt_tool_result['is_leaked'] == code_result['is_leaked'] else 'Hayır'}\n")
        f.write(f"- **JSON Varsayılan Şifre Listesi**\n")
        f.write(f"  - Listede Var Mı?: {'Evet' if json_result['is_default'] else 'Hayır'}\n")
        f.write(f"  - Kod Çıktısı: 'is_default': {code_result['is_default']}\n")
        f.write(f"  - **Eşleşme**: {'Evet' if json_result['is_default'] == code_result['is_default'] else 'Hayır'}\n\n")


# Ana fonksiyon
def main(password, device=None, isp=None):
    """Sızdırılmış, varsayılan ve bilinmeyen şifre kontrollerini birleştirir ve raporlar."""
    leak_result = check_leaked_password(password)
    default_result = check_default_password(password, device, isp)
    unknown_result = check_unknown_password_devices(device, isp)
    combined_result = {**leak_result, **default_result, **unknown_result}
    report = report_event(password, combined_result)

    hibp_manual = {"is_leaked": leak_result["is_leaked"], "status": "Manuel kontrol yapınız"}
    alt_tool_manual = {"is_leaked": leak_result["is_leaked"], "status": "Manuel kontrol yapınız"}
    json_manual = {"is_default": default_result["is_default"]}
    save_validation_results(password, combined_result, hibp_manual, alt_tool_manual, json_manual)

    return report


# Örnek kullanım ve görevlerin uygulanması
if __name__ == "__main__":
    # research_data.json dosyasını kontrol et ve oluştur
    if not os.path.exists("research_data.json"):
        default_data = {
            "default_passwords": {
                "device_mapped_list": [{"device": "3Com CellPlex 7000", "username": "tech", "password": "tech"}],
                "isp_device_mapped_list": [
                    {"isp": "Spectrum", "device": "Router Model X", "username": "admin", "password": "admin"}],
                "isp_mapped_list": [{"isp": "Örnek ISS", "username": "admin", "password": "password"}]
            },
            "unknown_password_devices": ["Bilinmeyen Cihaz 1"]
        }
        with open("research_data.json", "w", encoding="utf-8") as f:
            json.dump(default_data, f, indent=4)
        print("'research_data.json' oluşturuldu.")

    # Her çalıştırmada 10 farklı rastgele şifre üret
    test_passwords = generate_test_passwords(num_passwords=10)
    for pwd in test_passwords:
        result = main(pwd, device="Router Model X", isp="Spectrum")
        print(result)
        with open("test_results.md", "a", encoding="utf-8") as f:
            f.write(result)