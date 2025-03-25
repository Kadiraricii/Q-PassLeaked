** iPhone Network Device Detection**

- **Objective:** Use Grok3 DeepSearch to find techniques for detecting iPhone devices using Nmap and other tools. Then, create a script that takes target information as input, applies these techniques to determine if the target is an iPhone device, assesses the accuracy of the prediction, attempts to find the version if possible, handles multiple targets, and generates a detailed markdown report.
- **Module File:** `modules/iphone_network_device_detection.py`

Below is a comprehensive instruction set tailored for an amateur cybersecurity student, ensuring the task takes at least 40 minutes to complete while maintaining educational value and detailed guidance.

---

### Task 6: iPhone Network Device Detection / iPhone Ağ Cihazı Tespiti
**Assigned Role / Atanan Rol:** Sage / Bilge  
**Module File / Modül Dosyası:** `modules/iphone_network_device_detection.py`

#### Expanded Instruction Set for Amateur Cybersecurity Students / Amatör Siber Güvenlik Öğrencileri İçin Genişletilmiş Talimat Seti

##### **1. Research / Araştırma**
**English:** Your task is to use Grok3 DeepSearch to find all available techniques on the internet for detecting iPhone devices using Nmap and other tools. This includes identifying specific Nmap scripts, commands, or other network scanning tools that can help determine if a device is an iPhone running iOS.  
**Turkish:** Göreviniz, Grok3 DeepSearch'ü kullanarak internette Nmap ve diğer araçlarla iPhone cihazlarını tespit etmek için mevcut tüm teknikleri bulmaktır. Bu, bir cihazın iOS çalıştıran bir iPhone olup olmadığını belirlemeye yardımcı olabilecek belirli Nmap betikleri, komutları veya diğer ağ tarama araçlarını tanımlamayı içerir.

- **Action / Eylem:**  
  **English:** Use Grok3 DeepSearch with the following comprehensive prompt to ensure maximum results:  
  ```
  collect all collected info without missing any info in a json file.

  double check to not skip any item.

  even if no default pass or ... generate a list of devices used in a list devices_with_unkown_password

  generate isp lists
  devices lists
  all default user pass list
  a device_mapped_list (device + user pass)
  a isp_mapped_list (isp + user pass)
  a isp_device_mapped_list (isp , device + user pass(es))

  double check to not skip any found item and generate final json no matter how big file is.
  ```
  Focus on finding techniques that involve:  
  - Nmap scripts (e.g., `http-title`, `http-useragent`, `banner`, etc.).  
  - Other tools like Wireshark, tcpdump, or custom scripts.  
  - Fingerprinting methods specific to iPhone/iOS devices (e.g., TCP/IP stack behavior).  
  - Service banners or responses that indicate an iPhone device (e.g., Apple-specific services).  
  - Known ports or services commonly open on iPhone devices (e.g., AirDrop, Bonjour).  

  **Turkish:** Aşağıdaki kapsamlı komutu kullanarak Grok3 DeepSearch'ü kullanın ve maksimum sonuç sağlamak için:  
  ```
  collect all collected info without missing any info in a json file.

  double check to not skip any item.

  even if no default pass or ... generate a list of devices used in a list devices_with_unkown_password

  generate isp lists
  devices lists
  all default user pass list
  a device_mapped_list (device + user pass)
  a isp_mapped_list (isp + user pass)
  a isp_device_mapped_list (isp , device + user pass(es))

  double check to not skip any found item and generate final json no matter how big file is.
  ```
  Şunlara odaklanın:  
  - Nmap betikleri (ör. `http-title`, `http-useragent`, `banner`, vb.).  
  - Wireshark, tcpdump veya özel betikler gibi diğer araçlar.  
  - iPhone/iOS cihazlarına özgü parmak izi yöntemleri (ör. TCP/IP yığın davranışı).  
  - Bir iPhone cihazını gösteren hizmet banner’ları veya yanıtları (ör. Apple’a özgü hizmetler).  
  - iPhone cihazlarında yaygın olarak açık olan bilinen portlar veya hizmetler (ör. AirDrop, Bonjour).  

- **Documentation / Dokümantasyon:** For each technique or tool found, record:  
  **English:**  
  - **Technique/Tool Name**: (e.g., "Nmap http-useragent script").  
  - **Description**: How it works to detect iPhone devices.  
  - **Usage Instructions**: Commands or steps to use the technique.  
  - **Accuracy**: Any known accuracy rates or limitations.  
  - **Version Detection**: If the technique can detect the iOS version.  
  **Turkish:**  
  - **Teknik/Araç Adı**: (ör. "Nmap http-useragent betiği").  
  - **Açıklama**: iPhone cihazlarını nasıl tespit ettiği.  
  - **Kullanım Talimatları**: Tekniği kullanmak için komutlar veya adımlar.  
  - **Doğruluk**: Bilinen doğruluk oranları veya sınırlamalar.  
  - **Sürüm Tespiti**: Tekniğin iOS sürümünü tespit edip edemediği.  

