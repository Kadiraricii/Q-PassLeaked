### Task : Vulnerability Scanning of Linux Servers / Linux Sunucularında Güvenlik Açığı Tarama
**Assigned Role / Atanan Rol:** Architect / Mimar  
**Module File / Modül Dosyası:** `modules/vulnerability_scanner.py`

#### Expanded Instruction Set for Amateur Cybersecurity Students / Amatör Siber Güvenlik Öğrencileri İçin Genişletilmiş Talimat Seti

##### **1. Research / Araştırma**
**English:** Your task is to gather resources and methods for scanning Linux servers for vulnerabilities using tools like Nmap, OpenVAS, or Nikto.  
**Turkish:** Göreviniz, Nmap, OpenVAS veya Nikto gibi araçları kullanarak Linux sunucularını güvenlik açıkları açısından taramak için kaynaklar ve yöntemler toplamaktır.  
- **Action / Eylem:**  
  **English:** Search for resources on vulnerability scanning. Examples include:  
  - Nmap Vulnerability Scripts (e.g., `vuln.nse`, `vulners.nse`).  
  - OpenVAS (open-source vulnerability scanner).  
  - Nikto (web server scanner).  
  - Documentation (e.g., Nmap scripting guide, OpenVAS manual).  
  **Turkish:** Güvenlik açığı tarama kaynakları bulun. Örnekler:  
  - Nmap Güvenlik Açığı Betikleri (ör. `vuln.nse`, `vulners.nse`).  
  - OpenVAS (açık kaynaklı güvenlik açığı tarayıcı).  
  - Nikto (web sunucu tarayıcı).  
  - Dokümantasyon (ör. Nmap betik kılavuzu, OpenVAS kılavuzu).  
- **Documentation / Dokümantasyon:** For each resource, note:  
  **English:**  
  - **Name and Type**: (e.g., "Nmap - Tool").  
  - **Access Method**: (e.g., "Install via apt," "Download from website").  
  - **Coverage**: (e.g., "Scans for CVE vulnerabilities via service versions").  
  - **Usage Instructions**: (e.g., "Run `nmap -sV --script vuln`").  
  **Turkish:**  
  - **İsim ve Tür**: (ör. "Nmap - Araç").  
  - **Erişim Yöntemi**: (ör. "Apt ile kurulum," "Web sitesinden indirme").  
  - **Kapsam**: (ör. "Hizmet sürümleriyle CVE güvenlik açıklarını tarar").  
  - **Kullanım Talimatları**: (ör. "`nmap -sV --script vuln` komutunu çalıştırın").  
- **Additional Scope / Ek Kapsam:**  
  **English:** Investigate techniques to prioritize critical vulnerabilities (e.g., CVSS scores, exploit availability).  
  **Turkish:** Kritik güvenlik açıklarını önceliklendirme tekniklerini araştırın (ör. CVSS puanları, exploit kullanılabilirliği).  
- **Output / Çıktı:**  
  **English:** Create a markdown file (`research_notes.md`) with sections: **Vulnerability Tools**, **Techniques**. Compile data into a JSON file (`research_data.json`) with keys: `tools`, `techniques`.  
  **Turkish:** Bir markdown dosyası (`research_notes.md`) oluşturun: **Güvenlik Açığı Araçları**, **Teknikler**. Verileri bir JSON dosyasına (`research_data.json`) derleyin: `tools`, `techniques`.  

---

##### **2. Understand / Anlama**
**English:** Study the resources to understand how vulnerability scanning works. Focus on:  
- **Vulnerability Identification**: How tools detect weaknesses (e.g., outdated software).  
- **Severity Rating**: Understanding CVSS scores and their implications.  
- **False Positives**: Why scans may misidentify issues.  
- **Ethical Use**: Legal and responsible scanning practices.  
**Turkish:** Kaynakları inceleyerek güvenlik açığı taramasının nasıl çalıştığını anlayın. Şunlara odaklanın:  
- **Güvenlik Açığı Tespiti**: Araçların zayıflıkları nasıl bulduğu (ör. güncel olmayan yazılımlar).  
- **Ciddiyet Derecesi**: CVSS puanlarını ve etkilerini anlama.  
- **Yanlış Pozitifler**: Taramanın neden sorunları yanlış tespit edebileceği.  
- **Etik Kullanım**: Yasal ve sorumlu tarama uygulamaları.  
- **Reflection / Yansıma:**  
  **English:** Reflect on why vulnerability scanning is essential for securing Linux servers and preventing exploitation.  
  **Turkish:** Güvenlik açığı taramasının Linux sunucularını güvence altına alma ve sömürülmeyi önleme açısından neden önemli olduğunu düşünün.  
- **Output / Çıktı:**  
  **English:** Write a 200-250 word summary in `research_notes.md` under "Understanding Vulnerability Scanning / Güvenlik Açığı Taramasını Anlama," explaining methods and their cybersecurity importance.  
  **Turkish:** `research_notes.md` dosyasına "Güvenlik Açığı Taramasını Anlama" başlığı altında 200-250 kelimelik bir özet yazın; yöntemleri ve siber güvenlikteki önemini açıklayın.  

