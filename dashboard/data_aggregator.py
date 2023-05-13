from platform import machine
import re
from unittest import skip

######### PARSING .INI FILE TO KNOW WHICH NODES SHOULD BE MONITORED ###########

machines = {}

with open("./hosts.ini") as f:
    lines = f.readlines()

current_machine_group = ""

for line in lines:
    ignore_flag = False
    if line[0]=="#":
        print("Commented line",line,", ignoring ... ")
        ignore_flag = True
    if not(ignore_flag):
        print(line)
        machine_group_name = re.findall(r'\[(.*?)\]',line)
        machine_address = re.findall(r'\b\w+@\S+\.fr\b',line)
        if machine_group_name!=[]:
            current_machine_group = machine_group_name[0]
            machines[current_machine_group] = []
        elif machine_address!=[]:
            machines[current_machine_group].append(machine_address[0])
        else:
            print("Unrecognized line ", line," does not match name of group nor machine address.")

print(machines)

#################### CREATE DATABASE WITH CURRENT TIME AND ALL NEEDED FOR MACHIEN AND GROUPS AND SHIT #####

#### DATA COLLECTOR AND WRITER ############