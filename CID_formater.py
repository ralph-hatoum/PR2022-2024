


with open("CID.txt","r") as f:
    lines = f.readlines()

# print(lines[0].split(" ")[1])
    
with open("CID_formatted.txt","w") as f:
    f.write(lines[0].split(" ")[1])