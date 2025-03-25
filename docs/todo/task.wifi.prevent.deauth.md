## Task: Wi-Fi Deauth Detection and Defense / Wi-Fi Deauth Tespiti ve Savunması
**Module File / Modül Dosyası:** `modules/wifi_deauth_detection.py`

### Instruction Set for Amateur Cybersecurity Students / Amatör Siber Güvenlik Öğrencileri İçin Talimat Seti

#### 1. Research Phase / Araştırma Aşaması
- **Objective / Amaç:**  
  Understand Wi-Fi deauthentication attacks (where attackers send spoofed deauth frames to disconnect devices) and learn how to detect and defend against them, enhancing wireless network security. / Wi-Fi deauthentication saldırılarını (saldırganların cihazları bağlantıdan koparmak için sahte deauth frame’leri gönderdiği) anlamayı ve kablosuz ağ güvenliğini artırmak için bunları tespit etmeyi ve savunmayı öğrenin.

- **Approach / Yaklaşım:**  
  Research attack mechanisms, detection tools, packet analysis techniques, and mitigation strategies using a mix of practical tools, theoretical resources, and real-world scenarios. / Saldırı mekanizmalarını, tespit araçlarını, paket analizi tekniklerini ve hafifletme stratejilerini pratik araçlar, teorik kaynaklar ve gerçek dünya senaryolarını birleştirerek araştırın.

- **Advanced DeepSearch Prompt / Gelişmiş DeepSearch Komutu:**  
  ```json
  {
    "query": "Research all techniques, tools, and strategies to detect Wi-Fi deauthentication attacks and defend against them comprehensively. Include detection methods (e.g., Wireshark filters, Scapy packet sniffing, Aircrack-ng monitoring, Kismet), packet analysis specifics (e.g., identifying deauth frame subtypes, spoofed MACs), and defense mechanisms (e.g., WPA3 adoption, 802.11w protected management frames, IDS/IPS integration, MAC filtering). Provide detailed instructions for at least 12 unique approaches, including setup steps, command examples, expected outputs (e.g., 'Deauth frame from MAC AA:BB:CC'), and limitations (e.g., MAC spoofing, encrypted management frames). Include real-world examples from wireless penetration testing, network defense, or forensic investigations, covering both 2.4 GHz and 5 GHz bands."
  }
  ```

- **Steps / Adımlar:**  
  1. **Gather Information / Bilgi Toplama:**  
     - **Attack Tools / Saldırı Araçları:** Study tools like `aireplay-ng` (part of Aircrack-ng) to understand how deauth attacks are executed. / Deauth saldırılarının nasıl gerçekleştirildiğini anlamak için `aireplay-ng` (Aircrack-ng’nin bir parçası) gibi araçları inceleyin.  
     - **Detection Tools / Tespit Araçları:** Explore Wireshark, Scapy, Kismet, and Aircrack-ng for monitoring deauth frames. / Deauth frame’lerini izlemek için Wireshark, Scapy, Kismet ve Aircrack-ng’yi keşfedin.  
     - **Defense Strategies / Savunma Stratejileri:** Research modern defenses like WPA3, 802.11w (Protected Management Frames), and intrusion detection systems. / WPA3, 802.11w (Korumalı Yönetim Frame’leri) ve izinsiz giriş tespit sistemleri gibi modern savunmaları araştırın.  

  2. **Key Methods to Research / Araştırılacak Ana Yöntemler:**  
     - **Wireshark Detection / Wireshark Tespiti:**  
       - Filter: `wlan.fc.type_subtype == 0x0c` / Filtre: `wlan.fc.type_subtype == 0x0c`  
       - Purpose: Identifies deauthentication frames in captured traffic. / Yakalanan trafikte deauthentication frame’lerini tanımlar.  
       - Limitation: Requires monitor mode and may miss frames on other channels. / Sınırlama: Monitör modu gerektirir ve diğer kanallardaki frame’leri kaçırabilir.  
     - **Scapy Sniffing / Scapy Koklama:**  
       - Usage: Sniff packets and check for `Dot11Deauth` layer. / Paketleri koklayın ve `Dot11Deauth` katmanını kontrol edin.  
       - Purpose: Real-time detection of deauth packets. / Deauth paketlerinin gerçek zamanlı tespiti.  
       - Limitation: Needs a compatible Wi-Fi adapter in monitor mode. / Sınırlama: Monitör modunda uyumlu bir Wi-Fi adaptörü gerektirir.  
     - **Defense with WPA3 / WPA3 ile Savunma:**  
       - Usage: Upgrade routers to WPA3, which resists deauth attacks via stronger encryption. / Router’ları WPA3’e yükseltin; bu, daha güçlü şifreleme ile deauth saldırılarına direnir.  
       - Limitation: Not all devices support WPA3 yet. / Sınırlama: Henüz tüm cihazlar WPA3’ü desteklemiyor.  
     - **802.11w Implementation / 802.11w Uygulaması:**  
       - Purpose: Enables Protected Management Frames to prevent spoofed deauth packets. / Sahte deauth paketlerini önlemek için Korumalı Yönetim Frame’lerini etkinleştirir.  
       - Limitation: Requires support from both AP and clients. / Sınırlama: Hem erişim noktası hem de istemcilerden destek gerektirir.  

  3. **Document Findings / Bulguları Belgeleyin:**  
     - Create `research_notes_wifi.md` with this structure: / `research_notes_wifi.md` dosyasını şu yapıyla oluşturun:  
       - **Deauth Attack Overview / Deauth Saldırı Genel Bakış:** Explain mechanics (e.g., "Spoofed frames mimic AP"). / Mekanizmayı açıklayın (ör. "Sahte frame’ler AP’yi taklit eder").  
       - **Detection Techniques / Tespit Teknikleri:** List tools, filters, and sample outputs (e.g., "Deauth from MAC 00:11:22:33:44:55"). / Araçları, filtreleri ve örnek çıktıları listeleyin (ör. "MAC 00:11:22:33:44:55’ten deauth").  
       - **Defense Strategies / Savunma Stratejileri:** Detail WPA3, 802.11w, and IDS with setup steps. / WPA3, 802.11w ve IDS’yi kurulum adımlarıyla ayrıntılı olarak tarif edin.  
       - **Challenges / Zorluklar:** Note spoofing, channel hopping, and mitigation ideas (e.g., "Monitor all channels"). / Spoofing, kanal atlama ve hafifletme fikirlerini (ör. "Tüm kanalları izle") not edin.  

