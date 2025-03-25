### Task: Windows Server Detection / Windows Server Tespiti
**Assigned Role / Atanan Rol:** Sage / Bilge  
**Module File / Modül Dosyası:** `modules/win_server_detection.py`

#### Expanded Instruction Set for Amateur Cybersecurity Students / Amatör Siber Güvenlik Öğrencileri İçin Genişletilmiş Talimat Seti

##### **1. Research / Araştırma**
**English:** Your task is to collect resources and techniques for detecting Windows servers using tools like Nmap and others.  
**Turkish:** Göreviniz, Nmap ve diğer araçları kullanarak Windows sunucularını tespit etmek için kaynaklar ve teknikler toplamaktır.  
- **Action / Eylem:**  
  **English:** Search for resources on detecting Windows servers. Examples include:  
  - Nmap scripts (e.g., `smb-os-discovery.nse`).  
  - Other tools (e.g., Nessus, OpenVAS).  
  - Documentation and tutorials (e.g., Nmap Network Scanning book, online forums).  
  **Turkish:** Windows sunucularını tespit etmek için kaynaklar bulun. Örnekler:  
  - Nmap betikleri (ör. `smb-os-discovery.nse`).  
  - Diğer araçlar (ör. Nessus, OpenVAS).  
  - Dokümantasyon ve öğreticiler (ör. Nmap Network Scanning kitabı, çevrimiçi forumlar).  
- **Documentation / Dokümantasyon:** For each resource, note:  
  **English:**  
  - **Name and Type**: (e.g., "Nmap - Tool").  
  - **Access Method**: (e.g., "Install via apt," "Download from website").  
  - **Coverage**: (e.g., "Detects OS via SMB, RDP").  
  - **Usage Instructions**: (e.g., "Run `nmap -sV --script smb-os-discovery`").  
  **Turkish:**  
  - **İsim ve Tür**: (ör. "Nmap - Araç").  
  - **Erişim Yöntemi**: (ör. "Apt ile kurulum," "Web sitesinden indirme").  
  - **Kapsam**: (ör. "SMB, RDP ile işletim sistemini tespit eder").  
  - **Kullanım Talimatları**: (ör. "`nmap -sV --script smb-os-discovery` komutunu çalıştırın").  
- **Additional Scope / Ek Kapsam:**  
  **English:** Explore techniques to enhance detection accuracy (e.g., combining tools, analyzing service banners).  
  **Turkish:** Tespit doğruluğunu artırmak için teknikler araştırın (ör. araçları birleştirme, hizmet banner’larını analiz etme).  
- **Output / Çıktı:**  
  **English:** Create a markdown file (`research_notes.md`) with sections: **Detection Tools**, **Techniques**. Compile data into a JSON file (`research_data.json`) with keys: `tools`, `techniques`.  
  **Turkish:** Bir markdown dosyası (`research_notes.md`) oluşturun: **Tespit Araçları**, **Teknikler**. Verileri bir JSON dosyasına (`research_data.json`) derleyin: `tools`, `techniques`.  

---

##### **2. Understand / Anlama**
**English:** Study the resources to grasp how Windows server detection works. Focus on:  
- **OS Fingerprinting**: How tools identify the OS from network responses.  
- **Service Detection**: Identifying Windows-specific services (e.g., SMB, RDP).  
- **Accuracy Factors**: Reasons for detection inaccuracies (e.g., firewalls).  
- **Legal Considerations**: Ethical use of scanning tools.  
**Turkish:** Kaynakları inceleyerek Windows sunucu tespitinin nasıl çalıştığını anlayın. Şunlara odaklanın:  
- **İşletim Sistemi Parmak İzi**: Araçların ağ yanıtlarından işletim sistemini nasıl belirlediği.  
- **Hizmet Tespiti**: Windows’a özgü hizmetleri tanıma (ör. SMB, RDP).  
- **Doğruluk Faktörleri**: Tespitin neden yanlış olabileceği (ör. güvenlik duvarları).  
- **Yasal Hususlar**: Tarama araçlarının etik kullanımı.  
- **Reflection / Yansıma:**  
  **English:** Reflect on why accurate OS detection matters for vulnerability assessment and network auditing.  
  **Turkish:** Doğru işletim sistemi tespitinin güvenlik açığı değerlendirmesi ve ağ denetimi için neden önemli olduğunu düşünün.  
- **Output / Çıktı:**  
  **English:** Write a 200-250 word summary in `research_notes.md` under "Understanding OS Detection / İşletim Sistemi Tespitini Anlama," detailing detection methods and their cybersecurity role.  
  **Turkish:** `research_notes.md` dosyasına "İşletim Sistemi Tespitini Anlama" başlığı altında 200-250 kelimelik bir özet yazın; tespit yöntemleri ve siber güvenlikteki rollerini detaylandırın.  

