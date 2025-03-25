Below is the final markdown response tailored to your query. It includes a comprehensive guide for amateur security students to scan local networks for admin panels, with code split into manageable pieces for step-by-step implementation, English and Turkish subtitles for all text, testing steps to verify functionality and debug issues, and instructions for contributing to the GitHub repository `https://github.com/QLineTech/Q-Pentest`. This ensures students learn actively rather than copying and pasting the entire script, while maintaining an educational and ethical focus.

---

# Comprehensive Guide: Scanning Local Networks for Admin Panels  
## Kapsamlı Rehber: Yerel Ağları Yönetim Panelleri İçin Tarama  

This guide teaches amateur security students how to create a Python script to scan a local network, detect admin panels, identify ISPs, and test for default passwords—all while learning networking and security basics ethically. The code is split into small pieces for students to implement step-by-step, encouraging understanding over blind execution.  
Bu rehber, amatör güvenlik öğrencilerine bir Python betiği ile yerel bir ağı taramayı, yönetim panellerini tespit etmeyi, ISS'leri tanımlamayı ve varsayılan şifreleri test etmeyi öğretir—tüm bunları ağ ve güvenlik temellerini etik bir şekilde öğrenirken yapar. Kod, öğrencilerin adım adım uygulayarak anlamalarını teşvik etmek için küçük parçalara ayrılmıştır.

---

## Roadmap Overview  
## Yol Haritası Genel Bakış  

| Step / Adım                | Objective / Amaç                            | Key Learning / Temel Öğrenim                     |  
|----------------------------|---------------------------------------------|-------------------------------------------------|  
| 1. Learn Basics / Temelleri Öğren | Grasp networking fundamentals / Ağ temellerini kavra | IP addresses, subnets, ethics / IP adresleri, alt ağlar, etik |  
| 2. Obtain Permission / İzin Al | Ensure legal/ethical scanning / Yasal ve etik tarama sağla | Consent and responsibility / Onay ve sorumluluk |  
| 3. Scan Network / Ağı Tara | Find live devices / Canlı cihazları bul | Network scanning with `nmap` / `nmap` ile ağ tarama |  
| 4. Detect Panels / Panelleri Tespit Et | Locate admin interfaces / Yönetim arayüzlerini bul | HTTP requests, URL testing / HTTP istekleri, URL testi |  
| 5. Identify ISPs / ISS'leri Tanımla | Determine ISP from panel content / Panel içeriğinden ISS belirle | Web scraping, pattern matching / Web kazıma, desen eşleştirme |  
| 6. Test Passwords / Şifreleri Test Et | Check for default credentials / Varsayılan kimlik bilgilerini kontrol et | Authentication, security risks / Kimlik doğrulama, güvenlik riskleri |  
| 7. Report Findings / Bulguları Raporla | Summarize and save results / Sonuçları özetle ve kaydet | Reporting, file handling / Raporlama, dosya işleme |

---

## Step-by-Step Implementation  
## Adım Adım Uygulama  

To help students learn effectively, the code is split into small, manageable pieces. Each step includes a code snippet, usage details, and examples in both English and Turkish. Implement each part one by one to understand the process fully.  
Öğrencilerin etkili bir şekilde öğrenmelerine yardımcı olmak için kod, küçük ve yönetilebilir parçalara ayrılmıştır. Her adım, İngilizce ve Türkçe olarak kod parçacığı, kullanım detayları ve örnekler içerir. Süreci tam olarak anlamak için her parçayı tek tek uygulayın.

### Step 1: Learn Network Basics  
### Adım 1: Ağ Temellerini Öğrenin  
- **What / Ne**: Understand IP addresses (e.g., 192.168.1.1), subnets (e.g., /24 means 256 IPs), and why scanning requires caution.  
  IP adreslerini (ör. 192.168.1.1), alt ağları (ör. /24, 256 IP anlamına gelir) ve taramanın neden dikkat gerektirdiğini anlayın.  
