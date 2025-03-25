## Task : Android Network Device Detection

**Assigned Role:** Sage  
**Module File:** `modules/android_network_device_detection.py`

### Expanded Instruction Set for Amateur Cybersecurity Students

#### 1. Research
- **Objective:** Exhaustively gather techniques for detecting Android devices on a network using Nmap and other tools, focusing on Android-specific network behaviors.
- **Corrected DeepSearch Prompt:**  
  ```json
  {
    "query": "Find all techniques to detect Android devices using Nmap and other tools. Include Nmap scripts, service detection methods, fingerprinting techniques, and complementary tools like Wireshark or Netcat. Also, search for methods to identify Android versions or device models. Ensure no technique is missed, and provide detailed usage instructions, accuracy notes, and limitations for each."
  }
  ```
  - **Explanation:** This prompt ensures a thorough search, covering all tools, techniques, and version identification methods, with an emphasis on detailed documentation.
- **Action Steps:**
  1. **Execute DeepSearch:** Run the corrected prompt in Grok3 DeepSearch advanced mode to collect all relevant data.
  2. **Document Findings:** For each technique or tool:
     - **Technique/Tool Name:** e.g., "Nmap http-useragent script."
     - **Description:** How it identifies Android devices (e.g., user-agent strings with "Android").
     - **Usage Instructions:** Specific commands (e.g., `nmap -sV --script http-useragent <target_ip>`).
     - **Accuracy:** Reliability percentage (e.g., 80% if user-agent is present).
     - **Limitations:** Scenarios where it fails (e.g., disabled services).
  3. **Additional Scope:** Include methods to distinguish Android versions (e.g., 11 vs. 12) or device models (e.g., Google Pixel).
- **Output:**
  - **Markdown File:** `research_notes_android.md` with sections: *Techniques*, *Tools*, *Version Detection*, *Limitations*.
  - **JSON File:** `android_research_data.json` with keys: `techniques`, `tools`, `version_methods`, `limitations`.

#### 2. Understand
- **Objective:** Build a foundational understanding of Android network detection and its cybersecurity relevance.
- **Key Concepts:**
  - **Fingerprinting:** TCP/IP stack responses or service banners indicating Android OS.
  - **Service Analysis:** Unique Android services like Android Debug Bridge (ADB) on port 5555.
  - **Accuracy Factors:** ADB detection is reliable, but generic fingerprinting less so.
  - **Limitations:** Rooted devices or VPNs may obscure signatures.
- **Reflection Questions:**
  - Why is Android detection critical in penetration testing?
  - How could attackers exploit Android network vulnerabilities?
- **Action:** Write a 300-word summary in `research_notes_android.md` under "Understanding Android Detection," covering concepts, importance, and pitfalls. Example: "ADB on port 5555 strongly indicates Android, but secure setups may disable it."

#### 3. Plan
- **Objective:** Design a script structure for `android_network_device_detection.py`.
- **Components:**
  - **Inputs:** Single IP or list of IPs.
  - **Outputs:** Detection result (True/False), accuracy percentage, version (if detected), markdown report.
  - **Functions:**
    - `scan_target(target)`: Executes Nmap scan.
    - `analyze_results(nm, target)`: Parses scan data for Android signatures.
    - `determine_device(results)`: Confirms Android presence with accuracy and version.
    - `report_detection(target, result)`: Creates a markdown report.
    - `main(targets)`: Manages multiple targets.
  - **Error Handling:** Handle invalid IPs, unreachable hosts, or insufficient data.
- **Pseudocode:**
  ```
  FOR each target in targets:
      nm = scan_target(target)
      results = analyze_results(nm, target)
      detection = determine_device(results)
      report = report_detection(target, detection)
      SAVE report
  ```
- **Output:** Add a "Design Plan" section to `research_notes_android.md` with function details, inputs/outputs, and error scenarios.

