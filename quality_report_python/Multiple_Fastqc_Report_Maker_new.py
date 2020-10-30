try:
    from zipfile import ZipFile
    from bs4 import BeautifulSoup
    import base64, io
    import xlsxwriter
    import os
except ImportError as e:
    print("""
    Check packages given below are installed or not 
    zipfile, bs4, base64, io, os, xlsxwriter
    If not installed install using below commands
    Linux User:
    pip3 install package_name
    
    Windows user:
    pip install package_name
    """)

class style_sheet:
    merge_format = {
        'bold': True,
        'border': False,
        'align': 'center',
        'valign': 'vcenter',
        'bg_color':'#D9D9D9',
        'font_color': '#993300',
        'font_size':12,
        'font_name':'Arial'
    }
    text_wrap_format = {
        'text_wrap': True,
        'valign': 'top',
        'font_size':10,
        'font_name':'Arial'
    }
    text_heading_format ={
        'bold': True,
        'font_color': '#993300'
    }

def summary(file):
    f = open(file)
    html = f.read()
    soup = BeautifulSoup(html, 'html.parser')
    tables = soup.findAll("table")[0]
    list_of_rows = []
    for row in tables.findAll('tr')[1:]:
        list_of_cells = []
        for cell in row.findAll('td'):
            list_of_cells.append(cell.text)
        list_of_rows.append(list_of_cells)
    return (list_of_rows)


def create_summary_sheet(workbook, line):

    worksheet_summary = workbook.add_worksheet(name="Raw_Summary")
    worksheet_summary.set_tab_color('#D9D9D9')

    style = style_sheet()
    merge_format = workbook.add_format(style.merge_format)
    text_wrap_format = workbook.add_format(style.text_wrap_format)

    worksheet_summary.set_row(0, 40)
    if len(line) > 3:
        worksheet_summary.set_column('A:E', 15)
        worksheet_summary.merge_range('A1:E1', 'FastQC Quality Report', merge_format)
    else:
        worksheet_summary.set_column('A:C', 15)
        worksheet_summary.merge_range('A1:C1', 'FastQC Quality Report', merge_format)

    col = 0
    for file in line[1:len(line)]:
        #print(file)
        if file.endswith(".fq"):
            file = line[0]+"/"+file[:-3]+ "_fastqc/fastqc_report.html"
            #print(file)
        else:
            file = line[0]+"/"+file.replace(".fastq", "")+ "_fastqc/fastqc_report.html"

        s1 = summary(file)
        row = 2
        for s in s1:
            if col == 0:
                worksheet_summary.write(row, col, s[0], text_wrap_format)
            worksheet_summary.write(row, col + 1, s[1], text_wrap_format)
            row = row + 1
        col = col + 1
    return worksheet_summary

def Fastqc_data_sheet(workbook, line, first_col, sencond_col= None):
    style = style_sheet()
    merge_format = workbook.add_format(style.merge_format)
    text_wrap_format = workbook.add_format(style.text_wrap_format)

    if line[sencond_col].endswith(".fq"):
        name = line[sencond_col][:-3] + "_fastqc"
    else:
        name = line[first_col].replace(".fastq", "_fastqc")

    if len("Data_"+name) >= 31:
        worksheet_fastqc = workbook.add_worksheet(name=("Data_"+name)[:10]+name[-21:])
    else:
        worksheet_fastqc = workbook.add_worksheet(name=("Data_" + name))


    file_name = os.path.join(line[0], name, "fastqc_data.txt")
    print(file_name)
    f1 = open(file_name, "r")
    data = f1.read().split(">>END_MODULE")
    length_of_each = []
    col = 0
    row = 1
    for d in data:
        if "Basic Statistics" in d:
            worksheet_fastqc.set_row(0, 30)
            worksheet_fastqc.set_column('A:B', 15)
            worksheet_fastqc.merge_range('A1:B1', line[first_col], merge_format)
            all_data = d.strip().split("\n")
            # print(all_data)
            all_data.pop(0)

            for all_data_1 in all_data:
                s1 = all_data_1.split("\t")
                worksheet_fastqc.write(row, col, s1[0], text_wrap_format)
                worksheet_fastqc.write(row, col + 1, s1[1], text_wrap_format)
                row = row + 1
            col = col + 1

        if "#Base" in d:
            all_data = d.strip().split("\n")
            length_of_each.append(len(all_data))

    min_len = min(length_of_each)
    #print(min_len)
    cnt = 0
    old_row = row + 1
    old_col = 0
    for d in data:
        if "#Base" in d:
            all_data = d.strip().split("\n")
            all_data.pop(0)

            row = old_row
            for l in all_data:
                split_l = l.split("\t")
                # print(split_l)
                if cnt != 0:
                    split_l.pop(0)
                col = old_col
                for s in split_l:
                    worksheet_fastqc.write(row, col, s, text_wrap_format)
                    col = col + 1
                row = row + 1
            cnt = cnt + 1
            old_col = col
    f1.close()
    if sencond_col != None:
        if line[sencond_col].endswith(".fq"):
            name = line[sencond_col][:-3]+"_fastqc"
        else:
            name = line[sencond_col].replace(".fastq", "_fastqc")

        f1 = open(os.path.join(line[0], name, "fastqc_data.txt"), "r")
        data = f1.read().split(">>END_MODULE")
        length_of_each = []
        col = old_col +1
        row = 1
        for d in data:
            if "Basic Statistics" in d:
                worksheet_fastqc.set_column('N:O', 15)
                worksheet_fastqc.merge_range('N1:O1', line[sencond_col], merge_format)
                all_data = d.strip().split("\n")
                # print(all_data)
                all_data.pop(0)

                for all_data_1 in all_data:
                    s1 = all_data_1.split("\t")
                    worksheet_fastqc.write(row, col, s1[0], text_wrap_format)
                    worksheet_fastqc.write(row, col + 1, s1[1], text_wrap_format)
                    row = row + 1
                col = col + 1

            if "#Base" in d:
                all_data = d.strip().split("\n")
                length_of_each.append(len(all_data))

        min_len = min(length_of_each)
        #print(min_len)
        cnt = 0
        old_row = row + 1
        old_col = old_col+1
        for d in data:
            if "#Base" in d:
                all_data = d.strip().split("\n")
                all_data.pop(0)

                row = old_row
                for l in all_data:
                    split_l = l.split("\t")
                    # print(split_l)
                    if cnt != 0:
                        split_l.pop(0)
                    col = old_col
                    for s in split_l:
                        worksheet_fastqc.write(row, col, s, text_wrap_format)
                        col = col + 1
                    row = row + 1
                cnt = cnt + 1
                old_col = col
    return worksheet_fastqc