---

##### **3. Plan / Planlama**
**English:** Outline the script’s structure, including:  
- Functions: `scan_vulnerabilities`, `parse_results`, `prioritize_vulns`.  
- Inputs: Target IP or hostname.  
- Outputs: List of vulnerabilities with severity scores.  
- Error Scenarios: Tool failures, network issues.  
**Turkish:** Betiğin yapısını planlayın:  
- Fonksiyonlar: `scan_vulnerabilities`, `parse_results`, `prioritize_vulns`.  
- Girdiler: Hedef IP veya ana makine adı.  
- Çıktılar: Ciddiyet puanlarıyla güvenlik açıkları listesi.  
- Hata Senaryoları: Araç arızaları, ağ sorunları.  
- **Output / Çıktı:**  
  **English:** Add a "Design Plan / Tasarım Planı" section to `research_notes.md` with a function list, their purposes, and pseudocode (e.g., "Scan target → Parse vulnerabilities → Rank by severity").  
  **Turkish:** `research_notes.md` dosyasına "Tasarım Planı" bölümü ekleyin; fonksiyon listesi, amaçları ve sahte kod (ör. "Hedefi tara → Güvenlik açıklarını ayrıştır → Ciddiyete göre sırala") ile.  

---

##### **4. Implement / Uygulama**
**English:** Create `vulnerability_scanner.py` in the `modules` directory.  
**Turkish:** `modules` dizininde `vulnerability_scanner.py` dosyasını oluşturun.  

**Step-by-Step Implementation / Adım Adım Uygulama:**  
- **Step 1: Scan Vulnerabilities Function / Adım 1: Güvenlik Açıklarını Tarama Fonksiyonu**  
  **English:** Write `scan_vulnerabilities(target)` to perform an Nmap vuln scan.  
  **Turkish:** Nmap vuln taraması yapmak için `scan_vulnerabilities(target)` fonksiyonunu yazın.  
  ```python  
  import nmap  

  def scan_vulnerabilities(target):  
      nm = nmap.PortScanner()  
      nm.scan(target, arguments="-sV --script vuln,vulners")  
      return nm  
  ```  

- **Step 2: Parse Results Function / Adım 2: Sonuçları Ayrıştırma Fonksiyonu**  
  **English:** Write `parse_results(nm, target)` to extract vulnerability data.  
  **Turkish:** Güvenlik açığı verilerini çıkarmak için `parse_results(nm, target)` fonksiyonunu yazın.  
  ```python  
  def parse_results(nm, target):  
      vulns = []  
      if target in nm.all_hosts():  
          for port in nm[target].all_tcp():  
              if "script" in nm[target]["tcp"][port]:  
                  script_output = nm[target]["tcp"][port]["script"]  
                  vulns.append({"port": port, "details": script_output})  
      return vulns  
  ```  

- **Step 3: Prioritize Vulnerabilities Function / Adım 3: Güvenlik Açıklarını Önceliklendirme Fonksiyonu**  
  **English:** Write `prioritize_vulns(vulns)` to rank vulnerabilities by severity.  
  **Turkish:** Güvenlik açıklarını ciddiyete göre sıralamak için `prioritize_vulns(vulns)` fonksiyonunu yazın.  
  ```python  
  def prioritize_vulns(vulns):  
      for vuln in vulns:  
          details = vuln["details"]  
          severity = "Low"  
          if "CVSS" in str(details):  
              severity = "High" if "High" in str(details) else "Medium"  
          vuln["severity"] = severity  
      return sorted(vulns, key=lambda x: x["severity"], reverse=True)  
  ```  

- **Step 4: Error Handling / Adım 4: Hata İşleme**  
  **English:** Add try-except to `scan_vulnerabilities` for error management.  
  **Turkish:** Hata yönetimi için `scan_vulnerabilities` fonksiyonuna try-except ekleyin.  
  ```python  
  def scan_vulnerabilities(target):  
      try:  
          nm = nmap.PortScanner()  
          nm.scan(target, arguments="-sV --script vuln,vulners")  
          return nm  
      except nmap.PortScannerError as e:  
          raise Exception(f"Scan error: {str(e)}")  
  ```  

- **Step 5: Reporting Function / Adım 5: Raporlama Fonksiyonu**  
  **English:** Write `report_vulns(target, vulns)` for result logging.  
  **Turkish:** Sonuç kaydı için `report_vulns(target, vulns)` fonksiyonunu yazın.  
  ```python  
  import time  

  def report_vulns(target, vulns):  
      timestamp = time.strftime("%Y-%m-%d %H:%M:%S")  
      report = f"### Vulnerability Scan Result / Güvenlik Açığı Tarama Sonucu\n- **Time / Zaman:** {timestamp}\n- **Target / Hedef:** {target}\n"  
      for vuln in vulns:  
          report += f"- **Port / Port:** {vuln['port']} | **Severity / Ciddiyet:** {vuln['severity']} | **Details / Detaylar:** {vuln['details']}\n"  
      return report  
  ```  

