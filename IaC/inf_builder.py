import json
from pinger import ping_all_machines
from prometheus_conf_writer import prometheus_conf_writer
import os


## TODO GENERATE SWARM KEY !!!
with open("network_config_clusters.json","r") as f:
    config = json.load(f)

nodes_needed = int(config["IPFS_network"]["Nodes"])

username = config["Credentials"]

## CHECK CONFIG'S VALIDITY ##
if nodes_needed<2:
    print("\n\033[91mError : too few nodes ... you need at least two nodes in the network.\033[0m\n")
    exit(-1)

flag_clusters_to_build = False
try:
    clusters = config["IPFS_Clusters"]
    flag_clusters_to_build = True
except Exception as e:
    print("\nNo IPFSclusters detected in the configuration!\n")


if flag_clusters_to_build:
    clusters_to_build = []
    nodes_in_clusters = 0
    for cluster in list(clusters.keys()):
        nodes_in_clusters += int(clusters[cluster]["Nodes"])
        clusters_to_build.append(clusters[cluster]["Nodes"])
    if nodes_in_clusters > nodes_needed:
        print("\n\033[91mError : you have defined more nodes in clusters than there are nodes in the network. Please fix the configuration.\033[0m\n")
        exit(-1)

print("\n\033[0;32mYour configuration passed the checks !\033[0m\n")


print(f"\nThe network needs {nodes_needed} nodes -- checking for availability ...\n")

available_hosts = ping_all_machines(nodes_needed)

if len(available_hosts) < nodes_needed:
    print(f"\n\033[91mError : Not enough available nodes -- found {len(available_hosts)}, needed {nodes_needed} -- please change your configuration accordingly.\033[0m\n")
    exit(-1)
else:
    print(f"\n\033[0;32mFound {nodes_needed} available nodes, network can be built ! \033[0m\n")

#Elect bootstrap
#TODO add support for custom conf

bootstrap_node = available_hosts[0]
print(f"\nBootstrap chosen : {bootstrap_node}\n")


# Edit prometheus.yml
print("\nWriting Prometheus yaml file for data collection ...\n")
prometheus_conf_writer(available_hosts, 9100, "./prometheus/prometheus.yml")
print("\n\033[0;32mPrometheus file succesfully written ! \033[0m\n")

available_hosts.remove(bootstrap_node)


print("Building hosts.ini file ...")

with open("hosts.ini","w") as f:
    f.write(f"[Bootstrap-node]\n{username}@{bootstrap_node} label=bootstrap label_ip={bootstrap_node}\n")
    f.write('\n')
    f.write(f"[IPFS-nodes]\n")
    n = 0
    for host in available_hosts:
        f.write(f"{username}@{host} label=node{n} label_ip={host}\n")
        n +=1 
    f.write('\n')

print("\n\033[0;32mhosts.ini file successfully built!\033[0m\n")
    
available_hosts.append(bootstrap_node)

#TODO ADD SUPPORT FOR IPFS CLUSTERS
print("\nProvisioning nodes for IPFSClusters ...")

with open("hosts.ini","a") as f:
    n = 0
    p = 1
    for cluster in clusters_to_build:
        for node in range(int(cluster)):
            if node == 0:
                f.write(f"[IPFSCluster{p}_starter]\n")
                f.write(f"{username}@{available_hosts[n]} label=node{n} label_ip={available_hosts[n]}\n")
                f.write('\n')
                f.write(f"[IPFSCluster{p}]\n")
            else:
                f.write(f"{username}@{available_hosts[n]} label=node{n} label_ip={available_hosts[n]}\n")
                n+=1
        f.write('\n')
            
        p+=1
print("\n\033[0;32mClusters nodes initialized !\033[0m\n")

#TODO modify playbook if needed

#TODO ADD SUPPORT FOR DIFFERENT CONFIG FOR EACH NODE

# print("\nLaunching playbook ...")


# os.system("ansible-playbook playbook.yml -i hosts.ini --ask-pass")

