import nmap
from flask import jsonify

def scan_cidr_range(cidr_range='10.0.0.0/16', write_file=False):
    nmap_path = [r"C:\Program Files (x86)\Nmap\nmap.exe",]
    nm = nmap.PortScanner(nmap_search_path=nmap_path)
    
    # Perform a fast scan (-F) to quickly identify hosts
    nm.scan(hosts=cidr_range, arguments='-sn --min-rate 1300')
    
    if write_file == True:
        ip_list = {}
        for host in nm.all_hosts():
            if nm[host].state() == 'up':
                ip_list.append(host+', ')

        with open('hosts.txt', 'w') as file:
            file.write(ip_list)
        return jsonify({"status": "success"})
    else:
        # Extract and print the list of hosts that are up
        hosts_up = [host for host in nm.all_hosts() if nm[host].state() == 'up']
        return hosts_up