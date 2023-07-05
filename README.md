# ZabbixApi add host and link automaticaly 
python 
Zabix is discovered through the action discovery-action detects host then adds to (before pre-created groups). Then get all belongs id host with curl get group id:

curl -s -k -X POST -H 'Content-Type: application/json-rpc' -d '{
     "jsonrpc": "2.0",
     "method": "hostgroup.get",
     params: {
         "output": "extend"
     },
     "auth": "some token ",
     "id": 1
}' http://ip_address/api_jsonrpc.php | jq

After , added the hosts to the map using the obtained group_id (for example, 25):
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
After adding all the hosts, read their unique numbers connect by ssh router and read cdp, then added links to these hosts into map.
