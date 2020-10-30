f = open("test.blast", "r")
f1 = open("testOP.blast", "w")
dictionary= {}
for line in f:
    splitted =line.split("\t")
    if (splitted[0], splitted[1]) in dictionary.keys():
        tup = dictionary[(splitted[0], splitted[1])]
        #print(tup)
        #print(tup[0])
        l1 = tup[0]
        l2 = tup[1]
        l1.append(line.strip())
        l2.append(float(splitted[2]))
        dictionary[(splitted[0], splitted[1])] = (l1,l2)

    elif (splitted[1], splitted[0]) in dictionary.keys():
        tup = dictionary[(splitted[1], splitted[0])]
        l1 = tup[0]
        l2 = tup[1]
        l1.append(line.strip())
        l2.append(float(splitted[2]))
        dictionary[(splitted[1], splitted[0])] = (l1,l2)

    else:
        l1 = [line.strip(),]
        l2 = [float(splitted[2])]
        dictionary[(splitted[0], splitted[1])] = (l1,l2)

for k, v in dictionary.items():
    if len(v[0]) >1:
        """if len(v[0]) == 2:
            l1_num = float(v[0][0].split("\t")[2])
            l2_num = float(v[0][1].split("\t")[2])
            if l1_num > l2_num:
                #print(k, v)
                v[0].pop(1)
                #print(k, v)
            elif l1_num == l2_num:
                v[0].pop(1)
            else:
                #print(k, v)
                v[0].pop(0)
                #print(k, v)
            print(v[0], file=f1)
        else:
        if len(v[0]) != 2:
            print(len(v[0]),v)
            for v_0 in v[0]:
                if str(max(v[1])) in v_0:
                    print(v_0)
                    break
        """
        for v_0 in v[0]:
            if str(max(v[1])) in v_0:
                print(v_0, file=f1)
                break
    else:
        print(v[0][0], file=f1)
