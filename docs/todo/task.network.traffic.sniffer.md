### Task : Network Traffic Sniffer and Analyzer / Ağ Trafiği Koklayıcı ve Analizörü
**Assigned Role / Atanan Rol:** Seage / Bilge  
**Module File / Modül Dosyası:** `modules/network_traffic_analyzer.py`

#### Expanded Instruction Set for Amateur Cybersecurity Students / Amatör Siber Güvenlik Öğrencileri İçin Genişletilmiş Talimat Seti

##### **1. Research / Araştırma**
**English:** As Seage, your task is to gather resources to create a tool that sniffs and analyzes network traffic for security insights.  
**Turkish:** Bilge olarak göreviniz, ağ trafiğini koklayarak ve analiz ederek güvenlik içgörüleri sağlayan bir araç oluşturmak için kaynakları toplamaktır.  
- **Action / Eylem:**  
  **English:** Use a search tool to find resources on network sniffing and analysis. Examples include:  
  - Libraries (e.g., Scapy, Pyshark).  
  - Documentation (e.g., Wireshark guides, Scapy tutorials).  
  - Community resources (e.g., Stack Overflow, GitHub repositories).  
  **Turkish:** Ağ koklama ve analizi için kaynakları bulmak üzere bir arama aracı kullanın. Örnekler:  
  - Kütüphaneler (ör. Scapy, Pyshark).  
  - Dokümantasyon (ör. Wireshark kılavuzları, Scapy öğreticileri).  
  - Topluluk kaynakları (ör. Stack Overflow, GitHub depoları).  
- **Documentation / Dokümantasyon:** For each resource, record:  
  **English:**  
  - **Name and Type**: (e.g., "Scapy - Python Library").  
  - **Access Method**: (e.g., "Install via pip," "Clone from GitHub").  
  - **Coverage**: (e.g., "Packet sniffing, protocol analysis").  
  - **Usage Instructions**: (e.g., "Requires root privileges for sniffing").  
  **Turkish:**  
  - **İsim ve Tür**: (ör. "Scapy - Python Kütüphanesi").  
  - **Erişim Yöntemi**: (ör. "Pip ile kurulum," "GitHub’dan klonlama").  
  - **Kapsam**: (ör. "Paket koklama, protokol analizi").  
  - **Kullanım Talimatları**: (ör. "Koklama için root yetkileri gerektirir").  
- **Additional Scope / Ek Kapsam:**  
  **English:** Look for existing network traffic analysis scripts or tools to reference.  
  **Turkish:** Referans alınabilecek mevcut ağ trafiği analiz betikleri veya araçları arayın.  
- **Output / Çıktı:**  
  **English:** Create a markdown file (`research_notes.md`) with sections: **Network Sniffing Resources**, **Tools and Scripts**. Compile data into a JSON file (`research_data.json`) with: `sniffing_resources`, `tools_and_scripts`.  
  **Turkish:** Bir markdown dosyası (`research_notes.md`) oluşturun ve şu bölümleri ekleyin: **Ağ Koklama Kaynakları**, **Araçlar ve Betikler**. Verileri bir JSON dosyasına (`research_data.json`) derleyin: `sniffing_resources`, `tools_and_scripts`.  

**Example Search Prompt / Örnek Arama Komutu:**  
**English:**  
```
Find resources for sniffing and analyzing network traffic. Include Python libraries, documentation, and community resources. For each, note the name, type, access method, coverage, and usage instructions. Also, identify existing tools or scripts for network traffic analysis. Compile into a JSON file.
```  
**Turkish:**  
```
Ağ trafiğini koklama ve analiz için kaynakları bulun. Python kütüphaneleri, dokümantasyon ve topluluk kaynaklarını ekleyin. Her biri için isim, tür, erişim yöntemi, kapsam ve kullanım talimatlarını not edin. Ayrıca, ağ trafiği analizi için mevcut araçları veya betikleri belirleyin. Bir JSON dosyasına derleyin.
```