#### 2. Implementation Phase / Uygulama Aşaması
- **Objective / Amaç:**  
  Create a Python script to detect Wi-Fi deauth attacks in real-time and log incidents, with optional alerts for immediate response. / Wi-Fi deauth saldırılarını gerçek zamanlı olarak tespit eden ve olayları kaydeden, isteğe bağlı olarak anında yanıt için uyarılar içeren bir Python betiği oluşturun.

- **Steps / Adımlar:**  
  1. **Set Up Environment / Ortamı Kurun:**  
     - Install: `pip install scapy` / Kur: `pip install scapy`  
     - Configure Wi-Fi adapter to monitor mode: `sudo iwconfig wlan0 mode monitor` and `sudo ifconfig wlan0 up`. / Wi-Fi adaptörünü monitör moduna yapılandırın: `sudo iwconfig wlan0 mode monitor` ve `sudo ifconfig wlan0 up`.  
     - Verify with `iwconfig` that mode is "Monitor." / `iwconfig` ile modun "Monitor" olduğunu doğrulayın.  

  2. **Write the Code / Kodu Yazın:**  
     - Include these functions: / Şu fonksiyonları ekleyin:  
       - `sniff_deauth(interface)`: Sniffs for deauth packets on a specified interface. / Belirtilen bir arabirimde deauth paketlerini koklar.  
       - `alert_user(packet)`: Logs and alerts on deauth detection. / Deauth tespiti üzerine kaydeder ve uyarır.  
       - `log_incident(packet)`: Saves details to a log file. / Ayrıntıları bir log dosyasına kaydeder.  
     - Example Code / Örnek Kod:  
       ```python
       from scapy.all import *
       from datetime import datetime

       def alert_user(packet):
           if packet.haslayer(Dot11Deauth):
               src = packet.addr2
               dst = packet.addr1
               print(f"[ALERT] Deauth detected at {datetime.now()}: Source={src}, Dest={dst}")
               log_incident(packet)

       def log_incident(packet):
           with open("deauth_log.txt", "a") as f:
               f.write(f"{datetime.now()} - Deauth: Source={packet.addr2}, Dest={packet.addr1}\n")

       def sniff_deauth(interface):
           print(f"Starting deauth detection on {interface}...")
           sniff(iface=interface, prn=alert_user, filter="wlan.fc.type_subtype == 0x0c", store=0)

       # Run the script / Betiği çalıştırın
       interface = "wlan0"  # Replace with your interface / Arabiriminizle değiştirin
       sniff_deauth(interface)
       ```

  3. **Test the Script / Betiği Test Edin:**  
     - Simulate an attack: `sudo aireplay-ng --deauth 20 -a <bssid> wlan0` / Bir saldırı simüle edin: `sudo aireplay-ng --deauth 20 -a <bssid> wlan0`  
     - Run the script and verify it logs and alerts on deauth frames. / Betiği çalıştırın ve deauth frame’lerini kaydedip uyarı verdiğini doğrulayın.  
     - Check `deauth_log.txt` for incident details. / Olay ayrıntıları için `deauth_log.txt` dosyasını kontrol edin.  