def Fastqc_report_sheet(workbook, line, first_col, sencond_col= None):
    style = style_sheet()
    merge_format = workbook.add_format(style.merge_format)
    text_wrap_format = workbook.add_format(style.text_wrap_format)
    text_heading_format = workbook.add_format(style.text_heading_format)

    if line[sencond_col].endswith(".fq"):
        name = line[first_col][:-3] + "_fastqc"
    else:
        name = line[first_col].replace(".fastq", "_fastqc")

    if len("Data_" + name) >= 31:
        worksheet_fastqc = workbook.add_worksheet(name=("Report_" + name)[:31])
    else:
        worksheet_fastqc = workbook.add_worksheet(name=("Report_" + name))



    file = os.path.join(line[0], name, "fastqc_report.html")
    #print(file)
    worksheet_fastqc.set_row(0, 30)
    worksheet_fastqc.set_column('A:B', 15)
    worksheet_fastqc.merge_range('A1:B1', line[first_col], merge_format)

    f1 = open(file, "r")
    html_doc = f1.read()
    soup = BeautifulSoup(html_doc, 'html.parser')
    main_div = soup.findAll("div", {"class": "main"})
    inside_main_div = main_div[0].findAll("div", {"class": "module"})
    row = 2
    col = 0
    for module in inside_main_div:
        # print(len(module.findAll("table")))
        if len(module.findAll("table")) != 0:
            tables = module.findAll("table")
            for table in tables:

                for rowt in table.findAll('tr'):
                    subcellcol = col
                    for cellt in rowt.findAll('th'):
                        # print(rowt.text)
                        worksheet_fastqc.write(row, subcellcol, cellt.text, text_heading_format)
                        subcellcol = subcellcol + 1

                    subcellcol = col
                    for cellt in rowt.findAll('td'):
                        worksheet_fastqc.write(row, subcellcol, cellt.text, text_wrap_format)
                        subcellcol = subcellcol + 1
                    row = row + 1
                row = row + 1
        else:
            heading = module.findAll("h2")[0]
            heading_name = heading.findAll(text=True)

            img_name = heading_name[0].replace(" ", "_")
            heading_image = heading.findAll("img")[0]

            heading_image = heading_image['src'][heading_image['src'].find("base64,") + len("base64,"):]
            imgdata = base64.b64decode(heading_image)
            image = io.BytesIO(imgdata)

            worksheet_fastqc.insert_image('A' + str(row), img_name + "1.png",
                                          {'image_data': image, 'x_scale': 0.8, 'y_scale': 0.8})
            worksheet_fastqc.write(row - 1, col + 1, heading_name[0], text_heading_format)
            row = row + 2

            p = module = module.findAll("p")[0]

            img = p.findAll("img")
            if len(img) > 0:
                img = img[0]
                product_image = img['src'][img['src'].find("base64,") + len("base64,"):]
                imgdata = base64.b64decode(product_image)
                image = io.BytesIO(imgdata)
                worksheet_fastqc.insert_image('A' + str(row), img_name + ".png",
                                              {'image_data': image, 'x_scale': 0.4, 'y_scale': 0.4})
                row = row + 15
            else:
                name = p.findAll(text=True)[0]
                # print(name)
                worksheet_fastqc.write(row - 2, col + 1, name)
                row = row + 2

    if sencond_col != None:

        if line[sencond_col].endswith(".fq"):
            name = line[sencond_col][:-3]+"_fastqc"
        else:
            name = line[sencond_col].replace(".fastq", "_fastqc")

        file = os.path.join(line[0], name, "fastqc_report.html")
        # print(file)
        worksheet_fastqc.set_row(0, 30)
        file = os.path.join(line[0], name, "fastqc_report.html")
        worksheet_fastqc.set_row(0, 30)
        worksheet_fastqc.set_column('I:J', 15)
        worksheet_fastqc.merge_range('I1:J1', line[sencond_col], merge_format)

        f1 = open(file, "r")
        html_doc = f1.read()
        soup = BeautifulSoup(html_doc, 'html.parser')
        main_div = soup.findAll("div", {"class": "main"})
        inside_main_div = main_div[0].findAll("div", {"class": "module"})
        row = 2
        col = 8
        for module in inside_main_div:
            # print(len(module.findAll("table")))
            if len(module.findAll("table")) != 0:
                tables = module.findAll("table")
                for table in tables:

                    for rowt in table.findAll('tr'):
                        subcellcol = col
                        for cellt in rowt.findAll('th'):
                            # print(rowt.text)
                            worksheet_fastqc.write(row, subcellcol, cellt.text, text_heading_format)
                            subcellcol = subcellcol + 1

                        subcellcol = col
                        for cellt in rowt.findAll('td'):
                            worksheet_fastqc.write(row, subcellcol, cellt.text, text_wrap_format)
                            subcellcol = subcellcol + 1
                        row = row + 1
                    row = row + 1
            else:
                heading = module.findAll("h2")[0]
                heading_name = heading.findAll(text=True)

                img_name = heading_name[0].replace(" ", "_")
                heading_image = heading.findAll("img")[0]

                heading_image = heading_image['src'][heading_image['src'].find("base64,") + len("base64,"):]
                imgdata = base64.b64decode(heading_image)
                image = io.BytesIO(imgdata)

                worksheet_fastqc.insert_image('I' + str(row), img_name + "1.png",
                                              {'image_data': image, 'x_scale': 0.8, 'y_scale': 0.8})
                worksheet_fastqc.write(row - 1, col + 1, heading_name[0], text_heading_format)
                row = row + 2

                p = module.findAll("p")[0]

                img = p.findAll("img")
                if len(img) > 0:
                    img = img[0]
                    product_image = img['src'][img['src'].find("base64,") + len("base64,"):]
                    imgdata = base64.b64decode(product_image)
                    image = io.BytesIO(imgdata)
                    worksheet_fastqc.insert_image('I' + str(row), img_name + ".png",
                                                  {'image_data': image, 'x_scale': 0.4, 'y_scale': 0.4})
                    row = row + 15
                else:
                    name = p.findAll(text=True)[0]
                    worksheet_fastqc.write(row - 2, col + 1, name)
                    row = row + 2

    return worksheet_fastqc

