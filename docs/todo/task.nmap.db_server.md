### Task : Database Server Network Device Detection
**Assigned Role:** Sage  
**Module File:** `modules/dbserver_network_detection.py`

#### Expanded Instruction Set for Amateur Cybersecurity Students

##### **1. Research**
- **Objective:** Investigate all possible methods for detecting database servers on a network, ensuring a thorough understanding of tools and techniques.
- **DeepSearch Prompt:**  
  ```json
  {
    "query": "Investigate every technique for detecting database server devices on a network using Nmap and additional tools like Netcat, telnet, Wireshark, and sqlmap. Include Nmap scripts (e.g., mysql-info, ms-sql-info), service detection methods, fingerprinting strategies, and ways to identify database software versions (e.g., MySQL 5.7.32, PostgreSQL 13.4). Provide detailed command examples, expected outputs, accuracy metrics, potential errors, and limitations like disabled banners or encrypted connections. Include at least 10 distinct methods and reference their use in penetration testing."
  }
- **Action Steps:**
  1. **Run DeepSearch:** Execute the prompt in Grok3 DeepSearch advanced mode, saving output to `raw_dbserver_research.txt`.
  2. **Categorize Findings:**
     - **Nmap Scripts:** e.g., `mysql-info`, `oracle-tns-version`.
     - **Manual Tools:** e.g., `telnet <ip> 3306` for banner grabbing.
     - **Version Detection:** How to extract version info from banners or responses.
     - **Challenges:** Issues like non-default ports or firewall filtering.
  3. **Detail Each Method:** For at least 10 techniques:
     - **Name and Purpose:** e.g., "Nmap mysql-info - Retrieves MySQL server details."
     - **Command:** e.g., `nmap -p 3306 --script mysql-info <target_ip>`.
     - **Output Example:** e.g., "MySQL 5.7.32-log".
     - **Accuracy:** e.g., "95% if banner is enabled."
     - **Limitations:** e.g., "Fails if port is firewalled."
  4. **Real-World Context:** Search penetration testing blogs or GitHub repos for examples of these techniques in action.
  5. **Document Results:**
     - Write `research_notes_dbserver.md` with sections: *Nmap Techniques*, *Other Tools*, *Version Identification*, *Limitations*.
     - Create `dbserver_research_data.json` with keys: `techniques`, `tools`, `version_methods`, `limitations`.

##### **2. Understand**
- **Objective:** Gain a comprehensive understanding of database server detection and its cybersecurity relevance.
- **Key Topics:**
  - **Database Protocols:** Common ports (e.g., 3306 for MySQL, 1433 for MS SQL) and their behaviors.
  - **Banner Grabbing:** How banners reveal software details.
  - **Attack Vectors:** Why databases are targets (e.g., SQL injection).
  - **Mitigations:** How admins secure databases (e.g., disabling banners).
- **Action Steps:**
  1. **Study Protocols:** Read about MySQL, PostgreSQL, and MS SQL on their official documentation sites.
  2. **Test Banners:** Use `telnet <ip> 3306` on a local MySQL instance to see a banner.
  3. **Reflection Questions:**
     - How does knowing a database version aid an attacker?
     - What are the risks of misidentifying a database server?
     - Why might a database not respond to standard scans?
  4. **Write Summary:** Produce a 500-word section in `research_notes_dbserver.md` under "Understanding Database Detection," with examples (e.g., "A banner like '5.7.32 MySQL' is a giveaway, but many servers disable it").

##### **3. Plan**
- **Objective:** Architect a detailed script for `dbserver_network_detection.py`.
- **Components:**
  - **Inputs:** Single IP, list of IPs, or file input.
  - **Outputs:** Detection result, confidence score, version, report.
  - **Functions:**
    - `validate_input(targets)`: Verify IP validity.
    - `scan_target(target)`: Run Nmap with database scripts.
    - `analyze_results(nm, target)`: Check for database signatures.
    - `determine_device(results)`: Finalize detection and version.
    - `generate_report(target, result)`: Create markdown output.
    - `main(targets)`: Coordinate execution.
  - **Error Handling:** Manage scan failures, port blocking, and invalid inputs.
- **Pseudocode:**
  ```
  FUNCTION validate_input(targets):
      CONVERT targets to list if needed
      FOR each target:
          IF not valid IP:
              RAISE error
      RETURN targets

  FUNCTION scan_target(target):
      RUN Nmap with -sV, ports 3306,1433,1521, scripts (mysql-info, ms-sql-info)
      RETURN scan data

  FUNCTION main(targets):
      validated = validate_input(targets)
      FOR each target in validated:
          scan = scan_target(target)
          results = analyze_results(scan, target)
          detection = determine_device(results)
          report = generate_report(target, detection)
          SAVE report
  ```
- **Output:** Add "Script Design" to `research_notes_dbserver.md` with detailed function specs.

##### **4. Implement**
- **Objective:** Code a robust `dbserver_network_detection.py`.
- **Steps:**
  1. **Setup:** Install `python-nmap` (`pip install python-nmap`).
  2. **Validate Input:**
     ```python
     import re

     def validate_input(targets):
         if not isinstance(targets, list):
             targets = [targets]
         ip_pattern = re.compile(r"^(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$")
         return [t for t in targets if ip_pattern.match(t) or raise ValueError(f"Invalid IP: {t}")]
     ```
  3. **Scan Target:**
     ```python
     import nmap

     def scan_target(target):
         nm = nmap.PortScanner()
         nm.scan(target, ports="3306,1433,1521", arguments="-sV --script mysql-info,ms-sql-info,oracle-tns-version")
         if not nm.all_hosts():
             raise Exception(f"No response from {target}")
         return nm
     ```
  4. **Analyze Results:**
     ```python
     def analyze_results(nm, target):
         results = {"is_dbserver": False, "details": [], "confidence": 0}
         if target in nm.all_hosts():
             for port in [3306, 1433, 1521]:
                 if port in nm[target].get("tcp", {}):
                     port_data = nm[target]["tcp"][port]
                     if "mysql-info" in port_data.get("script", {}):
                         results["is_dbserver"] = True
                         results["details"].append(port_data["script"]["mysql-info"])
                         results["confidence"] += 50
                     if "ms-sql-info" in port_data.get("script", {}):
                         results["is_dbserver"] = True
                         results["details"].append(port_data["script"]["ms-sql-info"])
                         results["confidence"] += 50
                     if "oracle-tns-version" in port_data.get("script", {}):
                         results["is_dbserver"] = True
                         results["details"].append(port_data["script"]["oracle-tns-version"])
                         results["confidence"] += 50
         if not results["is_dbserver"]:
             results["details"] = ["No database signatures"]
         return results
     ```
  5. **Determine Device:**
     ```python
     def determine_device(results):
         if results["is_dbserver"]:
             version = "Unknown"
             for detail in results["details"]:
                 if "version" in detail.lower():
                     version = detail.split()[1]
                     break
             return {"is_dbserver": True, "confidence": min(results["confidence"], 95), "version": version}
         return {"is_dbserver": False, "confidence": 100, "version": "N/A"}
     ```
  6. **Generate Report:**
     ```python
     import time

     def generate_report(target, result):
         timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
         return f"""
 ### Database Server Report
 - **Timestamp:** {timestamp}
 - **Target IP:** {target}
 - **Is Database Server:** {result['is_dbserver']}
 - **Confidence:** {result['confidence']}%
 - **Version:** {result['version']}
 """
     ```
  7. **Main Function:**
     ```python
     def main(targets):
         reports = []
         validated = validate_input(targets)
         for target in validated:
             try:
                 nm = scan_target(target)
                 results = analyze_results(nm, target)
                 detection = determine_device(results)
                 reports.append(generate_report(target, detection))
             except Exception as e:
                 reports.append(f"### Error\n- **Target:** {target}\n- **Error:** {str(e)}")
         with open("dbserver_detection_report.md", "w") as f:
             f.write("\n\n".join(reports))
         return "\n\n".join(reports)
     ```

##### **5. Test**
- **Objective:** Validate across multiple scenarios.
- **Test Cases:**
  - Local MySQL server (e.g., 192.168.1.200).
  - Non-database device (e.g., 192.168.1.50).
  - Invalid IP (e.g., "999.999.999.999").
- **Procedure:**
  1. Run `main(["192.168.1.200", "192.168.1.50", "999.999.999.999"])`.
  2. Log results in `test_results_dbserver.md` with a detailed table.

##### **6. Confirm**
- **Objective:** Verify accuracy manually.
- **Steps:**
  1. Use `telnet <ip> 3306` to check banners.
  2. Compare with script output in `test_results_dbserver.md`.

##### **7. Contribute**
- **Steps:** Fork, branch (`feature/dbserver-detection`), commit, push, and submit a pull request to `https://github.com/QLineTech/Q-Pentest`.

