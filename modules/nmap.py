# modules/nmap.py
import nmap
import logging
import subprocess
import platform
from typing import Dict, List, Optional

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


class NmapScanner:
    """A class to handle comprehensive Nmap scanning operations with support for all Nmap parameters."""

    def __init__(self):
        self.scanner = nmap.PortScanner()

    def scan_network(self, hosts: str, ports: Optional[str] = None, arguments: str = '',
                     timing: Optional[str] = None, sudo: bool = False, **kwargs) -> Dict:
        """
        Perform an Nmap scan with full support for all Nmap parameters.

        Args:
            hosts (str): Target hosts (e.g., '192.168.1.1', 'example.com', '192.168.1.0/24')
            ports (str, optional): Port range (e.g., '22-443', '1-65535', 'U:53,111,T:21-25')
            arguments (str, optional): Nmap scan arguments (e.g., '-sS', '-sU', '-A', '-sn')
            timing (str, optional): Timing template (e.g., 'T0' to 'T5')
            sudo (bool, optional): Run scan with sudo (for privileged scans like SYN scan)
            **kwargs: Additional Nmap arguments as key-value pairs (e.g., verbose='-v', os_detection='-O')

        Returns:
            Dict: Scan results parsed into a dictionary containing hosts and scan info.

        Examples:
            - Basic SYN scan: scan_network('192.168.1.1', ports='22-443', arguments='-sS')
            - Ping scan: scan_network('192.168.1.0/24', arguments='-sn')
            - All ports scan: scan_network('example.com', arguments='-p- -sV', timing='T4')
        """
        try:
            # Construct the argument string
            args = arguments.strip()
            if ports:
                args += f" -p {ports}"
            if timing and timing in ['T0', 'T1', 'T2', 'T3', 'T4', 'T5']:
                args += f" -{timing}"
            for key, value in kwargs.items():
                args += f" -{key} {value}" if value else f" -{key}"

            logger.info(f"Starting Nmap scan on {hosts} with arguments: {args}")
            self.scanner.scan(hosts=hosts, arguments=args, sudo=sudo)
            return {
                'hosts': self.scanner.all_hosts(),
                'scan_info': self.scanner.scaninfo(),
                'command_line': self.scanner.command_line()
            }
        except nmap.PortScannerError as e:
            logger.error(f"Nmap scan failed: {str(e)}")
            raise
        except Exception as e:
            logger.error(f"Unexpected error during scan: {str(e)}")
            raise

    def get_open_ports(self, host: str, protocol: str = 'tcp') -> List[int]:
        """
        Retrieve open ports for a specific host and protocol from the last scan.

        Args:
            host (str): Target host (e.g., '192.168.1.1')
            protocol (str, optional): Protocol to check ('tcp', 'udp', 'sctp'). Defaults to 'tcp'.

        Returns:
            List[int]: List of open port numbers for the specified protocol.
        """
        try:
            if host not in self.scanner.all_hosts():
                logger.warning(f"Host {host} not found in scan results.")
                return []
            if protocol not in self.scanner[host]:
                logger.warning(f"No {protocol} scan data for host {host}.")
                return []
            ports = self.scanner[host][protocol].keys()
            return [port for port in ports if self.scanner[host][protocol][port]['state'] == 'open']
        except Exception as e:
            logger.error(f"Error retrieving open ports for {host}: {str(e)}")
            return []


def check_requirements() -> bool:
    """Check if Nmap is installed on the system."""
    try:
        result = subprocess.run(['nmap', '--version'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        if result.returncode == 0:
            logger.info("Nmap is installed.")
            return True
        else:
            logger.error("Nmap is not installed or not functioning correctly.")
            return False
    except FileNotFoundError:
        logger.error("Nmap is not installed. Please install Nmap to use this module.")
        return False


def main():
    """CLI interface for testing the Nmap module."""
    if not check_requirements():
        logger.info("Please install Nmap. Refer to the installation guide for your platform.")
        return

    scanner = NmapScanner()
    hosts = input("Enter target hosts (e.g., '192.168.1.1' or '192.168.1.0/24'): ")
    ports = input("Enter port range (e.g., '22-443', 'U:53,T:80', press Enter for all): ") or None
    arguments = input("Enter Nmap scan arguments (e.g., '-sS -sV', '-sn', press Enter for none): ") or ''
    timing = input("Enter timing template (e.g., 'T3', press Enter for default): ") or None
    sudo = input("Run with sudo? (y/N): ").lower() == 'y'

    result = scanner.scan_network(hosts, ports, arguments, timing, sudo)
    print(f"Scan Info: {result['scan_info']}")
    print(f"Command Line: {result['command_line']}")
    for host in result['hosts']:
        open_tcp_ports = scanner.get_open_ports(host, 'tcp')
        open_udp_ports = scanner.get_open_ports(host, 'udp')
        print(f"Host: {host}, Open TCP Ports: {open_tcp_ports}, Open UDP Ports: {open_udp_ports}")


if __name__ == "__main__":
    main()