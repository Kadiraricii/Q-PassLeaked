### Task : Network Device Firmware Control / Ağ Cihazı Firmware Kontrolü
**Assigned Role / Atanan Rol:** Maestro / Maestro  
**Module File / Modül Dosyası:** `modules/network_device_firmware_control.py`

#### Expanded Instruction Set for Amateur Cybersecurity Students / Amatör Siber Güvenlik Öğrencileri İçin Genişletilmiş Talimat Seti

##### **1. Research / Araştırma**
**English:** Your task as Maestro is to gather resources to build a tool that checks firmware updates for network devices such as routers, access points, and modems.  
**Turkish:** Maestro olarak göreviniz, yönlendiriciler, erişim noktaları ve modemler gibi ağ cihazları için firmware güncellemelerini kontrol eden bir araç oluşturmak için kaynakları toplamaktır.  
- **Action / Eylem:**  
  **English:** Search for resources on firmware updates. Examples include:  
  - Manufacturer websites (e.g., Netgear, TP-Link).  
  - Firmware update APIs or databases (if available).  
  - Community forums or GitHub repositories with firmware check scripts.  
  **Turkish:** Firmware güncellemeleri için kaynakları araştırın. Örnekler:  
  - Üretici web siteleri (ör. Netgear, TP-Link).  
  - Firmware güncelleme API'leri veya veritabanları (varsa).  
  - Firmware kontrol betikleri içeren topluluk forumları veya GitHub depoları.  
- **Documentation / Dokümantasyon:** For each resource, note:  
  **English:**  
  - **Name and Type**: (e.g., "TP-Link Firmware Page - Website").  
  - **Access Method**: (e.g., "Web scraping," "API call").  
  - **Coverage**: (e.g., "Supports routers and modems").  
  - **Usage Instructions**: (e.g., "Requires device model and current firmware version").  
  **Turkish:**  
  - **İsim ve Tür**: (ör. "TP-Link Firmware Sayfası - Web Sitesi").  
  - **Erişim Yöntemi**: (ör. "Web kazıma," "API çağrısı").  
  - **Kapsam**: (ör. "Yönlendiriciler ve modemleri destekler").  
  - **Kullanım Talimatları**: (ör. "Cihaz modeli ve mevcut firmware sürümü gerektirir").  
- **Additional Scope / Ek Kapsam:**  
  **English:** Seek scripts or tools that automate firmware checks for multiple devices.  
  **Turkish:** Birden fazla cihaz için firmware kontrollerini otomatikleştiren betikler veya araçlar arayın.  
- **Output / Çıktı:**  
  **English:** Create a markdown file (`research_notes.md`) with sections: **Firmware Update Resources**, **Automation Tools**. Compile data into a JSON file (`research_data.json`) with keys: `firmware_resources`, `automation_tools`.  
  **Turkish:** Bir markdown dosyası (`research_notes.md`) oluşturun ve şu bölümleri ekleyin: **Firmware Güncelleme Kaynakları**, **Otomasyon Araçları**. Verileri bir JSON dosyasına (`research_data.json`) derleyin: `firmware_resources`, `automation_tools`.  

---

##### **2. Understand / Anlama**
**English:** Study the collected resources to grasp how firmware updates function for network devices. Focus on:  
- **Firmware Importance**: Why updates are vital for security.  
- **Update Processes**: How updates are checked and applied.  
- **Versioning**: How firmware versions are formatted (e.g., major/minor releases).  
- **Automation Challenges**: Issues in automating checks across manufacturers.  
**Turkish:** Toplanan kaynakları inceleyerek ağ cihazları için firmware güncellemelerinin nasıl çalıştığını anlayın. Şunlara odaklanın:  
- **Firmware Önemi**: Güncellemelerin güvenlik için neden önemli olduğu.  
- **Güncelleme Süreçleri**: Güncellemelerin nasıl kontrol edildiği ve uygulandığı.  
- **Sürümleme**: Firmware sürümlerinin nasıl yapılandırıldığı (ör. ana/alt sürümler).  
- **Otomasyon Zorlukları**: Farklı üreticiler arasında kontrolleri otomatikleştirmenin zorlukları.  
- **Reflection / Yansıma:**  
  **English:** Think about security risks from outdated firmware, like exposure to known exploits.  
  **Turkish:** Bilinen açıklara maruz kalma gibi eski firmware’in güvenlik risklerini değerlendirin.  
- **Output / Çıktı:**  
  **English:** Write a 200-250 word summary in `research_notes.md` under "Understanding Firmware Updates / Firmware Güncellemelerini Anlama." Cover the importance of updates and automation challenges.  
  **Turkish:** `research_notes.md` dosyasına "Firmware Güncellemelerini Anlama" başlığı altında 200-250 kelimelik bir özet yazın. Güncellemelerin önemi ve otomasyon zorluklarını ele alın.  

