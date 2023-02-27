"""
Node activity simulator 

Inter-node communication simumlator

"""

import numpy as np
import time



def activity_on_node_realtime():
    file_number = 0
    files = []
    file_occurences = {}
    
    for _ in range(150):
        a = np.random.exponential(0.25)
        time.sleep(a)
        a = np.random.randint(0,3)
        if a == 0:
            print("Created new file file_"+str(file_number))
            files.append("file_"+str(file_number))
            file_number +=1
        if a == 1:
            if files != []:
                print("Deleted file")
                id = np.random.randint(0, len(files))
                files.pop(id)
            
        if a == 2 : 
            if files != []:
                id = np.random.randint(0, len(files))
                file = files[id]
                print("Opened file "+file)
                if file in file_occurences.keys():
                    file_occurences[file] +=1
                else:
                    file_occurences[file] = 1

    print(file_occurences)

def activity_on_node_generator():
    file_number = 0
    files = []
    file_occurences = {}
    t = 0
    with open("result.txt", "w") as f:
        for _ in range(150):
            a = np.random.exponential(0.25)
            #time.sleep(a)
            t+=a
            a = np.random.randint(0,3)
            if a == 0:
                #print("Created new file file_"+str(file_number))
                files.append("file_"+str(file_number))
                file_number +=1
                f.write(str(t)[:4]+" Created new file file_"+str(file_number)+"\n")
            if a == 1:
                if files != []:
                    id = np.random.randint(0, len(files))
                    f.write(str(t)[:4]+" Deleted file_"+str(id)+"\n")
                    files.pop(id)
                
            if a == 2 : 
                if files != []:
                    id = np.random.randint(0, len(files))
                    file = files[id]
                    f.write(str(t)[:4]+" Opened file_"+str(id)+"\n")
                    if file in file_occurences.keys():
                        file_occurences[file] +=1
                    else:
                        file_occurences[file] = 1

        for file in list(file_occurences.keys()):
            f.write("File "+file+" was consulted "+str(file_occurences[file])+" times \n")



activity_on_node_generator()