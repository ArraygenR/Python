import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
import sys

opts = [opt for opt in sys.argv[1:] if opt.startswith("--")]
args = [arg for arg in sys.argv[1:] if not arg.startswith("--")]
#print(opts)
#print(args)
if "--i" in opts and "--fc" in opts and "--pval" in opts:

    FCcol = int(args[opts.index("--fc")])-1
    PvalCol = int(args[opts.index("--pval")])-1
    file_path = args[opts.index("--i")]

    if "--sep" in opts:
        sep = args[opts.index("--sep")]
        if "\\" in sep:
            sep = sep.replace("\\t" ,"\t")
            sep = sep.replace("\\n", "\n")
            sep = sep.replace("\\r", "\r")
            print(sep)
    else:
        sep = "\t"

    if "--upreg" in opts:
        upreg = float(args[opts.index("--upreg")])
    else:
        upreg = 0.8

    if "--downreg" in opts:
        downreg = float(args[opts.index("--downreg")])
    else:
        downreg = -0.8

    if "--sig" in opts:
        sig = float(args[opts.index("--sig")])
    else:
        sig = 0.05

    if "--annot" in opts:
        annot = int(args[opts.index("--annot")])

        if not (annot == 0 or annot == 1):
            print("Annotation should be 0(No) or 1(Yes)")

        if annot == 1:
            if "--geneid" in opts:
                gene_id = int(args[opts.index("--geneid")]) - 1
            else:
                print("If --annot is set to 1 then its compulsory* have gene id col number")

            if "--annot_upreg" in opts:
                annot_upreg = float(args[opts.index("--annot_upreg")])
            else:
                annot_upreg = 3.5

            if "--annot_downpreg" in opts:
                annot_downpreg = float(args[opts.index("--annot_downpreg")])
            else:
                annot_downpreg = -3.5

            if "--annot_sig_from" in opts:
                annot_sig_from = float(args[opts.index("--annot_sig_from")])
            else:
                annot_sig_from = -np.log10(sig)

            if "--annot_sig_to" in opts:
                annot_sig_to = float(args[opts.index("--annot_sig_to")])
            else:
                annot_sig_to = 5
    else:
        annot = 0

    df = pd.read_csv(file_path, sep=sep, error_bad_lines=False)
    #print(df.iloc[:, PvalCol].head())
    df = df[(-np.log10(df.iloc[:, PvalCol]) != 0)]
    plt.figure(figsize=(12, 7))
    plt.scatter(df.iloc[:, [FCcol]], -np.log10(df.iloc[:, [PvalCol]]), color="gray", s=1)
    #print(df.iloc[:, [FCcol]].min()[0])
    #print([min(df.iloc[1:, [FCcol]]), max(df.iloc[1:, [FCcol]])])
    plt.xlim([ df.iloc[:, [FCcol]].min()[0], df.iloc[:, [FCcol]].max()[0]+2 ])

    up_data = df[(df.iloc[:, PvalCol] < sig) & (df.iloc[:, FCcol] > upreg)]
    plt.scatter(up_data.iloc[:, [FCcol]], -np.log10(up_data.iloc[:, [PvalCol]]), color="red", s=1)
    if annot == 1:
        #print(up_data.iloc[:, gene_id])
        for i, txt in enumerate(up_data.iloc[:, gene_id]):
            if up_data.iloc[i, FCcol] > annot_upreg:
                if -np.log10(up_data.iloc[i, PvalCol]) > annot_sig_from and -np.log10(up_data.iloc[i, PvalCol]) < annot_sig_to:
                    plt.annotate(txt, (up_data.iloc[i, FCcol], -np.log10(up_data.iloc[i, PvalCol])))

    down_data = df[(df.iloc[:, PvalCol] < sig) & (df.iloc[:, FCcol] < downreg)]
    plt.scatter(down_data.iloc[:, [FCcol]], -np.log10(down_data.iloc[:, [PvalCol]]), color="blue", s=1)

    if annot == 1:
        for i, txt in enumerate(down_data.iloc[:, gene_id]):
            if down_data.iloc[i, FCcol] < annot_downpreg:
                if -np.log10(down_data.iloc[i, PvalCol]) > annot_sig_from and -np.log10(down_data.iloc[i, PvalCol]) < annot_sig_to:
                    plt.annotate(txt, (down_data.iloc[i, FCcol], -np.log10(down_data.iloc[i, PvalCol])))

    plt.legend(["Not sig", "Up", "Down"], loc="center right", markerscale=3., fontsize=11)
    plt.xlabel(df.columns[FCcol])
    plt.ylabel('-log10(PValue)')
    sns.despine()
    # plt.show()
    plt.savefig(df.columns[FCcol]+str(annot)+'.png')

else:
    print("""
    Program: python3 volcano_plot_maker.cpython-36.pyc 
    
    Usage:   python3 volcano_plot_maker.cpython-36.pyc <command> [options]

    Commands:   
    
        --i                  Compulsory. This must have option of input file path with name ( file data must be tab separated)
        --sep                Optional. file data separator default set to "\\t"
        --fc                 Compulsory. Column number of FoldChange
        --pval               Compulsory. Column number of PValue
        
        --upreg              Optional. Default UpRegulated cut off set to > 0.8
        --downreg            Optional. Default DownRegulated cut off set to < -0.8
        --sig                Optional. Default Significant value set to < 0.05
        
        --annot              Optional. Default value 0(No need of annotation). Must be 0 or 1(Annotation for points)
        --geneid             Optional. Gene Id col number. If -annot is set to 1 then its compulsory* have gene id col number
        --annot_upreg        Optional. Default display annotation UpRegulated cut off set to  > 3.5
        --annot_downpreg     Optional. Default display annotation UpRegulated cut off set to  < -3.5
        --annot_sig_from     Optional. Default display annotation significant cut off set to  > -log10(sig)
        --annot_sig_to       Optional. Default display annotation significant cut off set to  < 5
    Ex :
        
        python3 volcano_plot_maker.cpython-36.pyc --i "input/DEG_Case_Vs_Control.csv" --fc 5 --pval 7
        
        python3 volcano_plot_maker.cpython-36.pyc --i "input/DEG_Case_Vs_Control.csv" --fc 5 --pval 7 --sep "," --annot 1 --geneid 1 --annot_upreg 3 --annot_downpreg -4 --annot_sig_to 4.5
       
    """)
