import requests
from datetime import datetime
import time
import argparse
import getpass
import json
from rich import print
import logging
import urllib3
from netmiko import ConnectHandler
from working.eve_up import get_nodes, get_links
#from ipaddress import *
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
logging.basicConfig(level=logging.DEBUG,
                    format=f'%(asctime)s %(levelname)s %(name)s %(threadName)s : %(message)s')


def base_config():
    counter = 1
    nodes = get_nodes(topo="Juniper/jncis-sp.unl")
    for key, value in nodes.items():
        try:
            if value["template"] == "vmxvcp":
                # Get the Telnet address and port set to variables
                url = value["url"].split(":")
                ip = url[1].replace("//", "")
                port = (url[2])
                node_conn = {
                    'device_type': 'juniper_junos_telnet',
                    'host': ip,
                    'port': port,
                }
                # Initiate connection to EVE
                net_connect = ConnectHandler(**node_conn)
                hostname = f'vMX{str(counter)}'
                counter += 1
                # Send commands and view output
                config_commands = ['set system root-authentication encrypted-password "$6$fwcVn5fO$3Q58R19MOEJDcUeBslODstHHYm.WrVqDVociEDYEFtjJ4C0KAf2h6SVIDmHpevg/xSaiHSqcK/YWR5hr.LDWU."',
                                   'delete chassis auto-image-upgrade',
                                   f'set system host-name {hostname}',
                                   'set system domain-name abc.co',
                                   'set system services ssh',
                                   'set system services netconf ssh',
                                   'set system login user knox class super-user authentication encrypted-password "$6$fwcVn5fO$3Q58R19MOEJDcUeBslODstHHYm.WrVqDVociEDYEFtjJ4C0KAf2h6SVIDmHpevg/xSaiHSqcK/YWR5hr.LDWU."']
                output = net_connect.send_config_set(
                    config_commands, exit_config_mode=False)
                print(output)
                # Commit
                output = net_connect.commit(and_quit=True)
                print(output)
        except Exception as err:
            print(err)
            continue


# def ip_addresser(subnet: str = '192.168.1.0/24'):
#     subnets = list(ip_network(subnet).subnets(new_prefix=30))
#     print(subnets)
#     for subn in subnets:
#         print(list(subn.hosts()))
#     links = get_links("Juniper/CSPF_MPLS.unl")
#     print(links)
#     return subnets


if __name__ == "__main__":
    base_config()
