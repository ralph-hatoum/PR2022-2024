from ensurepip import bootstrap
import json
from math import fabs
from pinger import ping_all_machines

with open("network_config.json","r") as f:
    config = json.load(f)

nodes_needed = int(config["IPFS_network"]["Nodes"])

username = config["Credentials"]

## CHECK CONFIG'S VALIDITY ##
if nodes_needed<2:
    print("\033[91mError : too few nodes ... you need at least two nodes in the network.\033[0m")
    exit(-1)

flag_clusters_to_build = False
try:
    clusters = config["IPFS_Clusters"]
    flag_clusters_to_build = True
except Exception as e:
    print("No clusters to build !")


if flag_clusters_to_build:
    nodes_in_clusters = 0
    for cluster in list(clusters.keys()):
        nodes_in_clusters += int(clusters[cluster]["Nodes"])
    if nodes_in_clusters > nodes_needed:
        print("\033[91mError : you have defined more nodes in clusters than there are nodes in the network. Please fix the configuration.\033[0m")
        exit(-1)

print("\033[0;32mYour configuration passed the checks !\033[0m")


print(f"The network needs {nodes_needed} nodes -- checking for availability ...")

available_hosts = ping_all_machines(nodes_needed)

if len(available_hosts) < nodes_needed:
    print(f"\033[91mError : Not enough available nodes -- found {len(available_hosts)}, needed {nodes_needed} -- please change your configuration accordingly.\033[0m")
    exit(-1)
else:
    print(f"Found {nodes_needed} available nodes, building hosts file ... ")

#Elect bootstrap & data aggregator
#TODO add support for custom conf

bootstrap_node = available_hosts[0]
print(f"Bootstrap chosen : {bootstrap_node}")
available_hosts.remove(bootstrap_node)
data_aggregator = available_hosts[len(available_hosts)//2]
print(f"Data aggregator elected : {data_aggregator}")

#TODO BUILD HOSTS.INI FILE AND LAUNCH PLAYBOOK

print("Building hosts.ini file ...")

with open("hosts.ini","w") as f:
    f.write(f"[Bootstrap-node]\n{username}@{bootstrap_node} label=bootstrap\n")
    f.write(f"[IPFS-nodes]\n")
    n = 0
    for host in available_hosts:
        f.write(f"{username}@{host} label=node{n}\n")
        n +=1 
    f.write(f"[datacollector]\n{username}@{data_aggregator} label=datacollector\n")

print("hosts.ini file successfully built!")
    

#TODO ADD SUPPORT FOR IPFS CLUSTERS
#TODO ADD SUPPORT FOR DIFFERENT CONFIG FOR EACH NODE





