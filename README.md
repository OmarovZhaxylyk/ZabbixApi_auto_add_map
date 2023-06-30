# ZabbixApi_auto_add_map
python 
Zabix is discovered through the action discovery-action detects host adds them to a pre-created group. I then extract the group number with curl:

curl -s -k -X POST -H 'Content-Type: application/json-rpc' -d '{
     "jsonrpc": "2.0",
     "method": "hostgroup.get",
     params: {
         "output": "extend"
     },
     "auth": "54f88584205e11948073a0bf09a1c1df",
     "id": 1
}' http://192.168.200.77/api_jsonrpc.php | jq

After that, I add the hosts to the map using the obtained group_id (for example, 25):
group_id = 25

# Get a list of hosts with the specified group_id
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
After adding all the hosts, I read their unique numbers in the map and add a link to these hosts.
