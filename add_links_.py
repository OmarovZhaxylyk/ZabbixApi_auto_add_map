import requests
import json
import paramiko
import time
import ssh_class

url = 'http://ip_addresss/api_jsonrpc.php'
headers = {'Content-Type': 'application/json-rpc'}
auth_token = ''
map_id = 1
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
links_data = []
i = 0
if 'result' in result:
    elements = result['result'][0]['links']
    for element in elements:
        print(element)
        links_data.append(element)

else:
    print('Error:', result['error'])




def get_host_info(host_id):
    # Zabbix API request payload
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
    #print(result)

    if 'result' in result:
        host_info = result['result'][0]
        return host_info
    else:
        #print('Error:', result['error'])
        return None #

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
# link by id host
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
selements_data = []
entry_hid = {}
response = requests.post(url, headers=headers, data=json.dumps(data), verify=False)
result = response.json()
#print(result)
if 'result' in result:
    elements = result['result'][0]['selements']

    for element in elements:
        selement_id = element['selementid']
        host_id = element['elements'][0]['hostid']
        host_info = get_host_info(host_id)
        ip_address = host_info['ip']
        entry_hid = {'Host ID': host_id, 'IP': ip_address, 'Selement ID': selement_id}
        selements_data.append(entry_hid)

    link_list = []
    entery1 = {}

    for entry in selements_data:
        host = entry['IP']
        host_id = entry['Host ID']
        host_s_id = entry['Selement ID']
        username = 'username'
        password = 'password'
        try:
            ssh = ssh_class.SSHClient(host, username, password)
            ssh.connect()

            command = 'show cdp neighbors detail'
            output = ssh.execute_command(command)

            parser = ssh_class.CDPNeighborParser(output)
            cdp_entries = parser.parse()

            for entry1 in cdp_entries:
                cdp_ip = entry1['IP Address']
                print('started')
                for entry in selements_data:
                    if cdp_ip == entry['IP']:
                        host_id = entry['Host ID']
                        host_s_id2 = entry['Selement ID']
                        FaI = entry1['Interface']
                        FaI2 = entry1['Port']
                        label = f"{FaI[:3]}/{FaI[-6:]}{FaI2[:3]}/{FaI2[-6:]}"

                        link_list.append((map_id, host_s_id, host_s_id2, label))

                        # Print the created link_list
                        print("Selement ID:", host_s_id)
                        print(entry1['Interface'][:3] + " " + entry1['ID'] + " " + entry1['Port'][:3])

            ssh.close()

        except Exception as e:
            print(f"SSH connection to host {host} failed: {str(e)}")
            continue

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
                       },)
print(link_h)
create_map_link(link_h)


