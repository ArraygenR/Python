import os
f = open("output1.txt", "r")
#fw1 = open("output2.txt", "w")
f.readline()
data = f.read().split("\n\n")
for i, d in enumerate(data):
    d_all_id = []
    if d.strip() != "":
        d1 = d.strip().split("\n")
        for d2 in d1:
            if d2.strip() != "":
                splitted = d2.split("\t")
                if len(splitted) >=21:
                    #print(d2)
                    if splitted[20].strip() != "":
                        #print(splitted[20])
                        d_all_id.append(splitted[20]+"\n")

    if len(d_all_id) != 0:
        output = []
        fw = open("provean_example/muta"+str(i)+".var", "w")
        fw.writelines(d_all_id)
        print(d_all_id)
        fw.close()
        os.system("provean.sh -q provean_example/protein.fasta --num_threads 3 -v provean_example/muta"+str(i)+".var > provean_example/PROVEAN_OUTPUT"+str(i)+".TXT")
