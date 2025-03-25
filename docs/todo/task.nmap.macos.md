## Task : macOS Network Device Detection

**Assigned Role:** Sage  
**Module File:** `modules/macos_network_device_detection.py`

### Expanded Instruction Set for Amateur Cybersecurity Students

#### 1. Research
- **Objective:** Compile techniques for detecting macOS devices using Nmap and other tools.
- **Corrected DeepSearch Prompt:**  
  ```json
  {
    "query": "Find all techniques to detect macOS devices using Nmap and other tools. Include Nmap scripts, service detection methods, fingerprinting techniques, and complementary tools like Wireshark or arp-scan. Also, search for methods to identify macOS versions (e.g., 10.15 Catalina). Ensure no technique is missed, and provide detailed usage instructions, accuracy notes, and limitations for each."
  }
  ```
  - **Explanation:** Ensures a comprehensive search for detection methods and version identification.
- **Action Steps:**
  1. **Execute DeepSearch:** Run the prompt in Grok3 DeepSearch.
  2. **Document Findings:** For each technique or tool:
     - **Technique/Tool Name:** e.g., "Nmap afp-serverinfo script."
     - **Description:** How it identifies macOS (e.g., AFP banners).
     - **Usage Instructions:** Commands (e.g., `nmap -sV --script afp-serverinfo <target_ip>`).
     - **Accuracy:** Reliability (e.g., high if AFP enabled).
     - **Limitations:** Failures (e.g., disabled services).
  3. **Additional Scope:** Identify macOS versions or device models (e.g., MacBook Pro).
- **Output:**
  - **Markdown File:** `research_notes_macos.md` with sections: *Techniques*, *Tools*, *Version Detection*, *Limitations*.
  - **JSON File:** `macos_research_data.json` with keys: `techniques`, `tools`, `version_methods`, `limitations`.

#### 2. Understand
- **Objective:** Understand macOS detection and its security implications.
- **Key Concepts:**
  - **Fingerprinting:** macOS-specific TCP/IP or Bonjour broadcasts.
  - **Service Analysis:** AFP, Bonjour, or SMB services.
  - **Accuracy Factors:** Service availability impacts detection.
  - **Limitations:** Firewalls or disabled services.
- **Reflection Questions:**
  - How does macOS differ from other OSes on the network?
  - Why detect macOS in a pentest?
- **Action:** Write a 300-word summary in `research_notes_macos.md` under "Understanding macOS Detection." Example: "Bonjour on port 5353 is a strong indicator but may be disabled."

#### 3. Plan
- **Objective:** Design `macos_network_device_detection.py`.
- **Components:**
  - **Inputs:** Single IP or list of IPs.
  - **Outputs:** Detection result, accuracy, version, report.
  - **Functions:**
    - `scan_target(target)`
    - `analyze_results(nm, target)`
    - `determine_device(results)`
    - `report_detection(target, result)`
    - `main(targets)`
  - **Error Handling:** Invalid IPs, unreachable hosts.
- **Pseudocode:**
  ```
  FOR each target in targets:
      nm = scan_target(target)
      results = analyze_results(nm, target)
      detection = determine_device(results)
      report = report_detection(target, detection)
      SAVE report
  ```
- **Output:** "Design Plan" section in `research_notes_macos.md`.

