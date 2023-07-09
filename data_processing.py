NB_OF_MEAS = 10

with open("measure_output.txt","r") as f:
    raw_data = f.readlines()


data = []

k = 0
j=0

while k<len(raw_data):
    data.append([])
    for _ in range(NB_OF_MEAS):
        data[j].append(float(raw_data[k][:-1]))
        k+=1
    j+=1
    

print(data)