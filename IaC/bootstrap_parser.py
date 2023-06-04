import os
import sys

args = sys.argv

bootstrap_ip_address=args[1]

with open("bootstrap_id.txt","r") as f:
    line = f.readlines()


peerId = line[0][20:-4]

ipfs_id_full = f"/ip4/{bootstrap_ip_address}/tcp/4001/ipfs/{peerId}"

os.system("rm -f bootstrap_id.txt")

with open("bootstrap_id.txt", "w") as f:
    f.write(ipfs_id_full)