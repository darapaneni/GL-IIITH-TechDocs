# Store this code in 'app.py' file
import os
import pathlib
import stat
import subprocess
import sys
import warnings
from os.path import exists
from pdflatex import PDFLaTeX       

from flask import request, Blueprint, make_response, jsonify, current_app
from config import ProdConfig
from ..UserAuthentication.JWTAuthentication import authentication

# Suppress warnings
warnings.filterwarnings("ignore")

sys.path.append('../')

convertLatexToPdfBlueprint = Blueprint('convertLatexToPdfBlueprint', __name__)
data_path = ProdConfig.DIR_ROOT + ProdConfig.DIR_DATA

@convertLatexToPdfBlueprint.route('/api/convertLatexToPdf', methods=['GET'])
@authentication
def convertToPdf(user_id):
    dirpath  = data_path + '/' + user_id
    # TeX source filename
    tex_filename = request.args.get("filename",'NotAvailable',type=str)
    print('filename:'+tex_filename)
    filepath = dirpath + '/' + tex_filename
    if(filepath):
        print('filepath:'+filepath)
        file_exists = os.path.exists(filepath)
        if file_exists:
            print('file exists')
            filename, ext = os.path.splitext(filepath)
            # the corresponding PDF filename
            pdf_filename = filename + '.pdf'
            log_filename = filename + '.log'
            aux_filename = filename + '.aux'
            path = pathlib.Path(filepath).parent
            #os.chmod(path, stat.S_IRWXO)
            print(pdf_filename)

            #pdfl = pdf.from_texfile(f'{tex_filename}')
            #pdf, log, completed_process = pdfl.create_pdf(keep_pdf_file=True, keep_log_file=True)

            #print(pdf)
            #compile TeX file
            subprocess.run('pdflatex -output-directory '+os.path.dirname(filepath)+' ' + filepath, shell=True, check=True)
            

            if os.path.exists(log_filename):
                os.remove(log_filename)
            if os.path.exists(aux_filename):
                os.remove(aux_filename)

            # check if PDF is successfully generated
            if not os.path.exists(pdf_filename):
                current_app.logger.info('Converted PDF file could not be found. Latex to PDF conversion failed for the '
                                        'file: ' + tex_filename)
                return make_response(jsonify('Latex to PDF conversion failed for the file: ' + tex_filename), 500)
            
            current_app.logger.info('Latex to PDF conversion successful for the file: ' + tex_filename)
            return make_response(jsonify(pdf_filename), 202)
        else:
            print('file not exists')
            current_app.logger.info('Provided Latex filepath ' + filepath + ' not found.')
            return make_response(jsonify(filepath), 404)
    else:
            print('file arg not exists')
            current_app.logger.info('Provided Latex filepath ' + filepath + ' not found.')
            return make_response(jsonify(filepath), 404)
