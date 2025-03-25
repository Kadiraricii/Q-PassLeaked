### Task : Leaked Password Checker / Sızdırılmış Şifre Kontrolü
**Assigned Role / Atanan Rol:** Weaver / Dokumacı  
**Module File / Modül Dosyası:** `modules/leaked_password.py`

#### Expanded Instruction Set for Amateur Cybersecurity Students / Amatör Siber Güvenlik Öğrencileri İçin Genişletilmiş Talimat Seti

##### **1. Research / Araştırma**
**English:** As Weaver, your role is to gather and synthesize resources to build a robust tool for identifying leaked passwords.  
**Turkish:** Dokumacı olarak göreviniz, sızdırılmış şifreleri tanımlamak için sağlam bir araç oluşturmak üzere kaynakları toplamak ve sentezlemektir.  
- **Action / Eylem:** Use a search tool (e.g., "grok3 DeepSearch advanced") to find resources for checking leaked passwords. Examples include:  
  **English:** Online databases (e.g., Have I Been Pwned - HIBP), APIs (e.g., HIBP API, DeHashed API), downloadable breach datasets (e.g., from forums or security research sites), default password lists for devices (e.g., routers, IoT devices) and ISPs.  
  **Turkish:** Çevrimiçi veritabanları (ör. Have I Been Pwned - HIBP), API'ler (ör. HIBP API, DeHashed API), indirilebilir ihlal veri setleri (ör. forumlardan veya güvenlik araştırma sitelerinden), cihazlar (ör. yönlendiriciler, IoT cihazları) ve ISS'ler için varsayılan şifre listeleri.  
- **Documentation / Dokümantasyon:** For each resource, record:  
  **English:**  
  - **Name and Type**: (e.g., "HIBP - API").  
  - **Access Method**: (e.g., "Requires API key," "Free download").  
  - **Coverage**: (e.g., "500 million passwords from 400 breaches").  
  - **Usage Restrictions**: (e.g., "10 requests per minute," "Paid subscription").  
  - **Reliability**: (e.g., "Updated monthly," "Trusted by NIST").  
  **Turkish:**  
  - **İsim ve Tür**: (ör. "HIBP - API").  
  - **Erişim Yöntemi**: (ör. "API anahtarı gerektirir," "Ücretsiz indirme").  
  - **Kapsam**: (ör. "400 ihlalden 500 milyon şifre").  
  - **Kullanım Kısıtlamaları**: (ör. "Dakikada 10 istek," "Ücretli abonelik").  
  - **Güvenilirlik**: (ör. "Aylık güncellenir," "NIST tarafından güvenilir").  
- **Additional Scope / Ek Kapsam:**  
  **English:** Search for default credentials for common devices (e.g., "admin:admin" for routers) and ISPs (e.g., Verizon, Comcast). If no default passwords are found for a device or ISP, note it in a "devices_with_unknown_passwords" list.  
  **Turkish:** Yaygın cihazlar (ör. yönlendiriciler için "admin:admin") ve ISS'ler (ör. Verizon, Comcast) için varsayılan kimlik bilgilerini arayın. Bir cihaz veya ISS için varsayılan şifre bulunamazsa, bunu "devices_with_unknown_passwords" listesine not edin.  
- **Output / Çıktı:**  
  **English:** Create a markdown file (`research_notes.md`) with sections: **Leaked Password Resources**, **Default Password Lists**, **Devices/ISP Mapping**. Compile all data into a JSON file (`research_data.json`) with: `leaked_password_resources`, `default_passwords` (device_mapped_list, isp_mapped_list, isp_device_mapped_list), `unknown_password_devices`.  
  **Turkish:** Bir markdown dosyası (`research_notes.md`) oluşturun ve şu bölümleri ekleyin: **Sızdırılmış Şifre Kaynakları**, **Varsayılan Şifre Listeleri**, **Cihazlar/ISS Eşleştirmesi**. Tüm verileri bir JSON dosyasına (`research_data.json`) derleyin: `leaked_password_resources`, `default_passwords` (device_mapped_list, isp_mapped_list, isp_device_mapped_list), `unknown_password_devices`.  

