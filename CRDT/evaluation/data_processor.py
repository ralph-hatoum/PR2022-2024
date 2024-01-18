import re
import matplotlib.pyplot as plt

RGX_ms=r"\d+(\.\d+)?(ms)"
RGX_s=r"\d+(\.\d+)?(s)"

with open("data.txt",'r') as f:
    lines = f.readlines()

X = []
Y_ev = []
Y_prod = []
S_ev = 0
S_prod=0
for i in range(len(lines)):
    if (i+1)%13==1:
        X.append(int(lines[i]))
        if (i+1)>1:
            Y_ev.append(S_ev/10)
            Y_prod.append(S_prod/10)
        S_ev = 0
        S_prod=0
    elif (i+1)%13==0:
        pass
    else:
        print(i)
        # print(lines[i])
        y_ev, y_prod = lines[i].split(" ")
        # print(y_ev,y_prod)

        if re.match(RGX_ms,y_ev):
            # Time expressed in ms
            y_ev = float(y_ev[:-2])
        elif re.match(RGX_s,y_ev) :
            #time in s
            y_ev = float(y_ev[:-1])*1000
        else :
            y_ev =y_ev.split("m")
            y_ev = float(y_ev[0])*60000+float(y_ev[1][:-1])*1000
            print(y_ev)

        
        if re.match(RGX_ms, y_prod):
            #time expressed in ms
            y_prod = float(y_prod[:-3])
        else :
            # time in S
            y_prod = float(y_prod[:-2])*1000
        
        S_ev += y_ev
        S_prod += y_prod

print(X)
print(Y_ev)
print(Y_prod)

plt.plot(X[:-1],Y_ev,"x")
plt.xlabel('Difficulty expressed as an integer')
plt.ylabel('Time to produce proof (ms)')
plt.title("Time to produce proof")
plt.show()

        
        