#### 4. Implement
- **Objective:** Code `android_network_device_detection.py` to detect Android devices with accuracy, version identification, and reporting.
- **Step-by-Step Implementation:**
  1. **Setup Environment:**
     - Install Python 3.x and `python-nmap` (`pip install python-nmap`).
  2. **Scan Target Function:**
     ```python
     import nmap

     def scan_target(target):
         try:
             nm = nmap.PortScanner()
             nm.scan(target, arguments="-sV --script http-useragent,banner,ssl-cert -O")
             if not nm.all_hosts():
                 raise Exception("No hosts detected")
             return nm
         except nmap.PortScannerError as e:
             raise Exception(f"Nmap error: {str(e)}")
         except Exception as e:
             raise Exception(f"Scan failed: {str(e)}")
     ```
     - **Explanation:** Uses service detection (-sV), scripts for user-agent and banners, and OS fingerprinting (-O).
  3. **Analyze Results Function:**
     ```python
     def analyze_results(nm, target):
         results = {"is_android": False, "details": ""}
         if target in nm.all_hosts():
             if 5555 in nm[target].get("tcp", {}):
                 if "android-adb" in nm[target]["tcp"][5555].get("name", ""):
                     results["is_android"] = True
                     results["details"] = "ADB service on port 5555 detected"
                     return results
             for port in nm[target].get("tcp", {}):
                 if "http-useragent" in nm[target]["tcp"][port].get("script", {}):
                     ua = nm[target]["tcp"][port]["script"]["http-useragent"]
                     if "Android" in ua:
                         results["is_android"] = True
                         results["details"] = f"User-Agent: {ua}"
                         return results
             if "osmatch" in nm[target]:
                 for os in nm[target]["osmatch"]:
                     if "Android" in os.get("name", ""):
                         results["is_android"] = True
                         results["details"] = f"OS Match: {os['name']}"
                         return results
         results["details"] = "No Android signatures found"
         return results
     ```
     - **Explanation:** Prioritizes ADB, then user-agent, then OS fingerprinting.
  4. **Determine Device Function:**
     ```python
     def determine_device(results):
         if results["is_android"]:
             accuracy = 95 if "ADB" in results["details"] else 85 if "User-Agent" in results["details"] else 75
             version = "Unknown"
             if "Android" in results["details"]:
                 parts = results["details"].split("Android")
                 if len(parts) > 1:
                     version = parts[1].split()[0].strip(";,)")
             return {"is_android": True, "accuracy": accuracy, "version": version}
         return {"is_android": False, "accuracy": 100, "version": "N/A"}
     ```
     - **Explanation:** Accuracy varies by method; version extracted from details.
  5. **Reporting Function:**
     ```python
     import time

     def report_detection(target, result):
         timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
         report = f"""
 ### Detection Report
 - **Timestamp:** {timestamp}
 - **Target IP:** {target}
 - **Is Android:** {result['is_android']}
 - **Accuracy:** {result['accuracy']}%
 - **Detected Version:** {result['version']}
 """
         return report.strip()
     ```
     - **Explanation:** Creates a formatted markdown report.
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
         with open("android_detection_report.md", "w") as f:
             f.write("\n\n".join(reports))
         return "\n\n".join(reports)
     ```
     - **Explanation:** Processes multiple targets and saves reports.

#### 5. Test
- **Objective:** Validate the script across various scenarios.
- **Test Cases:**
  - **Known Android:** IP of an Android device (e.g., 192.168.1.10).
  - **Non-Android:** IP of a Windows or iOS device.
  - **Edge Cases:** Invalid IP (e.g., "256.256.256.256"), unreachable host.
- **Procedure:**
  1. Run `main(["192.168.1.10", "192.168.1.11", "256.256.256.256"])`.
  2. Record in `test_results_android.md` with columns: *Input*, *Expected Output*, *Actual Output*, *Pass/Fail*, *Notes*.
- **Example Entry:**
  ```
  | Input          | Expected Output       | Actual Output         | Pass/Fail | Notes                  |
  |----------------|-----------------------|-----------------------|-----------|------------------------|
  | 192.168.1.10   | Is Android: True      | Is Android: True      | Pass      | ADB detected           |
  ```

#### 6. Confirm
- **Objective:** Manually verify script accuracy.
- **Methods:**
  - Use Wireshark to check ADB traffic or Android packets.
  - Confirm device type via network admin access.
- **Output:** Add "Confirmation Results" to `test_results_android.md`, noting accuracy (e.g., "90% accurate; missed one rooted device").

#### 7. Contribute
- **Objective:** Submit to `https://github.com/QLineTech/Q-Pentest`.
- **Steps:**
  1. Fork the repository.
  2. Create branch: `git checkout -b feature/android-detection`.
  3. Add files: `android_network_device_detection.py`, `research_notes_android.md`, `test_results_android.md`, `android_research_data.json`.
  4. Commit: `git commit -m "Add Android detection module with docs"`.
  5. Push: `git push origin feature/android-detection`.
  6. Submit a pull request with detailed description.
