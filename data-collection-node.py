import socket
import os


s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

file_to_track = "./P2Ptest"

s.bind(('127.0.0.1',62000))

s.listen(1)

def getFolderSize(folder):
    total_size = os.path.getsize(folder)
    for item in os.listdir(folder):
        itempath = os.path.join(folder, item)
        if os.path.isfile(itempath):
            total_size += os.path.getsize(itempath)
        elif os.path.isdir(itempath):
            total_size += getFolderSize(itempath)
    print(total_size)
    return total_size
                
while True:
    conn, addr = s.accept()

    msg = conn.recv(1024)
    print(msg.decode())

    if msg.decode()=="data-pls":
        size = getFolderSize(file_to_track)
        print(size)
        msg = str(size).encode()
        conn.send(msg)
    conn.close()
