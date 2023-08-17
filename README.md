# Research project - INSA Lyon 2022-2024

This is my personal repository for code written in for my research project about distributed cloud infrastructures. For now, only an SSH based IPFS private network deployer with data collection is ready to be used :

# IPFS private network deployer

The aim of this project is to provide a quick and efficient way to deploy a private IPFS network over a set of machines accessible via SSH connection. The tool also allows to setup an IPFSCluster within the IPFS network, as well as a data collection system to retrieve metrics in order to quantify and analyse the behavior of the network. 

This project was developped as part of my test bench for my masters thesis about IPFS and local private clouds.

## Quick start up

You'll need to describe your network in a JSON file. You'll need to define a number of IPFS nodes. You can optionally define IPFSCluster clusters. An example of a configuration is in the file network_config.json

```JSON
{
    "Credentials":"rhatoum",
    "IPFS_network":
    {
        "Nodes": 6,
        "GCPeriod": "15m",
        "MaxStorage": "15kb"
        
    },
   "IPFS_Clusters": {
       "1":{
           "Nodes":3
       },
       "2":{
            "Nodes":2
       }
   }
}
````
| JSON tag | Description | Required ?|
|----------|----------|----------|
| Credentials  | Username for SSH connection to machines   | Yes, but can be left empty |
| IPFS network | IPFS network configuration   | Yes   |
| Nodes  | Number of nodes in the IPFS network, inside the IPFS network tag  | Yes   |
| GCPeriod   | Garbage collection period for IPFS, inside the IPFS network tag  | No, will be set to default value if not given  |
| MaxStorage  | MaxStorage on IPFS node, inside the IPFS network tag   | No, will be set to default value if not given   |
| IPFS_Clusters   | IPFSCluster clusters you wish to set up  | No |

Each IPFSCluster cluster must be declared in the IPFS_Clusters tag, each cluster should be named after a number as described, and for each cluster you can declare the exact same tags as you can describe in the IPFS_Network tag. 

Your configuration should respect the following constraints : 
- the number sum of nodes in all clusters should be inferior or equal to the total number of nodes in the IPFS network

You'll need to provide a list of the IP addresses of the machines you have at your disposal, in the file ip_@.txt. For now, you need to make sure you have accepted their private key before otherwise the connection won't work. 

Once all of this is configured, you'll need to launch inf_builder.py.
Once basic configurations are performed by the script, and if enough nodes are available to satisfy your network build request, Ansible will ask you for a password, which you'll need to provide. 

Then, the system will begin setting up your network. Once it is done, start prometheus and setup a Grafana dashboard; you're good to go !

The network can be killed through the network_killer.yaml playbook :

```
ansible-playbook network_killer.yml -i hosts.ini --ask-pass
```
## General architecture 

This tool makes use of Ansible, a tool that allows for SSH connection automation. 

Actions to be done are described in yaml files called playbooks. We use two playbooks, one for setting up the network and one for killing the network.

The network is described in a JSON file. Then, a python script reads the configuration, makes sure it is valid (ie you aren't defining more nodes in clusters than there are nodes in the IPFS network for example). Once everything is validated, a python script will ping the ip addresses you've provided in the ip_@.txt file, and check which nodes are responsive. Once enough nodes have been found, the script fills up the hosts.inif file. This is a file used by ansible to know which actions to perform on which machines. 
First, we write all the nodes found so IPFS can be set up on all these nodes.
Then, if IPFSCluster clusters need to be setup, we define a group of nodes for each of the clusters, so we can do the required actions to build the cluster on these nodes.
Once the hosts.ini file is ready, we also fill up a Prometheus configuration for data collection, but we'll touch on that in the following section.
Then, we potentially modify the playbook to fit what is in the configuration. For instance, if we need to setup clusters, we need to setup particular actions for each clusters. 

Once that is done, we launch the playbook and let it do its work. 

### Data collection

For data collection, we use Prometheus, a tool that allows for efficient data retrieval. On each node, we set up an HTTP server on port 9100 (node_exporter.py). Each request on this server will return a text file, with each line giving us a metric about the node the server is running on. 
Prometheus is set up through a yaml config file. We give it the ip addresses of the nodes, and the tool will periodically retrieve metrics for us. 
Prometheus runs on the computer you are launching the network on, while the node_exporter servers run on the nodes of the network. This means your nodes need to be reachable by your computer in order for data collection to work. 

Prometheus will stream data to a pipeline, that we can connect to Grafana to have data visualization. In the grafan folder, you'll find a python script that will setup a basic dashboard for you. All you need is grafana to be running on your computer, and an API key to your grafana instance. 

Adding your own metrics if fairly straightforward. You'll need to write a python function that calculates the needed metric on the node, and add it to node_exporter.py. Then, you'll need to add it to the functions executed upon a request to the server, and add a line to the returned text, by following the format that is already written in the file. 

