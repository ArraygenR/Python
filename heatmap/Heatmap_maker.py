import seaborn as sns
import sys
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib as mpl

opts = [opt for opt in sys.argv[1:] if opt.startswith("--")]
args = [arg for arg in sys.argv[1:] if not arg.startswith("--")]

if "--i" in opts and "--fc" in opts and "--pval" in opts:
    file_path = args[opts.index("--i")]
    FCcol = list(map(lambda x: int(x)-1,list(args[opts.index("--fc")].strip().replace("[","").replace("]","").split(","))))
    PvalCol = list(map(lambda x: int(x)-1,list(args[opts.index("--pval")].strip().replace("[","").replace("]","").split(","))))
    if "--sep" in opts:
        sep = args[opts.index("--sep")]
        if "\\" in sep:
            sep = sep.replace("\\t" ,"\t")
            sep = sep.replace("\\n", "\n")
            sep = sep.replace("\\r", "\r")
            print(sep)
    else:
        sep = "\t"

    if "--sig" in opts:
        sig = float(args[opts.index("--sig")])
    else:
        sig = 0.05

    if "--c1" in opts and "--c2" in opts and "--c3" in opts:
        first_color = args[opts.index("--c1")]  # "green"
        second_color = args[opts.index("--c2")] # "white"
        third_color = args[opts.index("--c3")]  # "red"

        color_list = [(0, first_color), (0.35, second_color),(0.65, second_color), (1, third_color)]
        cmap1 = mpl.colors.LinearSegmentedColormap.from_list('unevently divided', color_list)
    else:
        cmap1 = sns.diverging_palette(10, 220, sep=80, n=100)

    df = pd.read_csv(file_path, sep =sep, header=0,low_memory=False)
    for FCcol_1 in FCcol:
        df = df.rename(columns={df.columns[FCcol_1]: df.columns[FCcol_1].replace("log2(fold_change)","").strip()})

    df['mean'] = df.iloc[:,PvalCol].mean(axis=1)
    filtered_data  = df[ df['mean'] < float(sig) ]
    if "--annot" in opts:
        annot = int(args[opts.index("--annot")])
        if annot == 1 and "--geneid" in opts:
            geneid = int(args[opts.index("--geneid")])-1
            data = filtered_data.iloc[:, FCcol]
            data = data.rename(index=filtered_data.iloc[:, geneid])
            #print(data)
            ytick = True
        elif annot == 1:
            geneid = 0
            data = filtered_data.iloc[:, FCcol]
            data = data.rename(index=filtered_data.iloc[:, geneid])
            print("You haven't mensioned --geneid. Therefor 1st column considered as geneid")
            ytick = True
        else:
            data = filtered_data.iloc[:, FCcol]
            ytick = False
    else:
        data = filtered_data.iloc[:, FCcol]
        ytick = False
    g = sns.clustermap(data,
                           cmap=cmap1,
                           yticklabels=ytick,
                           vmin = -2, vmax=2,
                           cbar_pos = (0, 1, .20, .05),
                           cbar_kws={"orientation": "horizontal",'ticks': [-1, 0, 1], 'label': 'LogFC'})
    g.cax.set_title("Color Key")
    output_name = file_path.split("/")[len(file_path.split("/"))-1].replace(".csv", "") + ".png"
    plt.savefig(output_name, bbox_inches = 'tight')

else:
    print("""
    Program: Heatmap_maker.cpython-36.pyc

    Usage:   Heatmap_maker.cpython-36.pyc <command> [options]

    Commands:   

        --i                  Compulsory. This must have option of input file path with name (file data must be tab separated)
        --sep                Optional. file data separator default set to "\\t"
        --fc                 Compulsory. Column number of FoldChange
        --pval               Compulsory. Column number of PValue

        --sig                Optional. Default Significant value set to < 0.05

        --annot              Optional. Default value 0(No need of annotation). Must be 0 or 1(Annotation for points)
        --geneid             Optional. Gene Id col number. If -annot is set to 1 then its compulsory* have gene id col number
        
        --c1                 Optional. Color 1 in Colorbar.
        --c2                 Optional. Color 2 in Colorbar.
        --c3                 Optional. Color 3 in Colorbar.
    Ex :

        Heatmap_maker.cpython-36.pyc --i "input/Combined_DEG1.csv" --fc [5,11] --pval [7,13] --sep "\\t"

        Heatmap_maker.cpython-36.pyc --i "input/Combined_DEG1.csv" --fc [5,11] --pval [7,13] --sep "," --c1 green --c2 white --c3 red

        Heatmap_maker.cpython-36.pyc --i "input/demo.csv" --fc [2,3,4,5,6,7,8,9] --pval [10] --sep "," --annot 1 --geneid 1 --c1 red --c2 "#fffffa" --c3 green

    """)