---

##### **3. Plan / Planlama**
**English:** Outline the script’s structure, including:  
- Functions: `scan_target`, `analyze_results`, `determine_os`.  
- Inputs: Target IP or range.  
- Outputs: OS detection results, confidence level.  
- Error Scenarios: Unreachable targets, insufficient permissions.  
**Turkish:** Betiğin yapısını planlayın:  
- Fonksiyonlar: `scan_target`, `analyze_results`, `determine_os`.  
- Girdiler: Hedef IP veya aralık.  
- Çıktılar: İşletim sistemi tespit sonuçları, güven seviyesi.  
- Hata Senaryoları: Erişilemeyen hedefler, yetersiz izinler.  
- **Output / Çıktı:**  
  **English:** Add a "Design Plan / Tasarım Planı" section to `research_notes.md` with a function list, their purposes, and pseudocode (e.g., "Scan target → Analyze output → Check for Windows server").  
  **Turkish:** `research_notes.md` dosyasına "Tasarım Planı" bölümü ekleyin; fonksiyon listesi, amaçları ve sahte kod ile (ör. "Hedefi tara → Çıktıyı analiz et → Windows sunucusu mu kontrol et").  

---

##### **4. Implement / Uygulama**
**English:** Create `win_server_detection.py` in the `modules` directory.  
**Turkish:** `modules` dizininde `win_server_detection.py` dosyasını oluşturun.  

**Step-by-Step Implementation / Adım Adım Uygulama:**  
- **Step 1: Scan Target Function / Adım 1: Hedefi Tarama Fonksiyonu**  
  **English:** Write `scan_target(target)` to perform an Nmap scan.  
  **Turkish:** Nmap taraması yapmak için `scan_target(target)` fonksiyonunu yazın.  
  ```python  
  import nmap  

  def scan_target(target):  
      nm = nmap.PortScanner()  
      nm.scan(target, arguments="-sV --script smb-os-discovery")  
      return nm  
  ```  

- **Step 2: Analyze Results Function / Adım 2: Sonuçları Analiz Etme Fonksiyonu**  
  **English:** Write `analyze_results(nm, target)` to extract OS data.  
  **Turkish:** İşletim sistemi verilerini çıkarmak için `analyze_results(nm, target)` fonksiyonunu yazın.  
  ```python  
  def analyze_results(nm, target):  
      if target in nm.all_hosts():  
          if "osmatch" in nm[target]:  
              return nm[target]["osmatch"]  
          if "smb-os-discovery" in nm[target]["hostscript"]:  
              return nm[target]["hostscript"]["smb-os-discovery"]  
      return None  
  ```  

- **Step 3: Determine OS Function / Adım 3: İşletim Sistemini Belirleme Fonksiyonu**  
  **English:** Write `determine_os(os_data)` to identify Windows servers.  
  **Turkish:** Windows sunucularını tespit etmek için `determine_os(os_data)` fonksiyonunu yazın.  
  ```python  
  def determine_os(os_data):  
      if os_data and "Windows Server" in str(os_data):  
          return {"is_windows_server": True, "details": os_data}  
      return {"is_windows_server": False, "details": os_data}  
  ```  

- **Step 4: Error Handling / Adım 4: Hata İşleme**  
  **English:** Add try-except to `scan_target` for error management.  
  **Turkish:** Hata yönetimi için `scan_target` fonksiyonuna try-except ekleyin.  
  ```python  
  def scan_target(target):  
      try:  
          nm = nmap.PortScanner()  
          nm.scan(target, arguments="-sV --script smb-os-discovery")  
          return nm  
      except nmap.PortScannerError as e:  
          raise Exception(f"Scan error: {str(e)}")  
  ```  

- **Step 5: Reporting Function / Adım 5: Raporlama Fonksiyonu**  
  **English:** Write `report_detection(target, result)` for result logging.  
  **Turkish:** Sonuç kaydı için `report_detection(target, result)` fonksiyonunu yazın.  
  ```python  
  import time  

  def report_detection(target, result):  
      timestamp = time.strftime("%Y-%m-%d %H:%M:%S")  
      return f"### Detection Result / Tespit Sonucu\n- **Time / Zaman:** {timestamp}\n- **Target / Hedef:** {target}\n- **Result / Sonuç:** {result}\n"  
  ```  

- **Step 6: Main Function / Adım 6: Ana Fonksiyon**  
  **English:** Write `main(target)` to tie all steps together.  
  **Turkish:** Tüm adımları birleştirmek için `main(target)` fonksiyonunu yazın.  
  ```python  
  def main(target):  
      nm = scan_target(target)  
      os_data = analyze_results(nm, target)  
      result = determine_os(os_data)  
      return report_detection(target, result)  
  ```  

