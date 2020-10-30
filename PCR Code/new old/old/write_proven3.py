import os
path = "/home/arraygen/Desktop/Akshata/Python/blast handing/provean_example/"
dictionary = {}
for files in os.listdir(path):
    if "PROVEAN_OUTPUT" in files:
        f1 = open(path+files)
        for line in f1:
            if not "#" in line.strip() and "["  not in line:
                splitted = line.strip().split("\t")
                if float(splitted[1]) > -2.5:
                    dictionary[splitted[0]] = [splitted[1],"neutral"]
                elif float(splitted[1]) < -2.5:
                    dictionary[splitted[0]] = [splitted[1], "deleterious"]

f = open("/home/arraygen/Desktop/Akshata/Python/blast handing/output.txt", "r")
fw = open("/home/arraygen/Desktop/Akshata/Python/blast handing/output2.txt", "w")
for line in f:
    splitted = line.split("\t")
    if len(splitted) > 19:
        #print(splitted[20].strip())
        if splitted[20].strip() in dictionary.keys():
            print("\t".join(splitted).rstrip("\n")+"\t"+"\t".join(dictionary[splitted[20].strip()]), file = fw)
        else:
            print("\t".join(splitted),end= "", file = fw)
    else:
        print("\t".join(splitted),end= "", file = fw)