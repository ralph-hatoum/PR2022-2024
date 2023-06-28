import socket
from datetime import datetime
import time
import matplotlib.pyplot as plt


N = 0
END = 100


hosts = ["127.0.0.1"]

collected_data = {}

for host in hosts :
    collected_data[host] = []
    collected_data[host].append([])
    collected_data[host].append([])

#f = open('data.txt','w')

start = time.time()

while N<END:
    for host in hosts:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((host, 62000))

        s.send(b"data-pls")

        data = s.recv(1024)
        print(data)
        end = time.time()
        timestamp = end-start

        collected_data[host][0].append(timestamp)
        collected_data[host][1].append(float(data.decode()))
        
        #print("Writing : "+str(timestamp)+" "+host+" "+data.decode()+" \n")    

        #f.write(str(timestamp)+" "+host+" "+data.decode()+" \n")
       # f.close()
    N+=1
    
    time.sleep(1)

print(collected_data)

for host in hosts:
    fig, ax = plt.subplots()
    ax.plot(collected_data[host][0],collected_data[host][1])
    ax.set_title("Size of datablocks folder on node "+host)
    ax.set_xlabel('Time elapsed (s)')  # Add an x-label to the axes.
    ax.set_ylabel('Size of folder (in bytes)')
    ax.legend()
    plt.savefig("./figures/"+host+".png")
