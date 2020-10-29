import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns

df = pd.read_csv("/home/arraygen/Desktop/Akshata/Python/volcanoplot/DEG_Case_Vs_Control.csv", sep ="\t", header = 1)

FCcol = 4
PvalCol = 6
annot = 1
df = df[(-np.log10(df.iloc[:,PvalCol]) != 0)]
plt.figure(figsize=(12,7))
plt.scatter(df.iloc[:,[FCcol]], -np.log10(df.iloc[:,[PvalCol]]), color= "gray",s=1)
plt.xlim([-6, 7])
up_data  = df[(df.iloc[:,PvalCol] < 0.05) & (df.iloc[:,FCcol] > 0.8) ]
plt.scatter(up_data.iloc[:,[FCcol]], -np.log10(up_data.iloc[:,[PvalCol]]), color= "red",s=1)
if annot == 1:
    for i, txt in enumerate(up_data.iloc[:,0]):
        if up_data.iloc[i,FCcol] > 2.8:
            if -np.log10(up_data.iloc[i,PvalCol]) < 5:
                plt.annotate(txt, (up_data.iloc[i,FCcol],  -np.log10(up_data.iloc[i,PvalCol])))

down_data  = df[(df.iloc[:,PvalCol] < 0.05) & (df.iloc[:,FCcol] < -0.8) ]
plt.scatter(down_data.iloc[:,[FCcol]], -np.log10(down_data.iloc[:,[PvalCol]]), color= "green",s=1)
if annot == 1:
    for i, txt in enumerate(down_data.iloc[:,0]):
        if down_data.iloc[i,FCcol] < -4.5:
            if -np.log10(down_data.iloc[i, PvalCol]) < 5:
                plt.annotate(txt, (down_data.iloc[i,FCcol],  -np.log10(down_data.iloc[i,PvalCol])))

plt.legend(["Not sig", "Up", "Down"], loc ="center right" ,markerscale=3. , fontsize=11)
plt.xlabel(df.columns[FCcol])
plt.ylabel('-log10(PValue)')
sns.despine()
#plt.show()
plt.savefig('fig2.png')
