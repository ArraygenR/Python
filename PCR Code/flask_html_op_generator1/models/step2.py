import os
def generateProvean(OP_file_name1,protein_fasta_file,OP_file_name2):
    f = open(OP_file_name1, "r")
    f.readline()
    data = f.read().split("\n\n")
    OP_file_name = OP_file_name1.split("/")
    OP_file_name.pop()
    OP_file_name = "/".join(OP_file_name)
    OP_file_name = os.path.join(OP_file_name,"provean_example")
    if not os.path.exists(OP_file_name):
        os.mkdir(OP_file_name)
    for i, d in enumerate(data):
        d_all_id = []
        if d.strip() != "":
            d1 = d.strip().split("\n")
            for d2 in d1:
                if d2.strip() != "":
                    splitted = d2.split("\t")
                    if len(splitted) >=21:
                        if splitted[20].strip() != "":
                            d_all_id.append(splitted[20]+"\n")

        if len(d_all_id) != 0:
            output = []
            fw = open(OP_file_name + "/muta"+str(i)+".var", "w")
            fw.writelines(d_all_id)
            fw.close()
            cmd = "provean.sh -q '"+protein_fasta_file+"' --num_threads 2 -v '"+OP_file_name+"/muta"+str(i)+".var' > '"+OP_file_name+"/PROVEAN_OUTPUT"+str(i)+".TXT'"
            print(cmd)
            os.system(cmd)

    path =OP_file_name+"/"
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

    f = open(OP_file_name1, "r")
    fw = open(OP_file_name2 , "w")
    for line in f:
        splitted = line.split("\t")
        if len(splitted) > 19:
            if splitted[20].strip() in dictionary.keys():
                print("\t".join(splitted).rstrip("\n")+"\t"+"\t".join(dictionary[splitted[20].strip()]), file = fw)
            else:
                print("\t".join(splitted),end= "", file = fw)
        else:
            print("\t".join(splitted),end= "", file = fw)
