
import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

df = pd.read_csv("NormalizedValues.csv")
df= df.set_index('Unnamed: 0')
l1=[]
for i in range(1,18):
    l1.append("Patient"+str(i))
for i in range(1,11):
    if i != 7:
        l1.append("Control"+str(i))
df.columns = l1
df= np.log2(df)
plt.figure(figsize=(15,15))
g= sns.clustermap(df, yticklabels=False, cmap="RdYlGn" )
ax = g.ax_heatmap
ax.set_ylabel("")
plt.savefig("heatmap_without_ids.png", bbox_inches = 'tight')
