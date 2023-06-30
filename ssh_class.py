import paramiko
import time

class SSHClient:
    def __init__(self, host, username, password):
        self.host = host
        self.username = username
        self.password = password
        self.ssh_client = paramiko.SSHClient()
        self.ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    def connect(self):
        self.ssh_client.connect(self.host, username=self.username, password=self.password)

    def execute_command(self, command):
        stdin, stdout, stderr = self.ssh_client.exec_command(command)
        time.sleep(2)
        output = stdout.read().decode('utf-8')
        return output

    def close(self):
        self.ssh_client.close()

class CDPNeighborParser:
    def __init__(self, output):
        self.output = output

    def parse(self):
        lines1 = self.output.replace(',', '\n')
        lines = lines1.split('\n')
        cdp_entries = []
        entry = {}

        for line in lines:
            line = line.strip()

            if line.startswith('Device ID:'):
                entry = {'ID': line.split(':')[1].strip()}
            elif line.startswith('IP address:'):
                entry['IP Address'] = line.split(':')[1].strip()
            elif line.startswith('Interface:'):
                entry['Interface'] = line.split(':')[1].strip()
            elif line.startswith('Port ID (outgoing port):'):
                entry['Port'] = line.split(':')[1].strip()
                cdp_entries.append(entry)

        return cdp_entries

