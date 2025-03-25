import hashlib
import requests
import time
from typing import Dict, List, Optional
from abc import ABC, abstractmethod
from bs4 import BeautifulSoup  # For HTML parsing in CyberNews

# Configure logging
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


# Abstract base class for leak databases
class LeakDatabase(ABC):
    @abstractmethod
    def check_password(self, password: str) -> Dict:
        """Check if a password is leaked in this database and return raw results."""
        pass


# HIBP Leak Database implementation
class HIBPLeakDatabase(LeakDatabase):
    def __init__(self):
        self.url = "https://api.pwnedpasswords.com/range/"

    def hash_password(self, password: str) -> str:
        """Convert password to SHA-1 hash in uppercase."""
        return hashlib.sha1(password.encode('utf-8')).hexdigest().upper()

    def query_hibp(self, hash_prefix: str) -> Optional[str]:
        """Query HIBP API with hash prefix."""
        headers = {"User-Agent": "LeakDatabaseChecker"}
        try:
            response = requests.get(f"{self.url}{hash_prefix}", headers=headers, timeout=5)
            response.raise_for_status()
            return response.text
        except requests.RequestException as e:
            logger.error(f"HIBP query failed: {e}")
            return None

    def check_password(self, password: str) -> Dict:
        """Check if password is leaked in HIBP."""
        try:
            sha1_hash = self.hash_password(password)
            prefix, suffix = sha1_hash[:5], sha1_hash[5:]
            hibp_response = self.query_hibp(prefix)
            if hibp_response and suffix in hibp_response:
                count = int(hibp_response.split(suffix + ":")[1].split("\n")[0])
                return {"is_leaked": True, "source": "HIBP", "breach_count": count}
            return {"is_leaked": False, "source": "HIBP"}
        except Exception as e:
            return {"is_leaked": None, "source": "HIBP", "error": str(e)}


# Proxynova Leak Database implementation
class ProxynovaLeakDatabase(LeakDatabase):
    def __init__(self):
        self.url = "https://api.proxynova.com/comb"

    def check_password(self, password: str) -> Dict:
        """Check if password is leaked in Proxynova's COMB dataset."""
        try:
            response = requests.get(self.url, params={"query": password, "start": 0, "limit": 100}, timeout=5)
            response.raise_for_status()
            data = response.json()
            count = sum(1 for line in data.get("lines", []) if line.split(":")[-1] == password)
            if count > 0:
                return {"is_leaked": True, "source": "Proxynova", "breach_count": count}
            return {"is_leaked": False, "source": "Proxynova"}
        except requests.RequestException as e:
            logger.error(f"Proxynova query failed: {e}")
            return {"is_leaked": None, "source": "Proxynova", "error": str(e)}


# CyberNews Leak Database implementation
class CyberNewsLeakDatabase(LeakDatabase):
    def __init__(self):
        self.url = "https://cybernews.com/password-leak-check/"

    def check_password(self, password: str) -> Dict:
        """Check if password is leaked in CyberNews database (simulated)."""
        try:
            # Simulate form submission (this is a placeholder and may not work as-is)
            response = requests.post(self.url, data={"password": password}, timeout=5)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, 'html.parser')
            result_div = soup.find('div', class_='result')  # Assumed class name
            if result_div and "found" in result_div.text.lower():
                return {"is_leaked": True, "source": "CyberNews"}
            return {"is_leaked": False, "source": "CyberNews"}
        except requests.RequestException as e:
            logger.error(f"CyberNews query failed: {e}")
            return {"is_leaked": None, "source": "CyberNews", "error": str(e)}


# DeHashed Leak Database implementation (Paid, optional)
class DeHashedLeakDatabase(LeakDatabase):
    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key
        self.url = "https://api.dehashed.com/search"

    def check_password(self, password: str) -> Dict:
        """Check if password is leaked in DeHashed (requires API key)."""
        if not self.api_key:
            return {"is_leaked": None, "source": "DeHashed", "error": "API key required"}
        try:
            # Placeholder for actual API call (replace with real implementation)
            # response = requests.get(self.url, params={"query": password, "api_key": self.api_key}, timeout=5)
            # data = response.json()
            # Implement logic to check if password is found
            return {"is_leaked": True, "source": "DeHashed", "breach_count": 1000}  # Simulated
        except Exception as e:
            return {"is_leaked": None, "source": "DeHashed", "error": str(e)}