#### 4. Implement
- **Objective:** Code `macos_network_device_detection.py`.
- **Step-by-Step Implementation:**
  1. **Setup Environment:** Install `python-nmap`.
  2. **Scan Target Function:**
     ```python
     import nmap

     def scan_target(target):
         try:
             nm = nmap.PortScanner()
             nm.scan(target, arguments="-sV --script smb-os-discovery,http-useragent,afp-serverinfo -O")
             if not nm.all_hosts():
                 raise Exception("No hosts detected")
             return nm
         except nmap.PortScannerError as e:
             raise Exception(f"Nmap error: {str(e)}")
         except Exception as e:
             raise Exception(f"Scan failed: {str(e)}")
     ```
  3. **Analyze Results Function:**
     ```python
     def analyze_results(nm, target):
         results = {"is_macos": False, "details": ""}
         if target in nm.all_hosts():
             if 548 in nm[target].get("tcp", {}):
                 if "afp" in nm[target]["tcp"][548].get("name", ""):
                     results["is_macos"] = True
                     results["details"] = "AFP service on port 548 detected"
                     return results
             if "smb-os-discovery" in nm[target].get("hostscript", {}):
                 os_info = nm[target]["hostscript"]["smb-os-discovery"]
                 if "macOS" in os_info or "Mac OS X" in os_info:
                     results["is_macos"] = True
                     results["details"] = f"SMB OS Info: {os_info}"
                     return results
             if "osmatch" in nm[target]:
                 for os in nm[target]["osmatch"]:
                     if "macOS" in os.get("name", "") or "Mac OS X" in os.get("name", ""):
                         results["is_macos"] = True
                         results["details"] = f"OS Match: {os['name']}"
                         return results
         results["details"] = "No macOS signatures found"
         return results
     ```
  4. **Determine Device Function:**
     ```python
     def determine_device(results):
         if results["is_macos"]:
             accuracy = 90 if "AFP" in results["details"] else 80
             version = "Unknown"
             if "macOS" in results["details"] or "Mac OS X" in results["details"]:
                 parts = results["details"].split("macOS") or results["details"].split("Mac OS X")
                 if len(parts) > 1:
                     version = parts[1].split()[0].strip(";,)")
             return {"is_macos": True, "accuracy": accuracy, "version": version}
         return {"is_macos": False, "accuracy": 100, "version": "N/A"}
     ```
  5. **Reporting Function:**
     ```python
     import time

     def report_detection(target, result):
         timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
         report = f"""
 ### Detection Report
 - **Timestamp:** {timestamp}
 - **Target IP:** {target}
 - **Is macOS:** {result['is_macos']}
 - **Accuracy:** {result['accuracy']}%
 - **Detected Version:** {result['version']}
 """
         return report.strip()
     ```
  6. **Main Function:**
     ```python
     def main(targets):
         if not isinstance(targets, list):
             targets = [targets]
         reports = []
         for target in targets:
             try:
                 nm = scan_target(target)
                 results = analyze_results(nm, target)
                 detection = determine_device(results)
                 report = report_detection(target, detection)
                 reports.append(report)
             except Exception as e:
                 reports.append(f"### Error Report\n- **Target:** {target}\n- **Error:** {str(e)}")
         with open("macos_detection_report.md", "w") as f:
             f.write("\n\n".join(reports))
         return "\n\n".join(reports)
     ```

#### 5. Test
- **Test Cases:**
  - **Known macOS:** IP 192.168.1.12.
  - **Non-macOS:** Windows or Linux IP.
  - **Edge Cases:** Invalid IP, unreachable host.
- **Procedure:**
  1. Run `main(["192.168.1.12", "192.168.1.13", "256.256.256.256"])`.
  2. Record in `test_results_macos.md`.
- **Example Entry:**
  ```
  | Input          | Expected Output       | Actual Output         | Pass/Fail | Notes                  |
  |----------------|-----------------------|-----------------------|-----------|------------------------|
  | 192.168.1.12   | Is macOS: True        | Is macOS: True        | Pass      | AFP detected           |
  ```

#### 6. Confirm
- **Methods:** Use Wireshark for Bonjour traffic; verify via admin access.
- **Output:** "Confirmation Results" in `test_results_macos.md` (e.g., "95% accurate; missed one device").

#### 7. Contribute
- **Steps:**
  1. Fork `https://github.com/QLineTech/Q-Pentest`.
  2. Branch: `git checkout -b feature/macos-detection`.
  3. Add files: `macos_network_device_detection.py`, `research_notes_macos.md`, `test_results_macos.md`, `macos_research_data.json`.
  4. Commit, push, and submit a pull request.
