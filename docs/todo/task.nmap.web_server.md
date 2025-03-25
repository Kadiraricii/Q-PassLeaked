### Task: Web Server Network Device Detection
**Assigned Role:** Sage  
**Module File:** `modules/webserver_network_detection.py`

#### Expanded Instruction Set for Amateur Cybersecurity Students

##### **1. Research**
- **Objective:** Conduct an exhaustive investigation into methods for detecting web servers on a network, focusing on tools like Nmap and supplementary utilities, to build a solid foundation for your script.
- **DeepSearch Prompt:**  
  ```json
  {
    "query": "Explore every possible technique for detecting web server devices on a network using Nmap and additional tools such as curl, Wappalyzer, Wireshark, and netcat. Include detailed Nmap scripts (e.g., http-enum, http-methods), service detection flags, fingerprinting approaches, and methods to identify specific web server software versions (e.g., Apache 2.4.41, Nginx 1.18.0). Provide step-by-step usage instructions for each technique, expected outputs, accuracy assessments, potential false positives/negatives, and limitations such as non-standard configurations or obfuscated headers. Cross-reference findings with real-world penetration testing scenarios and include at least 10 unique methods."
  }
- **Action Steps:**
  1. **Run DeepSearch:** Use the prompt in Grok3 DeepSearch advanced mode to gather a comprehensive dataset. Save the raw output as `raw_webserver_research.txt`.
  2. **Analyze Results:** Read through the output and categorize findings into:
     - **Nmap Techniques:** Scripts like `http-server-header`, `http-title`, and `http-enum`.
     - **Supplementary Tools:** How tools like `curl -I` or Wireshark packet analysis identify web servers.
     - **Version Detection:** Methods to pinpoint software versions (e.g., parsing HTTP headers).
     - **Edge Cases:** Situations where detection fails (e.g., servers behind proxies).
  3. **Expand Each Method:** For every technique (aim for at least 10):
     - **Name and Description:** e.g., "Nmap http-methods script - Identifies HTTP methods supported by the server."
     - **Command Syntax:** e.g., `nmap -p 80,443 --script http-methods <target_ip>`.
     - **Sample Output:** What the result looks like (e.g., "GET, POST, OPTIONS detected").
     - **Accuracy Notes:** Reliability factors (e.g., "95% if server responds, 50% if filtered").
     - **Limitations:** Scenarios where it fails (e.g., "Fails if port is non-standard").
  4. **Cross-Validation:** Search online forums (e.g., Stack Exchange, Reddit) for real-world examples of these techniques in use. Note any discrepancies or additional insights.
  5. **Compile Documentation:**
     - Create `research_notes_webserver.md` with sections: *Nmap Techniques*, *Supplementary Tools*, *Version Detection Methods*, *Challenges and Limitations*.
     - Create `webserver_research_data.json` with structured data: `{"techniques": [], "tools": [], "version_methods": [], "limitations": []}`.

##### **2. Understand**
- **Objective:** Develop a deep conceptual understanding of web server detection, its role in cybersecurity, and the challenges involved.
- **Key Topics to Explore:**
  - **HTTP Protocol Basics:** How web servers use HTTP/HTTPS, common ports (80, 443), and response headers.
  - **Fingerprinting Mechanics:** How tools infer server type from banners, response times, or packet patterns.
  - **Security Implications:** Why attackers target web servers (e.g., SQL injection, XSS vulnerabilities).
  - **Obfuscation Techniques:** How administrators hide server details (e.g., modifying `Server` header).
- **Action Steps:**
  1. **Read Documentation:** Study the Nmap scripting engine (NSE) documentation for HTTP-related scripts on the official Nmap website.
  2. **Explore Headers:** Use `curl -I http://example.com` on multiple websites to observe different `Server` headers (e.g., "Apache/2.4.41 (Ubuntu)").
  3. **Reflection Questions:**
     - What makes web server detection a critical step in network reconnaissance?
     - How do false positives/negatives impact a penetration test?
     - Why might a server admin obscure the `Server` header?
  4. **Write Summary:** Draft a detailed 500-word explanation in `research_notes_webserver.md` under "Understanding Web Server Detection." Include examples (e.g., "A server returning 'Server: nginx/1.18.0' is easily identified, but 'Server: custom' requires deeper analysis").

