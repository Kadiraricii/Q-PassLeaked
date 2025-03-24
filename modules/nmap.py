import subprocess
import logging
import json
from typing import Dict, List, Optional
import os

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


class NmapScanner:
    def __init__(self):
        """Initialize NmapScanner and verify Nmap installation."""
        self.check_requirements()

    def check_requirements(self) -> None:
        """Verify that Nmap is installed on the system."""
        try:
            subprocess.run(['nmap', '-V'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)
            logger.info("Nmap is installed and accessible.")
        except subprocess.CalledProcessError:
            logger.error("Nmap is not installed or not found in PATH.")
            raise EnvironmentError("Nmap is required. Please install it.")

    def list_scripts(self) -> List[str]:
        """Return a list of available Nmap scripts."""
        try:
            result = subprocess.run(['nmap', '--script-help', 'all'], stdout=subprocess.PIPE,
                                    stderr=subprocess.PIPE, text=True, check=True)
            scripts = [line.strip() for line in result.stdout.splitlines() if line.strip()]
            return scripts
        except subprocess.CalledProcessError as e:
            logger.error(f"Failed to list scripts: {e.stderr}")
            return []

    def scan_network(self, hosts: str, ports: Optional[str] = None, arguments: str = '',
                     timing: Optional[str] = None, sudo: bool = False,
                     output_file: Optional[str] = None, output_format: str = 'normal',
                     script_args: Optional[str] = None, **kwargs) -> Dict:
        """
        Execute a customizable Nmap scan.

        Args:
            hosts (str): Target hosts (e.g., '192.168.1.1', '192.168.1.0/24').
            ports (Optional[str]): Port range (e.g., '22-443').
            arguments (str): Nmap arguments (e.g., '-sS -A').
            timing (Optional[str]): Timing template (e.g., 'T4').
            sudo (bool): Run with sudo for privileged scans.
            output_file (Optional[str]): File to save output.
            output_format (str): Output format ('normal', 'xml', 'json').
            script_args (Optional[str]): NSE script arguments (e.g., '--script vuln').
            **kwargs: Additional Nmap options (e.g., decoy='-D RND:10').

        Returns:
            Dict: Scan results parsed into a dictionary.

        Raises:
            subprocess.CalledProcessError: If the Nmap command fails.
        """
        cmd = ['nmap']
        if sudo:
            cmd.insert(0, 'sudo')
        cmd.append(hosts)

        if ports:
            cmd.extend(['-p', ports])
        if timing:
            cmd.extend(['-T', timing])
        if script_args:
            cmd.append(script_args)
        if arguments:
            cmd.extend(arguments.split())
        for key, value in kwargs.items():
            cmd.append(f'--{key}={value}')

        # Handle output
        if output_file:
            if output_format == 'xml':
                cmd.extend(['-oX', output_file])
            elif output_format == 'json':
                cmd.extend(['-oJ', output_file])
            else:
                cmd.extend(['-oN', output_file])

        logger.info(f"Executing Nmap command: {' '.join(cmd)}")
        try:
            result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                                    text=True, check=True)
            logger.info("Scan completed successfully.")
            return self.parse_output(result.stdout, output_file, output_format)
        except subprocess.CalledProcessError as e:
            logger.error(f"Scan failed: {e.stderr}")
            raise

    def parse_output(self, output: str, output_file: Optional[str], output_format: str) -> Dict:
        """Parse Nmap output into a dictionary."""
        result = {'raw_output': output}
        if output_file and output_format in ['xml', 'json']:
            try:
                with open(output_file, 'r') as f:
                    if output_format == 'json':
                        result.update(json.load(f))
                    else:  # XML
                        result['xml_content'] = f.read()  # Simplified; use an XML parser for full parsing
            except Exception as e:
                logger.error(f"Failed to parse output file: {e}")
        return result

    def get_open_ports(self, hosts: str, ports: Optional[str] = None, sudo: bool = False) -> List[int]:
        """Scan for open ports on the target hosts."""
        cmd = ['nmap', '-p', ports or '1-65535', hosts]
        if sudo:
            cmd.insert(0, 'sudo')
        try:
            result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                                    text=True, check=True)
            ports = []
            for line in result.stdout.splitlines():
                if '/tcp' in line or '/udp' in line:
                    port = int(line.split('/')[0])
                    ports.append(port)
            return ports
        except subprocess.CalledProcessError as e:
            logger.error(f"Failed to get open ports: {e.stderr}")
            return []