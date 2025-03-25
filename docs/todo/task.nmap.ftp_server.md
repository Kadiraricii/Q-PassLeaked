## Task: FTP Server Network Device Detection / FTP Sunucusu Ağ Cihazı Tespiti
**Assigned Role / Atanan Rol:** Sage / Bilge  
**Module File / Modül Dosyası:** `modules/ftpserver_network_detection.py`

This task involves detecting FTP servers on a network, identifying their software versions, checking for anonymous access, and spotting potential vulnerabilities. Below, I’ve broken it down into three main phases to ensure a complete learning experience.

---

### 1. Research Phase / Araştırma Aşaması
**Objective / Amaç:**  
Conduct a detailed investigation into all possible techniques, tools, and methods for detecting FTP servers on a network. / Ağda FTP sunucularını tespit etmek için tüm teknikleri, araçları ve yöntemleri kapsayan ayrıntılı bir araştırma yapın.

#### Steps / Adımlar:
1. **Gather Information / Bilgi Toplama:**  
   Use online resources, manuals, and tools to explore FTP detection methods. Focus on:
   - **Tools / Araçlar:** Nmap, Wireshark, Netcat, telnet, Python scripts.  
   - **Techniques / Teknikler:** Port scanning, banner grabbing, packet analysis, vulnerability scanning.  
   - **Goals / Hedefler:** Detect FTP servers, identify versions (e.g., vsftpd 3.0.3), check anonymous access, and find vulnerabilities (e.g., CVE-2011-2523).  

2. **Explore Specific Methods / Özel Yöntemleri Keşfedin:**  
   Here are some key techniques to research (aim for at least 15 unique methods):  
   - **Nmap Scans / Nmap Taramaları:**  
     - Command / Komut: `nmap -p 21 <ip>`  
       - **Purpose / Amaç:** Checks if port 21 (default FTP port) is open. / Port 21'in (varsayılan FTP portu) açık olup olmadığını kontrol eder.  
       - **Output / Çıktı:** "21/tcp open ftp"  
       - **Limitation / Sınırlama:** Misses FTP servers on non-standard ports (e.g., 2121). / Standart dışı portlardaki FTP sunucularını kaçırır.  
     - Command / Komut: `nmap --script ftp-anon <ip>`  
       - **Purpose / Amaç:** Tests for anonymous FTP login. / Anonim FTP girişini test eder.  
       - **Output / Çıktı:** "Anonymous FTP login allowed"  
       - **Limitation / Sınırlama:** Fails if the server blocks anonymous logins. / Sunucu anonim girişleri engelliyorsa başarısız olur.  
   - **Manual Tools / Manuel Araçlar:**  
     - Command / Komut: `telnet <ip> 21`  
       - **Purpose / Amaç:** Connects to port 21 to grab the FTP banner. / Port 21'e bağlanarak FTP banner'ını alır.  
       - **Output / Çıktı:** "220 Welcome to vsftpd 3.0.3"  
       - **Limitation / Sınırlama:** Requires manual effort; no automation. / Manuel çaba gerektirir; otomasyon yoktur.  
   - **Packet Analysis / Paket Analizi:**  
     - Tool / Araç: Wireshark  
       - **Filter / Filtre:** `tcp.port == 21`  
       - **Purpose / Amaç:** Captures FTP traffic to analyze commands and responses. / FTP trafiğini yakalayarak komutları ve yanıtları analiz eder.  
       - **Limitation / Sınırlama:** Useless if traffic is encrypted (e.g., FTPS). / Trafik şifreliyse (ör. FTPS) işe yaramaz.  

3. **Document Findings / Bulguları Belgeleyin:**  
   Create a file called `research_notes_ftpserver.md` with sections like:  
   - Nmap Techniques / Nmap Teknikleri  
   - Manual Methods / Manuel Yöntemler  
   - Packet Analysis / Paket Analizi  
   - Custom Scripts / Özel Betikler  
   For each method, include:  
   - **Name / İsim:** e.g., "Nmap Anonymous Check / Nmap Anonim Kontrolü"  
   - **Command / Komut:** Exact syntax.  
   - **Output / Çıktı:** What to expect.  
   - **Accuracy / Doğruluk:** How reliable it is.  
   - **Limitations / Sınırlamalar:** Potential issues.  

