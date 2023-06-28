import re
#import mysql.connector
import datetime
import os
import socket
import time
import signal
import matplotlib.pyplot as plt

METRICS_TO_FETCH = ["datablocks_size"]
######### PARSING .INI FILE TO KNOW WHICH NODES SHOULD BE MONITORED ###########

machines = {}


with open("./IPFS_nodes/data-node/hosts.ini") as f:
    lines = f.readlines()

current_machine_group = ""

groups = []

for line in lines:
    ignore_flag = False
    if line[0]=="#":
        #print("Commented line",line,", ignoring ... ")
        ignore_flag = True
    if not(ignore_flag):
        #print(line)
        machine_group_name = re.findall(r'\[(.*?)\]',line)
        machine_address = re.findall(r'\b\w+@\S+\.fr\b',line)
        if machine_group_name!=[]:
            groups.append(machine_group_name[0])
            current_machine_group = machine_group_name[0]
            machines[current_machine_group] = []
        elif machine_address!=[]:
            machines[current_machine_group].append(machine_address[0])
        # else:
        #     #print("Unrecognized line ", line," does not match name of group nor machine address.")

print("Machines dictionary ",machines)
print("Machine groups ", groups)

groups.remove("datacollector")

################## PREPARING FOLDERS AND TEXT FILES FOR WRITING DATA ####################

current_date_time = datetime.datetime.now()

os.system("mkdir -p ./IPFS_nodes/data-node/data")

os.mkdir("./IPFS_nodes/data-node/data/"+str(current_date_time))

for group in groups:
    os.mkdir("./IPFS_nodes/data-node/data/"+str(current_date_time)+"/"+str(group
))

for group in groups:
    for machine in machines[group]:
        os.mkdir("./IPFS_nodes/data-node/data/"+str(current_date_time)+"/"+str(group)+"/"+machine)
        for metric in METRICS_TO_FETCH:
            with open(f"./IPFS_nodes/data-node/data/{str(current_date_time)}/{group}/{machine}/{metric}.txt","x") as f:
                f.write(f"{machine} - {metric} \n")

#### DATA COLLECTOR AND WRITER ############

collection_period = 0
collection_flag= True

def handler_stop_signals(signum, frame):
    global collection_flag
    collection_flag = False

signal.signal(signal.SIGINT, handler_stop_signals)
signal.signal(signal.SIGTERM, handler_stop_signals)

while collection_flag:
    for group in groups:
        for machine in machines[group]:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            print(machine[8:])
            s.connect((machine[8:], 62000))
            #s.connect((machine, 62000))

            s.send(b"data-pls")

            data = s.recv(1024)
            data = data.decode()
            
            for metric in METRICS_TO_FETCH:
                path = f"./IPFS_nodes/data-node/data/{str(current_date_time)}/{group}/{machine}/{metric}.txt"
                if os.path.exists(path):
                    with open(path,"a+") as f:
                        f.write(f"{collection_period} - {data} \n")
                else:
                    with open(f"./IPFS_nodes/data-node/data/{str(current_date_time)}/{group}/{machine}/{metric}.txt","x") as f:
                        f.write(f"{collection_period} - {data} \n")

    collection_period +=1
############# AUTO PLOTTER AFTER SIGNAL TO KILL DATA COLLECTOR ###########

print("POST SIGINT")

for group in groups:
    for machine in machines[group]:
        for metric in METRICS_TO_FETCH:
            with open(f"./IPFS_nodes/data-node/data/{str(current_date_time)}/{group}/{machine}/{metric}.txt","r") as f:
                data = f.readlines()
            data = [float(i) for i in data]
            X = range(collection_period)
            fig, ax = plt.subplots()

            ax.plot(X,data)
            ax.set_xlabel('Data collection period')  # Add an x-label to the axes.
            ax.set_ylabel('Size of folder (in bytes)')
            ax.legend()
            plt.savefig("./figures/"+machine+".png")