**Example DeepSearch Prompt / Örnek DeepSearch Komutu:**  
**English:**  
```
Find all resources for checking leaked passwords (databases, APIs, tools) and default password lists for devices and ISPs. Include access methods, coverage, restrictions, and reliability. Create lists: device_mapped_list (device + user:pass), isp_mapped_list (ISP + user:pass), isp_device_mapped_list (ISP, device + user:pass). If no defaults are found, list devices in devices_with_unknown_passwords. Compile everything into a JSON file.
```  
**Turkish:**  
```
Sızdırılmış şifreleri kontrol etmek için tüm kaynakları (veritabanları, API'ler, araçlar) ve cihazlar ile ISS'ler için varsayılan şifre listelerini bulun. Erişim yöntemleri, kapsam, kısıtlamalar ve güvenilirlik bilgilerini ekleyin. Şu listeleri oluşturun: device_mapped_list (cihaz + kullanıcı:şifre), isp_mapped_list (ISS + kullanıcı:şifre), isp_device_mapped_list (ISS, cihaz + kullanıcı:şifre). Varsayılanlar bulunamazsa, cihazları devices_with_unknown_passwords listesine ekleyin. Her şeyi bir JSON dosyasına derleyin.
```

##### **2. Understand / Anlama**
**English:**  
- Study your researched resources to grasp how leaked password checks function. Focus on: **Hashing** (e.g., SHA-1 in HIBP), **Breach Compilation** (how datasets are built), **Default Password Risks** (why unchanged defaults are vulnerabilities), **API Mechanics** (e.g., k-anonymity in HIBP).  
**Turkish:**  
- Araştırdığınız kaynakları inceleyerek sızdırılmış şifre kontrollerinin nasıl çalıştığını kavrayın. Şunlara odaklanın: **Karma (Hashing)** (ör. HIBP'de SHA-1), **İhlal Derlemesi** (veri setleri nasıl oluşturulur), **Varsayılan Şifre Riskleri** (değiştirilmeyen varsayılanların neden güvenlik açığı olduğu), **API Mekanizmaları** (ör. HIBP'de k-anonimlik).  
- **Reflection / Yansıma:**  
  **English:** Consider real-world impacts: How leaked passwords enable credential stuffing, how default credentials lead to IoT botnets (e.g., Mirai).  
  **Turkish:** Gerçek dünya etkilerini düşünün: Sızdırılmış şifreler kimlik bilgisi doldurma saldırılarını nasıl mümkün kılar, varsayılan kimlik bilgileri IoT botnetlerine (ör. Mirai) nasıl yol açar.  
- **Output / Çıktı:**  
  **English:** Write a 200-250 word summary in `research_notes.md` under "Understanding Password Security / Şifre Güvenliğini Anlama." Include what you’ve learned about leaks and defaults, their role in threats, and how this enhances security awareness.  
  **Turkish:** `research_notes.md` dosyasına "Şifre Güvenliğini Anlama" başlığı altında 200-250 kelimelik bir özet yazın. Sızıntılar ve varsayılanlar hakkında öğrendiklerinizi, tehditlerdeki rollerini ve bunun güvenlik farkındalığını nasıl artırdığını ekleyin.  

##### **3. Plan / Planlama**
**English:**  
- Before coding, outline your script’s structure: Functions needed (e.g., hashing, API query, result checking), inputs (passwords), outputs (leak status, security level), error scenarios (e.g., network failure, invalid input).  
**Turkish:**  
- Kod yazmadan önce betiğinizin yapısını planlayın: Gerekli fonksiyonlar (ör. karma, API sorgusu, sonuç kontrolü), girdiler (şifreler), çıktılar (sızıntı durumu, güvenlik seviyesi), hata senaryoları (ör. ağ arızası, geçersiz giriş).  
- **Output / Çıktı:**  
  **English:** Add a "Design Plan / Tasarım Planı" section to `research_notes.md` with a list of functions and their purposes, plus a flowchart or pseudocode (e.g., "Input password → Hash → Query API → Check result").  
  **Turkish:** `research_notes.md` dosyasına "Tasarım Planı" bölümü ekleyin; fonksiyon listesi ve amaçlarını, ayrıca bir akış şeması veya sahte kod (ör. "Şifre girişi → Karma → API sorgusu → Sonuç kontrolü") dahil edin.  

##### **4. Implement / Uygulama**
**English:** Build `leaked_password.py` in the `modules` directory.  
**Turkish:** `modules` dizininde `leaked_password.py` dosyasını oluşturun.  

**Step-by-Step Implementation (Sage’s Guidance) / Adım Adım Uygulama (Bilge’nin Rehberliği):**  
- **Step 1: Hashing Function / Adım 1: Karma Fonksiyonu**  
  **English:** Create `hash_password(password)` to generate an SHA-1 hash.  
  **Turkish:** SHA-1 karma oluşturmak için `hash_password(password)` fonksiyonunu oluşturun.  
  ```python  
  import hashlib  

  def hash_password(password):  
      return hashlib.sha1(password.encode('utf-8')).hexdigest().upper()  
  ```  

