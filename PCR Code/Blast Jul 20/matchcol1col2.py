f = open("test.blast", "r")
fw1 = open("testOP1.blast", "w")
fw2 = open("testOP2.blast", "w")

dictionary= {}
for line in f:
    splitted =line.split("\t")
    if (splitted[0], splitted[1]) in dictionary.keys():
        tup = dictionary[(splitted[0], splitted[1])]
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
    if len(v[0]) > 1:
        for v_0 in v[0]:
            if str(max(v[1])) in v_0:
                print(v_0, file=fw1)
                print(v_0, file=fw2)
                break
    else:
        print(v[0][0], file=fw1)