- **Additional Scope / Ek Kapsam:**  
  **English:** Look for techniques that can differentiate between iOS versions or specific iPhone models. Also, consider methods that analyze network behavior or traffic patterns unique to iPhone devices (e.g., mDNS responses).  
  **Turkish:** iOS sürümleri veya belirli iPhone modelleri arasında ayrım yapabilen teknikleri arayın. Ayrıca, iPhone cihazlarına özgü ağ davranışlarını veya trafik desenlerini analiz eden yöntemleri de göz önünde bulundurun (ör. mDNS yanıtları).  

- **Output / Çıktı:**  
  **English:** Create a markdown file (`research_notes.md`) with sections: **Detection Techniques**, **Tools**, and **Version Detection Methods**. Compile all data into a JSON file (`research_data.json`) with keys: `techniques`, `tools`, `version_detection`.  
  **Turkish:** Bir markdown dosyası (`research_notes.md`) oluşturun: **Tespit Teknikleri**, **Araçlar** ve **Sürüm Tespit Yöntemleri**. Verileri bir JSON dosyasına (`research_data.json`) derleyin: `techniques`, `tools`, `version_detection`.  

---

##### **2. Understand / Anlama**
**English:** Study the techniques and tools you’ve gathered to understand how they detect iPhone devices. Focus on:  
- **Fingerprinting**: How network responses or service banners reveal iOS.  
- **Service Analysis**: Which services are typically running on iPhone devices (e.g., Bonjour, AirPlay).  
- **Accuracy Factors**: Why some techniques may be more reliable than others.  
- **Limitations**: Scenarios where detection might fail (e.g., jailbroken devices, disabled services).  
**Turkish:** Topladığınız teknikleri ve araçları inceleyerek iPhone cihazlarını nasıl tespit ettiklerini anlayın. Şunlara odaklanın:  
- **Parmak İzi**: Ağ yanıtları veya hizmet banner’larının iOS’u nasıl ortaya çıkardığı.  
- **Hizmet Analizi**: iPhone cihazlarında tipik olarak hangi hizmetlerin çalıştığı (ör. Bonjour, AirPlay).  
- **Doğruluk Faktörleri**: Bazı tekniklerin neden diğerlerinden daha güvenilir olabileceği.  
- **Sınırlamalar**: Tespitin başarısız olabileceği senaryolar (ör. jailbreak yapılmış cihazlar, devre dışı bırakılmış hizmetler).  

- **Reflection / Yansıma:**  
  **English:** Consider the importance of accurate device detection in network security, such as identifying potential vulnerabilities or unauthorized devices on a network.  
  **Turkish:** Ağ güvenliğinde doğru cihaz tespitinin önemini düşünün, örneğin potansiyel güvenlik açıklarını veya ağdaki yetkisiz cihazları tanımlama.  

- **Output / Çıktı:**  
  **English:** Write a 200-250 word summary in `research_notes.md` under "Understanding iPhone Detection / iPhone Tespitini Anlama," explaining the key methods and their significance in cybersecurity.  
  **Turkish:** `research_notes.md` dosyasına "iPhone Tespitini Anlama" başlığı altında 200-250 kelimelik bir özet yazın; temel yöntemleri ve siber güvenlikteki önemini açıklayın.  

---

##### **3. Plan / Planlama**
**English:** Outline the script’s structure, including:  
- Functions: `scan_target`, `analyze_results`, `determine_device`.  
- Inputs: Target IP or list of IPs.  
- Outputs: Detection results, accuracy assessment, version (if detected).  
- Error Scenarios: Unreachable targets, insufficient data for detection.  
**Turkish:** Betiğin yapısını planlayın:  
- Fonksiyonlar: `scan_target`, `analyze_results`, `determine_device`.  
- Girdiler: Hedef IP veya IP listesi.  
- Çıktılar: Tespit sonuçları, doğruluk değerlendirmesi, sürüm (tespit edildiyse).  
- Hata Senaryoları: Erişilemeyen hedefler, tespit için yetersiz veri.  

- **Output / Çıktı:**  
  **English:** Add a "Design Plan / Tasarım Planı" section to `research_notes.md` with a function list, their purposes, and pseudocode (e.g., "Scan target → Analyze responses → Check for iPhone signatures").  
  **Turkish:** `research_notes.md` dosyasına "Tasarım Planı" bölümü ekleyin; fonksiyon listesi, amaçları ve sahte kod (ör. "Hedefi tara → Yanıtları analiz et → iPhone imzalarını kontrol et") ile.  

