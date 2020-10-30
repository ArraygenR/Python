from flask import Flask , render_template, send_file, request , redirect, flash
from werkzeug.utils import secure_filename

from models.model import generate_html_op, download_xlsx_op
from models.step1 import step1_make_input_for_provean
import os
app = Flask(__name__)
UPLOAD_FOLDER = '/home/arraygen/Desktop/Akshata/Python/blast handing/flask_html_op_generator/static/files/input_files'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/')
def upload_file():
   return render_template('index.html')


@app.route('/uploader', methods=['GET', 'POST'])
def upload_file1():
    if request.method == 'POST':
        files = request.files.getlist('files[]')
        if len(files) == 1:
            filename = secure_filename(files[0].filename)
            filename = secure_filename(files[0].filename)
            files[0].save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            step1_make_input_for_provean(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            table_row = generate_html_op(os.path.join(app.config['UPLOAD_FOLDER'], filename).replace(".txt", "")+"output.txt")
            return render_template('output.html', tblRows=table_row, status="NonProtein")

        elif len(files) == 3:
            all_file_names = []
            for file in files:
                filename = secure_filename(file.filename)
                all_file_names.append(filename)
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

            for filename in all_file_names:
                if "protein" in filename.lower():
                    print("Later needs to work on this")


@app.route('/output', methods=['GET'])
def index():
    if os.path.exists("/static/files/output2.txt"):
        table_row = generate_html_op(os.getcwd()+"/static/files/output2.txt")
        return render_template('upload.html', tblRows = table_row)
    else:
        step1_make_input_for_provean("/home/arraygen/Desktop/Akshata/Python/blast handing/flask_html_op_generator/static/files/input_files/AMPD.gene.Blast.Results1.txt")
        table_row = generate_html_op(os.getcwd() + "/static/files/output2.txt")
        return render_template('output.html', tblRows=table_row, status = "NonProtein")

@app.route('/download_xlsx_op/', methods=['GET'])
def download_xlsx():
    download_xlsx_op(os.getcwd()+"/static/files/output2.txt")
    return send_file(os.getcwd()+"/static/files/PCR_Product_Variants_Results.xlsx", as_attachment=True, attachment_filename='PCR_Product_Variants_Results.xlsx')

app.run()