- **Step 2: API Query Function / Adım 2: API Sorgu Fonksiyonu**  
  **English:** Create `query_hibp(hash_prefix)` to fetch HIBP data.  
  **Turkish:** HIBP verilerini almak için `query_hibp(hash_prefix)` fonksiyonunu oluşturun.  
  ```python  
  import requests  

  def query_hibp(hash_prefix):  
      url = f"https://api.pwnedpasswords.com/range/{hash_prefix}"  
      headers = {"User-Agent": "LeakedPasswordChecker"}  
      try:  
          response = requests.get(url, headers=headers, timeout=5)  
          return response.text if response.status_code == 200 else None  
      except requests.RequestException as e:  
          raise Exception(f"Ağ hatası / Network error: {str(e)}")  
  ```  

- **Step 3: Check Function / Adım 3: Kontrol Fonksiyonu**  
  **English:** Create `check_leaked_password(password)` to process and return results.  
  **Turkish:** Sonuçları işlemek ve döndürmek için `check_leaked_password(password)` fonksiyonunu oluşturun.  
  ```python  
  def check_leaked_password(password):  
      sha1_hash = hash_password(password)  
      prefix, suffix = sha1_hash[:5], sha1_hash[5:]  
      response = query_hibp(prefix)  
      if not response:  
          return {"is_leaked": None, "source": "HIBP", "security_level": "Bilinmeyen / Unknown", "error": "API hatası / API failure"}  
      if suffix in response:  
          count = int(response.split(suffix + ":")[1].split("\n")[0])  
          return {"is_leaked": True, "source": "HIBP", "security_level": "Düşük / Low", "breach_count": count}  
      return {"is_leaked": False, "source": "HIBP", "security_level": "Yüksek / High"}  
  ```  

- **Step 4: Default Password Check / Adım 4: Varsayılan Şifre Kontrolü**  
  **English:** Create `check_default_password(password, device=None, isp=None)` to cross-check against your JSON data.  
  **Turkish:** JSON verilerinizle çapraz kontrol için `check_default_password(password, device=None, isp=None)` fonksiyonunu oluşturun.  
  ```python  
  import json  

  def check_default_password(password, device=None, isp=None):  
      with open("research_data.json", "r") as f:  
          data = json.load(f)  
      for entry in data.get("default_passwords", {}).get("device_mapped_list", []):  
          if entry["password"] == password and (not device or entry["device"] == device):  
              return {"is_default": True, "source": "Cihaz Varsayılanları / Device Defaults", "device": entry["device"]}  
      return {"is_default": False, "source": "Cihaz Varsayılanları / Device Defaults"}  
  ```  

- **Step 5: Error Handling / Adım 5: Hata İşleme**  
  **English:** Add try-except blocks to handle errors in `check_leaked_password`.  
  **Turkish:** `check_leaked_password` fonksiyonuna hataları işlemek için try-except blokları ekleyin (zaten mevcut, ancak doğrulayın).  

- **Step 6: Reporting Function / Adım 6: Raporlama Fonksiyonu**  
  **English:** Create `report_event(password, result)` for markdown logs.  
  **Turkish:** Markdown günlükleri için `report_event(password, result)` fonksiyonunu oluşturun.  
  ```python  
  import time  

  def report_event(password, result):  
      timestamp = time.strftime("%Y-%m-%d %H:%M:%S")  
      return f"### Olay / Event\n- **Zaman / Time:** {timestamp}\n- **Şifre / Password:** {password}\n- **Sonuç / Result:** {result}\n"  
  ```  

- **Step 7: Main Function / Adım 7: Ana Fonksiyon**  
  **English:** Create `main(password, device=None, isp=None)` to integrate all checks.  
  **Turkish:** Tüm kontrolleri entegre etmek için `main(password, device=None, isp=None)` fonksiyonunu oluşturun.  
  ```python  
  def main(password, device=None, isp=None):  
      leak_result = check_leaked_password(password)  
      default_result = check_default_password(password, device, isp)  
      combined_result = {**leak_result, **default_result}  
      return report_event(password, combined_result)  
  ```  

##### **5. Test / Test Etme**
**English:**  
- Test your script with:  
  - **Leaked Passwords**: "123456," "password" (known HIBP leaks).  
  - **Non-Leaked**: "MySecure!2023," "UniquePass#99."  
  - **Default Passwords**: "admin" (common router default).  
  - **Edge Cases**: "", "特殊字符" (special characters).  
**Turkish:**  
- Betiğinizi şu şekilde test edin:  
  - **Sızdırılmış Şifreler**: "123456," "password" (bilinen HIBP sızıntıları).  
  - **Sızdırılmamış**: "MySecure!2023," "UniquePass#99."  
  - **Varsayılan Şifreler**: "admin" (yaygın yönlendirici varsayılanı).  
  - **Kenar Durumlar**: "", "特殊字符" (özel karakterler).  