---

##### **2. Understand / Anlama**
**English:**  
- Study the resources to understand network traffic sniffing and analysis. Focus on:  
  - **Packet Structure**: How packets are formatted (headers, payloads).  
  - **Protocols**: Common ones to analyze (e.g., TCP, UDP, HTTP).  
  - **Security Implications**: Detecting anomalies (e.g., unusual traffic volume).  
  - **Legal Considerations**: Ethical use of sniffing tools.  
**Turkish:**  
- Kaynakları inceleyerek ağ trafiği koklama ve analizini kavrayın. Şunlara odaklanın:  
  - **Paket Yapısı**: Paketlerin nasıl biçimlendirildiği (başlıklar, yükler).  
  - **Protokoller**: Analiz edilecek yaygın protokoller (ör. TCP, UDP, HTTP).  
  - **Güvenlik Etkileri**: Anormallikleri tespit etme (ör. olağandışı trafik hacmi).  
  - **Yasal Hususlar**: Koklama araçlarının etik kullanımı.  
- **Reflection / Yansıma:**  
  **English:** Consider why monitoring traffic is vital: Identifying threats, troubleshooting, and ensuring network health.  
  **Turkish:** Trafik izlemenin neden önemli olduğunu düşünün: Tehditleri belirleme, sorun giderme ve ağ sağlığını koruma.  
- **Output / Çıktı:**  
  **English:** Write a 200-250 word summary in `research_notes.md` under "Understanding Network Traffic Analysis / Ağ Trafiği Analizini Anlama." Include insights on packet sniffing and its cybersecurity role.  
  **Turkish:** `research_notes.md` dosyasına "Ağ Trafiği Analizini Anlama" başlığı altında 200-250 kelimelik bir özet yazın. Paket koklama ve siber güvenlikteki rolü hakkında içgörüler ekleyin.  

---

##### **3. Plan / Planlama**
**English:**  
- Outline the script’s structure: Functions needed (e.g., start sniffing, parse packets, analyze traffic), inputs (interface name), outputs (traffic summary, alerts), error scenarios (e.g., no permissions, invalid interface).  
**Turkish:**  
- Betiğin yapısını planlayın: Gerekli fonksiyonlar (ör. koklamayı başlatma, paketleri ayrıştırma, trafiği analiz etme), girdiler (arayüz adı), çıktılar (trafik özeti, uyarılar), hata senaryoları (ör. izin yok, geçersiz arayüz).  
- **Output / Çıktı:**  
  **English:** Add a "Design Plan / Tasarım Planı" section to `research_notes.md` with a function list and purposes, plus pseudocode (e.g., "Start sniffing → Capture packets → Parse headers → Flag anomalies").  
  **Turkish:** `research_notes.md` dosyasına "Tasarım Planı" bölümü ekleyin; fonksiyon listesi ve amaçları ile sahte kod (ör. "Koklamayı başlat → Paketleri yakala → Başlıkları ayrıştır → Anormallikleri işaretle") ekleyin.  

---

##### **4. Implement / Uygulama**
**English:** Build `network_traffic_analyzer.py` in the `modules` directory.  
**Turkish:** `modules` dizininde `network_traffic_analyzer.py` dosyasını oluşturun.  

**Step-by-Step Implementation / Adım Adım Uygulama:**  
- **Step 1: Start Sniffing Function / Adım 1: Koklamayı Başlatma Fonksiyonu**  
  **English:** Create `start_sniffing(interface)` to capture packets.  
  **Turkish:** Paketleri yakalamak için `start_sniffing(interface)` fonksiyonunu oluşturun.  
  ```python  
  from scapy.all import sniff  

  def start_sniffing(interface):  
      packets = sniff(iface=interface, count=100)  # Capture 100 packets  
      return packets  
  ```  

