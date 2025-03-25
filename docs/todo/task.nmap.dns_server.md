
## Task : DNS Server Detection / DNS Sunucusu Tespiti
**Module File / Modül Dosyası:** `modules/dnsserver_detection.py`

### Instruction Set for Amateur Cybersecurity Students / Amatör Siber Güvenlik Öğrencileri İçin Talimat Seti

#### 1. Research Phase / Araştırma Aşaması
- **Objective / Amaç:**  
  Identify all methods to detect DNS servers on a network, which translate domain names (e.g., google.com) to IP addresses (e.g., 8.8.8.8), a critical component for network reconnaissance and security auditing. / Domain adlarını (ör. google.com) IP adreslerine (ör. 8.8.8.8) çeviren DNS sunucularını ağda tespit etmek için tüm yöntemleri belirleyin; bu, ağ keşfi ve güvenlik denetimi için kritik bir bileşendir.

- **Approach / Yaklaşım:**  
  Use a combination of automated scanning tools, manual querying techniques, packet analysis, and custom scripts to locate DNS servers, typically running on UDP/TCP port 53, and determine their software versions or configurations. / DNS sunucularını bulmak için genellikle UDP/TCP port 53’te çalışan otomatik tarama araçları, manuel sorgulama teknikleri, paket analizi ve özel betiklerin bir kombinasyonunu kullanın ve yazılım sürümlerini veya yapılandırmalarını belirleyin.

- **Advanced DeepSearch Prompt / Gelişmiş DeepSearch Komutu:**  
  ```json
  {
    "query": "Investigate all techniques, tools, and methodologies to detect DNS servers on a network comprehensively. Include advanced Nmap scripts (e.g., dns-nsid, dns-service-discovery, dns-recursion), manual querying tools (e.g., dig, nslookup, host), packet analysis techniques (e.g., Wireshark, tcpdump, tshark), and custom scripting approaches (e.g., Python with Scapy or socket). Provide detailed instructions for at least 12 unique methods, including command syntax, expected outputs (e.g., 'BIND 9.16.1'), accuracy considerations, and limitations (e.g., firewalled ports, version hiding, encrypted DNS like DoH). Include real-world examples from penetration testing, network troubleshooting, or forensic analysis contexts, with a focus on both IPv4 and IPv6 environments."
  }
  ```