- **Output / Çıktı:**  
  **English:** Log in `test_results.md`: **Input** (password, device/ISP if applicable), **Expected Result**, **Actual Result**, **Observations**.  
  **Turkish:** `test_results.md` dosyasına kaydedin: **Giriş** (şifre, varsa cihaz/ISS), **Beklenen Sonuç**, **Gerçek Sonuç**, **Gözlemler**.  

##### **6. Confirm / Doğrulama**
**English:**  
- Validate results with: HIBP website (manual check), another tool (e.g., DeHashed, local breach file), your JSON default password list.  
**Turkish:**  
- Sonuçları şu şekilde doğrulayın: HIBP web sitesi (manuel kontrol), başka bir araç (ör. DeHashed, yerel ihlal dosyası), JSON varsayılan şifre listeniz.  
- **Output / Çıktı:**  
  **English:** Add a "Confirmation / Doğrulama" section to `test_results.md` with cross-check findings and accuracy summary.  
  **Turkish:** `test_results.md` dosyasına "Doğrulama" bölümü ekleyin; çapraz kontrol bulguları ve doğruluk özeti ile.  

##### **7. Contribute / Katkı Sağlama**
**English:**  
- Submit to `https://github.com/QLineTech/Q-Pentest`: Fork the repo, branch (`feature/leaked-password-checker`), commit `leaked_password.py`, `research_notes.md`, `test_results.md`, `research_data.json`, submit pull request with a detailed description.  
**Turkish:**  
- `https://github.com/QLineTech/Q-Pentest` adresine gönderin: Depoyu çatallayın, dal oluşturun (`feature/leaked-password-checker`), `leaked_password.py`, `research_notes.md`, `test_results.md`, `research_data.json` dosyalarını taahhüt edin, detaylı bir açıklama ile pull request gönderin.  

---

#### Roadmap (Generated by Architect) / Yol Haritası (Mimar Tarafından Oluşturuldu)
**English:**  
- **Phase 1: Preparation / Hazırlık**: Research resources, document in markdown and JSON.  
- **Phase 2: Learning and Planning / Öğrenme ve Planlama**: Study resources, write summary, create design plan.  
- **Phase 3: Implementation / Uygulama**: Build hashing, API, check, default, error handling, reporting, and main functions.  
- **Phase 4: Testing and Validation / Test ve Doğrulama**: Test with various inputs, confirm with external sources.  
- **Phase 5: Contribution / Katkı**: Prepare files, submit to GitHub.  

**Turkish:**  
- **Aşama 1: Hazırlık**: Kaynakları araştırın, markdown ve JSON’da belgeleyin.  
- **Aşama 2: Öğrenme ve Planlama**: Kaynakları inceleyin, özet yazın, tasarım planı oluşturun.  
- **Aşama 3: Uygulama**: Karma, API, kontrol, varsayılan, hata işleme, raporlama ve ana fonksiyonları oluşturun.  
- **Aşama 4: Test ve Doğrulama**: Çeşitli girdilerle test edin, harici kaynaklarla doğrulayın.  
- **Aşama 5: Katkı**: Dosyaları hazırlayın, GitHub’a gönderin.  

---

#### Small Implementation Steps (Sage’s Guidance) / Küçük Uygulama Adımları (Bilge’nin Rehberliği)
**English:**  
- **Hashing**: Encode to UTF-8, use SHA-1, uppercase result.  
- **API Query**: Set timeout, add headers, handle exceptions.  
- **Leak Check**: Split hash, parse response, extract breach count.  
- **Default Check**: Load JSON, match password and context.  
- **Error Handling**: Catch network timeouts, invalid JSON, empty inputs.  
- **Reporting**: Format timestamp, structure markdown cleanly.  
- **Main**: Combine results logically, ensure modularity.  

**Turkish:**  
- **Karma**: UTF-8’e kodlayın, SHA-1 kullanın, sonucu büyük harf yapın.  
- **API Sorgusu**: Zaman aşımı belirleyin, başlıklar ekleyin, istisnaları ele alın.  
- **Sızıntı Kontrolü**: Karmayı ayırın, yanıtı ayrıştırın, ihlal sayısını çıkarın.  
- **Varsayılan Kontrol**: JSON’u yükleyin, şifre ve bağlamı eşleştirin.  
- **Hata İşleme**: Ağ zaman aşımı, geçersiz JSON, boş girdileri yakalayın.  
- **Raporlama**: Zaman damgasını biçimlendirin, markdown’ı düzenli yapılandırın.  
- **Ana**: Sonuçları mantıklı bir şekilde birleştirin, modülerliği sağlayın.  