# specifying the zip file name
try:
    config_file = open("config.csv","r")
except:
    config_file = open(input("Enter Path of file :"),"r")

config_file.readline()
for lines in config_file:
    line = list(filter(None, lines.strip().split(",")))
    os.chdir(line[0])

    for file in os.listdir(line[0]):
        if file.endswith(".zip"):
            with ZipFile(os.path.join(line[0], file), 'r') as zip:
                zip.extractall()
    print(line)
    workbook = xlsxwriter.Workbook((line[0].split("/")[len(line[0].split("/"))-1]+'.xlsx'))
    worksheet_summary = create_summary_sheet(workbook , line)
    
    if len(line) > 3:
        Fastqc_data_sheet1 = Fastqc_data_sheet(workbook , line, 1, 3)
        Fastqc_data_sheet2 = Fastqc_data_sheet(workbook, line, 2, 4)

        Fastqc_report_sheet1 = Fastqc_report_sheet(workbook, line, 1, 3)
        Fastqc_report_sheet2 = Fastqc_report_sheet(workbook, line, 2, 4)
    elif len(line) == 3:
        if line[1].endswith(".fq"):
            name = line[1][:-3]+"_fastqc"
        else:
            name = line[1].replace(".fastq", "_fastqc")

        if name in line[2]:

            Fastqc_data_sheet1 = Fastqc_data_sheet(workbook, line, 1, 2)
            Fastqc_report_sheet1 = Fastqc_report_sheet(workbook, line, 1, 2)

        else:
            Fastqc_data_sheet1 = Fastqc_data_sheet(workbook, line, 1)
            Fastqc_data_sheet2 = Fastqc_data_sheet(workbook, line, 2)

            Fastqc_report_sheet1 = Fastqc_report_sheet(workbook, line, 1)
            Fastqc_report_sheet2 = Fastqc_report_sheet(workbook, line, 2)
    else:
        Fastqc_data_sheet1 = Fastqc_data_sheet(workbook, line, 1)
        Fastqc_report_sheet1 = Fastqc_report_sheet(workbook, line, 1)

    workbook.close()
