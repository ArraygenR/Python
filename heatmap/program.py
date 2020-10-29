import seaborn as sns
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib as mpl

#sns.set(color_codes=True)
#DEG_Common.csv
#DEG_Common_Control Vs UPF3B_KO_Clone-1 & UPF3B_KO_Clone-3.csv

df = pd.read_csv("/home/arraygen/Desktop/Akshata/Python/heatmap/Combined_DEG1.csv", sep ="\t" , header = 1,low_memory=False)
print(df)
#df.set_index([df.columns[0],], inplace=True)
FCcol = [4,10]
PvalCol = [6, 12]

for FCcol_1 in FCcol:
    df = df.rename(columns={df.columns[FCcol_1]: df.columns[FCcol_1].replace("log2(fold_change)","").strip()})

print(df)


df['mean'] = df.iloc[:,PvalCol].mean(axis=1)
filtered_data  = df[ df['mean'] < 0.05 ]
#filtered_data = df
color_list = [(0, 'green'),  (0.5, 'white'),(1, 'red')]
#sns.diverging_palette(10, 220, sep=80, n=100)
#cmap1 = mpl.colors.LinearSegmentedColormap.from_list('unevently divided', color_list)
#sns.diverging_palette(10, 220, sep=80, n=100)
g = sns.clustermap(filtered_data.iloc[:, FCcol],
                   #figsize=(14, 14),
                   cmap= sns.diverging_palette(10, 220, sep=80, n=100),
                   yticklabels=False,
                   vmin = -2, vmax=2,
                   cbar_pos = (0, 1, .20, .05),
                   cbar_kws={"orientation": "horizontal",'ticks': [-1, 0, 1], 'label': 'LogFC'})
g.cax.set_title("Color Key")
plt.setp(g.ax_heatmap.yaxis.get_majorticklabels(), rotation=40)
g.savefig("heatmaptest.png")
#plt.show()