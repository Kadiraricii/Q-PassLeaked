#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Subdomain Finder ve Takeover Aracı
----------------------------------
Bu araç, verilen bir alan adı için alt alan adlarını tespit eder
ve bunların arasında ele geçirilebilir (takeover) olanları belirler.

Kullanım:
    python subdomain_finder_takeover.py <alan_adı> [seçenekler]
    Örnek: python subdomain_finder_takeover.py example.com --output results
"""

import os
import sys
import subprocess
import argparse
import logging
import json
import time
import ssl
import whois
import socket
import dns.resolver
import requests
import certifi
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime
from urllib.parse import urlparse


class SubdomainFinderTakeover:
    """
    Subdomain bulma ve takeover tespit sınıfı
    """

    def __init__(self, domain, output_dir=None, timeout=10, max_workers=20, verify_ssl=False, verbose=False):
        """
        SubdomainFinderTakeover sınıfını başlatır

        Args:
            domain (str): Taranacak alan adı
            output_dir (str, optional): Çıktı dizini
            timeout (int): İstek zaman aşımı süresi (saniye)
            max_workers (int): Maksimum eşzamanlı iş parçacığı sayısı
            verify_ssl (bool): SSL sertifikalarını doğrulama
            verbose (bool): Ayrıntılı çıktı
        """
        self.domain = domain
        self.output_dir = output_dir or os.path.join(os.getcwd(), "logs", domain)
        self.timeout = timeout
        self.max_workers = max_workers
        self.verify_ssl = verify_ssl
        self.verbose = verbose  # <-- Make sure to add this line

        # Log dizinini oluştur
        os.makedirs(self.output_dir, exist_ok=True)

        # Logger yapılandırması
        log_level = logging.DEBUG if verbose else logging.INFO
        self.logger = self._setup_logger(log_level)

        # Bulunan subdomainleri depolamak için
        self.subdomains = set()

        # Takeover için savunmasız servisler veritabanı
        self.vulnerable_services = {
            'AWS S3 Bucket': ['s3.amazonaws.com', 'NoSuchBucket', 'The specified bucket does not exist'],
            'AWS CloudFront': ['cloudfront.net', 'The request could not be satisfied', 'Bad request'],
            'GitHub Pages': ['github.io', 'There isn\'t a GitHub Pages site here', '404: Not Found'],
            'Heroku': ['herokuapp.com', 'No such app', 'heroku'],
            'Vercel': ['vercel.app', '404: Not Found', 'The deployment could not be found'],
            'Netlify': ['netlify.app', 'Not found', 'netlify'],
            'Azure App Service': ['azurewebsites.net', 'Microsoft Azure App Service', '404 Not Found'],
            'Azure TrafficManager': ['trafficmanager.net', 'Page not found', 'Not found'],
            'Zendesk': ['zendesk.com', 'Help Center Closed', 'Zendesk'],
            'Shopify': ['myshopify.com', 'Sorry, this shop is currently unavailable', 'Shopify'],
            'Fastly': ['fastly.net', 'Fastly error: unknown domain', 'Fastly'],
            'Pantheon': ['pantheonsite.io', 'The gods are wise', '404 Not Found'],
            'Tumblr': ['tumblr.com', 'There\'s nothing here', 'Tumblr'],
            'WordPress': ['wordpress.com', 'Do you want to register', 'WordPress'],
            'Acquia': ['acquia-sites.com', 'No site found', 'The requested URL was not found'],
            'Ghost': ['ghost.io', 'The thing you were looking for is no longer here', 'Ghost'],
            'Cargo': ['cargocollective.com', '404 Not Found', 'Cargo'],
            'Webflow': ['webflow.io', 'The page you are looking for doesn\'t exist', 'Webflow'],
            'Surge.sh': ['surge.sh', '404 Not Found', 'Surge'],
            'Squarespace': ['squarespace.com', 'Website Expired', 'Squarespace'],
            'Fly.io': ['fly.dev', '404 Not Found', 'Fly.io'],
            'Brightcove': ['bcvp0rtal.com', 'Brightcove Error', 'Brightcove'],
            'Unbounce': ['unbounce.com', 'The requested URL was not found', 'Unbounce'],
            'Strikingly': ['strikinglydns.com', '404 Not Found', 'Strikingly'],
            'UptimeRobot': ['stats.uptimerobot.com', '404 Not Found', 'UptimeRobot'],
            'UserVoice': ['uservoice.com', 'This UserVoice is currently being set up', 'UserVoice'],
            'Pingdom': ['stats.pingdom.com', '404 Not Found', 'Pingdom'],
            'Amazon CloudFront': ['cloudfront.net', 'The request could not be satisfied', 'CloudFront'],
            'Desk': ['desk.com', 'Please try again', 'Desk'],
            'Tilda': ['tilda.ws', '404 Not Found', 'Tilda'],
            'Helpjuice': ['helpjuice.com', '404 Not Found', 'Helpjuice'],
            'HelpScout': ['helpscoutdocs.com', 'No settings were found', 'HelpScout'],
            'Campaign Monitor': ['createsend.com', '404 Not Found', 'Campaign Monitor'],
            'Digital Ocean': ['digitalocean.app', '404 Not Found', 'Digital Ocean'],
            'AWS Elastic Beanstalk': ['elasticbeanstalk.com', '404 Not Found', 'Elastic Beanstalk'],
            'Readthedocs': ['readthedocs.io', 'Not Found', 'readthedocs'],
            'BitBucket': ['bitbucket.io', '404 Not Found', 'BitBucket'],
            'Intercom': ['custom.intercom.help', '404 Not Found', 'Intercom'],
            'Firebase': ['firebaseapp.com', '404 Not Found', 'Firebase'],
            'Kinsta': ['kinsta.cloud', '404 Not Found', 'Kinsta'],
            'LaunchRock': ['launchrock.com', '404 Not Found', 'LaunchRock'],
            'GetResponse': ['gr8.com', '404 Not Found', 'GetResponse'],
            'Aftership': ['aftership.app', '404 Not Found', 'Aftership']
        }

        # HTTP başlıkları
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
            "Accept-Language": "en-US,en;q=0.5",
            "Connection": "keep-alive",
            "Upgrade-Insecure-Requests": "1"
        }

    def _setup_logger(self, log_level):
        """
        Logger yapılandırmasını ayarlar

        Args:
            log_level (int): Günlük kayıt seviyesi

        Returns:
            logging.Logger: Yapılandırılmış logger nesnesi
        """
        logger = logging.getLogger(__name__)
        logger.setLevel(log_level)

        # Konsol handler'ı
        console_handler = logging.StreamHandler()
        console_handler.setLevel(log_level)
        console_format = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
        console_handler.setFormatter(console_format)

        # Dosya handler'ı
        file_handler = logging.FileHandler(os.path.join(self.output_dir, f"{self.domain}_scan.log"))
        file_handler.setLevel(log_level)
        file_format = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
        file_handler.setFormatter(file_format)

        # Handler'ları ekle
        logger.addHandler(console_handler)
        logger.addHandler(file_handler)

        return logger

    def find_subdomains_with_subfinder(self):
        """
        Subfinder aracını kullanarak subdomainleri bulur

        Returns:
            list: Bulunan subdomain listesi
        """
        try:
            # Subfinder'ı çalıştır
            result = subprocess.run(
                ["subfinder", "-d", self.domain],
                capture_output=True,
                text=True,
                check=True
            )

            # Subfinder çıktısını işle
            subdomains = result.stdout.splitlines()

            # Sonuçları dosyaya kaydet
            output_file = os.path.join(self.output_dir, f"{self.domain}-subdomains.txt")
            with open(output_file, "w") as file:
                file.write("\n".join(subdomains))

            print(f"Found {len(subdomains)} subdomains for {self.domain}")

            # Bulunan subdomainleri set'e ekle
            for subdomain in subdomains:
                if subdomain.strip():
                    self.subdomains.add(subdomain.strip())

            return subdomains

        except FileNotFoundError:
            print(f"\033[91mError: Subfinder is not installed or added to PATH.\033[0m")
            return []

        except subprocess.CalledProcessError as e:
            print(f"\033[91mError: Failed to run Subfinder: {e}\033[0m")
            return []

    def load_subdomains_from_file(self, file_path):
        """
        Dosyadan subdomain listesini yükler

        Args:
            file_path (str): Subdomain listesi içeren dosyanın yolu

        Returns:
            list: Yüklenen subdomain listesi
        """
        if not os.path.exists(file_path):
            print(f"\033[91mError: File {file_path} not found\033[0m")
            return []

        with open(file_path, "r") as file:
            subdomains = [line.strip() for line in file if line.strip()]

        print(f"Loaded {len(subdomains)} subdomains from {file_path}")

        # Bulunan subdomainleri set'e ekle
        for subdomain in subdomains:
            if subdomain.strip():
                self.subdomains.add(subdomain.strip())

        return subdomains

    def get_domain_registration_info(self, domain):
        """
        Alan adı kayıt bilgilerini alır (süresi dolmuş alan adlarını kontrol etmek için)

        Args:
            domain (str): Kontrol edilecek alan adı

        Returns:
            dict: Alan adı kayıt bilgileri veya hata durumunda None
        """
        try:
            w = whois.whois(domain)
            result = {
                "registrar": w.registrar,
                "creation_date": None,
                "expiration_date": None,
                "updated_date": None,
                "is_registered": True if w.registrar else False
            }

            # Tarihleri düzgün şekilde işle
            if w.creation_date:
                if isinstance(w.creation_date, list):
                    result["creation_date"] = w.creation_date[0].strftime("%Y-%m-%d") if isinstance(w.creation_date[0],
                                                                                                    datetime) else str(
                        w.creation_date[0])
                else:
                    result["creation_date"] = w.creation_date.strftime("%Y-%m-%d") if isinstance(w.creation_date,
                                                                                                 datetime) else str(
                        w.creation_date)

            if w.expiration_date:
                if isinstance(w.expiration_date, list):
                    result["expiration_date"] = w.expiration_date[0].strftime("%Y-%m-%d") if isinstance(
                        w.expiration_date[0], datetime) else str(w.expiration_date[0])
                else:
                    result["expiration_date"] = w.expiration_date.strftime("%Y-%m-%d") if isinstance(w.expiration_date,
                                                                                                     datetime) else str(
                        w.expiration_date)

            if w.updated_date:
                if isinstance(w.updated_date, list):
                    result["updated_date"] = w.updated_date[0].strftime("%Y-%m-%d") if isinstance(w.updated_date[0],
                                                                                                  datetime) else str(
                        w.updated_date[0])
                else:
                    result["updated_date"] = w.updated_date.strftime("%Y-%m-%d") if isinstance(w.updated_date,
                                                                                               datetime) else str(
                        w.updated_date)

            return result
        except Exception as e:
            if self.verbose:
                print(f"\033[93mWarning: Error getting WHOIS for {domain}: {str(e)}\033[0m")
            return None

    def check_dns_configuration(self, subdomain):
        """
        Bir subdomain için DNS yapılandırmasını kontrol eder (A, AAAA, CNAME kayıtları dahil)

        Args:
            subdomain (str): Kontrol edilecek subdomain

        Returns:
            dict: DNS yapılandırma bilgisi
        """
        dns_info = {
            "a_records": [],
            "aaaa_records": [],
            "cname_records": [],
            "mx_records": [],
            "txt_records": [],
            "ns_records": [],
            "has_valid_dns": False
        }

        # A kayıtlarını kontrol et
        try:
            answers = dns.resolver.resolve(subdomain, 'A')
            dns_info["a_records"] = [str(answer) for answer in answers]
            dns_info["has_valid_dns"] = True
        except (dns.resolver.NoAnswer, dns.resolver.NXDOMAIN, dns.resolver.NoNameservers) as e:
            if self.verbose:
                print(f"Debug: No A records for {subdomain}")

        # AAAA kayıtlarını kontrol et
        try:
            answers = dns.resolver.resolve(subdomain, 'AAAA')
            dns_info["aaaa_records"] = [str(answer) for answer in answers]
            dns_info["has_valid_dns"] = True
        except (dns.resolver.NoAnswer, dns.resolver.NXDOMAIN, dns.resolver.NoNameservers) as e:
            if self.verbose:
                print(f"Debug: No AAAA records for {subdomain}")

        # CNAME kayıtlarını kontrol et
        try:
            answers = dns.resolver.resolve(subdomain, 'CNAME')
            dns_info["cname_records"] = [str(answer.target).rstrip('.') for answer in answers]
            dns_info["has_valid_dns"] = True
        except (dns.resolver.NoAnswer, dns.resolver.NXDOMAIN, dns.resolver.NoNameservers) as e:
            if self.verbose:
                print(f"Debug: No CNAME records for {subdomain}")

        # MX kayıtlarını kontrol et
        try:
            answers = dns.resolver.resolve(subdomain, 'MX')
            dns_info["mx_records"] = [str(answer.exchange).rstrip('.') for answer in answers]
            dns_info["has_valid_dns"] = True
        except (dns.resolver.NoAnswer, dns.resolver.NXDOMAIN, dns.resolver.NoNameservers) as e:
            if self.verbose:
                print(f"Debug: No MX records for {subdomain}")

        # TXT kayıtlarını kontrol et
        try:
            answers = dns.resolver.resolve(subdomain, 'TXT')
            dns_info["txt_records"] = [str(answer).strip('"') for answer in answers]
            dns_info["has_valid_dns"] = True
        except (dns.resolver.NoAnswer, dns.resolver.NXDOMAIN, dns.resolver.NoNameservers) as e:
            if self.verbose:
                print(f"Debug: No TXT records for {subdomain}")

        # NS kayıtlarını kontrol et
        try:
            answers = dns.resolver.resolve(subdomain, 'NS')
            dns_info["ns_records"] = [str(answer).rstrip('.') for answer in answers]
            dns_info["has_valid_dns"] = True
        except (dns.resolver.NoAnswer, dns.resolver.NXDOMAIN, dns.resolver.NoNameservers) as e:
            if self.verbose:
                print(f"Debug: No NS records for {subdomain}")

        return dns_info

    def check_website_availability(self, subdomain):
        """
        Bir web sitesinin HTTP/HTTPS üzerinden erişilebilir olup olmadığını kontrol eder

        Args:
            subdomain (str): Kontrol edilecek subdomain

        Returns:
            dict: Web sitesi erişilebilirlik bilgisi
        """
        result = {
            "http_status": None,
            "https_status": None,
            "response_time": None,
            "http_response": None,
            "https_response": None,
            "http_headers": None,
            "https_headers": None,
            "ssl_info": None,
            "is_accessible": False,
            "redirect_chain": []
        }

        # HTTP dene
        try:
            start_time = time.time()
            http_response = requests.get(
                f"http://{subdomain}",
                headers=self.headers,
                timeout=self.timeout,
                verify=certifi.where() if self.verify_ssl else False,
                allow_redirects=True
            )
            response_time = time.time() - start_time

            result["http_status"] = http_response.status_code
            result["response_time"] = response_time
            result["http_headers"] = dict(http_response.headers)
            result["http_response"] = http_response.text[:500]  # İlk 500 karakteri sakla

            # Yönlendirme zincirini takip et
            if http_response.history:
                result["redirect_chain"] = [{"url": r.url, "status_code": r.status_code} for r in http_response.history]
                result["redirect_chain"].append({"url": http_response.url, "status_code": http_response.status_code})

            if 200 <= http_response.status_code < 400:
                result["is_accessible"] = True
        except requests.RequestException as e:
            if self.verbose:
                print(f"Debug: HTTP error for {subdomain}: {str(e)}")
            result["http_status"] = "Error"

        # HTTPS dene
        try:
            https_response = requests.get(
                f"https://{subdomain}",
                headers=self.headers,
                timeout=self.timeout,
                verify=certifi.where() if self.verify_ssl else False,
                allow_redirects=True
            )

            result["https_status"] = https_response.status_code
            result["https_headers"] = dict(https_response.headers)
            result["https_response"] = https_response.text[:500]  # İlk 500 karakteri sakla

            # Yönlendirme zinciri henüz izlenmemişse izle
            if https_response.history and not result["redirect_chain"]:
                result["redirect_chain"] = [{"url": r.url, "status_code": r.status_code} for r in
                                            https_response.history]
                result["redirect_chain"].append({"url": https_response.url, "status_code": https_response.status_code})

            if 200 <= https_response.status_code < 400:
                result["is_accessible"] = True

            # SSL bilgilerini al
            try:
                hostname = subdomain
                context = ssl.create_default_context()
                context.check_hostname = False
                context.verify_mode = ssl.CERT_NONE

                with socket.create_connection((hostname, 443), timeout=self.timeout) as sock:
                    with context.wrap_socket(sock, server_hostname=hostname) as ssock:
                        cert = ssock.getpeercert()
                        result["ssl_info"] = {
                            "issuer": dict(x[0] for x in cert['issuer']),
                            "subject": dict(x[0] for x in cert['subject']),
                            "version": cert['version'],
                            "notBefore": cert['notBefore'],
                            "notAfter": cert['notAfter']
                        }

                        # SAN (Subject Alternative Names) kontrolü
                        if 'subjectAltName' in cert:
                            result["ssl_info"]["subjectAltName"] = cert['subjectAltName']
            except Exception as e:
                if self.verbose:
                    print(f"Debug: SSL info error for {subdomain}: {str(e)}")
        except requests.RequestException as e:
            if self.verbose:
                print(f"Debug: HTTPS error for {subdomain}: {str(e)}")
            result["https_status"] = "Error"

        return result

    def check_for_misconfigurations(self, dns_info, website_info):
        """
        Takeover güvenlik açığına işaret edebilecek ek yanlış yapılandırmaları arar

        Args:
            dns_info (dict): DNS yapılandırma bilgisi
            website_info (dict): Web sitesi erişilebilirlik bilgisi

        Returns:
            dict: Bulunursa yanlış yapılandırma bilgisi, aksi takdirde None
        """
        # Asılı kalan kayıtları kontrol et (çözünmeyen CNAME)
        if dns_info.get("cname_records") and not dns_info.get("a_records") and not website_info.get("is_accessible"):
            cname = dns_info["cname_records"][0]
            try:
                socket.gethostbyname(cname)
            except socket.gaierror:
                return {
                    "type": "Dangling CNAME",
                    "details": f"CNAME kaydı, IP'ye çözünmeyen {cname}'e işaret ediyor"
                }

        # Var olmayan nameserver'a NS delegasyonunu kontrol et
        if dns_info.get("ns_records"):
            for ns in dns_info["ns_records"]:
                try:
                    socket.gethostbyname(ns)
                except socket.gaierror:
                    return {
                        "type": "Dangling NS",
                        "details": f"NS kaydı, IP'ye çözünmeyen {ns}'e işaret ediyor"
                    }

        # Eksik SPF ancak MX kayıtları var
        has_spf = False
        for txt in dns_info.get("txt_records", []):
            if "v=spf1" in txt:
                has_spf = True
                break

        if dns_info.get("mx_records") and not has_spf:
            return {
                "type": "Missing SPF",
                "details": "Alan adında MX kayıtları var ancak SPF kaydı yok, potansiyel e-posta güvenlik sorunu"
            }

        # Şüpheli yönlendirmeleri kontrol et
        if website_info.get("redirect_chain"):
            for redirect in website_info["redirect_chain"]:
                if any(service in redirect["url"] for service in ["s3.amazonaws.com", "github.io", "herokuapp.com"]):
                    return {
                        "type": "Suspicious Redirect",
                        "details": f"Potansiyel olarak savunmasız bir hizmete yönlendiriyor: {redirect['url']}"
                    }

        return None

    def check_takeover_vulnerability(self, subdomain):
        """
        Bir subdomain'i takeover güvenlik açıkları için kontrol eder

        Args:
            subdomain (str): Kontrol edilecek subdomain

        Returns:
            dict: Güvenlik açığı bilgisi veya güvenlik açığı bulunamazsa None
        """
        if self.verbose:
            print(f"Checking takeover vulnerability for {subdomain}")

        try:
            # DNS yapılandırmasını kontrol et
            dns_info = self.check_dns_configuration(subdomain)

            # Web sitesi erişilebilirliğini kontrol et
            website_info = self.check_website_availability(subdomain)

            # Alan adı kaydını kontrol et
            whois_info = self.get_domain_registration_info(subdomain)

            # Ek yanlış yapılandırmaları kontrol et
            misconfiguration = self.check_for_misconfigurations(dns_info, website_info)

            # Güvenlik açığı tespitini başlat
            vulnerability_detected = False
            vulnerability_details = {}

            # Durum 1: CNAME bir hizmete işaret eder, ancak içerik hata parmak iziyle eşleşir
            if dns_info["cname_records"]:
                for cname in dns_info["cname_records"]:
                    for service, fingerprints in self.vulnerable_services.items():
                        cname_pattern = fingerprints[0]
                        error_pattern = fingerprints[1]
                        additional_pattern = fingerprints[2] if len(fingerprints) > 2 else None

                        if cname_pattern.lower() in cname.lower():
                            # Web sitesi içeriğinin hata mesajı içerip içermediğini kontrol et
                            http_content = website_info.get("http_response", "")
                            https_content = website_info.get("https_response", "")
                            content = http_content or https_content or ""

                            if error_pattern.lower() in content.lower() or (
                                    additional_pattern and additional_pattern.lower() in content.lower()):
                                vulnerability_detected = True
                                vulnerability_details = {
                                    "type": "CNAME Error Pattern",
                                    "service": service,
                                    "cname": cname,
                                    "error_pattern": error_pattern,
                                    "confidence": "High",
                                    "description": f"The subdomain has a CNAME record pointing to {service} ({cname}) and returns an error message indicating the resource doesn't exist."
                                }
                                break

                    if vulnerability_detected:
                        break

            # Durum 2: CNAME var ama çözünmüyor (asılı kalan CNAME)
            if not vulnerability_detected and dns_info["cname_records"] and not website_info["is_accessible"] and not \
            dns_info["a_records"]:
                for cname in dns_info["cname_records"]:
                    try:
                        # CNAME hedefini çözmeyi dene
                        socket.gethostbyname(cname)
                    except socket.gaierror:
                        # CNAME hedefi çözünmüyor - potansiyel asılı kalan CNAME
                        vulnerability_detected = True
                        vulnerability_details = {
                            "type": "Dangling CNAME",
                            "cname": cname,
                            "confidence": "Medium",
                            "description": f"The subdomain has a CNAME record pointing to {cname} which doesn't resolve to an IP address."
                        }

                        # Hizmeti belirlemeye çalış
                        for service, fingerprints in self.vulnerable_services.items():
                            cname_pattern = fingerprints[0]
                            if cname_pattern.lower() in cname.lower():
                                vulnerability_details["service"] = service
                                vulnerability_details["confidence"] = "High"
                                vulnerability_details[
                                    "description"] = f"The subdomain has a CNAME record pointing to {service} ({cname}) which doesn't resolve to an IP address."
                                break
                        break

            # Durum 3: DNS kayıtları var ama web sitesi belirli hata kodları döndürüyor
            if not vulnerability_detected and dns_info["has_valid_dns"] and website_info.get("http_status") in [404,
                                                                                                                500,
                                                                                                                502,
                                                                                                                503]:
                # Herhangi bir yaygın üçüncü taraf barındırma tespit edilip edilmediğini kontrol et
                if any(provider in str(dns_info) for provider in
                       ['aws', 'amazon', 'azure', 'heroku', 'github', 'vercel']):
                    vulnerability_detected = True
                    vulnerability_details = {
                        "type": "Third-Party Service Error",
                        "http_status": website_info.get("http_status"),
                        "confidence": "Medium",
                        "description": f"The subdomain has valid DNS records pointing to a third-party service, but returns a {website_info.get('http_status')} error code."
                    }
                else:
                    # Bu daha düşük güven göstergesidir
                    vulnerability_detected = True
                    vulnerability_details = {
                        "type": "DNS Record with Error Response",
                        "http_status": website_info.get("http_status"),
                        "confidence": "Low",
                        "description": f"The subdomain has valid DNS records but returns a {website_info.get('http_status')} error code."
                    }

            # Durum 4: Ek yanlış yapılandırmalar
            if not vulnerability_detected and misconfiguration:
                vulnerability_detected = True
                vulnerability_details = {
                    "type": misconfiguration["type"],
                    "confidence": "Medium" if misconfiguration["type"] in ["Dangling CNAME", "Dangling NS",
                                                                           "Suspicious Redirect"] else "Low",
                    "description": misconfiguration["details"]
                }

            # Bir güvenlik açığı tespit edildiyse, tam sonucu oluştur
            if vulnerability_detected:
                result = {
                    "subdomain": subdomain,
                    "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    "dns_info": dns_info,
                    "website_info": website_info,
                    "whois_info": whois_info,
                    "vulnerable": True,
                    "service": vulnerability_details.get("service", "Unknown"),
                    "vulnerability_type": vulnerability_details.get("type", "Unknown"),
                    "confidence": vulnerability_details.get("confidence", "Low"),
                    "cname": vulnerability_details.get("cname", None),
                    "description": vulnerability_details.get("description", None),
                    "exploitation_difficulty": self.assess_exploitation_difficulty(vulnerability_details, dns_info,
                                                                                   website_info),
                    "mitigation": self.suggest_mitigation(vulnerability_details)
                }

                # Güvenlik açığı verilerini JSON olarak kaydet
                output_file = os.path.join(self.output_dir, f"takeover_{subdomain.replace('.', '_')}.json")
                with open(output_file, "w") as f:
                    json.dump(result, f, indent=4)

                print(
                    f"\033[93m[!] Potential {result['confidence']} confidence takeover vulnerability found in {subdomain} ({result['service']})\033[0m")
                return result

            return None
        except Exception as e:
            print(f"\033[91mError checking {subdomain}: {str(e)}\033[0m")
            return None

    def assess_exploitation_difficulty(self, vulnerability_details, dns_info, website_info):
        """
        Güvenlik açığını istismar etme zorluğunu değerlendirir

        Args:
            vulnerability_details (dict): Güvenlik açığının ayrıntıları
            dns_info (dict): DNS yapılandırma bilgisi
            website_info (dict): Web sitesi erişilebilirlik bilgisi

        Returns:
            str: Zorluk değerlendirmesi (Easy, Medium, Hard)
        """
        vuln_type = vulnerability_details.get("type", "")
        service = vulnerability_details.get("service", "Unknown")

        if vuln_type == "CNAME Error Pattern":
            # Genellikle talep etmesi kolay olan hizmetler
            easy_services = ["GitHub Pages", "Heroku", "Vercel", "Netlify", "Surge.sh"]
            if service in easy_services:
                return "Easy"

            # Hesap sahipliği veya doğrulama gerektiren hizmetler
            medium_services = ["AWS S3 Bucket", "Firebase", "Ghost", "WordPress"]
            if service in medium_services:
                return "Medium"

            return "Hard"

        elif vuln_type == "Dangling CNAME":
            # CNAME bir üçüncü taraf hizmetindeki özel bir alan adına işaret ediyorsa
            if service != "Unknown":
                return "Medium"
            return "Hard"

        elif "DNS Record with Error" in vuln_type:
            return "Hard"

        elif "Dangling NS" in vuln_type:
            return "Medium"

        elif "Suspicious Redirect" in vuln_type:
            return "Medium"

        return "Medium"

    def suggest_mitigation(self, vulnerability_details):
        """
        Güvenlik açığına dayalı olarak azaltma stratejileri önerir

        Args:
            vulnerability_details (dict): Güvenlik açığının ayrıntıları

        Returns:
            str: Azaltma önerisi
        """
        vuln_type = vulnerability_details.get("type", "")
        service = vulnerability_details.get("service", "Unknown")

        if vuln_type == "CNAME Error Pattern":
            return f"CNAME kaydını kaldırın veya {service} üzerindeki kaynağı yeniden talep edin. DNS kayıtlarını ona yönlendirmeden önce hizmeti düzgün bir şekilde kurduğunuzdan emin olun."

        elif vuln_type == "Dangling CNAME":
            return "Var olmayan bir uç noktaya işaret eden CNAME kaydını kaldırın. Hizmet hala gerekiyorsa, hedef hizmette kaynağı yeniden oluşturun."

        elif "DNS Record with Error" in vuln_type:
            return "Kaynağın hedef hizmette var olduğunu doğrulayın. Hizmet artık kullanılmıyorsa, DNS kaydını kaldırın."

        elif "Dangling NS" in vuln_type:
            return "NS kayıtlarınızı geçerli ad sunucularına işaret edecek şekilde güncelleyin. Artık var olmayan ad sunucularına yapılan delegasyonları kaldırın."

        elif "Suspicious Redirect" in vuln_type:
            return "Yönlendirme zincirinizi kontrol edin ve kontrolünüzde olmayan hizmetlere işaret etmediğinden emin olun. İstenmeyen yönlendirmeleri kaldırmak için yapılandırmanızı güncelleyin."

        elif "Missing SPF" in vuln_type:
            return "E-posta sahteciliğine karşı koruma için bir SPF kaydı ekleyin. Örneğin: 'v=spf1 mx -all'"

        return "DNS yapılandırmasını gözden geçirin ve artık kullanılmayan hizmetlere veya kaynaklara yapılan referansları kaldırın."

    def print_status(self, message, message_type="info"):
        """
        Ekrana renkli bir durum mesajı yazdırır

        Args:
            message (str): Yazdırılacak mesaj
            message_type (str): Mesaj tipi (info, success, warning, error)
        """
        if message_type == "info":
            print(f"\033[94m{message}\033[0m")
        elif message_type == "success":
            print(f"\033[92m{message}\033[0m")
        elif message_type == "warning":
            print(f"\033[93m{message}\033[0m")
        elif message_type == "error":
            print(f"\033[91m{message}\033[0m")
        else:
            print(message)

    def run(self, input_file=None):
        """
        Subdomain finder ve takeover tarayıcısını çalıştırır

        Args:
            input_file (str, optional): Subdomain listesi içeren giriş dosyası.
                                        Eğer None ise, subfinder kullanarak subdomainleri otomatik olarak bulmaya çalışır.

        Returns:
            dict: Tarama sonuçları
        """
        start_time = time.time()
        print(f"Starting subdomain finder and takeover scan for {self.domain}")

        # Adım 1: Subdomainleri bul
        if input_file:
            # Dosyadan subdomainleri yükle
            print(f"Loading subdomains from file: {input_file}")
            self.load_subdomains_from_file(input_file)
        else:
            # Subfinder ile subdomainleri bul
            print(f"Starting subdomain finder for {self.domain}")
            self.find_subdomains_with_subfinder()

        if not self.subdomains:
            print(f"\033[91mNo subdomains found for {self.domain}, terminating scan\033[0m")
            return {
                "error": "No subdomains found",
                "domain": self.domain
            }

        print(f"Found {len(self.subdomains)} subdomains")

        # Tüm bulunan subdomainleri dosyaya yaz
        all_subdomains_file = os.path.join(self.output_dir, f"{self.domain}-all-subdomains.txt")
        with open(all_subdomains_file, "w") as f:
            for subdomain in sorted(self.subdomains):
                f.write(f"{subdomain}\n")

        print(f"All subdomains saved to: {all_subdomains_file}")

        # Adım 2: Takeover güvenlik açıklarını kontrol et
        print(f"Starting subdomain takeover module for {self.domain}")
        print(f"Scanning {len(self.subdomains)} subdomains for takeover vulnerabilities")

        vulnerable_subdomains = []
        with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
            future_to_subdomain = {executor.submit(self.check_takeover_vulnerability, subdomain): subdomain for
                                   subdomain in self.subdomains}

            completed = 0
            total = len(self.subdomains)
            for future in future_to_subdomain:
                result = future.result()
                if result:
                    vulnerable_subdomains.append(result)

                # İlerleme göster
                completed += 1
                if completed % 10 == 0 or completed == total:
                    print(f"\rProgress: {completed}/{total} subdomains checked", end="")
            print()  # Yeni satır

        # Sonuçları güven seviyesine göre sırala
        confidence_order = {"High": 0, "Medium": 1, "Low": 2}
        vulnerable_subdomains.sort(key=lambda x: confidence_order.get(x.get("confidence", "Low"), 3))

        # İstatistikleri hesapla
        scan_time = time.time() - start_time
        high_confidence = sum(1 for r in vulnerable_subdomains if r.get("confidence") == "High")
        medium_confidence = sum(1 for r in vulnerable_subdomains if r.get("confidence") == "Medium")
        low_confidence = sum(1 for r in vulnerable_subdomains if r.get("confidence") == "Low")

        # Özet JSON oluştur
        summary = {
            "scan_info": {
                "domain": self.domain,
                "subdomains_scanned": len(self.subdomains),
                "vulnerable_subdomains": len(vulnerable_subdomains),
                "scan_time_seconds": round(scan_time, 2),
                "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "services_checked": len(self.vulnerable_services)
            },
            "statistics": {
                "vulnerable_subdomains_count": len(vulnerable_subdomains),
                "high_confidence": high_confidence,
                "medium_confidence": medium_confidence,
                "low_confidence": low_confidence,
                "by_vulnerability_type": {},
                "by_service": {}
            },
            "vulnerable_subdomains": vulnerable_subdomains
        }

        # Güvenlik açığı türüne ve hizmete göre say
        vuln_types = {}
        services = {}

        for result in vulnerable_subdomains:
            vuln_type = result.get("vulnerability_type", "Unknown")
            service = result.get("service", "Unknown")

            if vuln_type in vuln_types:
                vuln_types[vuln_type] += 1
            else:
                vuln_types[vuln_type] = 1

            if service in services:
                services[service] += 1
            else:
                services[service] = 1

        summary["statistics"]["by_vulnerability_type"] = vuln_types
        summary["statistics"]["by_service"] = services

        # Özeti dosyaya kaydet
        summary_file = os.path.join(self.output_dir, f"subdomain_takeover_summary_{self.domain}.json")
        with open(summary_file, "w") as f:
            json.dump(summary, f, indent=4)

        # Sonuçları ekrana yazdır
        if vulnerable_subdomains:
            print("\n\033[93m" + "=" * 50 + "\033[0m")
            print("\033[93m--- SUBDOMAIN TAKEOVER VULNERABILITIES ---\033[0m")
            print("\033[93m" + "=" * 50 + "\033[0m")
            print(f"\033[94mTotal Vulnerable Subdomains:\033[0m {len(vulnerable_subdomains)}")
            print(f"\033[91mHigh Confidence:\033[0m {high_confidence}")
            print(f"\033[93mMedium Confidence:\033[0m {medium_confidence}")
            print(f"\033[94mLow Confidence:\033[0m {low_confidence}")

            if high_confidence > 0:
                print("\n\033[91mCritical Vulnerabilities:\033[0m")
                for subdomain in vulnerable_subdomains:
                    if subdomain["confidence"] == "High":
                        print(
                            f"  \033[91m{subdomain['subdomain']}\033[0m - {subdomain['vulnerability_type']} ({subdomain['service']})")
                        print(f"    → \033[93mExploitation Difficulty:\033[0m {subdomain['exploitation_difficulty']}")
                        print(f"    → \033[92mMitigation:\033[0m {subdomain['mitigation']}")

            print(f"\n\033[94mDetailed results saved to:\033[0m {summary_file}")
        else:
            print("\n\033[92mNo subdomain takeover vulnerabilities found.\033[0m")

        return summary


def main():
    """Ana fonksiyon"""
    import warnings
    from urllib3.exceptions import InsecureRequestWarning
    warnings.filterwarnings("ignore", category=InsecureRequestWarning)

    parser = argparse.ArgumentParser(description="Subdomain Finder ve Takeover Aracı")
    parser.add_argument("domain", help="Taranacak alan adı")
    parser.add_argument("-i", "--input", help="Subdomain listesi içeren giriş dosyası")
    parser.add_argument("-o", "--output", help="Çıktı dizini")
    parser.add_argument("-t", "--timeout", type=int, default=10, help="İstek zaman aşımı süresi (saniye)")
    parser.add_argument("-w", "--workers", type=int, default=20, help="Maksimum eşzamanlı iş parçacığı sayısı")
    parser.add_argument("-v", "--verbose", action="store_true", help="Ayrıntılı çıktı")
    parser.add_argument("--verify-ssl", action="store_true", help="SSL sertifikalarını doğrula")

    args = parser.parse_args()

    # Scanner'ı başlat
    scanner = SubdomainFinderTakeover(
        domain=args.domain,
        output_dir=args.output,
        timeout=args.timeout,
        max_workers=args.workers,
        verify_ssl=args.verify_ssl,
        verbose=args.verbose
    )

    # Taramayı çalıştır
    scanner.run(input_file=args.input)


if __name__ == "__main__":
    main()