from Bio.KEGG import REST
import os

def download_data(entry, fw):
    request = REST.kegg_get(entry)
    data = request.read()
    splitted = data.split("///")
    splitted1 = [s[s.find("DEFINITION") + len("DEFINITION"): s.find("\n", s.find("DEFINITION"))].strip() for s in
                splitted if s.strip() != ""]
    for i in range(len(entry)):
        print(entry[i], end="\t", file=fw)
        print(splitted1[i],  end="\t", file=fw)
        current_section = None
        pathways = []
        for line in splitted[i].rstrip().split("\n"):
            section = line[:12].strip()  # section names are within 12 columns
            if not section == "":
                current_section = section
            if current_section == "PATHWAY":
                pathway = line[12:]
                pathway = pathway[pathway.find(" "):].strip()
                pathways.append(pathway)
        print(";".join(pathways), file=fw)


file_name="query.ko"
acc=set()
for x in open(file_name,"r"):
    acc.add(x.rstrip())
acc = list(acc)
l = len(acc)
print(l)
fw = open("KEGG_OP.txt", "w")
for start in range(0,len(acc), 10):
    entry = acc[start:start+10]
    download_data(entry, fw)
fw.close()
