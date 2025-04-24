import socket
# import subprocess
# import re
from concurrent.futures import ThreadPoolExecutor, as_completed



def scan_port(target, port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(1)
    result = sock.connect_ex((target, port))
    sock.close()
    if result == 0:
        #print(f"Port {port} is open")
        return port
    return None

def scan(ip):
    # result = subprocess.run(['ipconfig'], capture_output=True, text=True)
    # ip_pattern = re.compile(r'IPv4 Address[^\d]*(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})')
    # ip_addresses = ip_pattern.findall(result.stdout)

    scan_list={}
    open_ports = []
    try:
        with ThreadPoolExecutor(max_workers=100) as executor:
            futures = {executor.submit(scan_port, ip, port): port for port in range(1, 1000)}
            for future in as_completed(futures):
                port = future.result() 
                if port is not None:
                    open_ports.append(port)
        target_dict = {ip: open_ports}
        scan_list.update(target_dict)
    
    except KeyboardInterrupt:
        print("\nScan interrupted by user. Shutting down...")
        executor.shutdown(wait=False, cancel_futures=True)

    return scan_list