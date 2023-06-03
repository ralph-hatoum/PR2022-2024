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


nodes = ["node1","node3"]


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
    os.system(f"cp config_model.json configs/{node}/config.json")
    with open(f"configs/{node}/config.json","r") as f:
        config = json.load(f)

    # MODIFYING NEEDED VALUES #

    config["Bootstrap"]=[bootstrap_ipfs_id]
    config["GCPeriod"]="10m"
    config["StorageMax"]="200kB"

    with open(f"configs/{node}/config.json","w",encoding='utf-8') as f:
        json.dump(config, f, indent=4,ensure_ascii=False)
    
    os.system(f"mv configs/{node}/config.json configs/{node}/config")
    os.system(f"rm -f configs/{node}/config.json")
    print(f"Configuration generated for node {node} : \033[0;32mOK!\033[0m")


