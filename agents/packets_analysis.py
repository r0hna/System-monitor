import scapy.all as scapy

def capture_network_traffic(iface='Intel(R) 82574L Gigabit Network Connection #2', packet_count=1):
    # Capture network traffic on the specified interface
    packets = scapy.sniff(iface=iface, count=packet_count)
    
    #scapy.show_interfaces()
    all_packets = []
    try:
        for packet in packets:
            all_packets.append(packet.show())
        return all_packets
    
    except KeyboardInterrupt:
        print("Keyboard detected!")
