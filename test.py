# Script will read test description, build the right playbook, launch the test and retrieve data - maybe build graphs too ?

import json
import yaml

with open("test.json","r") as f:
    test = json.load(f)

data = test["DATA_TO_PIN"]
nb_of_meas = test["NB_MEAS"]
max_nodes = test["MAX_NB_COPIES"]

# We will assume there is an initial network launched with one node in an ipfs cluster, we build the playbook with this in mind

#TODO BUILD HOSTS.INI file based on previous hosts.INI file

## USEFUL STRINGS ##
NODES = ["ClusterNode1","ClusterNode2"]


with open('test_playbooks/bootstrap.yml', 'r') as file:
    bootstrap = yaml.safe_load(file)

with open('test_playbooks/node.yml', 'r') as file:
    node = yaml.safe_load(file)



# TODO WRITE PLAYBOOK

existing_data = bootstrap


for _ in range(nb_of_meas):
    existing_data.append(node[0])


for name in NODES :  
    # print(node_name)
    # print(node_in_clust(node_name)[0])
    # node_[0]['hosts']=node_name
    with open('test_playbooks/node_in_cluster.yml', 'r') as file:
        node_ = yaml.safe_load(file)
    node_[0]['hosts']=name
    existing_data.append(node_[0])

    existing_data.append(bootstrap[0])

    # print(existing_data)

    for _ in range(nb_of_meas):
        existing_data.append(node[0])   
        
# # with open("playbook.txt","w") as f:
#     f.write(playbook) 

# yaml_obj = yaml.safe_load(playbook)

with open("meas_playbook.yml","w") as f:
    yaml.safe_dump(existing_data, f)