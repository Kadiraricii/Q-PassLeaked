## Task : Device EOL (End-of-Life) Check / Cihaz EOL (Ömrünün Sonu) Kontrolü
**Module File / Modül Dosyası:** `modules/device_eol_check.py`

### Instruction Set for Amateur Cybersecurity Students / Amatör Siber Güvenlik Öğrencileri İçin Talimat Seti

#### 1. Research Phase / Araştırma Aşaması
- **Objective / Amaç:**  
  Learn how to determine if a network device (e.g., router, switch, firewall) has reached its End-of-Life (EOL) stage, where the manufacturer ceases providing firmware updates, security patches, or technical support. This is critical for assessing security risks in a network. / Bir ağ cihazının (ör. router, switch, firewall) Ömrünün Sonu (EOL) aşamasına gelip gelmediğini, yani üreticinin artık yazılım güncellemeleri, güvenlik yamaları veya teknik destek sağlamadığını öğrenin. Bu, bir ağdaki güvenlik risklerini değerlendirmek için kritik öneme sahiptir.

- **Approach / Yaklaşım:**  
  Investigate a wide range of resources, including vendor-specific EOL databases, automated tools, APIs, and community-driven solutions, to identify EOL status using device model numbers, serial numbers, or firmware versions. Explore both manual and programmatic methods. / Cihaz model numaraları, seri numaraları veya yazılım sürümlerini kullanarak EOL durumunu belirlemek için üreticiye özgü EOL veritabanları, otomatik araçlar, API’ler ve topluluk odaklı çözümler gibi geniş bir kaynak yelpazesini araştırın. Hem manuel hem de programatik yöntemleri keşfedin.

- **Advanced DeepSearch Prompt / Gelişmiş DeepSearch Komutu:**  
  ```json
  {
    "query": "Explore all possible methods, tools, and resources to determine if a network device (e.g., router, switch, firewall) has reached End-of-Life (EOL). Include detailed vendor-specific EOL databases (e.g., Cisco Product Lifecycle, Juniper Support Portal, Fortinet EOL Notices), automated tools (e.g., SNMP-based queries, SSH automation, Nessus EOL plugins), public and private APIs (e.g., Cisco PSIRT API), and open-source community scripts (e.g., Python-based scrapers). Provide step-by-step instructions for at least 12 distinct techniques, including how to gather device details (model, serial number, firmware version), query EOL status, and interpret results (e.g., 'End of Support' vs. 'End of Sale'). Highlight advanced challenges such as deprecated devices not listed in databases, regional variations in EOL policies, and manual lookup inefficiencies. Include real-world examples from network auditing or penetration testing contexts."
  }
  ```

