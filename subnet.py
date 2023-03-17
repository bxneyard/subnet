#!/usr/bin/env python3
# usage: subnet.py <ip/cidr>
# alternative: subnet.py <ip> <mask>

import sys

def main():
    try:
        if len(sys.argv) == 2:
            if '/' in sys.argv[1]:
                address, cidr = sys.argv[1].split('/')
                cidr = int(cidr)
                address = [int(x) for x in address.split('.')]  
                for i in range(4):
                    if address[i] >= 0 and address[i] <= 255:
                        if cidr >= 0 and cidr <= 32:
                            mask = [(((1 << 32) - 1) << (32 - cidr) >> i) & 255 for i in reversed(range(0, 32, 8))]
                        else:
                            print('Invalid address(es)')
                            sys.exit(1)
                    else:
                        print('Invalid address(es)')
                        sys.exit(1)
            else:
                print('Include cidr or subnet mask')
                sys.exit(1)

        elif len(sys.argv) == 3:
            address = [int(x) for x in sys.argv[1].split('.')]
            mask = [int(x) for x in sys.argv[2].split('.')]
            for i in range(4):
                if address[i] >= 0 and address[i] <= 255:
                    for i in mask:
                        if i >= 0 and i <= 255:
                            cidr = sum((bin(x).count('1') for x in mask))
                        else:
                            print('Invalid address(es)')
                            sys.exit(1)
                else:
                    print('Invalid address(es)')
                    sys.exit(1)

        else:
            print(f'''
usage: {sys.argv[0]} <ip/cidr>
alternative: {sys.argv[0]} <ip> <mask>''')
            sys.exit(1)

        if address[0] >= 0 and address[0] <= 127:
            ip_class = 'A'
        if address[0] >= 128 and address[0] <= 191:
            ip_class = 'B'
        if address[0] >= 192 and address[0] <= 223:
            ip_class = 'C'
        if address[0] >= 224 and address[0] <= 239:
            ip_class = 'D'
        if address[0] >= 240 and address[0] <= 255:
            ip_class = 'E'

        if address[0] == 10:
            ip_type = 'Private'
        elif address[0] == 172:
            if address[1] >= 16 and address[1] <= 31:
                ip_type = 'Private'
        elif address[0] == 192:
            if address[1] == 168:
                ip_type = 'Private'
            else:
                ip_type = 'Public'
        else:
            ip_type = 'Public'
        
        network = [address[i] & mask[i] for i in range(4)]
        broadcast = [(address[i] & mask[i]) | (255 ^ mask[i]) for i in range(4)]
        first = network[:3] + [network[3] + 1]
        last = broadcast[:3] + [broadcast[3] - 1]
        hosts = 2 ** (32 - cidr)
        usable = hosts - 2 if hosts - 2 >= 0 else 0
        wildcard = [(~x & (1 << 8) - 1) for x in mask]
        bin_ip = [bin(x)[2:].zfill(8) for x in address]
        bin_mask = [bin(x)[2:].zfill(8) for x in mask]

        print(f'''
IP Address: {".".join(map(str, address))}
Binary IP: {".".join(map(str, bin_ip))}
IP Class: {ip_class}
IP Type: {ip_type}
Network Address: {".".join(map(str, network))}
Usable Host Range: {".".join(map(str, first))} - {".".join(map(str, last))}
Broadcast Address: {".".join(map(str, broadcast))}
Total Number of Hosts: {hosts}
Number of Usable Hosts: {usable}
Subnet Mask: {".".join(map(str, mask))}
Binary Subnet Mask: {".".join(map(str, bin_mask))}
Wildcard Mask: {".".join(map(str, wildcard))}
CIDR: /{cidr}
Short: {".".join(map(str, address))}/{cidr}''')
              
    except (ValueError, IndexError):
        print('Invalid address(es)')
        sys.exit(1)

if __name__ == '__main__':
    main()