---

##### **3. Plan / Planlama**
**English:** Outline the script’s structure, including:  
- Functions: `get_device_info`, `check_firmware_version`, `compare_versions`.  
- Inputs: Device model, current firmware version.  
- Outputs: Update status, latest version.  
- Error Scenarios: Unsupported device, network errors.  
**Turkish:** Betiğin yapısını planlayın:  
- Fonksiyonlar: `get_device_info`, `check_firmware_version`, `compare_versions`.  
- Girdiler: Cihaz modeli, mevcut firmware sürümü.  
- Çıktılar: Güncelleme durumu, en son sürüm.  
- Hata Senaryoları: Desteklenmeyen cihaz, ağ hataları.  
- **Output / Çıktı:**  
  **English:** Add a "Design Plan / Tasarım Planı" section to `research_notes.md` with a function list, purposes, and pseudocode (e.g., "Input device info → Fetch latest version → Compare → Report").  
  **Turkish:** `research_notes.md` dosyasına "Tasarım Planı" bölümü ekleyin; fonksiyon listesi, amaçları ve sahte kod (ör. "Cihaz bilgisi girişi → En son sürümü al → Karşılaştır → Raporla") ile.  

---

##### **4. Implement / Uygulama**
**English:** Develop `network_device_firmware_control.py` in the `modules` directory.  
**Turkish:** `modules` dizininde `network_device_firmware_control.py` dosyasını oluşturun.  

**Step-by-Step Implementation / Adım Adım Uygulama:**  
- **Step 1: Get Device Info Function / Adım 1: Cihaz Bilgisi Alma Fonksiyonu**  
  **English:** Write `get_device_info(model)` to simulate fetching device details.  
  **Turkish:** Cihaz detaylarını simüle etmek için `get_device_info(model)` fonksiyonunu yazın.  
  ```python  
  def get_device_info(model):  
      device_db = {  
          "TP-Link Archer C7": {"manufacturer": "TP-Link", "update_url": "https://www.tp-link.com/support/download/archer-c7/"}  
      }  
      return device_db.get(model, None)  
  ```  

- **Step 2: Check Firmware Version Function / Adım 2: Firmware Sürümünü Kontrol Etme Fonksiyonu**  
  **English:** Write `check_firmware_version(device_info)` to fetch the latest version.  
  **Turkish:** En son sürümü almak için `check_firmware_version(device_info)` fonksiyonunu yazın.  
  ```python  
  import requests  
  from bs4 import BeautifulSoup  

  def check_firmware_version(device_info):  
      url = device_info["update_url"]  
      try:  
          response = requests.get(url)  
          soup = BeautifulSoup(response.text, "html.parser")  
          version_tag = soup.find("span", class_="version")  
          return version_tag.text if version_tag else "Unknown"  
      except Exception as e:  
          raise Exception(f"Error fetching firmware version: {str(e)}")  
  ```  

- **Step 3: Compare Versions Function / Adım 3: Sürümleri Karşılaştırma Fonksiyonu**  
  **English:** Write `compare_versions(current_version, latest_version)` to check for updates.  
  **Turkish:** Güncelleme kontrolü için `compare_versions(current_version, latest_version)` fonksiyonunu yazın.  
  ```python  
  def compare_versions(current_version, latest_version):  
      if current_version == latest_version:  
          return "Up to date / Güncel"  
      elif current_version < latest_version:  
          return "Update available / Güncelleme mevcut"  
      else:  
          return "Unknown status / Bilinmeyen durum"  
  ```  

- **Step 4: Error Handling / Adım 4: Hata İşleme**  
  **English:** Ensure `check_firmware_version` includes try-except for network errors (already added).  
  **Turkish:** `check_firmware_version` fonksiyonunun ağ hataları için try-except içerdiğinden emin olun (zaten eklendi).  

- **Step 5: Reporting Function / Adım 5: Raporlama Fonksiyonu**  
  **English:** Write `report_firmware_status(model, current_version, status, latest_version)` for logs.  
  **Turkish:** Günlükler için `report_firmware_status(model, current_version, status, latest_version)` fonksiyonunu yazın.  
  ```python  
  import time  

  def report_firmware_status(model, current_version, status, latest_version):  
      timestamp = time.strftime("%Y-%m-%d %H:%M:%S")  
      return f"### Firmware Check / Firmware Kontrolü\n- **Zaman / Time:** {timestamp}\n- **Cihaz / Device:** {model}\n- **Mevcut Sürüm / Current Version:** {current_version}\n- **Durum / Status:** {status}\n- **En Son Sürüm / Latest Version:** {latest_version}\n"  
  ```  