---

### 2. Implementation Phase / Uygulama Aşaması
**Objective / Amaç:**  
Turn your research into a working Python script to detect FTP servers. / Araştırmanızı FTP sunucularını tespit eden çalışan bir Python betiğine dönüştürün.

#### Steps / Adımlar:
1. **Set Up Your Environment / Ortamı Kurun:**  
   - Install required tools:  
     - `pip install python-nmap scapy`  
     - Ensure `nmap` is installed on your system (e.g., `sudo apt install nmap` on Linux).  
   - **Turkish Note / Türkçe Not:** Bu araçlar kod yazmayı ve taramayı kolaylaştırır. / These tools make coding and scanning easier.

2. **Write the Code / Kodu Yazın:**  
   Create `ftpserver_network_detection.py` with these functions:  
   - **Port Scanning / Port Tarama:** Check if port 21 is open.  
   - **Banner Grabbing / Banner Alma:** Get the server’s version.  
   - **Anonymous Testing / Anonim Testi:** Try logging in as "anonymous."  
   - **Vulnerability Check / Güvenlik Açığı Kontrolü:** Look up known issues for the version.  
   - Example Code / Örnek Kod:  
     ```python
     import nmap

     def scan_ftp(ip):
         nm = nmap.PortScanner()
         nm.scan(ip, '21', arguments='--script ftp-anon')
         if 'tcp' in nm[ip] and 21 in nm[ip]['tcp']:
             result = nm[ip]['tcp'][21]['script']['ftp-anon']
             return f"FTP Scan Result / FTP Tarama Sonucu: {result}"
         return "No FTP server found / FTP sunucusu bulunamadı"

     # Test it
     print(scan_ftp("192.168.1.1"))
     ```

3. **Test the Script / Betiği Test Edin:**  
   - Set up a test FTP server (e.g., install `vsftpd` on a virtual machine).  
   - Run your script: `python ftpserver_network_detection.py <ip>`  
   - Try different scenarios: non-standard ports, firewalled servers, etc.  

---

### 3. Documentation Phase / Dokümantasyon Aşaması
**Objective / Amaç:**  
Provide clear instructions so others can use and understand your work. / Başkalarının çalışmanızı kullanabilmesi ve anlayabilmesi için net talimatlar sağlayın.

#### Deliverables / Teslim Edilecekler:
1. **README.md:**  
   - **Overview / Genel Bakış:** Explain what the script does. / Betiğin ne yaptığını açıklayın.  
   - **Installation / Kurulum:** List commands to install dependencies. / Bağımlılıkları kurmak için komutları listeleyin.  
   - **Usage / Kullanım:** Show how to run it, e.g., `python ftpserver_network_detection.py 192.168.1.1`.  
   - Example / Örnek:  
     ```
     # Install dependencies / Bağımlılıkları kur
     pip install python-nmap

     # Run the script / Betiği çalıştır
     python ftpserver_network_detection.py 192.168.1.1
     ```

2. **research_notes_ftpserver.md:**  
   - Include all 15+ techniques from the research phase, fully detailed with commands, outputs, and limitations.  

---

### Sample Techniques / Örnek Teknikler
Here’s a preview of what your research might include:  
1. **Nmap Port Scan / Nmap Port Tarama**  
   - **Command / Komut:** `nmap -p 21 <ip>`  
   - **Output / Çıktı:** "21/tcp open ftp"  
   - **Accuracy / Doğruluk:** High for port 21. / Port 21 için yüksek.  
   - **Limitation / Sınırlama:** Misses other ports. / Diğer portları kaçırır.  
2. **Telnet Banner Grab / Telnet Banner Alma**  
   - **Command / Komut:** `telnet <ip> 21`  
   - **Output / Çıktı:** "220 Welcome to ProFTPD 1.3.5"  
   - **Limitation / Sınırlama:** Manual process. / Manuel süreç.  
3. **Wireshark Analysis / Wireshark Analizi**  
   - **Filter / Filtre:** `tcp.port == 21`  
   - **Output / Çıktı:** FTP commands like "USER anonymous"  
   - **Limitation / Sınırlama:** Can’t see encrypted data. / Şifreli verileri göremez.  