---

##### **5. Test / Test Etme**
**English:** Test the script with:  
- **Windows Server**: A known Windows server IP.  
- **Non-Windows Server**: A Linux or other OS IP.  
- **Edge Cases**: Invalid IP, unreachable target.  
**Turkish:** Betiği şu şekilde test edin:  
- **Windows Sunucusu**: Bilinen bir Windows sunucusu IP’si.  
- **Windows Olmayan Sunucu**: Linux veya başka bir işletim sistemi IP’si.  
- **Kenar Durumlar**: Geçersiz IP, erişilemeyen hedef.  
- **Output / Çıktı:**  
  **English:** Document in `test_results.md`: **Input** (target), **Expected Result**, **Actual Result**, **Observations**.  
  **Turkish:** `test_results.md` dosyasına kaydedin: **Giriş** (hedef), **Beklenen Sonuç**, **Gerçek Sonuç**, **Gözlemler**.  

---

##### **6. Confirm / Doğrulama**
**English:** Verify the OS manually using another tool (e.g., `netcat`, `telnet`).  
**Turkish:** İşletim sistemini başka bir araçla manuel olarak doğrulayın (ör. `netcat`, `telnet`).  
- **Output / Çıktı:**  
  **English:** Add a "Confirmation / Doğrulama" section to `test_results.md` with cross-check results and accuracy notes.  
  **Turkish:** `test_results.md` dosyasına "Doğrulama" bölümü ekleyin; çapraz kontrol sonuçları ve doğruluk notlarıyla.  

---

##### **7. Contribute / Katkı Sağlama**
**English:** Submit to `https://github.com/QLineTech/Q-Pentest`:  
- Fork the repo, create a branch (`feature/win-server-detection`), commit `win_server_detection.py`, `research_notes.md`, `test_results.md`, `research_data.json`, and submit a pull request with a detailed description.  
**Turkish:** `https://github.com/QLineTech/Q-Pentest` adresine gönderin:  
- Depoyu çatallayın, bir dal oluşturun (`feature/win-server-detection`), `win_server_detection.py`, `research_notes.md`, `test_results.md`, `research_data.json` dosyalarını taahhüt edin ve detaylı bir açıklama ile pull request gönderin.  

---

#### Roadmap / Yol Haritası
**English:**  
- **Phase 1: Preparation / Hazırlık**: Research tools and techniques, document findings.  
- **Phase 2: Learning and Planning / Öğrenme ve Planlama**: Study resources, summarize insights, plan the script.  
- **Phase 3: Implementation / Uygulama**: Build functions for scanning, analyzing, and OS determination.  
- **Phase 4: Testing and Validation / Test ve Doğrulama**: Test the script, confirm results with other tools.  
- **Phase 5: Contribution / Katkı**: Submit work to GitHub.  
**Turkish:**  
- **Aşama 1: Hazırlık**: Araçları ve teknikleri araştırın, bulguları belgeleyin.  
- **Aşama 2: Öğrenme ve Planlama**: Kaynakları inceleyin, içgörüleri özetleyin, betiği planlayın.  
- **Aşama 3: Uygulama**: Tarama, analiz ve işletim sistemi belirleme fonksiyonlarını oluşturun.  
- **Aşama 4: Test ve Doğrulama**: Betiği test edin, sonuçları diğer araçlarla doğrulayın.  
- **Aşama 5: Katkı**: Çalışmayı GitHub’a gönderin.  

---

#### Small Implementation Steps / Küçük Uygulama Adımları
**English:**  
- **Scanning**: Use Nmap with scripts to scan the target.  
- **Analyzing**: Extract OS data from Nmap results.  
- **Determining OS**: Check if the OS is a Windows server.  
- **Error Handling**: Manage scan errors and invalid inputs.  
- **Reporting**: Format detection results in markdown.  
- **Main**: Integrate functions to process and report detection.  
**Turkish:**  
- **Tarama**: Hedefi taramak için Nmap ve betikleri kullanın.  
- **Analiz**: Nmap sonuçlarından işletim sistemi verilerini çıkarın.  
- **İşletim Sistemini Belirleme**: İşletim sisteminin Windows sunucusu olup olmadığını kontrol edin.  
- **Hata İşleme**: Tarama hatalarını ve geçersiz girdileri yönetin.  
- **Raporlama**: Tespit sonuçlarını markdown formatında düzenleyin.  
- **Ana**: Tespiti işlemek ve raporlamak için fonksiyonları entegre edin.  

