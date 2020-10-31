import os , pandas as pd

in1 = input("Enter Column name")

result = pd.DataFrame({})
cnt = 0
for files in os.listdir("."):
    if files.endswith(".csv"):
        #print(files)
        df = pd.read_csv(files, sep="\t")
        column = df[in1]
        column = column.dropna()
        list1 = []
        for _, r in column.iteritems():
            list1.extend(
                [k[:k.find("{")].strip() if "{" in k.strip() else k[:k.find("[")].strip() if "[" in k else k.strip() for
                 k in r.replace("PATHWAY:", "").strip().split(';')])
        df1 = pd.DataFrame(list1, columns=[in1])
        count = df1[in1].value_counts()
        count = pd.DataFrame(count).reset_index()
        count = count.rename(columns={"index": in1, in1: files.replace(".csv", "")})
        if cnt == 0:
            result = count.copy()
        else:
            result = pd.merge(count, result, how='outer', on=[in1])
        cnt += 1

result = result.fillna(0)
result.to_csv(in1+".txt", index=False, sep="\t")