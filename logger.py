from scapy.all import sniff, IP, TCP

# IP addresses for configuration
printer_ip = "192.168.0.101"
pos_ip = "192.168.0.106"

# Keywords to look for
look_for = ["ROBOT", "FOR HERE"]

def packet_callback(pkt):
    if pkt.haslayer(IP) and pkt.haslayer(TCP):
        src_ip = pkt[IP].src
        dst_ip = pkt[IP].dst
        
        # Checking for traffic between the specified IPs
        if {src_ip, dst_ip} == {printer_ip, pos_ip}:
            if src_ip == pos_ip:
                log_packet("POS", pkt)
            elif src_ip == printer_ip:
                log_packet("PRINTER", pkt)

def log_packet(prefix, pkt):
    if pkt[TCP].payload:
        payload_data = pkt[TCP].payload
        try:
            # Check if the payload starts with 0x1b
            if payload_data.load.startswith(b'\x1b'):
                payload_str = payload_data.load.decode('utf-8').strip()

                # Debug: print ASCII values of characters
                # print(f"{prefix}: ASCII values: {[ord(char) for char in payload_str]}")

                # Check if payload_str contains any of the keywords
                if any(keyword in payload_str for keyword in look_for):
                    print("---------- ORDER UP ----------")
                    print(f"\n{payload_str}")
                    print("------------ END ------------")

        except UnicodeDecodeError:
            pass
            # Not UTF-8 encoded data, logging as hex and ASCII where possible
            # hex_data = payload_data.load.hex()
            # print(f"Data (Hex): {hex_data}")
        except AttributeError:
            pass
            # print("Data: No payload data")
    else:
        pass
        #print("Data: No payload data")


# Sniff packets on br0 interface
sniff(iface="br0", prn=packet_callback, store=0)