##### **3. Plan**
- **Objective:** Design a detailed script architecture for `webserver_network_detection.py` that is robust and flexible.
- **Components to Define:**
  - **Inputs:** Accept a single IP, a list of IPs, or a file containing IPs.
  - **Outputs:** Boolean result (is it a web server?), confidence score, detected version, and a detailed report.
  - **Functions:**
    - `validate_input(targets)`: Check IP format and reachability.
    - `scan_target(target)`: Execute Nmap scans with multiple scripts.
    - `analyze_results(nm, target)`: Parse scan data for web server evidence.
    - `determine_device(results)`: Assess findings and assign confidence/version.
    - `generate_report(target, result)`: Format output in markdown.
    - `main(targets)`: Orchestrate the process for multiple targets.
  - **Error Handling:** Account for timeouts, invalid IPs, permission issues, and incomplete scans.
- **Detailed Pseudocode:**
  ```
  FUNCTION validate_input(targets):
      IF targets is not list:
          CONVERT targets to list
      FOR each target in targets:
          IF not valid IP:
              RAISE error "Invalid IP format"
      RETURN validated_targets

  FUNCTION scan_target(target):
      INITIALIZE Nmap scanner
      RUN scan with -sV, -p 80,443, scripts (http-server-header, http-methods, http-title)
      RETURN scan results

  FUNCTION main(targets):
      validated_targets = validate_input(targets)
      FOR each target in validated_targets:
          results = scan_target(target)
          analysis = analyze_results(results, target)
          detection = determine_device(analysis)
          report = generate_report(target, detection)
          APPEND report to reports list
      SAVE reports to file
  ```
- **Output:** Add a "Script Design Plan" section to `research_notes_webserver.md` with function descriptions, input/output specs, and error-handling strategies.