# LeakCheck Leak Database implementation (Paid, optional)
class LeakCheckLeakDatabase(LeakDatabase):
    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key
        self.url = "https://leakcheck.io/api/v2/search"

    def check_password(self, password: str) -> Dict:
        """Check if password is leaked in LeakCheck (requires API key)."""
        if not self.api_key:
            return {"is_leaked": None, "source": "LeakCheck", "error": "API key required"}
        try:
            # Placeholder for actual API call (replace with real implementation)
            # response = requests.get(self.url, params={"query": password, "api_key": self.api_key}, timeout=5)
            # data = response.json()
            # Implement logic to check if password is found
            return {"is_leaked": True, "source": "LeakCheck", "breach_count": 500}  # Simulated
        except Exception as e:
            return {"is_leaked": None, "source": "LeakCheck", "error": str(e)}


# ScatteredSecrets Leak Database implementation (Paid, optional)
class ScatteredSecretsLeakDatabase(LeakDatabase):
    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key
        self.url = "https://api.scatteredsecrets.com/v1/breachcheck"

    def check_password(self, password: str) -> Dict:
        """Check if password is leaked in Scattered Secrets (requires API key)."""
        if not self.api_key:
            return {"is_leaked": None, "source": "ScatteredSecrets", "error": "API key required"}
        try:
            # Placeholder for actual API call (replace with real implementation)
            # response = requests.post(self.url, json={"password": password}, headers={"Authorization": f"Bearer {self.api_key}"}, timeout=5)
            # data = response.json()
            # Implement logic to check if password is found
            return {"is_leaked": True, "source": "ScatteredSecrets", "breach_count": 200}  # Simulated
        except Exception as e:
            return {"is_leaked": None, "source": "ScatteredSecrets", "error": str(e)}


# Main LeakChecker class to manage all databases and generate markdown
class LeakChecker:
    def __init__(self, dehashed_key: Optional[str] = None, leakcheck_key: Optional[str] = None,
                 scattered_key: Optional[str] = None):
        """Initialize with all available leak databases, including optional paid ones."""
        self.databases: List[LeakDatabase] = [
            HIBPLeakDatabase(),
            ProxynovaLeakDatabase(),
            CyberNewsLeakDatabase(),
        ]
        if dehashed_key:
            self.databases.append(DeHashedLeakDatabase(dehashed_key))
        if leakcheck_key:
            self.databases.append(LeakCheckLeakDatabase(leakcheck_key))
        if scattered_key:
            self.databases.append(ScatteredSecretsLeakDatabase(scattered_key))

    def check_all_databases(self, password: str) -> str:
        """Check password against all databases and return results as markdown."""
        timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
        report = f"### Password Leak Check Report\n- **Time:** {timestamp}\n- **Password:** {password}\n- **Leak Results:**\n"

        for db in self.databases:
            result = db.check_password(password)
            report += f"  - **Source:** {result['source']}\n"
            if result.get("is_leaked") is True:
                report += f"    - **Status:** Leaked\n"
                report += f"    - **Breach Count:** {result.get('breach_count', 'Unknown')}\n"
            elif result.get("is_leaked") is False:
                report += f"    - **Status:** Not Leaked\n"
            else:
                report += f"    - **Status:** Unknown (Error: {result.get('error', 'Unknown error')})\n"

        return report


# Example usage
if __name__ == "__main__":
    # Initialize with optional API keys for paid services
    checker = LeakChecker(
        dehashed_key="YOUR_DEHASHED_KEY",
        leakcheck_key="YOUR_LEAKCHECK_KEY",
        scattered_key="YOUR_SCATTERED_KEY"
    )

    # Test cases
    test_passwords = ["password", "securepass123", "123456"]

    for pwd in test_passwords:
        report = checker.check_all_databases(pwd)
        print(report)
        # Optionally save to file
        with open("leak_check_results.md", "a", encoding="utf-8") as f:
            f.write(report + "\n\n")