#### 3. Documentation Phase / Dokümantasyon Aşaması
- **Objective / Amaç:**  
  Provide thorough documentation to guide users through setup, usage, and understanding of deauth detection. / Kullanıcıları kurulum, kullanım ve deauth tespiti anlayışında yönlendirmek için kapsamlı dokümantasyon sağlayın.

- **Deliverables / Teslim Edilecekler:**  
  - **README.md:**  
    - **Overview / Genel Bakış:** "This script detects Wi-Fi deauth attacks in real-time using Scapy, logging incidents to a file." / "Bu betik, Scapy kullanarak Wi-Fi deauth saldırılarını gerçek zamanlı olarak tespit eder ve olayları bir dosyaya kaydeder."  
    - **Installation / Kurulum:**  
      - "Install: `pip install scapy`" / "Kur: `pip install scapy`"  
      - "Set adapter to monitor mode: `sudo iwconfig wlan0 mode monitor`" / "Adaptörü monitör moduna ayarlayın: `sudo iwconfig wlan0 mode monitor`"  
    - **Usage / Kullanım:**  
      - "Run: `python wifi_deauth_detection.py <interface>` (e.g., `wlan0`)" / "Çalıştır: `python wifi_deauth_detection.py <arabirim>` (ör. `wlan0`)"  
      - "Output: Alerts in terminal and logs in `deauth_log.txt`." / "Çıktı: Terminalde uyarılar ve `deauth_log.txt` dosyasında loglar."  
    - **Limitations / Sınırlamalar:** "Requires monitor mode support and root privileges." / "Monitör modu desteği ve kök ayrıcalıkları gerektirir."  

  - **research_notes_wifi.md:**  
    - Detailed notes on 12+ methods for detection and defense, including tools, commands, outputs, and challenges (e.g., "MAC spoofing bypasses filters"). / Tespit ve savunma için 12’den fazla yöntem hakkında ayrıntılı notlar, araçlar, komutlar, çıktılar ve zorluklar (ör. "MAC spoofing filtreleri atlar") ile birlikte.

---

### Contribute Instruction / Katkı Talimatı
To share your work with the cybersecurity community, follow these steps to contribute to the GitHub repository: / Çalışmanızı siber güvenlik topluluğuyla paylaşmak için GitHub deposuna katkıda bulunmak üzere şu adımları izleyin:

1. **Fork the Repository / Depoyu Çatallayın:**  
   - Visit `https://github.com/QLineTech/Q-Pentest` and click "Fork" to create your own copy. / `https://github.com/QLineTech/Q-Pentest` adresine gidin ve kendi kopyanızı oluşturmak için "Fork" tıklayın.

2. **Clone Your Fork / Çatalınızı Klonlayın:**  
   - Run: `git clone https://github.com/<your_username>/Q-Pentest.git` / Çalıştırın: `git clone https://github.com/<kullanıcı_adınız>/Q-Pentest.git`

3. **Create a Branch / Bir Dal Oluşturun:**  
   - Run: `git checkout -b feature/<task_name>` / Çalıştırın: `git checkout -b feature/<görev_adı>`  
   - Example: `git checkout -b feature/dns-server-detection` / Örnek: `git checkout -b feature/dns-server-detection`

4. **Add Your Files / Dosyalarınızı Ekleyin:**  
   - Add your script (e.g., `dnsserver_detection.py`), research notes (e.g., `research_notes_dns.md`), and any test outputs (e.g., `dns_report.txt`). / Betiğinizi (ör. `dnsserver_detection.py`), araştırma notlarınızı (ör. `research_notes_dns.md`) ve test çıktılarını (ör. `dns_report.txt`) ekleyin.

5. **Commit Changes / Değişiklikleri Taahhüt Edin:**  
   - Run: `git add .` then `git commit -m "Added <task_name> with research, script, and tests"` / Çalıştırın: `git add .` ardından `git commit -m "<görev_adı> araştırma, betik ve testlerle eklendi"`

6. **Push to Your Fork / Çatalınıza İtin:**  
   - Run: `git push origin feature/<task_name>` / Çalıştırın: `git push origin feature/<görev_adı>`

7. **Create a Pull Request / Pull Request Oluşturun:**  
   - Go to your fork on GitHub, click "New Pull Request," and submit it to the original repository. / GitHub’daki çatalınıza gidin, "New Pull Request" tıklayın ve orijinal depoya gönderin.  
   - Include a detailed description of your contribution (e.g., "Implemented DNS detection with Nmap and Scapy, added research on 12 methods"). / Katkınızın ayrıntılı bir açıklamasını ekleyin (ör. "Nmap ve Scapy ile DNS tespiti uygulandı, 12 yöntem üzerine araştırma eklendi").