##### **4. Implement**
- **Objective:** Write a fully functional `webserver_network_detection.py` script with extensive error checking and reporting.
- **Step-by-Step Implementation:**
  1. **Environment Setup:**
     - Install Python 3.x and required libraries: `pip install python-nmap`.
     - Verify Nmap is installed on your system (`nmap --version`).
  2. **Validate Input Function:**
     ```python
     import re

     def validate_input(targets):
         if not isinstance(targets, list):
             targets = [targets]
         valid_targets = []
         ip_pattern = re.compile(r"^(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$")
         for target in targets:
             if not ip_pattern.match(target):
                 raise ValueError(f"Invalid IP address: {target}")
             valid_targets.append(target)
         return valid_targets
     ```
     - **Explanation:** Ensures all inputs are valid IPv4 addresses using regex.
  3. **Scan Target Function:**
     ```python
     import nmap

     def scan_target(target):
         nm = nmap.PortScanner()
         try:
             nm.scan(target, ports="80,443", arguments="-sV --script http-server-header,http-methods,http-title,http-enum")
             if not nm.all_hosts():
                 raise Exception(f"No response from {target}")
             return nm
         except nmap.PortScannerError as e:
             raise Exception(f"Nmap error: {str(e)}")
         except Exception as e:
             raise Exception(f"Scan failed for {target}: {str(e)}")
     ```
     - **Explanation:** Scans ports 80 and 443 with multiple HTTP scripts for comprehensive detection.
  4. **Analyze Results Function:**
     ```python
     def analyze_results(nm, target):
         results = {"is_webserver": False, "details": [], "confidence": 0}
         if target in nm.all_hosts():
             for port in [80, 443]:
                 if port in nm[target].get("tcp", {}):
                     port_data = nm[target]["tcp"][port]
                     if "http-server-header" in port_data.get("script", {}):
                         header = port_data["script"]["http-server-header"]
                         results["is_webserver"] = True
                         results["details"].append(f"Server Header: {header}")
                         results["confidence"] += 50
                     if "http-methods" in port_data.get("script", {}):
                         methods = port_data["script"]["http-methods"]
                         results["is_webserver"] = True
                         results["details"].append(f"HTTP Methods: {methods}")
                         results["confidence"] += 30
                     if "http-title" in port_data.get("script", {}):
                         title = port_data["script"]["http-title"]
                         results["details"].append(f"Page Title: {title}")
                         results["confidence"] += 20
         if not results["is_webserver"]:
             results["details"] = ["No web server signatures detected"]
         return results
     ```
     - **Explanation:** Accumulates evidence from multiple scripts, assigning confidence scores.
  5. **Determine Device Function:**
     ```python
     def determine_device(results):
         if results["is_webserver"]:
             version = "Unknown"
             for detail in results["details"]:
                 if "Server Header" in detail and len(detail.split()) > 2:
                     version = detail.split()[2]
                     break
             return {
                 "is_webserver": True,
                 "confidence": min(results["confidence"], 95),
                 "version": version
             }
         return {"is_webserver": False, "confidence": 100, "version": "N/A"}
     ```
     - **Explanation:** Caps confidence at 95% and extracts version from headers if available.
  6. **Generate Report Function:**
     ```python
     import time

     def generate_report(target, result):
         timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
         report = f"""
 ### Web Server Detection Report
 - **Timestamp:** {timestamp}
 - **Target IP:** {target}
 - **Is Web Server:** {result['is_webserver']}
 - **Confidence Level:** {result['confidence']}%
 - **Detected Version:** {result['version']}
 """
         return report.strip()
     ```
     - **Explanation:** Produces a clean, markdown-formatted report.
  7. **Main Function:**
     ```python
     def main(targets):
         reports = []
         try:
             validated_targets = validate_input(targets)
         except ValueError as e:
             return f"### Error\n- **Message:** {str(e)}"
         for target in validated_targets:
             try:
                 nm = scan_target(target)
                 results = analyze_results(nm, target)
                 detection = determine_device(results)
                 report = generate_report(target, detection)
                 reports.append(report)
             except Exception as e:
                 reports.append(f"### Error Report\n- **Target:** {target}\n- **Error:** {str(e)}")
         with open("webserver_detection_report.md", "w") as f:
             f.write("\n\n".join(reports))
         return "\n\n".join(reports)
     ```
     - **Explanation:** Ties everything together, handling multiple targets and errors.

##### **5. Test**
- **Objective:** Thoroughly validate the script across diverse scenarios.
- **Test Cases:**
  - Local web server (e.g., 192.168.1.100 with Apache).
  - Public web server (e.g., an IP you control or a known site).
  - Non-web server (e.g., a local printer).
  - Invalid IP (e.g., "256.256.256.256").
  - Unreachable host (e.g., a powered-off device).
- **Procedure:**
  1. Run the script with: `main(["192.168.1.100", "example.com", "192.168.1.50", "256.256.256.256"])`.
  2. Create `test_results_webserver.md` with a table:
     - Columns: *Input IP*, *Expected Result*, *Actual Result*, *Pass/Fail*, *Observations*.
  3. For each test, note discrepancies (e.g., "Detected Apache but missed version due to custom header").
  4. Run each test twice to check consistency.

##### **6. Confirm**
- **Objective:** Manually verify script accuracy against alternative methods.
- **Verification Steps:**
  1. Use `curl -I <target_ip>` to check headers manually.
  2. Run `nmap -sV <target_ip>` separately and compare outputs.
  3. If possible, access the target device to confirm its role (e.g., via admin interface).
  4. Document findings in `test_results_webserver.md` under "Manual Confirmation," including accuracy percentage (e.g., "Matched 9/10 targets").

##### **7. Contribute**
- **Objective:** Share your work with the Q-Pentest project.
- **Steps:**
  1. Fork `https://github.com/QLineTech/Q-Pentest`.
  2. Create a branch: `git checkout -b feature/webserver-detection`.
  3. Add files: `webserver_network_detection.py`, `research_notes_webserver.md`, `test_results_webserver.md`, `webserver_research_data.json`.
  4. Commit with a detailed message: `git commit -m "Implemented web server detection with Nmap, extensive research, and testing"`.
  5. Push: `git push origin feature/webserver-detection`.
  6. Submit a pull request with a full description of your work.