- **Step 2: Parse Packets Function / Adım 2: Paketleri Ayrıştırma Fonksiyonu**  
  **English:** Create `parse_packets(packets)` to extract key info.  
  **Turkish:** Önemli bilgileri çıkarmak için `parse_packets(packets)` fonksiyonunu oluşturun.  
  ```python  
  def parse_packets(packets):  
      parsed_data = []  
      for pkt in packets:  
          if pkt.haslayer('IP'):  
              data = {  
                  "src": pkt['IP'].src,  
                  "dst": pkt['IP'].dst,  
                  "proto": pkt['IP'].proto  
              }  
              parsed_data.append(data)  
      return parsed_data  
  ```  

- **Step 3: Analyze Traffic Function / Adım 3: Trafiği Analiz Etme Fonksiyonu**  
  **English:** Create `analyze_traffic(parsed_data)` to detect anomalies.  
  **Turkish:** Anormallikleri tespit etmek için `analyze_traffic(parsed_data)` fonksiyonunu oluşturun.  
  ```python  
  def analyze_traffic(parsed_data):  
      src_count = {}  
      for data in parsed_data:  
          src_count[data["src"]] = src_count.get(data["src"], 0) + 1  
      anomalies = [src for src, count in src_count.items() if count > 50]  # Threshold: 50  
      return {"total_packets": len(parsed_data), "anomalies": anomalies}  
  ```  

- **Step 4: Error Handling / Adım 4: Hata İşleme**  
  **English:** Add try-except to `start_sniffing` for permission errors.  
  **Turkish:** İzin hataları için `start_sniffing` fonksiyonuna try-except ekleyin.  
  ```python  
  def start_sniffing(interface):  
      try:  
          packets = sniff(iface=interface, count=100)  
          return packets  
      except PermissionError:  
          raise Exception("Root privileges required for sniffing.")  
      except Exception as e:  
          raise Exception(f"Error sniffing traffic: {str(e)}")  
  ```  

- **Step 5: Reporting Function / Adım 5: Raporlama Fonksiyonu**  
  **English:** Create `report_traffic(analysis)` for markdown logs.  
  **Turkish:** Markdown günlükleri için `report_traffic(analysis)` fonksiyonunu oluşturun.  
  ```python  
  import time  

  def report_traffic(analysis):  
      timestamp = time.strftime("%Y-%m-%d %H:%M:%S")  
      return f"### Traffic Analysis / Trafik Analizi\n- **Zaman / Time:** {timestamp}\n- **Toplam Paket / Total Packets:** {analysis['total_packets']}\n- **Anormallikler / Anomalies:** {analysis['anomalies']}\n"  
  ```  

- **Step 6: Main Function / Adım 6: Ana Fonksiyon**  
  **English:** Create `main(interface)` to integrate all steps.  
  **Turkish:** Tüm adımları entegre etmek için `main(interface)` fonksiyonunu oluşturun.  
  ```python  
  def main(interface):  
      packets = start_sniffing(interface)  
      parsed_data = parse_packets(packets)  
      analysis = analyze_traffic(parsed_data)  
      return report_traffic(analysis)  
  ```  

---

##### **5. Test / Test Etme**
**English:**  
- Test your script with:  
  - **Normal Traffic**: Sniff on a valid interface (e.g., "eth0").  
  - **High Traffic**: Generate traffic (e.g., using `ping`) to trigger anomalies.  
  - **Edge Cases**: Invalid interface, no root privileges.  
**Turkish:**  
- Betiğinizi şu şekilde test edin:  
  - **Normal Trafik**: Geçerli bir arayüzde koklama yapın (ör. "eth0").  
  - **Yüksek Trafik**: Anormallikleri tetiklemek için trafik oluşturun (ör. `ping` kullanarak).  
  - **Kenar Durumlar**: Geçersiz arayüz, root yetkisi yok.  