---

### Task 11: DNS Server Network Device Detection
**Assigned Role:** Sage  
**Module File:** `modules/dnsserver_network_detection.py`

#### Expanded Instruction Set for Amateur Cybersecurity Students

##### **1. Research**
- **Objective:** Explore all DNS server detection techniques comprehensively.
- **DeepSearch Prompt:**  
  ```json
  {
    "query": "Examine all techniques for detecting DNS server devices on a network using Nmap and tools like dig, nslookup, Wireshark, and dnsrecon. Include Nmap scripts (e.g., dns-nsid, dns-service-discovery), UDP/TCP detection methods, fingerprinting approaches, and version identification for software like BIND 9.11 or PowerDNS. Provide detailed command examples, sample outputs, accuracy assessments, failure scenarios (e.g., disabled NSID), and at least 10 unique methods. Include penetration testing use cases."
  }
- **Action Steps:**
  1. **Run DeepSearch:** Save output to `raw_dnsserver_research.txt`.
  2. **Organize Findings:**
     - **Nmap Methods:** e.g., `dns-nsid`.
     - **External Tools:** e.g., `dig @<ip> version.bind chaos txt`.
     - **Version Detection:** Extracting software versions.
     - **Limitations:** Non-responsive servers or filtered ports.
  3. **Detail Methods:** Document 10+ techniques with commands, outputs, and accuracy.
  4. **Validate:** Check online resources for practical examples.
  5. **Output:** Create `research_notes_dnsserver.md` and `dnsserver_research_data.json`.

##### **2. Understand**
- **Objective:** Master DNS server detection concepts.
- **Topics:**
  - **DNS Protocol:** Role of port 53, UDP vs. TCP.
  - **Fingerprinting:** NSID and response analysis.
  - **Security Risks:** DNS spoofing, amplification attacks.
- **Steps:**
  1. Study DNS basics online.
  2. Test `dig` commands on public DNS (e.g., 8.8.8.8).
  3. Write a 500-word summary in `research_notes_dnsserver.md`.

##### **3. Plan**
- **Objective:** Design `dnsserver_network_detection.py`.
- **Components:** Similar to previous tasks with DNS-specific functions.
- **Pseudocode:** Detailed flow for scanning and reporting.
- **Output:** Add design to `research_notes_dnsserver.md`.

##### **4. Implement**
- **Steps:** Code functions similar to prior tasks, using `-sU -p 53` and DNS scripts.
- **Main Function:** Handle UDP scans and report generation.

##### **5. Test**
- **Cases:** Public DNS (8.8.8.8), local device, invalid IP.
- **Procedure:** Log results in `test_results_dnsserver.md`.

##### **6. Confirm**
- **Steps:** Use `dig` for manual checks, update `test_results_dnsserver.md`.

##### **7. Contribute**
- **Steps:** Submit to GitHub as with previous tasks.