---

##### **4. Implement / Uygulama**
**English:** Create `iphone_network_device_detection.py` in the `modules` directory.  
**Turkish:** `modules` dizininde `iphone_network_device_detection.py` dosyasını oluşturun.  

**Step-by-Step Implementation / Adım Adım Uygulama:**  

- **Step 1: Scan Target Function / Adım 1: Hedefi Tarama Fonksiyonu**  
  **English:** Write `scan_target(target)` to perform Nmap scans using the techniques found in research.  
  **Turkish:** Araştırmada bulunan teknikleri kullanarak Nmap taramaları yapmak için `scan_target(target)` fonksiyonunu yazın.  
  ```python  
  import nmap  

  def scan_target(target):  
      nm = nmap.PortScanner()  
      # Example: Use scripts like http-useragent and banner  
      nm.scan(target, arguments="-sV --script http-useragent,banner")  
      return nm  
  ```  

- **Step 2: Analyze Results Function / Adım 2: Sonuçları Analiz Etme Fonksiyonu**  
  **English:** Write `analyze_results(nm, target)` to extract relevant data for iPhone detection.  
  **Turkish:** iPhone tespiti için ilgili verileri çıkarmak için `analyze_results(nm, target)` fonksiyonunu yazın.  
  ```python  
  def analyze_results(nm, target):  
      if target in nm.all_hosts():  
          # Example: Check for iPhone/iOS in user-agent or banner  
          if "http-useragent" in nm[target]["tcp"].get(80, {}).get("script", {}):  
              user_agent = nm[target]["tcp"][80]["script"]["http-useragent"]  
              if "iPhone" in user_agent or "iOS" in user_agent:  
                  return {"is_iphone": True, "details": user_agent}  
          elif "banner" in nm[target]["tcp"].get(5353, {}).get("script", {}):  
              banner = nm[target]["tcp"][5353]["script"]["banner"]  
              if "Apple" in banner:  
                  return {"is_iphone": True, "details": banner}  
      return {"is_iphone": False, "details": "No iPhone signature found"}  
  ```  

- **Step 3: Determine Device Function / Adım 3: Cihazı Belirleme Fonksiyonu**  
  **English:** Write `determine_device(results)` to assess if the device is an iPhone and estimate accuracy.  
  **Turkish:** Cihazın iPhone olup olmadığını değerlendirmek ve doğruluğu tahmin etmek için `determine_device(results)` fonksiyonunu yazın.  
  ```python  
  def determine_device(results):  
      if results["is_iphone"]:  
          accuracy = 85  # Example accuracy percentage  
          version = "Unknown"  # Placeholder for version detection  
          if "OS" in results["details"]:  
              version = results["details"].split("OS")[1].split()[0]  # Attempt to extract version  
          return {"is_iphone": True, "accuracy": accuracy, "version": version}  
      return {"is_iphone": False, "accuracy": 100}  
  ```  

- **Step 4: Error Handling / Adım 4: Hata İşleme**  
  **English:** Add try-except to `scan_target` for managing scan errors.  
  **Turkish:** Tarama hatalarını yönetmek için `scan_target` fonksiyonuna try-except ekleyin.  
  ```python  
  def scan_target(target):  
      try:  
          nm = nmap.PortScanner()  
          nm.scan(target, arguments="-sV --script http-useragent,banner")  
          return nm  
      except nmap.PortScannerError as e:  
          raise Exception(f"Scan error: {str(e)}")  
  ```  

- **Step 5: Reporting Function / Adım 5: Raporlama Fonksiyonu**  
  **English:** Write `report_detection(target, result)` for markdown logging.  
  **Turkish:** Markdown kaydı için `report_detection(target, result)` fonksiyonunu yazın.  
  ```python  
  import time  

  def report_detection(target, result):  
      timestamp = time.strftime("%Y-%m-%d %H:%M:%S")  
      return f"### Detection Result / Tespit Sonucu\n- **Time / Zaman:** {timestamp}\n- **Target / Hedef:** {target}\n- **Is iPhone / iPhone mu:** {result['is_iphone']}\n- **Accuracy / Doğruluk:** {result['accuracy']}%\n- **Version / Sürüm:** {result.get('version', 'N/A')}\n"  
  ```  

- **Step 6: Main Function / Adım 6: Ana Fonksiyon**  
  **English:** Write `main(targets)` to process multiple targets and generate reports.  
  **Turkish:** Birden fazla hedefi işlemek ve raporlar oluşturmak için `main(targets)` fonksiyonunu yazın.  
  ```python  
  def main(targets):  
      reports = []  
      for target in targets:  
          nm = scan_target(target)  
          results = analyze_results(nm, target)  
          detection = determine_device(results)  
          report = report_detection(target, detection)  
          reports.append(report)  
      return "\n".join(reports)  
  ```  

