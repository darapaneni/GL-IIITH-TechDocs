import os
import subprocess
from flask import current_app
import sqlalchemy as db
from sqlalchemy import create_engine, select, update, delete
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
##from DBConnect import session_factory
##from orm_Tables import Document, Permission, DocumentHistory, UserHistory, User
import pdflatex
from pdflatex import PDFLaTeX

#data_path = ProdConfig.DIR_ROOT + ProdConfig.DIR_DATA 
data_path = "/techdocs_filesystem/testdata/be04e5f4-ea34-4ad7-9258-4b02a7021097"

all_tex_files = []

##session  = session_factory()
##sql_stmt = (select(User.UserId))
##sql_result = session.execute(sql_stmt)
      
##for row in sql_result:
   ## userid = row[0]
file_directory = data_path 
    ##+ '/' + userid
for dirs,subdirs,files in os.walk(file_directory):  
    for file in files:
        if file.endswith(".tex"):
            all_tex_files.append(os.path.join(dirs,file))

for tex_files in all_tex_files:
    pdfl = PDFLaTeX.from_texfile(tex_files)
    pdf, log, completed_process = pdfl.create_pdf(keep_pdf_file=True, keep_log_file=True)

##session.close()
    
