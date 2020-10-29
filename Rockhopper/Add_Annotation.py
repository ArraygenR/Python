import os, pandas as pd


df = pd.read_csv("Annotation.txt", sep ="\t")
print(df.shape)
df = df.set_index("Synonym")
df = df[~df.index.duplicated(keep='first')]
df = df.drop_duplicates(keep='first')
data_dict = df.to_dict('index')
all_columns = "\t".join(df.columns).strip()



for folder in os.listdir("."):
    if(os.path.isdir(folder)):
        for sub_folder in (os.listdir(folder)):
            if(os.path.isdir(os.path.join(folder, sub_folder))):
                for sub_sub_folder in os.listdir(os.path.join(folder, sub_folder)):
                    if (os.path.isdir(os.path.join(folder, sub_folder,sub_sub_folder))):
                        file = [file  for file in os.listdir(os.path.join(folder, sub_folder, sub_sub_folder)) if (file.endswith("DE_results") and not file.startswith("Annot_"))][0]
                        input_file = os.path.join(folder, sub_folder, sub_sub_folder, file)
                        output_file = os.path.join(folder, sub_folder, sub_sub_folder, "Annot_"+file)
                        fw = open(output_file, "w")
                        f = open(input_file)
                        inside_columns= f.readline().strip()
                        print(all_columns+"\t"+inside_columns, file=fw)
                        for line in f:
                            splitted = line.strip().split("\t")
                            if splitted[0] in data_dict.keys():
                                print(line.strip()+"\t","\t".join([str(data_dict[splitted[0]][x]) for x in df.columns]), file=fw)
                                print(line.strip()+"\t","\t".join([str(data_dict[splitted[0]][x]) for x in df.columns]))
                                print(data_dict[splitted[0]])
