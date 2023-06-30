import requests
import json
# Добавляем хосты из группы в существующи карту
url = 'http://ip_address/api_jsonrpc.php'
headers = {'Content-Type': 'application/json-rpc'}
auth_token = ''
map_id = 1

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
i = 0
if 'result' in result:
    elements = result['result'][0]['selements']
    for element in elements:
        print(element)
        selements_data.append(element)

else:
    print('Error:', result['error'])
#Окыдык канша хост бар екенин картада

group_id = 25

# Енду жана хост косамыз белгили список пен
data = {
    'jsonrpc': '2.0',
    'method': 'host.get',
    'params': {
        'output': ['host', 'name', 'ip'],
        'groupids': group_id
    },
    'auth': auth_token,
    'id': 1
}

response = requests.post(url, headers=headers, data=json.dumps(data), verify=False)
result = response.json()

if 'result' in result:
    hosts = result['result']
    print('Host Information:')
    selements_data2 = []

    i = 0
    j = 0
    for host in hosts:
        element_label = host['name']
        element_host_id = host['hostid']
        i += 1
        j += 2
        print(i)
        print('Name:', host['name'])
        print('ID:', host['hostid'])
        print('---')

        # Step 2: Update map element
        selements_data2.append(
            {
                "selementid": '',
                "sysmapid": "1",
                "elementtype": "0",
                "iconid_off": "128",
                "iconid_on": "0",
                "label": element_label,
                "label_location": "-1",
                "x": i+10,
                "y": "10",
                "iconid_disabled": "0",
                "iconid_maintenance": "0",
                "elementsubtype": "0",
                "areatype": "0",
                "width": "200",
                "height": "200",
                "viewtype": "0",
                "use_iconmap": "1",
                "evaltype": "0",
                "elements": [
                    {
                        "hostid": element_host_id
                    }
                ],
                "urls": [],
                "tags": [],
                "permission": 1
        })

        '''
        selements_data.append({
            "itemid": i,
            'sysmapid': map_id,
            'selementid': '',  # Example: 10, 11, 12, ...
            'elements': [
                {'hostid': element_host_id}
            ],
            'elementtype': 0,  # 0 for host, 4 for map
            'iconid_off': element_icon,
            'label': element_label,
            'x': i + 5,  # Example: 10, 20, 30, ...
            'y': j  # Example: 0 for all
        })
'''
    data = {
        'jsonrpc': '2.0',
        'method': 'map.update',
        'params': {
            'sysmapid': map_id,
            'name': 'TP_ALES2',
            'selements': selements_data + selements_data2
        },
        'auth': auth_token,
        'id': 2
    }

    response = requests.post(url, headers=headers, data=json.dumps(data), verify=True)
    result = response.json()

    if 'result' in result:
        print('Element added successfully.')
        print("Done.")
    else:
        print('Error:', result['error'])
else:
    print('Error:', result['error'])
