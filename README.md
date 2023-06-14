# IPFS private network deployer

The aim of this project is to provide a quick and efficient way to deploy a private IPFS network over a set of machines accessible via SSH connection. The tool also allows to setup an IPFSCluster within the IPFS network, as well as a data collection system to retrieve metrics in order to quantify and analyse the behavior of the network. 

This project was developped as part of my test bench for my masters thesis about IPFS and local private clouds.


## General architecture 

This tool makes use of Ansible, a tool that allows for SSH connection automation. 

Actions to be done are described in yaml files called playbooks. We use two playbooks.

The first playbook will turn on the IPFS daemons, IPFSCluster daemons and data collectors on network nodes, as well as a node called _data-aggregator_. 
The second playbook will turn off all daemons and data collectors. 

In this first version, we'll assume all needed files are already available on machines. The next version will focus on dynamically setting up the network on a given set of machines and installing all needed requirements, essentially allowing for infrasture as code like use. 

### Data collection

For data collection, each node running IPFS will have a python script responsible for assessing how much data is currently stored on the node. This python script runs a tcp server, listening to connections. The data-aggregator is a node that will periodically contact the nodes and ask for the data they have collected. While this choice might seem a bit unsettling, it is the best way I have found to collect data efficiently. Centralizing will also allow us to easily setup a grafana dashboard to visualize activity on the network (not available yet).

## Quick start

In the hosts.ini file, change the username in front of each machine address.

You can start the IPFS network as you described it in the previous file with the command : 

``` ansible-playbook playbook-u.yml -i hosts.ini --ask-pass ```

To kill the network : 

``` ansible-playbook playbook-d.yml -i hosts.ini --ask-pass ```
