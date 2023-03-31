with open("./text.txt", 'r') as f:
    lines = f.readlines()
    with open("./output.txt",'w') as out:
        for line in lines:
            out.write(line[3:]+'\n')