---

##### **5. Test / Test Etme**
**English:** Test the script with:  
- **Known iPhone Device**: An IP known to be an iPhone.  
- **Non-iPhone Device**: An Android or Windows device.  
- **Edge Cases**: Invalid IP, unreachable target.  
**Turkish:** Betiği şu şekilde test edin:  
- **Bilinen iPhone Cihazı**: iPhone olduğu bilinen bir IP.  
- **iPhone Olmayan Cihaz**: Android veya Windows cihazı.  
- **Kenar Durumlar**: Geçersiz IP, erişilemeyen hedef.  

- **Output / Çıktı:**  
  **English:** Document in `test_results.md`: **Input** (targets), **Expected Result**, **Actual Result**, **Observations**.  
  **Turkish:** `test_results.md` dosyasına kaydedin: **Giriş** (hedefler), **Beklenen Sonuç**, **Gerçek Sonuç**, **Gözlemler**.  

---

##### **6. Confirm / Doğrulama**
**English:** Manually verify the detection using another method (e.g., checking device manually, using other tools like Wireshark).  
**Turkish:** Tespiti başka bir yöntemle manuel olarak doğrulayın (ör. cihazı manuel olarak kontrol etme, Wireshark gibi diğer araçları kullanma).  

- **Output / Çıktı:**  
  **English:** Add a "Confirmation / Doğrulama" section to `test_results.md` with cross-check results and accuracy notes.  
  **Turkish:** `test_results.md` dosyasına "Doğrulama" bölümü ekleyin; çapraz kontrol sonuçları ve doğruluk notlarıyla.  

---

##### **7. Contribute / Katkı Sağlama**
**English:** Submit to `https://github.com/QLineTech/Q-Pentest`:  
- Fork the repo, create a branch (`feature/iphone-detection`), commit `iphone_network_device_detection.py`, `research_notes.md`, `test_results.md`, `research_data.json`, and submit a pull request with a detailed description.  
**Turkish:** `https://github.com/QLineTech/Q-Pentest` adresine gönderin:  
- Depoyu çatallayın, bir dal oluşturun (`feature/iphone-detection`), `iphone_network_device_detection.py`, `research_notes.md`, `test_results.md`, `research_data.json` dosyalarını taahhüt edin ve detaylı bir açıklama ile pull request gönderin.  

---

#### Roadmap / Yol Haritası
**English:**  
- **Phase 1: Preparation / Hazırlık**: Research techniques and tools, document findings.  
- **Phase 2: Learning and Planning / Öğrenme ve Planlama**: Study resources, summarize insights, plan the script.  
- **Phase 3: Implementation / Uygulama**: Build functions for scanning, analyzing, and determining devices.  
- **Phase 4: Testing and Validation / Test ve Doğrulama**: Test the script, confirm results with manual checks.  
- **Phase 5: Contribution / Katkı**: Submit work to GitHub.  
**Turkish:**  
- **Aşama 1: Hazırlık**: Teknikleri ve araçları araştırın, bulguları belgeleyin.  
- **Aşama 2: Öğrenme ve Planlama**: Kaynakları inceleyin, içgörüleri özetleyin, betiği planlayın.  
- **Aşama 3: Uygulama**: Tarama, analiz ve cihaz belirleme fonksiyonlarını oluşturun.  
- **Aşama 4: Test ve Doğrulama**: Betiği test edin, sonuçları manuel kontrollerle doğrulayın.  
- **Aşama 5: Katkı**: Çalışmayı GitHub’a gönderin.  

---

#### Small Implementation Steps / Küçük Uygulama Adımları
**English:**  
- **Scanning**: Use Nmap with specific scripts to scan the target.  
- **Analyzing**: Extract data from scan results that indicate an iPhone.  
- **Determining Device**: Assess if the device is an iPhone and estimate accuracy.  
- **Error Handling**: Manage scan errors and invalid inputs.  
- **Reporting**: Format detection results in markdown.  
- **Main**: Process multiple targets and generate reports.  
**Turkish:**  
- **Tarama**: Hedefi taramak için belirli betiklerle Nmap kullanın.  
- **Analiz**: Tarama sonuçlarından iPhone’u gösteren verileri çıkarın.  
- **Cihazı Belirleme**: Cihazın iPhone olup olmadığını değerlendirin ve doğruluğu tahmin edin.  
- **Hata İşleme**: Tarama hatalarını ve geçersiz girdileri yönetin.  
- **Raporlama**: Tespit sonuçlarını markdown formatında düzenleyin.  
- **Ana**: Birden fazla hedefi işleyin ve raporlar oluşturun.  