- **Why / Neden**: Foundation for all network tasks.  
  Tüm ağ görevleri için temel.  
- **Resource / Kaynak**: [Networking Basics / Ağ Temelleri](https://www.cisco.com/c/en/us/solutions/enterprise-networks/what-is-a-computer-network.html)  

### Step 2: Obtain Permission  
### Adım 2: İzin Alın  
- **What / Ne**: Ensure the network you scan belongs to you or you have explicit permission to test it.  
  Tarama yaptığınız ağın size ait olduğundan veya test etmek için açıkça izin aldığınızdan emin olun.  
- **Why / Neden**: Unauthorized scanning is illegal in many jurisdictions (e.g., U.S. Computer Fraud and Abuse Act).  
  Yetkisiz tarama birçok yargı alanında yasa dışıdır (ör. ABD Bilgisayar Dolandırıcılığı ve Kötüye Kullanım Yasası).  
- **How / Nasıl**: This script assumes user permission—add a disclaimer if distributing.  
  Bu betik, kullanıcının iznini varsayar—dağıtıyorsanız bir uyarı ekleyin.  

### Step 3: Scan the Local Network  
### Adım 3: Yerel Ağı Tara  
- **Code / Kod**:  
  ```python  
  import nmap  

  def scan_network():  
      nm = nmap.PortScanner()  
      network = "192.168.1.0/24"  # Common local subnet / Ortak yerel alt ağ  
      nm.scan(hosts=network, arguments="-p 80,443 --open")  # Scan for HTTP/HTTPS / HTTP/HTTPS için tarama  
      hosts = []  
      for host in nm.all_hosts():  
          if nm[host].state() == "up":  
              ports = [p for p in nm[host]["tcp"] if nm[host]["tcp"][p]["state"] == "open"]  
              if ports:  
                  hosts.append({"ip": host, "ports": ports})  
      return hosts  
  ```  
- **Usage / Kullanım**: Finds devices with open HTTP/HTTPS ports.  
  HTTP/HTTPS portları açık olan cihazları bulur.  
- **Example / Örnek**: Detects a router at 192.168.1.1 with port 80 open.  
  80 portu açık olan 192.168.1.1 adresindeki bir yönlendiriciyi tespit eder.  

### Step 4: Detect Admin Panels  
### Adım 4: Yönetim Panellerini Tespit Et  
- **Code / Kod**:  
  ```python  
  import requests  

  def detect_admin_panel(ip, ports):  
      urls = [f"http://{ip}/{path}" for path in ["", "admin", "login", "setup"]]  
      if 443 in ports:  
          urls += [url.replace("http://", "https://") for url in urls]  
      for url in urls:  
          try:  
              response = requests.get(url, timeout=5, allow_redirects=True)  
              if response.status_code == 200:  
                  return {"url": url, "content": response.text}  
          except requests.RequestException:  
              continue  
      return None  
  ```  
- **Usage / Kullanım**: Tests common admin URLs.  
  Ortak yönetim URL'lerini test eder.  
- **Example / Örnek**: Finds `http://192.168.1.1/admin` as a valid panel.  
  `http://192.168.1.1/admin` adresini geçerli bir panel olarak bulur.  

### Step 5: Identify Routers and ISPs  
### Adım 5: Yönlendiricileri ve ISS'leri Tanımla  
- **Code / Kod**:  
  ```python  
  from bs4 import BeautifulSoup  

  def identify_isp(content):  
      soup = BeautifulSoup(content, "html.parser")  
      text = soup.get_text().lower()  
      isp_clues = {  
          "verizon": ["verizon", "fios"],  
          "comcast": ["xfinity", "comcast"],  
          "at&t": ["att", "u-verse"]  
      }  
      for isp, keywords in isp_clues.items():  
          if any(keyword in text for keyword in keywords):  
              return isp  
      return "Unknown"  
  ```  
- **Usage / Kullanım**: Scrapes panel content for ISP clues.  
  Panel içeriğini ISS ipuçları için kazır.  
- **Example / Örnek**: Detects "Comcast" from "Welcome to Xfinity" text.  
  "Welcome to Xfinity" metninden "Comcast"ı tespit eder.  

### Step 6: Test Default Passwords  
### Adım 6: Varsayılan Şifreleri Test Et  
- **Code / Kod**:  
  ```python  
  import requests  
  import time  

  def test_default_passwords(url):  
      credentials = [  
          {"username": "admin", "password": "admin"},  
          {"username": "admin", "password": "password"},  
          {"username": "user", "password": "user"}  
      ]  
      session = requests.Session()  
      for cred in credentials:  
          try:  
              response = session.post(url, data=cred, timeout=5)  
              if response.status_code == 200 and "login" not in response.url.lower():  
                  return f"Default found / Varsayılan bulundu: {cred['username']}:{cred['password']}"  
              time.sleep(1)  # Prevent lockouts / Kilitlenmeleri önlemek için  
          except requests.RequestException:  
              continue  
      return "No default credentials found / Varsayılan kimlik bilgileri bulunamadı"  
  ```  
- **Usage / Kullanım**: Tests common default logins.  
  Ortak varsayılan girişleri test eder.  
- **Example / Örnek**: Finds "admin:admin" works.  
  "admin:admin" kombinasyonunun çalıştığını bulur.  

### Step 7: Report Findings  
### Adım 7: Bulguları Raporla  
- **Code / Kod**:  
  ```python  
  import json  

  def report_findings(results):  
      with open("scan_report.json", "w") as f:  
          json.dump(results, f, indent=4)  
      print("Scan complete. Results saved to scan_report.json / Tarama tamamlandı. Sonuçlar scan_report.json dosyasına kaydedildi.")  
  ```  
- **Usage / Kullanım**: Saves results as JSON.  
  Sonuçları JSON olarak kaydeder.  
- **Example Output / Örnek Çıktı**:  
  ```json  
  [{"ip": "192.168.1.1", "url": "http://192.168.1.1/admin", "isp": "comcast", "password_status": "Default found / Varsayılan bulundu: admin:admin"}]  
  ```  

### Putting It Together  
### Hepsini Birleştirme  
After implementing each function, combine them in a `main()` function:  
Her fonksiyonu uyguladıktan sonra, bir `main()` fonksiyonunda birleştirin:  
- **Code / Kod**:  
  ```python  
  def main():  
      results = []  
      hosts = scan_network()  
      for host in hosts:  
          panel = detect_admin_panel(host["ip"], host["ports"])  
          if panel:  
              isp = identify_isp(panel["content"])  
              password_status = test_default_passwords(panel["url"])  
              results.append({  
                  "ip": host["ip"],  
                  "url": panel["url"],  
                  "isp": isp,  
                  "password_status": password_status  
              })  
      report_findings(results)  

  if __name__ == "__main__":  
      main()  
  ```  
- **Usage / Kullanım**: Runs the full scan and saves results.  
  Tam taramayı çalıştırır ve sonuçları kaydeder.  

---

## Testing Steps  
## Test Adımları  

Test your code to ensure it works and fix bugs if they arise. Follow these steps:  
Kodunuzu test ederek çalıştığından emin olun ve varsa hataları düzeltin. Şu adımları izleyin:  

1. **Install Requirements / Gereksinimleri Yükleyin**:  
   ```bash  
   pip install python-nmap requests beautifulsoup4  
   ```  
   Install necessary libraries / Gerekli kütüphaneleri yükleyin.  

2. **Run the Script / Betiği Çalıştırın**:  
   - Save each function in a file (e.g., `router_admin_panel.py`) and run:  
     Her fonksiyonu bir dosyaya (ör. `router_admin_panel.py`) kaydedin ve çalıştırın:  
     ```bash  
     python router_admin_panel.py  
     ```  

3. **Check Results / Sonuçları Kontrol Edin**:  
   - Open `scan_report.json` and verify the format matches expectations.  
     `scan_report.json` dosyasını açın ve formatın beklentilere uyduğunu doğrulayın.  
   - Debug by running each function individually if errors occur.  
     Hatalar olursa her fonksiyonu tek tek çalıştırarak hata ayıklayın.  

4. **Fix Bugs / Hataları Düzeltin**:  
   - **Bug / Hata**: `nmap` scan finds no devices / `nmap` taraması cihaz bulamıyor.  
     - **Fix / Çözüm**: Check your network subnet and update the `network` variable (e.g., "192.168.0.0/24").  
       Ağınızın alt ağını kontrol edin ve `network` değişkenini güncelleyin (ör. "192.168.0.0/24").  
   - **Bug / Hata**: `requests` connection error / `requests` bağlantı hatası.  
     - **Fix / Çözüm**: Ensure the device is reachable and verify URLs.  
       Cihazın erişilebilir olduğundan emin olun ve URL'leri kontrol edin.  

---

## Contributing to GitHub  
## GitHub'a Katkı Sağlama  

Add your script to the `QLineTech/Q-Pentest` repository:  
Betiğinizi `QLineTech/Q-Pentest` deposuna ekleyin:  

1. **Fork the Repo / Depoyu Çatallayın**:  
   - Visit [https://github.com/QLineTech/Q-Pentest](https://github.com/QLineTech/Q-Pentest) and click "Fork".  
     [https://github.com/QLineTech/Q-Pentest](https://github.com/QLineTech/Q-Pentest) adresine gidin ve "Fork" tıklayın.  

2. **Add the Script / Betiği Ekleyin**:  
   - Clone your fork, then add `router_admin_panel.py` to the `modules` folder:  
     Çatalınızı klonlayın, ardından `router_admin_panel.py` dosyasını `modules` klasörüne ekleyin:  
     ```bash  
     git clone <your-fork-url>  
     cd Q-Pentest  
     mv router_admin_panel.py modules/  
     ```  

3. **Commit Changes / Değişiklikleri Taahhüt Edin**:  
   ```bash  
   git add modules/router_admin_panel.py  
   git commit -m "Add router admin panel scanner / Yönlendirici yönetim paneli tarayıcısı ekle"  
   ```  

4. **Submit a Pull Request / Pull Request Gönderin**:  
   - Push to your fork and create a pull request to the original repo.  
     Çatalınıza itin ve orijinal depoya bir pull request oluşturun:  
     ```bash  
     git push origin main  
     ```  
   - Go to your fork on GitHub and click "Pull Request".  
     GitHub'daki çatalınıza gidin ve "Pull Request" tıklayın.  

---

## Ethical Notes  
## Etik Notlar  
- **Permission / İzin**: Only scan networks you own or have explicit permission to test.  
  Yalnızca size ait olan veya açıkça izin aldığınız ağları tarayın.  
- **Security / Güvenlik**: Limit password attempts to avoid locking out users.  
  Şifre denemelerini sınırlayın ve kullanıcıları kilitlemeyin.  
- **Responsibility / Sorumluluk**: Report vulnerabilities to network owners and suggest fixes.  
  Ağ sahiplerine güvenlik açıklarını bildirin ve düzeltmeler önerin.  

---

## References  
## Referanslar  
- [Nmap Documentation / Nmap Belgeleri](https://nmap.org/book/man.html)  
- [Requests Library / Requests Kütüphanesi](https://docs.python-requests.org/en/master/)  
- [BeautifulSoup Documentation / BeautifulSoup Belgeleri](https://www.crummy.com/software/BeautifulSoup/bs4/doc/)  
- [OWASP Web Security Testing Guide / OWASP Web Güvenlik Test Rehberi](https://owasp.org/www-project-web-security-testing-guide/)  