- **Steps / Adımlar:**  
  1. **Gather Information / Bilgi Toplama:**  
     - **Tool Research / Araç Araştırması:** Study Nmap’s DNS-related scripts, manual tools like `dig` and `nslookup`, and packet capture tools like Wireshark or tcpdump. / Nmap’in DNS ile ilgili betiklerini, `dig` ve `nslookup` gibi manuel araçları ve Wireshark veya tcpdump gibi paket yakalama araçlarını inceleyin.  
     - **Protocol Understanding / Protokol Anlayışı:** Learn DNS protocol basics (e.g., port 53, UDP vs. TCP, query/response structure) using resources like RFC 1035 or online tutorials. / RFC 1035 veya çevrimiçi eğitimler gibi kaynakları kullanarak DNS protokolü temellerini (ör. port 53, UDP vs. TCP, sorgu/yanıt yapısı) öğrenin.  
     - **Community Insights / Topluluk Görüşleri:** Explore forums (e.g., StackExchange, PenTest forums) and GitHub for custom DNS detection scripts or techniques. / Özel DNS tespit betikleri veya teknikleri için forumları (ör. StackExchange, PenTest forumları) ve GitHub’ı keşfedin.  

  2. **Key Methods to Research / Araştırılacak Ana Yöntemler:**  
     - **Nmap DNS Scans / Nmap DNS Taramaları:**  
       - Command: `nmap -sU -p 53 --script dns-nsid,dns-service-discovery <ip_range>` / Komut: `nmap -sU -p 53 --script dns-nsid,dns-service-discovery <ip_aralığı>`  
       - Purpose: Detects DNS servers and extracts version info (e.g., "BIND 9.11"). / DNS sunucularını tespit eder ve sürüm bilgisini çıkarır (ör. "BIND 9.11").  
       - Limitation: UDP scans are slower and may miss firewalled servers. / Sınırlama: UDP taramaları daha yavaştır ve güvenlik duvarlı sunucuları kaçırabilir.  
     - **Manual DNS Queries / Manuel DNS Sorguları:**  
       - Command: `dig @<ip> version.bind chaos txt` / Komut: `dig @<ip> version.bind chaos txt`  
       - Purpose: Requests the DNS server’s software version (if not obscured). / DNS sunucusunun yazılım sürümünü talep eder (gizlenmemişse).  
       - Limitation: Many servers disable version reporting for security. / Sınırlama: Birçok sunucu güvenlik için sürüm bildirimini devre dışı bırakır.  
     - **Packet Analysis / Paket Analizi:**  
       - Wireshark Filter: `udp.port == 53 or tcp.port == 53` / Wireshark Filtresi: `udp.port == 53 or tcp.port == 53`  
       - Purpose: Captures DNS queries/responses to identify active servers. / Aktif sunucuları tanımlamak için DNS sorgularını/yanıtlarını yakalar.  
       - Limitation: Requires access to network traffic and may miss encrypted DNS (e.g., DNS over HTTPS). / Sınırlama: Ağ trafiğine erişim gerektirir ve şifreli DNS’yi (ör. HTTPS üzerinden DNS) kaçırabilir.  
     - **Custom Socket Query / Özel Soket Sorgusu:**  
       - Tool: Python with `socket` library. / Araç: `socket` kütüphanesi ile Python.  
       - Purpose: Sends a raw DNS query to port 53 and checks for a response. / Port 53’e ham bir DNS sorgusu gönderir ve yanıt kontrol eder.  
       - Limitation: Requires low-level networking knowledge. / Sınırlama: Düşük seviye ağ bilgisi gerektirir.  

  3. **Document Findings / Bulguları Belgeleyin:**  
     - Create `research_notes_dns.md` with this structure: / `research_notes_dns.md` dosyasını şu yapıyla oluşturun:  
       - **Nmap Techniques / Nmap Teknikleri:** List commands, sample outputs (e.g., "dns-nsid: BIND 9.16"), and pros/cons. / Komutları, örnek çıktıları (ör. "dns-nsid: BIND 9.16") ve artıları/eksileri listeleyin.  
       - **Manual Methods / Manuel Yöntemler:** Detail `dig`, `nslookup`, and `host` with examples (e.g., `dig @8.8.8.8 google.com`). / `dig`, `nslookup` ve `host`’u örneklerle (ör. `dig @8.8.8.8 google.com`) ayrıntılı olarak tarif edin.  
       - **Packet Analysis / Paket Analizi:** Explain setup (e.g., Wireshark on a mirror port) and filters. / Kurulumu (ör. bir yansıma portunda Wireshark) ve filtreleri açıklayın.  
       - **Challenges / Zorluklar:** Discuss encrypted DNS, firewalled ports, and mitigation ideas (e.g., "Use DNS traffic patterns"). / Şifreli DNS, güvenlik duvarlı portlar ve hafifletme fikirlerini (ör. "DNS trafik modellerini kullan") tartışın.  

#### 2. Implementation Phase / Uygulama Aşaması
- **Objective / Amaç:**  
  Build a Python script to automate DNS server detection across a network range, using Nmap and custom queries, with a report of findings. / Nmap ve özel sorgular kullanarak bir ağ aralığında DNS sunucusu tespitini otomatikleştiren ve bulguların bir raporunu üreten bir Python betiği oluşturun.

