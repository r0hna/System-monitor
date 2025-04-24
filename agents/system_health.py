import psutil
from os import system
import subprocess
import re
from flask import jsonify
import platform

def get_system_health():
    # CPU usage
    cpu_usage = psutil.cpu_percent(interval=1)
    
    # Memory usage
    memory = psutil.virtual_memory()
    memory_usage = memory.percent
    
    # Disk usage
    disk = psutil.disk_usage('/')
    disk_usage = disk.percent
    
    # Network stats
    net_io = psutil.net_io_counters()
    network_stats = {
        "bytes_sent": net_io.bytes_sent,
        "bytes_recv": net_io.bytes_recv,
        "packets_sent": net_io.packets_sent, 
        "packets_recv": net_io.packets_recv
    }

    def get_ip_address():
        # getting the ip list

        if platform.system() == "Windows":
            result = subprocess.run(['ipconfig'], capture_output=True, text=True)

            # Regular expression to match IP addresses but exclude common subnet masks
            ip_pattern = re.compile(r'IPv4 Address[^\d]*(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})')
            #subnet_masks = ['255.255.255.0', '255.255.0.0', '255.0.0.0']
            
            # Find all IP addresses
            ip_addresses = ip_pattern.findall(result.stdout)
            
            #IP address list
            return ip_addresses

        elif platform.system() in ["MacOs", "Linux", "Macos", "linux"]:
            result = subprocess.run(['ifconfig'], capture_output=True, text=True)

            # Regular expression to match IP addresses but exclude common subnet masks
            ip_pattern = re.compile(r'IPv4 Address[^\d]*(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})')
            #subnet_masks = ['255.255.255.0', '255.255.0.0', '255.0.0.0']
            
            # Find all IP addresses
            ip_addresses = ip_pattern.findall(result.stdout)
            
            #IP address list
            return ip_addresses
        else:
            return "This system is not supported"
    
    
        #Hostname
        # def get_hostname(ip_address):
        #     try:
        #         hostname, _, _ = socket.gethostbyaddr(ip_address)
        #         return hostname
        #     except socket.herror:
        #         return "Hostname could not be found."

    def my_hostname():
        try:
            result = subprocess.run(['hostname'], stdout=subprocess.PIPE, text=True)
            return result.stdout.strip()
        except:
            return "Not found"
    
    
    health_data = {
        "cpu_usage": cpu_usage,
        "memory_usage": memory_usage,
        "disk_usage": disk_usage,
        "network_stats": network_stats,
        "my_hostname": my_hostname(),
        "ip_address": get_ip_address()
    }
    
    return jsonify(health_data)