- **Step 6: Main Function / Adım 6: Ana Fonksiyon**  
  **English:** Write `main(model, current_version)` to tie everything together.  
  **Turkish:** Her şeyi birleştirmek için `main(model, current_version)` fonksiyonunu yazın.  
  ```python  
  def main(model, current_version):  
      device_info = get_device_info(model)  
      if not device_info:  
          return "Device not supported / Cihaz desteklenmiyor"  
      latest_version = check_firmware_version(device_info)  
      status = compare_versions(current_version, latest_version)  
      return report_firmware_status(model, current_version, status, latest_version)  
  ```  

---

##### **5. Test / Test Etme**
**English:** Test the script with:  
- **Supported Device**: "TP-Link Archer C7" with a known version.  
- **Unsupported Device**: "Unknown Model."  
- **Edge Cases**: Empty model, invalid version.  
**Turkish:** Betiği şu şekilde test edin:  
- **Desteklenen Cihaz**: Bilinen bir sürümle "TP-Link Archer C7."  
- **Desteklenmeyen Cihaz**: "Bilinmeyen Model."  
- **Kenar Durumlar**: Boş model, geçersiz sürüm.  
- **Output / Çıktı:**  
  **English:** Log in `test_results.md`: **Input** (model, current_version), **Expected Result**, **Actual Result**, **Observations**.  
  **Turkish:** `test_results.md` dosyasına kaydedin: **Giriş** (model, current_version), **Beklenen Sonuç**, **Gerçek Sonuç**, **Gözlemler**.  

---

##### **6. Confirm / Doğrulama**
**English:** Manually verify the firmware version on the manufacturer’s website.  
**Turkish:** Firmware sürümünü üreticinin web sitesinde manuel olarak doğrulayın.  
- **Output / Çıktı:**  
  **English:** Add a "Confirmation / Doğrulama" section to `test_results.md` with cross-check results and accuracy notes.  
  **Turkish:** `test_results.md` dosyasına "Doğrulama" bölümü ekleyin; çapraz kontrol sonuçları ve doğruluk notlarıyla.  

---

##### **7. Contribute / Katkı Sağlama**
**English:** Submit to `https://github.com/QLineTech/Q-Pentest`:  
- Fork the repo, create branch (`feature/firmware-control`), commit `network_device_firmware_control.py`, `research_notes.md`, `test_results.md`, `research_data.json`, and submit a pull request with a detailed description.  
**Turkish:** `https://github.com/QLineTech/Q-Pentest` adresine gönderin:  
- Depoyu çatallayın, dal oluşturun (`feature/firmware-control`), `network_device_firmware_control.py`, `research_notes.md`, `test_results.md`, `research_data.json` dosyalarını taahhüt edin ve detaylı bir açıklama ile pull request gönderin.  

---

#### Roadmap / Yol Haritası
**English:**  
- **Phase 1: Preparation / Hazırlık**: Research and document firmware resources.  
- **Phase 2: Learning and Planning / Öğrenme ve Planlama**: Study resources, summarize findings, plan script.  
- **Phase 3: Implementation / Uygulama**: Build functions for device info, firmware checks, and reporting.  
- **Phase 4: Testing and Validation / Test ve Doğrulama**: Test script, confirm results.  
- **Phase 5: Contribution / Katkı**: Submit work to GitHub.  
**Turkish:**  
- **Aşama 1: Hazırlık**: Firmware kaynaklarını araştırın ve belgeleyin.  
- **Aşama 2: Öğrenme ve Planlama**: Kaynakları inceleyin, bulguları özetleyin, betiği planlayın.  
- **Aşama 3: Uygulama**: Cihaz bilgisi, firmware kontrolü ve raporlama için fonksiyonlar oluşturun.  
- **Aşama 4: Test ve Doğrulama**: Betiği test edin, sonuçları doğrulayın.  
- **Aşama 5: Katkı**: Çalışmayı GitHub’a gönderin.  

---

#### Small Implementation Steps / Küçük Uygulama Adımları
**English:**  
- **Device Info**: Simulate fetching device details.  
- **Firmware Check**: Scrape the latest version from a website.  
- **Version Comparison**: Compare current and latest versions.  
- **Error Handling**: Manage unsupported devices and network issues.  
- **Reporting**: Format results in markdown.  
- **Main**: Integrate all functions into a workflow.  
**Turkish:**  
- **Cihaz Bilgisi**: Cihaz detaylarını simüle ederek alın.  
- **Firmware Kontrolü**: En son sürümü bir web sitesinden kazıyın.  
- **Sürüm Karşılaştırması**: Mevcut ve en son sürümleri karşılaştırın.  
- **Hata İşleme**: Desteklenmeyen cihazları ve ağ sorunlarını yönetin.  
- **Raporlama**: Sonuçları markdown formatında düzenleyin.  
- **Ana**: Tüm fonksiyonları bir iş akışına entegre edin.  