- **Steps / Adımlar:**  
  1. **Set Up Environment / Ortamı Kurun:**  
     - Install: `pip install python-nmap scapy` / Kur: `pip install python-nmap scapy`  
     - Ensure Nmap is installed on your system (`sudo apt install nmap` on Linux). / Sisteminizde Nmap’in kurulu olduğundan emin olun (Linux’ta `sudo apt install nmap`).  

  2. **Write the Code / Kodu Yazın:**  
     - Include these functions: / Şu fonksiyonları ekleyin:  
       - `scan_dns(ip_range)`: Scans a range with Nmap for DNS services. / Bir aralığı Nmap ile DNS hizmetleri için tarar.  
       - `query_version(ip)`: Attempts a manual version query using Scapy. / Scapy kullanarak manuel bir sürüm sorgusu dener.  
       - `generate_report(results)`: Saves results to `dns_report.txt`. / Sonuçları `dns_report.txt` dosyasına kaydeder.  
     - Example Code / Örnek Kod:  
       ```python
       import nmap
       from scapy.all import *

       def scan_dns(ip_range):
           nm = nmap.PortScanner()
           nm.scan(ip_range, '53', arguments='-sU --script dns-nsid')
           results = {}
           for host in nm.all_hosts():
               if 'udp' in nm[host] and 53 in nm[host]['udp']:
                   results[host] = nm[host]['udp'][53]['script'].get('dns-nsid', 'DNS detected, no version')
           return results

       def query_version(ip):
           # Simple DNS version query / Basit DNS sürüm sorgusu
           try:
               packet = IP(dst=ip)/UDP(dport=53)/DNS(rd=1, qd=DNSQR(qname="version.bind", qtype="TXT", qclass="CH"))
               response = sr1(packet, timeout=2, verbose=0)
               if response and response.haslayer(DNS):
                   return response[DNS].an.rdata[0].decode()
           except Exception:
               return "Version query failed"
           return "No version response"

       def generate_report(results):
           with open("dns_report.txt", "w") as f:
               f.write("DNS Server Detection Report\n")
               f.write("=" * 25 + "\n")
               for ip, data in results.items():
                   f.write(f"IP: {ip}\nNmap Result: {data['nmap']}\nVersion Query: {data['version']}\n\n")

       # Test the script / Betiği test edin
       ip_range = "192.168.1.1-10"
       scan_results = scan_dns(ip_range)
       final_results = {ip: {"nmap": res, "version": query_version(ip)} for ip, res in scan_results.items()}
       generate_report(final_results)
       for ip, data in final_results.items():
           print(f"IP: {ip}\nNmap: {data['nmap']}\nVersion: {data['version']}\n")
       ```

  3. **Test the Script / Betiği Test Edin:**  
     - Test with a known DNS server (e.g., "8.8.8.8") and a local network range (e.g., "192.168.1.1-255"). / Bilinen bir DNS sunucusu (ör. "8.8.8.8") ve yerel bir ağ aralığı (ör. "192.168.1.1-255") ile test edin.  
     - Verify detection accuracy and version query success against manual checks. / Tespit doğruluğunu ve sürüm sorgusu başarısını manuel kontrollere karşı doğrulayın.  

#### 3. Documentation Phase / Dokümantasyon Aşaması
- **Objective / Amaç:**  
  Deliver clear, detailed documentation to make the script accessible and educational for beginners. / Betiği yeni başlayanlar için erişilebilir ve eğitici hale getirmek için net, ayrıntılı dokümantasyon sunun.

- **Deliverables / Teslim Edilecekler:**  
  - **README.md:**  
    - **Overview / Genel Bakış:** "This script detects DNS servers on a network using Nmap and Scapy, providing a detailed report." / "Bu betik, Nmap ve Scapy kullanarak ağda DNS sunucularını tespit eder ve ayrıntılı bir rapor sağlar."  
    - **Installation / Kurulum:**  
      - "Install: `pip install python-nmap scapy` and `sudo apt install nmap`" / "Kur: `pip install python-nmap scapy` ve `sudo apt install nmap`"  
    - **Usage / Kullanım:**  
      - "Run: `python dnsserver_detection.py <ip_range>` (e.g., `192.168.1.1-255`)" / "Çalıştır: `python dnsserver_detection.py <ip_aralığı>` (ör. `192.168.1.1-255`)"  
      - "Output: See `dns_report.txt`." / "Çıktı: `dns_report.txt` dosyasını görün."  
    - **Limitations / Sınırlamalar:** "May miss servers with blocked ports or encrypted DNS." / "Engellenmiş portlara veya şifreli DNS’ye sahip sunucuları kaçırabilir."  

  - **research_notes_dns.md:**  
    - Comprehensive notes on at least 12 detection methods, with commands, outputs, and challenges (e.g., "Encrypted DNS like DoH requires traffic analysis"). / En az 12 tespit yöntemi hakkında kapsamlı notlar, komutlar, çıktılar ve zorluklar (ör. "DoH gibi şifreli DNS trafik analizi gerektirir") ile birlikte.
