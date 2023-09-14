import re
import requests
import json
import paramiko
import time
import ssh_class

url = 'http://192.168.200.*/api_jsonrpc.php'
headers = {'Content-Type': 'application/json-rpc'}
auth_token = '54f88584205e**948073a0bf09a*c*df'
map_id = 3

data = {
    'jsonrpc': '2.0',
    'method': 'map.get',
    'params': {
        'sysmapids': [map_id],
        'selectLinks': 'extend'
    },
    'auth': auth_token,
    'id': 1
}
response = requests.post(url, headers=headers, data=json.dumps(data), verify=False)
result = response.json()
links_data = []  # Store existing map links

if 'result' in result:
    elements = result['result'][0]['links']
    for element in elements:
        links_data.append(element)  # Add existing links to a list
else:
    print('Error:', result['error'])


def get_host_info(host_id):
    payload = {
        'jsonrpc': '2.0',
        'method': 'hostinterface.get',
        'params': {
            'output': 'extend',
            'hostids': host_id
        },
        'auth': auth_token,
        'id': 1
    }

    response = requests.post(url, headers=headers, data=json.dumps(payload), verify=False)
    result = response.json()

    if 'result' in result:
        host_info = result['result'][0]
        return host_info
    else:
        return None


def create_map_link(link):
    payload = {
        'jsonrpc': '2.0',
        'method': 'map.update',
        'params': {
            'sysmapid': map_id,
            'links': links_data + link
        },
        'auth': auth_token,
        'id': 1
    }

    response = requests.post(url, headers=headers, data=json.dumps(payload), verify=False)
    result = response.json()

    if 'result' in result:
        print('Link created successfully!')
    else:
        print('Error:', result['error'])


# Step 1: Get Zabbix map and element data
data = {
    'jsonrpc': '2.0',
    'method': 'map.get',
    'params': {
        'output': 'extend',
        'sysmapids': [map_id],
        'selectSelements': 'extend'
    },
    'auth': auth_token,
    'id': 1
}
response = requests.post(url, headers=headers, data=json.dumps(data), verify=False)
result = response.json()

selements_data = []

if 'result' in result:
    elements = result['result'][0]['selements']

    for element in elements:
        selement_id = element['selementid']
        host_id = element['elements'][0]['hostid']
        host_info = get_host_info(host_id)
        if host_info:
            ip_address = host_info['ip']
            selements_data.append({'Host ID': host_id, 'IP': ip_address, 'Selement ID': selement_id})

link_list = []

passwords = ['pw1', 'pw2', 'pw3']

for entry in selements_data:
    host = entry['IP']
    host_id = entry['Host ID']
    host_s_id = entry['Selement ID']
    username = 'admin'

    ip_interface_dict = {}  # Initialize ip_interface_dict as an empty dictionary

    for password in passwords:
        try:
            ssh = ssh_class.SSHClient(host, username, password)
            ssh.connect()

            command = 'show arp'
            output = ssh.execute_command(command)

            # Parse the 'show arp' output to extract IP addresses and interface ports
            lines = output.splitlines()
            for line in lines:
                match = re.match(r'Internet\s+(\S+)\s+\d+\s+(\S+)\s+ARPA\s+(\S+)', line)
                if match:
                    ip_address = match.group(1)
                    interface_port = match.group(3)

                    ip_interface_dict[ip_address] = interface_port

            ssh.close()
            print(ip_interface_dict)
            break

        except Exception as e:
            print(f"SSH connection to host {host} failed: {str(e)}")
            continue

    for cdp_ip, cdp_interface in ip_interface_dict.items():
        for entry1 in selements_data:
            if cdp_ip == entry1['IP']:
                host_s_id2 = entry1['Selement ID']
                FaI = cdp_interface
                label = f"{FaI[:3]}/{FaI[-6:]}"
                link_list.append((map_id, host_s_id, host_s_id2, label))

# Create a list of links in the required format
link_h = []
for link in link_list:
    map_id, host_s_id, host_s_id2, label = link
    link_h.append({'linkid': '',
                   'sysmapid': '1',
                   'selementid1': host_s_id,
                   'selementid2': host_s_id2,
                   'drawtype': '0',
                   'color': '000000',
                   'label': label,
                   'linktriggers': [],
                   'permission': 1
                   })

# Create map links with the combined data
create_map_link(link_h)
