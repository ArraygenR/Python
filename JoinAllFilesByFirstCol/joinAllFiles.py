import pandas as pd
import os
result = pd.DataFrame({})
cnt = 0
for files in os.listdir("count_L"):
    if files.endswith(".txt"):
        df = pd.read_csv(os.path.join("count_L", files), sep="\t", names=['Gene', files.replace(".txt","")])
        if cnt == 0:
            result = df.copy()
        else:
            result = pd.merge(df, result, how='outer', on=['Gene'])
        cnt += 1

result = result.fillna(0)
result.to_csv("combined.txt", index=False, sep="\t")