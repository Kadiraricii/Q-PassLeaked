# Penetration Testing Modules Roadmap

This roadmap outlines the development of Python modules under `<root>/modules/*.py` to implement functions utilizing the features of cross-platform penetration testing packages. Each module will focus on a specific package, enabling comprehensive pentesting capabilities for 2025 technologies (websites, WiFi, Bluetooth, Android/iOS apps, routers, monitoring, MITM, etc.).

## Development Tasks

| **Package**           | **Functionality**                                                                 | **Usage**                                                                                       | **TR (Technical Requirement)**                     |
|-----------------------|-----------------------------------------------------------------------------------|-------------------------------------------------------------------------------------------------|----------------------------------------------------|
| **python-nmap**       | Run Nmap scans and parse results                                                 | Execute Nmap scans (e.g., `nmap.scan('host', 'ports')`)                                        | Requires Nmap installed                            |
| *Türkçe: Nmap Çalıştırma ve Sonuç Analizi* | **TODO**: `<root>/modules/nmap_module.py` - Implement scan execution, port enumeration, and result parsing (XML/JSON) | | |
| **dnspython**         | DNS lookups and queries                                                          | Query DNS records (e.g., `dns.resolver.resolve('example.com', 'A')`)                           | Pure Python, no external tools needed              |
| *Türkçe: DNS Sorguları* | **TODO**: `<root>/modules/dns_module.py` - Create functions for A, MX, NS lookups and DNS enumeration | | |
| **python-whois**      | WHOIS lookups for domain information                                             | Get domain details (e.g., `whois.whois('example.com')`)                                        | Pure Python, no external tools needed              |
| *Türkçe: WHOIS Sorguları* | **TODO**: `<root>/modules/whois_module.py` - Build WHOIS query and domain info extraction functions | | |
| **Scapy**             | Packet manipulation (ARP, DNS, WiFi, MITM)                                       | Craft/send packets (e.g., `send(ARP(op=2, pdst='target_ip'))`)                                 | Admin/root privileges; WiFi limited on Windows     |
| *Türkçe: Paket Manipülasyonu* | **TODO**: `<root>/modules/scapy_module.py` - Develop ARP spoofing, DNS poisoning, WiFi deauth, and packet sniffing | | |
| **sqlmap**            | Automated SQL injection and database takeover                                    | Run SQL injection (e.g., `os.system('sqlmap -u url')`)                                         | Python-based, requires sqlmap installed            |
| *Türkçe: SQL Enjeksiyonu* | **TODO**: `<root>/modules/sqlmap_module.py` - Integrate SQLmap API for automated injection and DB enumeration | | |
| **mitmproxy**         | HTTP/HTTPS traffic interception and manipulation                                 | Intercept web traffic (e.g., `mitmproxy` with Python script)                                   | Python 3.8+, works out-of-the-box                  |
| *Türkçe: HTTP/HTTPS Trafik Yakalama* | **TODO**: `<root>/modules/mitmproxy_module.py` - Create MITM scripts for traffic interception and modification | | |
| **PyBluez**           | Bluetooth device discovery and attacks                                           | Discover devices (e.g., `bluetooth.discover_devices()`)                                        | Requires Bluetooth support on OS                   |
| *Türkçe: Bluetooth Keşif ve Saldırı* | **TODO**: `<root>/modules/bluetooth_module.py` - Implement device discovery, pairing attacks, and data extraction | | |
| **Requests**          | HTTP requests for web exploitation                                               | Send HTTP requests (e.g., `requests.post('url', data=payload)`)                                | Pure Python, ideal for web pentesting              |
| *Türkçe: HTTP İstekleri* | **TODO**: `<root>/modules/requests_module.py` - Build functions for GET/POST, session handling, and payload injection | | |
| **Netifaces**         | Network interface enumeration                                                    | List network interfaces (e.g., `netifaces.interfaces()`)                                       | Pure Python, simpler than Impacket                 |
| *Türkçe: Ağ Arayüzü Sayımı* | **TODO**: `<root>/modules/netifaces_module.py` - Enumerate interfaces and retrieve IP/MAC details | | |
| **AsyncSSH**          | SSH client/server for remote access                                              | SSH connect (e.g., `await asyncssh.connect('host', username='user')`)                          | Python 3.6+, async support, pure Python            |
| *Türkçe: SSH İstemci/Sunucu* | **TODO**: `<root>/modules/ssh_module.py` - Develop async SSH connection, command execution, and tunneling | | |
| **Cryptography**      | Encryption/decryption and cryptographic operations                               | Encrypt data (e.g., `fernet.Fernet(key).encrypt(data)`)                                        | Pure Python, modern and widely adopted             |
| *Türkçe: Şifreleme/Çözme* | **TODO**: `<root>/modules/crypto_module.py` - Implement AES, RSA, and hash functions for data security | | |
| **Ropper**            | ROP chain generation for binary exploitation                                     | Find gadgets (e.g., `ropper --file binary --search "pop rax"`)                                 | Python-based, requires binary analysis tools       |
| *Türkçe: ROP Zincir Oluşturma* | **TODO**: `<root>/modules/ropper_module.py` - Create ROP chain generator and exploit builder | | |
| **Aiohttp**           | Async network clients/servers for web pentesting                                 | Async HTTP client (e.g., `await aiohttp.ClientSession().get('url')`)                           | Python 3.5+, lightweight and fast                  |
| *Türkçe: Asenkron Ağ İstemcileri* | **TODO**: `<root>/modules/aiohttp_module.py` - Build async HTTP clients for web scraping and attacks | | |
| **Pcap-ct**           | Packet parsing for network analysis                                              | Parse PCAP files (e.g., `Pcap('file.pcap').packets`)                                           | Pure Python, no Tshark dependency                  |
| *Türkçe: Paket Analizi* | **TODO**: `<root>/modules/pcap_module.py` - Develop PCAP parsing and traffic analysis functions | | |
| **Frida**             | Dynamic instrumentation for Android/iOS apps                                     | Hook app functions (e.g., `frida.attach('process').script.load('script.js')`)                  | Requires Frida server on target device             |
| *Türkçe: Dinamik Enstrümantasyon* | **TODO**: `<root>/modules/frida_module.py` - Implement app hooking, memory inspection, and runtime manipulation | | |
| **Kivy**              | Build pentesting GUIs for cross-platform apps                                    | Create GUI (e.g., `App().run()` with pentest tools)                                            | Pure Python, supports desktop/mobile               |
| *Türkçe: GUI Geliştirme* | **TODO**: `<root>/modules/kivy_module.py` - Design GUI for integrating pentesting tools | | |
| **PySharkbite**       | Router firmware analysis and exploitation                                        | Analyze firmware (e.g., custom scripts for packet injection)                                   | Python-based, may need router-specific tools       |
| *Türkçe: Yönlendirici Yazılım Analizi* | **TODO**: `<root>/modules/router_module.py` - Build firmware extraction and exploit functions | | |
| **PyNetfilter**       | Network monitoring and filtering                                                 | Monitor traffic (e.g., hook netfilter queues)                                                  | Requires Linux kernel support, partial on others   |
| *Türkçe: Ağ İzleme* | **TODO**: `<root>/modules/netfilter_module.py` - Implement traffic monitoring and filtering | | |
| **Bettercap (Python API)** | MITM, WiFi, Bluetooth, and network attacks                                  | Run via Python API (e.g., `bettercap.run('wifi.recon on')`)                                    | Requires Bettercap installed, cross-platform       |
| *Türkçe: MITM ve Ağ Saldırıları* | **TODO**: `<root>/modules/bettercap_module.py` - Integrate Bettercap API for WiFi/BT/network attacks | | |
| **Objection**         | Mobile app pentesting (Android/iOS)                                              | Inject runtime hooks (e.g., `objection -g com.app explore`)                                    | Requires Frida, cross-platform with setup          |
| *Türkçe: Mobil Uygulama Testi* | **TODO**: `<root>/modules/objection_module.py` - Develop mobile app hooking and security testing | | |
| **PyWiFi**            | WiFi network management and attacks                                              | Scan/control WiFi (e.g., `pywifi.PyWiFi().scan()`)                                             | Limited on Windows, better on Linux/macOS          |
| *Türkçe: WiFi Yönetimi ve Saldırı* | **TODO**: `<root>/modules/wifi_module.py` - Create WiFi scanning, connection, and attack functions | | |

