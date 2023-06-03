import os

available_hosts =[]

with open("ip_@.txt",'r') as f:
    hosts = f.readlines()

for host in hosts:
    response = os.system("ping -c 1 " + host + " &> /dev/null")
    if response == 0:
        available_hosts.append(host)

print(f"Out of {len(hosts)} provided hosts addresses, found {len(available_hosts)} available hosts.")