- **Steps / Adımlar:**  
  1. **Gather Information / Bilgi Toplama:**  
     - **Vendor Research / Üretici Araştırması:** Investigate EOL policies and official databases for major vendors such as Cisco (End of Life Portal), Juniper (Support Portal), Fortinet (EOL Notices), and Ubiquiti (Community Forums). / Cisco (EOL Portalı), Juniper (Destek Portalı), Fortinet (EOL Bildirimleri) ve Ubiquiti (Topluluk Forumları) gibi büyük üreticilerin EOL politikalarını ve resmi veritabanlarını araştırın.  
     - **Tool Exploration / Araç Keşfi:** Explore tools like SNMP (Simple Network Management Protocol), SSH clients (e.g., Paramiko), and vulnerability scanners (e.g., Nessus, OpenVAS) that can extract device details and cross-reference EOL status. / SNMP (Basit Ağ Yönetim Protokolü), SSH istemcileri (ör. Paramiko) ve güvenlik açığı tarayıcıları (ör. Nessus, OpenVAS) gibi cihaz detaylarını çıkarabilen ve EOL durumunu çapraz kontrol edebilen araçları keşfedin.  
     - **Community Resources / Topluluk Kaynakları:** Search GitHub, Reddit (r/networking), and cybersecurity forums for scripts or tools automating EOL checks (e.g., Python scripts scraping vendor websites). / GitHub, Reddit (r/networking) ve siber güvenlik forumlarında EOL kontrollerini otomatikleştiren betikler veya araçlar (ör. üretici web sitelerini kazıyan Python betikleri) arayın.  

  2. **Key Methods to Research / Araştırılacak Ana Yöntemler:**  
     - **Vendor EOL Databases / Üretici EOL Veritabanları:**  
       - Example: Cisco’s EOL/EOS Portal (search "Cisco End of Life Policy"). / Örnek: Cisco’nun EOL/EOS Portalı ("Cisco End of Life Policy" araması).  
       - Usage: Enter a device model (e.g., "Cisco Catalyst 2950") into the search tool and check its status (e.g., "End of Support: 2012-10-31"). / Kullanım: Bir cihaz modelini (ör. "Cisco Catalyst 2950") arama aracına girin ve durumunu kontrol edin (ör. "Destek Sonu: 2012-10-31").  
       - Limitation: Manual process; outdated or unlisted devices may require contacting support. / Sınırlama: Manuel süreç; eski veya listelenmemiş cihazlar destekle iletişime geçmeyi gerektirebilir.  
     - **SNMP Queries / SNMP Sorguları:**  
       - Command: `snmpwalk -v2c -c public <device_ip> 1.3.6.1.2.1.1.5` / Komut: `snmpwalk -v2c -c public <cihaz_ip> 1.3.6.1.2.1.1.5`  
       - Purpose: Retrieves the device’s system name and description (e.g., "Cisco ISR 4331, IOS 16.9"). Cross-reference with vendor EOL data. / Amaç: Cihazın sistem adını ve açıklamasını alır (ör. "Cisco ISR 4331, IOS 16.9"). Üretici EOL verileriyle çapraz kontrol edilir.  
       - Limitation: Requires SNMP enabled and correct community string; some devices block this. / Sınırlama: SNMP’nin etkinleştirilmesini ve doğru topluluk dizesini gerektirir; bazı cihazlar bunu engeller.  
     - **API Queries / API Sorguları:**  
       - Example: Cisco’s Product Security Incident Response Team (PSIRT) API. / Örnek: Cisco’nun Ürün Güvenlik Olay Müdahale Ekibi (PSIRT) API’si.  
       - Usage: Use an API key to query `https://api.cisco.com/product/v1/information/<model>` for lifecycle data. / Kullanım: Yaşam döngüsü verileri için bir API anahtarıyla `https://api.cisco.com/product/v1/information/<model>` sorgulayın.  
       - Limitation: Requires API access (often enterprise-only) and coding knowledge. / Sınırlama: API erişimi (genellikle yalnızca kurumsal) ve kodlama bilgisi gerektirir.  
     - **Web Scraping / Web Kazıma:**  
       - Tool: Python with `requests` and `beautifulsoup4`. / Araç: `requests` ve `beautifulsoup4` ile Python.  
       - Purpose: Automate lookups by scraping EOL pages (e.g., Fortinet’s support site). / Amaç: EOL sayfalarını kazıyarak aramaları otomatikleştirin (ör. Fortinet’in destek sitesi).  
       - Limitation: Vendor sites may block bots or change layouts frequently. / Sınırlama: Üretici siteleri botları engelleyebilir veya düzenleri sık sık değiştirebilir.  

  3. **Document Findings / Bulguları Belgeleyin:**  
     - Create a file named `research_notes_eol.md` with the following structure: / `research_notes_eol.md` adında bir dosya oluşturun ve şu yapıyı kullanın:  
       - **Vendor EOL Resources / Üretici EOL Kaynakları:** List URLs and descriptions (e.g., "Cisco EOL Portal: Comprehensive lifecycle data"). / URL’leri ve açıklamaları listeleyin (ör. "Cisco EOL Portalı: Kapsamlı yaşam döngüsü verileri").  
       - **Automated Tools and Scripts / Otomatik Araçlar ve Betikler:** Describe tools like `pysnmp`, Nessus plugins, or custom Python scrapers with usage examples. / `pysnmp`, Nessus eklentileri veya özel Python kazıyıcılar gibi araçları kullanım örnekleriyle tarif edin.  
       - **Challenges and Solutions / Zorluklar ve Çözümler:** Note issues like unlisted legacy devices and propose workarounds (e.g., contacting vendors directly). / Listelenmemiş eski cihazlar gibi sorunları not edin ve çözümler önerin (ör. doğrudan üreticilerle iletişime geçmek).  
     - For each method, include its name, detailed steps, a practical example (e.g., querying "Juniper EX2200"), and limitations. / Her yöntem için adını, ayrıntılı adımları, pratik bir örneği (ör. "Juniper EX2200" sorgulama) ve sınırlamaları ekleyin.

#### 2. Implementation Phase / Uygulama Aşaması
- **Objective / Amaç:**  
  Develop a Python script to automate EOL checks for multiple network devices, integrating at least two methods (e.g., SNMP and web scraping) and generating a detailed report. / Birden fazla ağ cihazı için EOL kontrollerini otomatikleştiren, en az iki yöntemi (ör. SNMP ve web kazıma) entegre eden ve ayrıntılı bir rapor üreten bir Python betiği geliştirin.

