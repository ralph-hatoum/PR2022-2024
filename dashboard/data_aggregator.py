import re
import mysql.connector
import datetime
import os
import socket
import time
import signal

METRICS_TO_FETCH = ["datablocks_size"]
######### PARSING .INI FILE TO KNOW WHICH NODES SHOULD BE MONITORED ###########

machines = {}

with open("./hosts.ini") as f:
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

################## PREPARING FOLDERS AND TEXT FILES FOR WRITING DATA ####################

current_date_time = datetime.datetime.now()

os.mkdir("./data/"+str(current_date_time))

for group in groups:
    os.mkdir("./data/"+str(current_date_time)+"/"+str(group))

for group in groups:
    for machine in machines[group]:
        os.mkdir("./data/"+str(current_date_time)+"/"+str(group)+"/"+machine)
        for metric in METRICS_TO_FETCH:
            with open(f"./data/{str(current_date_time)}/{group}/{machine}/{metric}.txt","x") as f:
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
    print("coLLECTING data ...")
    time.sleep(2)
    # for group in groups:
    #     for machine in machines[group]:
    #         s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    #         s.connect((machine, 62000))

    #         s.send(b"data-pls")

    #         data = s.recv(1024)
    #         data = data.decode()
            
    #         for metric in METRICS_TO_FETCH:
    #             with open(f"./data/{str(current_date_time)}/{group}/{machine}/{metric}.txt","x") as f:
    #                 f.write(f"{collection_period} - {data} \n")


############# AUTO PLOTTER AFTER SIGNAL TO KILL DATA COLLECTOR ###########