## Development Plan

1. **Setup Environment**
   - Install Python 3.9+ and required dependencies (`pip install -r requirements.txt`).
   - Ensure external tools (Nmap, sqlmap, Bettercap, Frida) are installed where needed.

2. **Module Structure**
   - Each module in `<root>/modules/*.py` should:
     - Import the respective package.
     - Define functions for key features (e.g., scan, query, attack).
     - Include error handling and logging.
     - Provide a simple CLI interface for testing.

3. **Implementation Phases**
   - **Phase 1**: Core network tools (`nmap_module.py`, `dns_module.py`, `whois_module.py`, `scapy_module.py`).
   - **Phase 2**: Web and database tools (`requests_module.py`, `sqlmap_module.py`, `mitmproxy_module.py`, `aiohttp_module.py`).
   - **Phase 3**: Wireless and mobile tools (`bluetooth_module.py`, `wifi_module.py`, `frida_module.py`, `objection_module.py`).
   - **Phase 4**: Advanced features (`crypto_module.py`, `ropper_module.py`, `bettercap_module.py`, `router_module.py`).
   - **Phase 5**: GUI and monitoring (`kivy_module.py`, `netfilter_module.py`, `pcap_module.py`).

4. **Testing**
   - Test each module on Windows, macOS, and Linux.
   - Validate against 2025 tech (e.g., WPA3 WiFi, modern web apps, Android 15/iOS 18).

5. **Documentation**
   - Add docstrings and README for each module.
   - Include usage examples and TR notes.

## Notes
- **Cross-Platform**: Ensure compatibility across Windows, macOS, and Linux, noting limitations (e.g., WiFi on Windows).
- **Ethical Use**: Obtain authorization before testing networks/devices.
- **Future-Proofing**: Focus on modern protocols (HTTP/3, BLE, IoT) and emerging attack surfaces.

Start with `<root>/modules/nmap_module.py` and proceed sequentially. Good luck!


---

after finishing ux with Kivy also I will implement alternative WEB Panel UX 
which user can choose.

also we need to support cli-based usage for opertating systems without GUI support, like UBUNTU-SERVER, VPS, ...