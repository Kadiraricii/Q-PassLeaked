import asyncio
import socket
import sys
import ipaddress

async def async_ftp_check(ip, port=21, timeout=5):
    """Asenkron olarak IP adresinde FTP sunucusunu kontrol eder."""
    try:
        # Soket bağlantısı oluştur ve zaman aşımı ayarla
        reader, writer = await asyncio.wait_for(
            asyncio.open_connection(ip, port), timeout=timeout
        )
        
        # Banner'ı al
        banner = (await reader.read(1024)).decode('utf-8').strip()
        print(f"[+] {ip}: Port {port} open - Banner: {banner}")
        
        # Anonim giriş denemesi (USER anonymous komutu)
        writer.write(b"USER anonymous\r\n")
        await writer.drain()
        response = (await reader.read(1024)).decode('utf-8').strip()
        
        if "331" in response or "230" in response:
            print(f"[!] {ip}: Anonymous login possible - Response: {response}")
        else:
            print(f"[-] {ip}: Anonymous login not allowed - Response: {response}")
        
        # Bağlantıyı kapat
        writer.close()
        await writer.wait_closed()
        
    except asyncio.TimeoutError:
        print(f"[-] {ip}: Port {port} timeout (closed or filtered)")
    except ConnectionRefusedError:
        print(f"[-] {ip}: Port {port} closed")
    except Exception as e:
        print(f"[!] {ip}: Error - {e}")

async def scan_ip_range(ip_range):
    """IP aralığını tarar ve her IP için FTP kontrolü yapar."""
    try:
        network = ipaddress.ip_network(ip_range, strict=False)
        tasks = []
        for ip in network.hosts():
            ip_str = str(ip)
            tasks.append(async_ftp_check(ip_str))
        
        # Tüm görevleri eşzamanlı çalıştır
        await asyncio.gather(*tasks)
    except ValueError as e:
        print(f"[!] Invalid IP range: {e}")

async def scan_single_ip(ip):
    """Tek bir IP adresini tarar."""
    await async_ftp_check(ip)

def main(target):
    """Ana fonksiyon: IP veya IP aralığını kontrol eder ve taramayı başlatır."""
    print(f"[*] Starting FTP server detection on {target}...")
    loop = asyncio.get_event_loop()
    
    if '/' in target:
        # IP aralığı tarama
        loop.run_until_complete(scan_ip_range(target))
    else:
        # Tek IP tarama
        loop.run_until_complete(scan_single_ip(target))

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python async_ftp_detector.py <target_ip_or_range>")
        print("Example: python async_ftp_detector.py 192.168.1.100")
        print("Example: python async_ftp_detector.py 192.168.1.0/24")
        sys.exit(1)
    
    target = sys.argv[1]
    main(target)