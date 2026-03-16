#!/usr/bin/env python3
"""
TCP Port Scanner
Hedef IP adresinde açık portları tespit eder
Author: Efe Altıparmakoğlu
"""

import socket
import argparse
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime


def scan_port(ip: str, port: int) -> bool:
    """Tek bir portu tara"""
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(1)
        result = sock.connect_ex((ip, port))
        sock.close()
        return result == 0
    except:
        return False


def scan_ports(ip: str, start_port: int = 1, end_port: int = 1024, threads: int = 100):
    """Port aralığını tara"""
    print(f"🔍 Hedef: {ip}")
    print(f"📊 Port aralığı: {start_port}-{end_port}")
    print(f"⚡ Thread sayısı: {threads}\n")
    
    open_ports = []
    start_time = datetime.now()
    
    with ThreadPoolExecutor(max_workers=threads) as executor:
        futures = {executor.submit(scan_port, ip, port): port 
                   for port in range(start_port, end_port + 1)}
        
        for future in futures:
            port = futures[future]
            if future.result():
                open_ports.append(port)
                print(f"✅ Port {port} AÇIK")
    
    duration = (datetime.now() - start_time).total_seconds()
    
    print(f"\n{'='*50}")
    print(f"📊 Tarama tamamlandı: {duration:.2f} saniye")
    print(f"🔓 Açık port sayısı: {len(open_ports)}")
    
    if open_ports:
        print(f"\n📝 Açık portlar: {', '.join(map(str, open_ports))}")
    else:
        print("\n❌ Açık port bulunamadı")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="TCP Port Scanner")
    parser.add_argument("target", help="Hedef IP adresi")
    parser.add_argument("-s", "--start", type=int, default=1, help="Başlangıç portu")
    parser.add_argument("-e", "--end", type=int, default=1024, help="Bitiş portu")
    parser.add_argument("-t", "--threads", type=int, default=100, help="Thread sayısı")
    
    args = parser.parse_args()
    scan_ports(args.target, args.start, args.end, args.threads)
