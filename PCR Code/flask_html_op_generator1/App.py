from flask import Flask , render_template, send_file, request, redirect, url_for
from werkzeug.utils import secure_filename
from models.model import generate_html_op, download_xlsx_op , pie_chart, barplot, stote_in_database_file, fetch_from_database_file
from models.step1 import step1_make_input_for_provean
from models.step2 import generateProvean


import os
app = Flask(__name__)
UPLOAD_FOLDER = 'static/FileDatabase'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/', methods=['GET'])
def index():
    return render_template("index.html")

@app.route('/submit_data/', methods=['POST'])
def submit():
    if request.method == "POST":
        name= request.form['name']
        date = request.form['date']
        ATPL = request.form['ATPL']
        gene = request.form['gene']
        organism = request.form['organism']
        No_of_Sample = request.form['No_of_Sample']
        fileGblast= request.files['gblast']
        filePblast= request.files['pblast']
        filePfa= request.files['pfa']
        
        output_folder_name = str(ATPL+name+gene).replace(" ", "_")
        if not os.path.exists(os.path.join(app.config['UPLOAD_FOLDER'], output_folder_name)):
            os.mkdir(os.path.join(app.config['UPLOAD_FOLDER'], output_folder_name))

        filenameGblast = ""
        if fileGblast.filename != '':
            filenameGblast = secure_filename(fileGblast.filename)
            fileGblast.save(os.path.join(app.config['UPLOAD_FOLDER'],output_folder_name, filenameGblast))

        filenamePblast = ""
        if filePblast.filename != '':
            filenamePblast = secure_filename(filePblast.filename)
            filePblast.save(os.path.join(app.config['UPLOAD_FOLDER'],output_folder_name, filenamePblast))

        filenamePfa=""
        if filePfa.filename != '':
            filenamePfa = secure_filename(filePfa.filename)
            filePfa.save(os.path.join(app.config['UPLOAD_FOLDER'],output_folder_name, filenamePfa))

        stote_in_database_file(name, date, ATPL, gene, organism, No_of_Sample, output_folder_name, filenameGblast, filenamePblast, filenamePfa)
        return redirect(url_for('result'))

@app.route('/result/', methods=['GET'])
def result():
    tblRows = fetch_from_database_file()
    return render_template("result.html" , tblRows=tblRows)

@app.route('/output/', methods=['GET'])
def output():
    if request.method == "GET":

        folder = request.args['folder']
        gene_blast_file = request.args['gene_blast_file']
        protein_blast_file = request.args['protein_blast_file']
        protein_fasta_file = request.args['protein_fasta_file']
        details ={
            "name" : request.args['name'],
            "date" : request.args.get('date'),
            "ATPL" : request.args.get('ATPL'),
            "gene" : request.args['gene'],
            "organism" : request.args['organism'],
            "No_of_Sample" : request.args['No_of_Sample']
        }
        OP_file_name = os.path.join(os.getcwd() ,"static/FileDatabase", folder,gene_blast_file).split("/")
        f_name = "OP_" + OP_file_name.pop()
        OP_file_name.append(f_name)
        OP_file_name = "/".join(OP_file_name)
        print(OP_file_name)
        if not os.path.exists(OP_file_name) :
            if protein_blast_file == "" and protein_fasta_file == "":
                step1_make_input_for_provean(os.path.join("static/FileDatabase", folder , gene_blast_file))

            else:
                step1_make_input_for_provean(
                    os.path.join("static/FileDatabase", folder , gene_blast_file),
                    os.path.join("static/FileDatabase", folder , protein_blast_file),
                    os.path.join("static/FileDatabase", folder , protein_fasta_file)
                )
                OP_file_name1 = os.path.join(os.getcwd() ,"static/FileDatabase", folder, gene_blast_file).split("/")
                OP_file_name1.pop()
                OP_file_name1.append("output.txt")
                OP_file_name1 = "/".join(OP_file_name1,)

                generateProvean(OP_file_name1, os.path.join(os.getcwd() , "static/FileDatabase", folder, protein_fasta_file) ,OP_file_name)
                #step1_make_input_for_provean(os.path.join("static/FileDatabase", folder , gene_blast_file))

        html_data=generate_html_op(OP_file_name)
        p = html_data[2]
        Mutation_p = [len(p), p.count("SNP"), p.count("insertion"), p.count("deletion")]
        g = html_data[3]
        Mutation_g = [len(g), g.count("SNP"), g.count("insertion"), g.count("deletion")]
        del_or_neu = html_data[4]
        Mutation_p_del_or_neu = [del_or_neu.count("neutral"), del_or_neu.count("deleterious")]
        status = html_data[5]
        if status != "NonProtein":
            pie = pie_chart(Mutation_g, Mutation_p)
        else:
            pie = pie_chart(Mutation_g, Mutation_p=None)
        return render_template('output.html',Details =details, tblRows=html_data[0], TotalSample=len(html_data[1]),
                               Mutation_p=Mutation_p,
                               Mutation_g=Mutation_g, pie_chart=pie,
                               Mutation_p_del_or_neu=barplot(Mutation_p_del_or_neu), status=status)

@app.route('/download_xlsx_op/', methods=['GET'])
def download_xlsx():
    if request.method == "GET":
        folder = request.args['folder']
        gene_blast_file = request.args['gene_blast_file']
        OP_file_name = os.path.join("static/FileDatabase", folder, gene_blast_file).split("/")
        f_name = "OP_" + OP_file_name.pop()
        OP_file_name.append(f_name)
        OP_file_name = "/".join(OP_file_name)
        download_xlsx_op(OP_file_name)
        return send_file(OP_file_name+".xlsx", as_attachment=True, attachment_filename=f_name+'.xlsx')

app.run()