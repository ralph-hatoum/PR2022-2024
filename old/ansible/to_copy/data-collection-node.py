import socket
import os
import sys


if len(sys.argv)!=2:
    print("Error : please provide IP address of host")

IP_ADDRESS=sys.argv[1]

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

file_to_track = "./IPFS_nodes/node6/kubo/.ipfs/blocks"

s.bind((IP_ADDRESS,62000))

s.listen(1)

def getFolderSize(folder):
    total_size = os.path.getsize(folder)
    for item in os.listdir(folder):
        itempath = os.path.join(folder, item)
        if os.path.isfile(itempath):
            total_size += os.path.getsize(itempath)
        elif os.path.isdir(itempath):
            total_size += getFolderSize(itempath)
    #print(total_size)
    return total_size

while True:
    conn, addr = s.accept()

    msg = conn.recv(1024)
    #print(msg.decode())

    if msg.decode()=="data-pls":
        size = getFolderSize(file_to_track)
        #print(size)
        msg = str(size).encode()
        conn.send(msg)
    conn.close()