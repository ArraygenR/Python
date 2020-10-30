import pandas as pd
import os
import matplotlib.pyplot as plt
import io
import base64
import seaborn as sns

class provean():
    def __init__(self, Query="", QLength="", Gene="", GLength="", GScore="", GExcept="", GIdentities="", GGaps="", GVariation="", GPosition="", GMutation_Type="", Protein="", PLength="", PScore="", PExcept="", PIdentities="", PGaps="", PVariation="", PPosition="", PMutation_Type="", PROVEAN_Input_Variants="",PROVEAN_Score="", Prediction_cutoff_2_dot_5=""):
         self.Query = Query
         self.QLength = QLength
         self.Gene = Gene
         self.GLength = GLength
         self.GScore = GScore
         self.GExcept = GExcept
         self.GIdentities = GIdentities
         self.GGaps = GGaps
         self.GVariation = GVariation
         self.GPosition = GPosition
         self.GMutation_Type = GMutation_Type
         self.Protein = Protein
         self.PLength = PLength
         self.PScore = PScore
         self.PExcept = PExcept
         self.PIdentities =PIdentities
         self.PGaps = PGaps
         self.PVariation = PVariation
         self.PPosition = PPosition
         self.PMutation_Type = PMutation_Type
         self.PROVEAN_Input_Variants = PROVEAN_Input_Variants
         self.PROVEAN_Score = PROVEAN_Score
         self.Prediction_cutoff_2_dot_5 = Prediction_cutoff_2_dot_5.strip()

class database():
    def __init__(self,name, date, ATPL, gene, organism, No_of_Sample, folder_name ,gene_blast_file, protein_blast_file ="", protein_fasta_file="" ):
        self.name = name
        self.date = date
        self.ATPL = ATPL
        self.gene = gene
        self.organism = organism
        self.No_of_Sample = No_of_Sample
        self.folder_name = folder_name
        self.gene_blast_file = gene_blast_file
        self.protein_blast_file = protein_blast_file
        self.protein_fasta_file = protein_fasta_file

def generate_html_op(file_path):
    Sample = []
    Mutation_g = []
    Mutation_p = []
    Mutation_p_del_or_neu = []
    status = "NonProtein"
    return_list = []
    f = open(file_path, "r")
    f.readline()
    for line in f:
        splitted = line.rstrip().split("\t")
        if len(list(filter(None, splitted))) > 0:
            if splitted[0].strip() != "":
                Sample.append(splitted[0].strip())
            if len(splitted) >= 20:
                if splitted[19].strip() != "":
                    Mutation_p.append(splitted[19].strip())
                    status = "Protein"
            if len(splitted) >= 23:
                if splitted[22].strip() != "":
                    Mutation_p_del_or_neu.append(splitted[22].strip())
            if splitted[10].strip() != "":
                Mutation_g.append(splitted[10].strip())
            c1 = provean(*splitted)
            return_list.append(c1)
    return [return_list, Sample, Mutation_p, Mutation_g , Mutation_p_del_or_neu, status]

def download_xlsx_op(file_path):
    df = pd.read_csv(file_path, sep ="\t")
    writer = pd.ExcelWriter(file_path+".xlsx", engine='xlsxwriter')
    df.to_excel(writer, sheet_name='PCR Product Variants Results', index= False)
    workbook = writer.book
    worksheet = writer.sheets['PCR Product Variants Results']

    # Add a header format.
    header_format = workbook.add_format({
        'bold': True,
        'text_wrap': True,
        'valign': 'top',
        'fg_color': '#D7E4BC',
        'border': 1})

    # Write the column headers with the defined format.
    for col_num, value in enumerate(df.columns.values):
        worksheet.write(0, col_num, value, header_format)
    writer.save()

def pie_chart(Mutation_g , Mutation_p = None):
    img = io.BytesIO()

    labels = ['SNP', 'Insertion', 'Deletion']
    if Mutation_p != None:
        fig1, (ax1, ax2) = plt.subplots(1,2)
        ax1.pie(Mutation_g[1:], autopct='%1.1f%%', startangle=30, pctdistance=1.3,labeldistance=1.1)
        #ax1.set_title('Fig 1 : Gene')
        ax2.pie(Mutation_p[1:], autopct='%1.1f%%', startangle=30, pctdistance=1.3,labeldistance=1.1)
       # ax2.set_title('Fig 2 : Protein')
        lgd = plt.legend(labels, bbox_to_anchor=(1.05, 1), loc='upper left')
    else:
        fig1, ax1 = plt.subplots()
        ax1.pie(Mutation_g[1:], autopct='%1.1f%%', startangle=65, pctdistance=1.3,labeldistance=1.2)
       # ax1.set_title('Fig 1 : Gene')

        lgd = plt.legend(labels, bbox_to_anchor=(1.05, 1), loc='upper left')

    plt.savefig(img, format='png', bbox_inches = 'tight',bbox_extra_artists=(lgd,),pad_inches = 0.3)
    img.seek(0)

    plot_url = base64.b64encode(img.getvalue()).decode()

    return plot_url

def barplot(Mutation_p_del_or_neu):
    img = io.BytesIO()
    fig1, ax1 = plt.subplots()

    ax1 = sns.barplot(x = ["Neutral", "Deleterious"], y= Mutation_p_del_or_neu )
   # ax1.set_title('Fig 3 : Prediction (cutoff = -2.5)')

    plt.savefig(img, format='png', bbox_inches='tight')
    img.seek(0)
    plot_url = base64.b64encode(img.getvalue()).decode()
    return plot_url

def stote_in_database_file(*argv):
    f = open("static/database_file.txt" , "a")
    f.write("\t".join(argv)+"\n")
    f.close()

def fetch_from_database_file():
    f = open("static/database_file.txt" , "r")
    data_list = []
    f.readline()
    for line in f:
        if line.strip() !="":
            splitted = line.split("\t")
            data = database(*splitted)
            data_list.append(data)
    f.close()
    return data_list
