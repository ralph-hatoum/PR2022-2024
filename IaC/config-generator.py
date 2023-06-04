from __future__ import print_function
from os import urandom
from binascii import b2a_hex
import os
import time
import json



def swarm_key_generator(filename):
    key = b2a_hex(urandom(32))
    with open(filename,"w") as f:
        f.write('/key/swarm/psk/1.0.0/\n')
        f.write('/base16/\n')
        f.write(key.decode())


nodes = ["node1","node3","test"]


print("Generating all needed configuration files and swarm key ...")

## SWARM KEY ##

print("Generating swarm key ...")
swarm_key_generator("swarm.key")
print("Swarm key generated")

## BOOTSTRAP SETUP ##

bootstrap_ipfs_id = "test"

## IPFS NODE CONFIG FILES ##

print("Generating config files in directory configs...")

os.system("mkdir -p configs")
for node in nodes:
    os.system(f"mkdir -p configs/{node}")

for node in nodes:
    os.system(f"mkdir -p configs/{node}/ipfs")
    os.system(f"echo  > configs/{node}/ipfs/config.json")
    with open(f"config_model_ipfs.json","r") as f:
        config = json.load(f)

    # MODIFYING NEEDED VALUES #

    config["Bootstrap"]=[bootstrap_ipfs_id]
    config["GCPeriod"]="10m"
    config["StorageMax"]="200kB"

    with open(f"configs/{node}/ipfs/config.json","w") as f:
        json.dump(config, f, indent=4,ensure_ascii=False)
    
    os.system(f"mv configs/{node}/ipfs/config.json configs/{node}/ipfs/config")
    os.system(f"rm -f configs/{node}/ipfs/config.json")
    print(f"IPFS configuration generated for node {node} : \033[0;32mOK!\033[0m")


## IPFSCluster NODE CONFIG FILES ##

cluster_secret=""

for node in nodes:
    print(node)
    os.system(f"mkdir -p configs/{node}/ipfs-cluster")
    os.system(f"echo  > configs/{node}/ipfs-cluster/service.json")
    with open("config_model_cluster.json","r") as f:
        config = json.load(f)
    
    # MODIFYING NEEDED VALUES #

    config["cluster"]["peername"]=node
    config["cluster"]["secret"]=cluster_secret

    with open(f"configs/{node}/ipfs-cluster/service.json","w") as f:
        json.dump(config, f, indent=4)
    
    print(f"IPFS-cluster configuration generated for node {node} : \033[0;32mOK!\033[0m")