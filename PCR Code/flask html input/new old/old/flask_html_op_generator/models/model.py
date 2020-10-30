import pandas as pd
import os

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


def generate_html_op(file_path):
    retuen_list = []
    f = open(file_path, "r")
    f.readline()
    for line in f:
        splitted = line.rstrip().split("\t")
        if len(list(filter(None, splitted))) > 0:
            c1 = provean(*splitted)
            retuen_list.append(c1)
    return retuen_list

def download_xlsx_op(file_path):
    df = pd.read_csv(file_path, sep ="\t")
    writer = pd.ExcelWriter(os.getcwd()+"/static/files/PCR_Product_Variants_Results.xlsx", engine='xlsxwriter')
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