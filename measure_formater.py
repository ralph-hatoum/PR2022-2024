DEST = "measure_output.txt"

LINE_FORMAT= ""

with open("measure.txt","r") as f:
    lines = f.readlines()

data = lines[3][4:]

# We now have data in format X minutes X seconds; lets conver it all in seconds

data = data.split("m")
data[1] = ".".join(data[1][:-2].split(","))
data = list(map(lambda x : float(x),data))

time_in_seconds=data[0]*60+data[1]

TO_WRITE = LINE_FORMAT+f"{time_in_seconds}\n"

with open(DEST,"a") as f:
    f.write(TO_WRITE)


