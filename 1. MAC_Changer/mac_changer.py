#!/usr/bin/env python

import subprocess
import optparse
import re

def get_arguments():
    parser = optparse.OptionParser()
    parser.add_option('-i', '--interface', dest='interface', help='Interface to change it\'s MAC Address')
    parser.add_option('-m', '--mac', dest='new_mac', help='New MAC Address')
    (options, arguments) = parser.parse_args()
    if not options.interface:
        parser.error('[-] Please specify an interface, use --help for more info')
    elif not options.new_mac:
        parser.error('[-] Please specify an MAC, use --help for more info')
    return options

def change_mac(interface, new_mac):
    print('[+] Changing MAC Address for ' + interface + ' to ' + new_mac)

    subprocess.call(['ifconfig', interface, 'down'])
    subprocess.call(['ifconfig', interface, 'hw', 'ether', new_mac])
    subprocess.call(['ifconfig', interface, 'up'])

def get_current_mac(interface):
    try:
        ifconfig_result = str(subprocess.check_output(['ifconfig', interface]))
        mac_search_result = re.search(r'\w\w:\w\w:\w\w:\w\w:\w\w:\w\w', ifconfig_result)
        if mac_search_result:
            return mac_search_result.group(0)
        else:
            print('[-] Couldn\'t read MAC Address!')
    except:
        print('[-] Interface doesn\'t exists!')

options = get_arguments()
change_mac(options.interface, options.new_mac)
current_mac = get_current_mac(options.interface)

if current_mac==options.new_mac:
    print('[+] MAC Changed Successfully to ' + options.new_mac)
else:
    print('[-] MAC didn\'t Changed!')

#Default MAC: ether 08:00:27:85:78:b6