- **Output / Çıktı:**  
  **English:** Log in `test_results.md`: **Input** (interface), **Expected Result**, **Actual Result**, **Observations**.  
  **Turkish:** `test_results.md` dosyasına kaydedin: **Giriş** (arayüz), **Beklenen Sonuç**, **Gerçek Sonuç**, **Gözlemler**.  

---

##### **6. Confirm / Doğrulama**
**English:**  
- Validate by comparing results with a tool like Wireshark.  
**Turkish:**  
- Sonuçları Wireshark gibi bir araçla karşılaştırarak doğrulayın.  
- **Output / Çıktı:**  
  **English:** Add a "Confirmation / Doğrulama" section to `test_results.md` with cross-check findings and accuracy summary.  
  **Turkish:** `test_results.md` dosyasına "Doğrulama" bölümü ekleyin; çapraz kontrol bulguları ve doğruluk özeti ile.  

---

##### **7. Contribute / Katkı Sağlama**
**English:**  
- Submit to `https://github.com/QLineTech/Q-Pentest`: Fork the repo, branch (`feature/network-traffic-analyzer`), commit `network_traffic_analyzer.py`, `research_notes.md`, `test_results.md`, `research_data.json`, submit pull request with a detailed description.  
**Turkish:**  
- `https://github.com/QLineTech/Q-Pentest` adresine gönderin: Depoyu çatallayın, dal oluşturun (`feature/network-traffic-analyzer`), `network_traffic_analyzer.py`, `research_notes.md`, `test_results.md`, `research_data.json` dosyalarını taahhüt edin, detaylı bir açıklama ile pull request gönderin.  

---

#### Roadmap / Yol Haritası
**English:**  
- **Phase 1: Preparation / Hazırlık**: Research sniffing resources, document in markdown and JSON.  
- **Phase 2: Learning and Planning / Öğrenme ve Planlama**: Study resources, write summary, create design plan.  
- **Phase 3: Implementation / Uygulama**: Build sniffing, parsing, analysis, error handling, reporting, and main functions.  
- **Phase 4: Testing and Validation / Test ve Doğrulama**: Test with various scenarios, confirm with external tools.  
- **Phase 5: Contribution / Katkı**: Prepare files, submit to GitHub.  

**Turkish:**  
- **Aşama 1: Hazırlık**: Koklama kaynaklarını araştırın, markdown ve JSON’da belgeleyin.  
- **Aşama 2: Öğrenme ve Planlama**: Kaynakları inceleyin, özet yazın, tasarım planı oluşturun.  
- **Aşama 3: Uygulama**: Koklama, ayrıştırma, analiz, hata işleme, raporlama ve ana fonksiyonları oluşturun.  
- **Aşama 4: Test ve Doğrulama**: Çeşitli senaryolarla test edin, harici araçlarla doğrulayın.  
- **Aşama 5: Katkı**: Dosyaları hazırlayın, GitHub’a gönderin.  

---

#### Small Implementation Steps / Küçük Uygulama Adımları
**English:**  
- **Sniffing**: Capture packets from a specified interface.  
- **Parsing**: Extract source, destination, and protocol from packets.  
- **Analysis**: Count packets per source, flag high traffic.  
- **Error Handling**: Handle permission and interface errors.  
- **Reporting**: Format analysis in markdown.  
- **Main**: Integrate functions to process traffic and report results.  

**Turkish:**  
- **Koklama**: Belirtilen arayüzden paketleri yakalayın.  
- **Ayrıştırma**: Paketlerden kaynak, hedef ve protokolü çıkarın.  
- **Analiz**: Kaynak başına paketleri sayın, yüksek trafiği işaretleyin.  
- **Hata İşleme**: İzin ve arayüz hatalarını ele alın.  
- **Raporlama**: Analizi markdown’da formatlayın.  
- **Ana**: Trafiği işlemek ve sonuçları raporlamak için fonksiyonları entegre edin.  