- **Step 6: Main Function / Adım 6: Ana Fonksiyon**  
  **English:** Write `main(target)` to tie all steps together.  
  **Turkish:** Tüm adımları birleştirmek için `main(target)` fonksiyonunu yazın.  
  ```python  
  def main(target):  
      nm = scan_vulnerabilities(target)  
      vulns = parse_results(nm, target)  
      prioritized_vulns = prioritize_vulns(vulns)  
      return report_vulns(target, prioritized_vulns)  
  ```  

---

##### **5. Test / Test Etme**
**English:** Test the script with:  
- **Vulnerable Server**: A Linux server with known vulnerabilities (e.g., test environment).  
- **Secure Server**: A patched Linux server.  
- **Edge Cases**: Invalid IP, no open ports.  
**Turkish:** Betiği şu şekilde test edin:  
- **Güvenlik Açığı Olan Sunucu**: Bilinen güvenlik açıkları olan bir Linux sunucusu (ör. test ortamı).  
- **Güvenli Sunucu**: Yamalı bir Linux sunucusu.  
- **Kenar Durumlar**: Geçersiz IP, açık port yok.  
- **Output / Çıktı:**  
  **English:** Document in `test_results.md`: **Input** (target), **Expected Result**, **Actual Result**, **Observations**.  
  **Turkish:** `test_results.md` dosyasına kaydedin: **Giriş** (hedef), **Beklenen Sonuç**, **Gerçek Sonuç**, **Gözlemler**.  

---

##### **6. Confirm / Doğrulama**
**English:** Verify vulnerabilities manually using another tool (e.g., OpenVAS, manual CVE lookup).  
**Turkish:** Güvenlik açıklarını başka bir araçla manuel olarak doğrulayın (ör. OpenVAS, manuel CVE sorgulama).  
- **Output / Çıktı:**  
  **English:** Add a "Confirmation / Doğrulama" section to `test_results.md` with cross-check results and accuracy notes.  
  **Turkish:** `test_results.md` dosyasına "Doğrulama" bölümü ekleyin; çapraz kontrol sonuçları ve doğruluk notlarıyla.  

---

##### **7. Contribute / Katkı Sağlama**
**English:** Submit to `https://github.com/QLineTech/Q-Pentest`:  
- Fork the repo, create a branch (`feature/vulnerability-scanner`), commit `vulnerability_scanner.py`, `research_notes.md`, `test_results.md`, `research_data.json`, and submit a pull request with a detailed description.  
**Turkish:** `https://github.com/QLineTech/Q-Pentest` adresine gönderin:  
- Depoyu çatallayın, bir dal oluşturun (`feature/vulnerability-scanner`), `vulnerability_scanner.py`, `research_notes.md`, `test_results.md`, `research_data.json` dosyalarını taahhüt edin ve detaylı bir açıklama ile pull request gönderin.  

---

#### Roadmap / Yol Haritası
**English:**  
- **Phase 1: Preparation / Hazırlık**: Research tools and techniques, document findings.  
- **Phase 2: Learning and Planning / Öğrenme ve Planlama**: Study resources, summarize insights, plan the script.  
- **Phase 3: Implementation / Uygulama**: Build functions for scanning, parsing, and prioritizing vulnerabilities.  
- **Phase 4: Testing and Validation / Test ve Doğrulama**: Test the script, confirm results with other tools.  
- **Phase 5: Contribution / Katkı**: Submit work to GitHub.  
**Turkish:**  
- **Aşama 1: Hazırlık**: Araçları ve teknikleri araştırın, bulguları belgeleyin.  
- **Aşama 2: Öğrenme ve Planlama**: Kaynakları inceleyin, içgörüleri özetleyin, betiği planlayın.  
- **Aşama 3: Uygulama**: Tarama, ayrıştırma ve güvenlik açıklarını önceliklendirme fonksiyonlarını oluşturun.  
- **Aşama 4: Test ve Doğrulama**: Betiği test edin, sonuçları diğer araçlarla doğrulayın.  
- **Aşama 5: Katkı**: Çalışmayı GitHub’a gönderin.  

---

#### Small Implementation Steps / Küçük Uygulama Adımları
**English:**  
- **Scanning**: Use Nmap with vuln scripts to scan the target.  
- **Parsing**: Extract vulnerability data from Nmap results.  
- **Prioritizing**: Rank vulnerabilities by severity.  
- **Error Handling**: Manage scan errors and invalid inputs.  
- **Reporting**: Format vulnerability results in markdown.  
- **Main**: Integrate functions to process and report vulnerabilities.  
**Turkish:**  
- **Tarama**: Hedefi taramak için Nmap ve vuln betiklerini kullanın.  
- **Ayrıştırma**: Nmap sonuçlarından güvenlik açığı verilerini çıkarın.  
- **Önceliklendirme**: Güvenlik açıklarını ciddiyete göre sıralayın.  
- **Hata İşleme**: Tarama hatalarını ve geçersiz girdileri yönetin.  
- **Raporlama**: Güvenlik açığı sonuçlarını markdown formatında düzenleyin.  
- **Ana**: Güvenlik açıklarını işlemek ve raporlamak için fonksiyonları entegre edin.  