- **Steps / Adımlar:**  
  1. **Set Up Environment / Ortamı Kurun:**  
     - Install dependencies: / Bağımlılıkları kurun:  
       - `requests` (HTTP requests): `pip install requests`  
       - `beautifulsoup4` (HTML parsing): `pip install beautifulsoup4`  
       - `pysnmp` (SNMP queries): `pip install pysnmp`  
       - `paramiko` (SSH access): `pip install paramiko`  
     - Ensure network access to target devices and vendor websites. / Hedef cihazlara ve üretici web sitelerine ağ erişimi olduğundan emin olun.  

  2. **Write the Code / Kodu Yazın:**  
     - Include these core functions: / Şu temel fonksiyonları ekleyin:  
       - `get_device_info(ip)`: Extracts model and version via SNMP or SSH. / Model ve sürümü SNMP veya SSH ile çıkarır.  
       - `check_eol(model, vendor)`: Queries EOL status (e.g., via API or scraping). / EOL durumunu sorgular (ör. API veya kazıma yoluyla).  
       - `generate_report(results)`: Outputs a formatted report to `eol_report.txt`. / `eol_report.txt` dosyasına biçimlendirilmiş bir rapor çıkarır.  
     - Example Code / Örnek Kod:  
       ```python
       import requests
       from bs4 import BeautifulSoup
       from pysnmp.hlapi import *
       import json

       def get_device_info(ip):
           # SNMP query for device description / Cihaz açıklaması için SNMP sorgusu
           iterator = getCmd(SnmpEngine(), CommunityData('public'), 
                             UdpTransportTarget((ip, 161)), ContextData(),
                             ObjectType(ObjectIdentity('1.3.6.1.2.1.1.1.0')))
           error, _, _, result = next(iterator)
           if error:
               return f"SNMP Error: {error}"
           return result[0][1].prettyPrint()  # e.g., "Cisco ISR 4331, IOS 16.9"

       def check_eol(model, vendor="cisco"):
           # Simulated web scraping (replace with real vendor URL) / Simüle edilmiş web kazıma (gerçek üretici URL'si ile değiştirin)
           url = f"https://www.cisco.com/c/en/us/products/{model}/eos-eol-notice.html"
           try:
               response = requests.get(url, timeout=5)
               soup = BeautifulSoup(response.text, 'html.parser')
               status = soup.find('div', class_='eol-status') or "Not Found"
               return status.text if status != "Not Found" else "EOL status unavailable"
           except Exception as e:
               return f"Error: {e}"

       def generate_report(results):
           with open("eol_report.txt", "w") as f:
               f.write("EOL Check Report\n")
               f.write("=" * 20 + "\n")
               for ip, data in results.items():
                   f.write(f"IP: {ip}\nInfo: {data['info']}\nEOL Status: {data['status']}\n\n")

       # Test the script / Betiği test edin
       ip = "192.168.1.1"
       info = get_device_info(ip)
       status = check_eol(info.split(",")[0])  # Extract model from info
       results = {ip: {"info": info, "status": status}}
       generate_report(results)
       print(f"Device Info: {info}\nEOL Status: {status}")
       ```

  3. **Test the Script / Betiği Test Edin:**  
     - Test with multiple devices: a known EOL device (e.g., "Cisco 2800 Series") and a current one (e.g., "Cisco ISR 1100"). / Birden fazla cihazla test edin: bilinen bir EOL cihazı (ör. "Cisco 2800 Serisi") ve güncel bir cihaz (ör. "Cisco ISR 1100").  
     - Validate results against vendor documentation or manual lookups. / Sonuçları üretici dokümantasyonu veya manuel aramalarla doğrulayın.  
     - Debug issues like SNMP timeouts or blocked web requests. / SNMP zaman aşımı veya engellenmiş web istekleri gibi sorunları giderin.

#### 3. Documentation Phase / Dokümantasyon Aşaması
- **Objective / Amaç:**  
  Provide comprehensive, beginner-friendly documentation explaining the script’s purpose, setup, and usage, ensuring it’s accessible to users with minimal experience. / Betiğin amacını, kurulumunu ve kullanımını açıklayan, minimum deneyime sahip kullanıcılar için erişilebilir, kapsamlı ve başlangıç dostu dokümantasyon sağlayın.

- **Deliverables / Teslim Edilecekler:**  
  - **README.md:**  
    - **Overview / Genel Bakış:** "This Python script automates EOL checks for network devices using SNMP and web scraping, generating a report of findings." / "Bu Python betiği, SNMP ve web kazıma kullanarak ağ cihazları için EOL kontrollerini otomatikleştirir ve bulguların bir raporunu üretir."  
    - **Installation / Kurulum:**  
      - "Install dependencies: `pip install requests beautifulsoup4 pysnmp paramiko`" / "Bağımlılıkları kurun: `pip install requests beautifulsoup4 pysnmp paramiko`"  
      - "Ensure SNMP is enabled on target devices with community string 'public'." / "Hedef cihazlarda SNMP’nin 'public' topluluk dizesiyle etkinleştirildiğinden emin olun."  
    - **Usage / Kullanım:**  
      - "Run: `python device_eol_check.py <device_ip>`" / "Çalıştır: `python device_eol_check.py <cihaz_ip>`"  
      - "Output: Check `eol_report.txt` for results." / "Çıktı: Sonuçlar için `eol_report.txt` dosyasını kontrol edin."  
    - **Limitations / Sınırlamalar:** "Requires network access and may fail if vendors block scraping." / "Ağ erişimi gerektirir ve üreticiler kazımayı engellerse başarısız olabilir."  

  - **research_notes_eol.md:**  
    - Detailed findings from the research phase, including at least 12 methods, vendor links, tool descriptions, challenges (e.g., "Legacy devices missing from databases"), and mitigation ideas (e.g., "Use archived vendor PDFs"). / Araştırma aşamasından ayrıntılı bulgular, en az 12 yöntem, üretici bağlantıları, araç açıklamaları, zorluklar (ör. "Veritabanlarında eksik eski cihazlar") ve hafifletme fikirleri (ör. "Arşivlenmiş üretici PDF’lerini kullanın") dahil.
