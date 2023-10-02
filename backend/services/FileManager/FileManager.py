# Libraries
# from asyncore import file_dispatcher
import os
import warnings
import logging
import yaml
import requests
import json
import re
#from functools import singledispatchmethod
from datetime import datetime
from xml.dom.xmlbuilder import DocumentLS 
import sqlalchemy as db
from sqlalchemy import create_engine, select, update, delete
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from DBConnect import session_factory
from orm_Tables import Document, Permission, DocumentHistory, UserHistory, User
from flask import Flask, render_template, url_for, redirect, session, flash, request, jsonify, json, make_response
from flask import Blueprint
from flask import current_app
from config import ProdConfig
from ..UserAuthentication.JWTAuthentication import authentication
from ..DocumentVersionManager.DocumentVersionManager import VersionManage
from ..UserHistoryManager import *
from ..Permissions.permissions import get_user_permissions

# Suppress warnings
warnings.filterwarnings("ignore")

fileManagerBlueprint = Blueprint('fileManagerBlueprint', __name__)

data_path = ProdConfig.DIR_ROOT + ProdConfig.DIR_DATA 
log_path = ProdConfig.DIR_ROOT + ProdConfig.DIR_LOG
logging.basicConfig(filename=log_path)

# @fileManagerBlueprint.before_request
# def before_request_func():

#     data_path = current_app.config["DIR_ROOT"] + current_app.config["DIR_DATA"] 
#     log_path = current_app.config['DIR_ROOT'] + current_app.config['DIR_LOG']
#     if not os.path.exists(log_path):
#         open(log_path, 'a').close()
#     logging.basicConfig(filename=log_path)
    
#     return data_path, log_path

####################
# File Manager Class
class FileManage:
    v_filename = ''
    v_filepath = ''
    v_version  = 0
        
    @classmethod
    def createNewFile(cls, userid, filename, doctext):
        # data_path, log_path = before_request_func()
        datestr  = datetime.today().strftime('%Y%m%d%H%M%S')
        dirpath  = data_path + '/' + userid
        if (filename == ""):
            filename = 'untitled_'+datestr+'.tex'
        filepath = dirpath+'/'+filename
        if not os.path.exists(dirpath):
            os.makedirs(dirpath)
        cls.v_filename = filename
        cls.v_filepath = filepath
        
    
    @classmethod
    def writeToFile(cls, filepath, text):
        file_obj = open(filepath, "w")
        file_obj.write(text)
        file_obj.close()
        
    @classmethod
    def createNewVersion(cls, CurrVer):
        cls.v_version = CurrVer + 1
    
    @classmethod
    def uploadFile(cls, userid, filename, docdata):
        # data_path, log_path = before_request_func()
        #datestr  = datetime.today().strftime('%Y%m%d%H%M%S')
        dirpath  = data_path + '/' + userid
        filepath = dirpath+'/'+filename
        if not os.path.exists(dirpath):
            os.makedirs(dirpath)
        file_obj = open(filepath, "w")
        file_obj.write(docdata)
        file_obj.close() 

        cls.v_filename = filename
        cls.v_filepath = filepath
        
'''
# API to create a new file either empty or with data given
# Input: {'DocId':'', 'DocName':'', 'DocText':'', 'Uploaded':'', 'RefDocId':''}
# Processing: 
# 1. Authenticate user
# 2. Extract all input data 
# 3. Create file on the folder path
# 4. If data given, write the data to the file
# 5. Create an entry into Documents & Permissions table
# 6. Output: UserId, DocId, DocName, FilePath 
'''
@fileManagerBlueprint.route('/api/filecreate', methods = ['GET', 'POST'])
@authentication
def file_Create(user_id):
    userid      = 0
    docid       = 0
    docname     = ''
    doctext     = ''
    ver         = 0
    newfilepath = ''
    refdocid    = 0
    reffilepath = ''
    data_out    = {}
    mess_out    = 0
    username    = ''
    # data_path, log_path = before_request_func()

    current_app.logger.info("Service File Create initiated")

    if(request.method == 'POST'):
        # request data
        content  = request.get_json(silent=True)
        userid   = user_id
        docid    = int(content['DocId'])
        docname  = content['DocName']
        doctext  = content['DocText']
        isupload = bool(content['IsUpload'])
        refdocid = int(content['RefDocId'])
        istrash = 0
        
        docname_only = docname.split(".")[0]
        
        session  = session_factory()
        file_obj = FileManage()
        ver_obj  = VersionManage()
        
        # Save data into database
        try:
            # new file
            if ((docid == 0) or (docid == '')):
                ver = 1
            else:
                raise Exception("Wrong service called. Create file is for new file only!")
            
            # validate if User and document combination exists. Error out if so
            sql_stmt = select(Document.DocId).where(Document.DocName == docname_only, Document.UserId == userid)
            sql_result = session.execute(sql_stmt)
            noofrecords = len(sql_result.all())
            if (noofrecords > 0):
                raise Exception("filename already exists")
            
            # dry run testing - request from front end people to send out username instead of userid
            sql_stmt = (select(User.UserName).where(User.UserId == userid))
            sql_result = session.execute(sql_stmt)
            # there is always only 1 row
            for row in sql_result:
                username = row[0]
            
            # Method to create a new file path - object will store the values of filename, file path
            ver_obj.createNewVersionFile(userid, docname, ver, '')
            newfilepath = ver_obj.v_file_path
            docname     = ver_obj.v_file_name
        
            # create the file
            open(newfilepath, 'a').close()
        
            # entry into Documents table
            doc_entry = Document(userid, docname, newfilepath, datetime.today(), ver, isupload, istrash)
            session.add(doc_entry)
            session.flush()
            docid_out = doc_entry.DocId
            session.commit()
            # entry into permissions table
            perm_entry = Permission(docid_out, userid, 'WRASD') #(W)rite/(R)ead/(A)nalytics/(S)hare/(D)elete
            session.add(perm_entry)
            session.flush()
            session.commit()
            # entry into DocumentHistory table
            dochist_entry = DocumentHistory(userid, docid_out, datetime.today(), docname, newfilepath, ver)
            session.add(dochist_entry)
            session.flush()
            session.commit()
            # entry into UserHistory table
            userhist_entry = UserHistory(userid, docid_out, datetime.today(), docname, 'Create')
            session.add(userhist_entry)
            session.flush()
            session.commit()
            
            # if there is a reference document given, copy the contents to the new file
            if (refdocid != 0):
                sql_stmt = select(Document.FilePath).where(Document.DocId == refdocid)
                sql_result = session.execute(sql_stmt)
                # there is always only 1 row
                for row in sql_result:
                    reffilepath = row.FilePath
                
                with open(reffilepath, 'r') as firstfile, open(newfilepath, 'a') as secondfile:
                    for line in firstfile:
                        secondfile.write(line)
                
                with open(reffilepath, 'r') as firstfile:
                    doctext = firstfile.read() 
            # Write data if given from the user
            elif (doctext != ''):
                file_obj.writeToFile(newfilepath, doctext)
            
            session.close()
            # building output data
            data_out = {"UserId":username, "DocId":docid_out, "DocName":docname, "DocText":doctext, "Filepath": newfilepath}
            mess_out = 200
        except Exception as err:
            data_out = {"message":str(err)}
            mess_out = 500
            current_app.logger.exception("Failure Creating File! "+str(err))
    
    current_app.logger.info("Service File Create ended")
    # return the message and data string as response
    return make_response(jsonify(data_out), mess_out)

'''
# API to modify a file
## This can be to update a file or save the file
# Input: {'DocId':'', 'DocName':'', 'DocText':''}
# Processing: 
# 1. Authenticate user
# 2. Extract all input data 
# 3. Process the request - update the document or save the document
# 3.a Update the current document - expect DocId to be sent
# 3.b Save the current document - expect DocId to be sent
# - we create a new file every time this request is sent to keep history of things
# 4. Output: UserId, DocId, DocName, FilePath
'''
@fileManagerBlueprint.route('/api/filemodify', methods = ['GET', 'POST'])
@authentication
def file_Modify(user_id):
    current_app.logger.info("Service File Modify initiated")
    data_out = {}
    mess_out = 0

    if(request.method == 'POST'):
        # retrieve data inputs from the request
        content     = request.get_json(silent=True)
        userid      = user_id
        docid       = content['DocId']
        docname     = content['DocName']
        doctext     = content['DocText']
        sql_stmt    = ''
        newfilepath = ''
        ver         = 0
        username    = ''
        
        # open db connection
        session  = session_factory()
        file_obj = FileManage()
        ver_obj  = VersionManage()
        
        try:
            if ((docid == 0) or (docid == '')):
                raise Exception('Document reference id not given. Cannot process!')
                    
            # check if the document exists
            sql_stmt = select(Document.DocId).where(Document.DocId == docid)
            sql_result = session.execute(sql_stmt)
            noofrecords = len(sql_result.all())
            
            # DocId not found so create a new file & save - mostly save operation
            if (noofrecords == 0):
                error_desc = 'Document cannot be retrieved with the given DocId: '+str(docid)+'. Cannot process!'
                raise Exception(error_desc)
                # ver = 1
                # ver_obj.createNewVersionFile(userid, docname, ver, '')
                # newfilepath = ver_obj.v_file_path
                # docname     = ver_obj.v_file_name
                
                # # entry into Documents table
                # doc_entry = Document(userid, docname, newfilepath, datetime.today(), ver, 0, 0)
                # session.add(doc_entry)
                # session.flush()
                # docid = doc_entry.DocId
                # session.commit()
                
                # # entry into permissions table
                # perm_entry = Permission(docid, userid, 'WRASD') #(W)rite/(R)ead/(A)nalytics/(S)hare/(D)elete
                # session.add(perm_entry)
                # session.flush()
                # session.commit()
            # Continue either updating or saving the file
            else:
                userperm = get_user_permissions(userid, docid)
                # User has write permission
                if 'W' in userperm:
                    # get and create a new version for the document
                    sql_stmt = (select(Document.Version).where(Document.DocId == docid))
                    sql_result = session.execute(sql_stmt)
                    # there is always only 1 row
                    for row in sql_result:
                        ver_row = row[0]
                        file_obj.createNewVersion(ver_row)
                        ver = file_obj.v_version
                    # create a new file with new version
                    ver_obj.createNewVersionFile(userid, docname, ver, '')
                    newfilepath = ver_obj.v_file_path
                    docname     = ver_obj.v_file_name
                    
                    # dry run testing - request from front end people to send out username instead of userid
                    sql_stmt = (select(User.UserName).where(User.UserId == userid))
                    sql_result = session.execute(sql_stmt)
                    # there is always only 1 row
                    for row in sql_result:
                        username = row[0]
                    
                    # UPDATES
                    mod_date = datetime.today()
                    # update Documents table with the latest version
                    sql_stmt = update(Document)\
                        .where(Document.DocId == docid)\
                        .values({Document.FilePath:newfilepath, Document.Version:ver, Document.ModifiedDate:mod_date, Document.ModifiedBy:username})
                    session.execute(sql_stmt)
                    session.commit()
                else:
                    raise Exception("User does not have access to modify!")
            
            # update the content to this file
            file_obj.writeToFile(newfilepath, doctext)
            # insert new entry into the Document History table
            dochist_entry = DocumentHistory(userid, docid, datetime.today(), docname, newfilepath, ver)
            session.add(dochist_entry)
            session.flush()
            session.commit()
            # entry into UserHistory table
            userhist_entry = UserHistory(userid, docid, datetime.today(), docname, 'edit')
            session.add(userhist_entry)
            session.flush()
            session.commit()
            
            session.close()

            # building output data
            data_out = {"UserId":username, "DocId":docid, "DocName":docname, "DocText":doctext, "Filepath": newfilepath}
            mess_out = 200
        except Exception as err:
            data_out = {"message":str(err)}
            mess_out = 500
            current_app.logger.exception("Failure Modifying file! "+str(err))
    
    current_app.logger.info("Service File Modify ended")
    # return the message and data string as response
    return make_response(jsonify(data_out), mess_out)

'''
# API to rename a file
## This can be to rename a file
# Input: {'DocId':'', 'DocName':'', 'DocText':''}
# Processing: 
# 1. Authenticate user
# 2. Create a new file with the name
# 3. If document content sent, copy the content else copy ethe previous version content
# 4. Update respective tables - Documents, DocHistory, UserHistory
# 5. Output: UserId, DocId, DocName
'''
@fileManagerBlueprint.route('/api/filerename', methods = ['GET', 'POST'])
@authentication
def file_Rename(user_id):
    current_app.logger.info("Service File Rename initiated")
    data_out = {}
    mess_out = 0

    if(request.method == 'POST'):
        # retrieve data inputs from the request
        content     = request.get_json(silent=True)
        userid      = user_id
        docid       = int(content['DocId'])
        docname     = content['DocName']
        # doctext     = content['DocText']
        sql_stmt    = ''
        ver         = 0
        oldfilepath = ''
        newfilepath = ''
        username    = ''
        
        # open db connection
        session  = session_factory()
        file_obj = FileManage()
        ver_obj  = VersionManage()
        
        try:
            sql_stmt = select(Document.DocId).where(Document.DocName == docname, Document.UserId == userid)
            sql_result = session.execute(sql_stmt)
            noofrecords = len(sql_result.all())
            
            if (noofrecords > 0):
                raise Exception("file name already exists")
            
            if ((docid == 0) or (docid == '')):
                raise Exception('Document reference id not given. Cannot process!')
            
            userperm = get_user_permissions(userid, docid)
            # User has write permission
            if 'W' not in userperm:
                raise Exception('Uesr does not have Write access. Cannot process to rename!')
            
            # check if the document exists
            sql_stmt = select(Document.DocId).where(Document.DocId == docid)
            sql_result = session.execute(sql_stmt)
            noofrecords = len(sql_result.all())
            
            if (noofrecords == 0):
                raise Exception('Document reference id not found. Cannot rename!')
            else:
                mod_date = datetime.today()
                # get and create a new version for the document
                sql_stmt = (select(Document.Version, Document.FilePath).where(Document.DocId == docid))
                sql_result = session.execute(sql_stmt)
                # there is always only 1 row
                for row in sql_result:
                    oldfilepath = row[1]
                    ver_row = row[0]
                    file_obj.createNewVersion(ver_row)
                    ver = file_obj.v_version
                
                # dry run testing - request from front end people to send out username instead of userid
                sql_stmt = (select(User.UserName).where(User.UserId == userid))
                sql_result = session.execute(sql_stmt)
                # there is always only 1 row
                for row in sql_result:
                    username = row[0]
                
                # create a new file with new version
                ver_obj.createNewVersionFile(userid, docname, ver, '')
                newfilepath = ver_obj.v_file_path
                # get the content of the latest version of the file if not sent from front end
                # if (doctext == ''):
                with open(oldfilepath, 'r') as file:
                        doctext = file.read()
                
                # update the content to this new file created
                file_obj.writeToFile(newfilepath, doctext) 
                                
                # update Documents table with the latest file name, document version and so on
                sql_stmt = update(Document)\
                    .where(Document.DocId == docid)\
                    .values({Document.DocName:docname, Document.Version:ver, Document.ModifiedDate:mod_date, Document.ModifiedBy:username})
                session.execute(sql_stmt)
                session.commit()
                #entry into DocumentHistory table
                dochist_entry = DocumentHistory(userid, docid, datetime.today(), docname, newfilepath, ver)
                session.add(dochist_entry)
                session.flush()
                session.commit()
                #entry into user history table                
                userhist_entry = UserHistory(userid, docid, datetime.today(), docname, 'rename')
                session.add(userhist_entry)
                session.flush()
                session.commit()
                session.close()
                # file_paths_stmt = (select(DocumentHistory.FilePath).where(DocumentHistory.DocId==docid))
                # file_paths = session.execute(file_paths_stmt).all()
                # for path in file_paths:
                #     path = path[0]
                #     pattern = re.compile(r"/tmp/testdata/"+userid+r"/[a-zA-Z]+")
                #     replacement = r"/tmp/testdata/"+userid+r"/"+docname
                #     new_path = re.sub(pattern,replacement,path)
                #     os.rename(path, new_path)
                #     sql_stmt = sql_stmt = update(Document)\
                #     .where(Document.DocId == docid)\
                #     .values({Document.DocName:docname, Document.ModifiedDate:mod_date, Document.ModifiedBy:userid, Document.FilePath:new_path})
                #     sql_stmt_2 = update (DocumentHistory)\
                #         .where (DocumentHistory.DocId == docid)\
                #             .values({DocumentHistory.DocName:docname, DocumentHistory.FilePath:new_path})
                #     session.execute(sql_stmt)
                #     session.execute(sql_stmt_2)
                #     session.commit()
                #     mod_date = datetime.today()
                #     # update Documents table with the latest version
                    
                #     index = docname.index('.tex')
                #     docname = docname[:index]
            
                # building output data
                data_out = {"UserId":username, "DocId":docid, "DocName":docname}
                mess_out = 200
        except Exception as err:
            data_out = {"message":str(err)}
            mess_out = 500
            current_app.logger.exception("Failure Renaming file! "+str(err))
    
    current_app.logger.info("Service File Rename ended")
    # return the message and data string as response
    return make_response(jsonify(data_out), mess_out)

'''
# API to get document list
## This can be to provide a list of documents for a user
# Input: {'UserId':''}
# Processing: 
# 1. Extract all input data 
# 2. Process the request
# 3.a Get the list of active documents of the user
# 4. Output: UserId, DocumentList
'''
@fileManagerBlueprint.route('/api/filegetlist', methods = ['GET', 'POST'])
@authentication
def file_GetList(user_id):
    current_app.logger.info("Service Get Document List initiated")
    data_out = {}
    mess_out = 0
    docslist = []

    if(request.method == 'GET'):
        userid = user_id
        json_str = {}
    
        # open db connection
        session  = session_factory()
    
        try:
            # get the documents of the user
            sql_stmt = select(Document.DocId, Document.DocName, Document.FilePath, Document.Version, Document.ModifiedDate, Document.ModifiedBy)\
                .where(Document.UserId == userid ,Document.IsTrash == 0)
            sql_result = session.execute(sql_stmt) 
        
            for row in sql_result:
                json_str = {"DocId": row.DocId, \
                    "DocName":row.DocName , \
                    "FilePath": row.FilePath, \
                    "Version": row.Version, \
                    "LastModifiedOn": row.ModifiedDate, \
                    "LastModifiedBy": row.ModifiedBy}
                
                docslist.append(json_str)
            
            session.close()
            # json object with array of json documents list 
            data_out = {"Documents": docslist}
            mess_out = 200
        except Exception as err:
            data_out = {"message":str(err)}
            mess_out = 500
            current_app.logger.exception("Failure getting the list of files! "+str(err))
    
    current_app.logger.info("Service Get Document List ended")
    # return the message and data string as response
    return make_response(jsonify(data_out), mess_out)

'''
# API to get shared document list 
## This can be to provide a list of documents shared to the user
## This is the list of documents shared to the user by other users
# Input: AuthToken of the user
# Processing: 
# 1. Extract all input data 
# 2. Process the request
# 3.a Get the list of active documents shared to the user
# 4. Output: UserId, DocumentList
'''
@fileManagerBlueprint.route('/api/getsharedlist', methods = ['GET', 'POST'])
@authentication
def file_GetSharedList(user_id):
    current_app.logger.info("Service Get Shared Document List initiated")
    data_out = {}
    mess_out = 0
    docslist = []
    
    if(request.method == 'GET'):
        userid = user_id
        json_str = {}
    
        # open db connection
        session  = session_factory()
    
        try:
            # get the documents of the user
            sql_result = session.query(Document.DocId, Document.DocName, Document.FilePath, Document.Version, Document.ModifiedDate, Document.ModifiedBy)\
                .join(Permission, Document.DocId==Permission.DocId)\
                .filter(Document.IsTrash == 0, Document.UserId != userid, Permission.UserId == userid, Permission.UserPermissions.isnot(None)).all()
            
            for row in sql_result:
                json_str = {"DocId": row.DocId, \
                    "DocName":row.DocName , \
                    "FilePath": row.FilePath, \
                    "Version": row.Version, \
                    "LastModifiedOn": row.ModifiedDate, \
                    "LastModifiedBy": row.ModifiedBy}
                
                docslist.append(json_str)
            
            session.close()
            # json object with array of json documents list 
            data_out = {"Documents": docslist}
            mess_out = 200
        except Exception as err:
            data_out = {"message":str(err)}
            mess_out = 500
            current_app.logger.exception("Failure getting the list of shared files! "+str(err))
    
    current_app.logger.info("Service Get Shared Document List ended")
    # return the message and data string as response
    return make_response(jsonify(data_out), mess_out)


'''
Api to delete a file
'''
@fileManagerBlueprint.route('/api/filedelete', methods=['GET', 'POST'])
@authentication
def file_delete(user_id):
    userid   = ''
    docid    = ''
    filename = ''
    data_out = {}
    mess_out = 0

    current_app.logger.info("Service file/delete initiated")
    if(request.method == 'POST'):
        content  = request.get_json(silent=True)
        userid   = user_id
        docid    = int(content['DocId'])
        
        userperm = get_user_permissions(userid, docid)
        try:
            if 'D' in userperm:
                session = session_factory()
                file_paths_stmt = (select(DocumentHistory.FilePath).where(DocumentHistory.DocId == docid))
                file_paths = session.execute(file_paths_stmt).all()
                sql_stmt = (select(Document.DocName).where(Document.DocId == docid))
                docname = session.execute(sql_stmt).first()[0]
                sql_stmt_2 = delete(Document) .where(Document.DocId == docid)
                sql_stmt_3 = delete(DocumentHistory).where (DocumentHistory.DocId == docid)
                userhist_entry = UserHistory(userid, docid, datetime.today(), docname, 'delete')
                session.add(userhist_entry)
                session.execute(sql_stmt_2)
                session.execute(sql_stmt_3)
                session.flush()
                session.commit()
                session.close()
                for file in file_paths:
                    if (os.path.exists(file[0])):
                        os.remove(file[0])
                    else:
                        current_app.logger.error("File does not exist at the path: ", file)
                data_out = {"message":"success"}
                mess_out=200
            else:
                raise Exception("Access to delete denied!")
        except Exception as err:
            data_out = {"message":str(err)}
            mess_out=500
            current_app.logger.exception("Failure deleting file!")
    current_app.logger.info("Service file/delete ended")
    return make_response(jsonify(data_out), mess_out)

'''
Api to view a file
'''
@fileManagerBlueprint.route('/api/fileview', methods=['GET', 'POST'])
@authentication
def file_view(user_id):
    userid   = user_id
    data_out = {}
    mess_out = 0

    if(request.method == "POST"):
        content = request.get_json(silent=True)
        docid   = int(content['DocId'])
        username = ''

        userperm = get_user_permissions(userid, docid)
        try:
            if('R' in userperm):
                session = session_factory()
                sql_stmt = (select(Document.FilePath, Document.DocName, Document.Version).where(Document.DocId==docid))
                result = session.execute(sql_stmt)
                session.close()

                #There will be 1 row only as we fetched using first()
                for row in result:
                    file_path = row.FilePath
                    doc_ver = row.Version
                    doc_name = row.DocName
                
                # dry run testing - request from front end people to send out username instead of userid
                sql_stmt = (select(User.UserName).where(User.UserId == userid))
                sql_result = session.execute(sql_stmt)
                # there is always only 1 row
                for row in sql_result:
                    username = row[0]
                
                with open(file_path,'r') as f:
                    data = f.read()
                
                data_out = {"UserId":username, "DocId":docid, "DocName":doc_name, "Version":doc_ver, "DocText":data}
                mess_out = 200
        except:
            data_out = {"message":"Unknown Exception caught. Check logs"}
            mess_out = 500
    return make_response(jsonify(data_out), mess_out)

'''
Api to mark a file as trash
'''
@fileManagerBlueprint.route('/api/filetrash', methods = ['GET', 'POST'])
@authentication
def file_trash(user_id):
    current_app.logger.info("Service file/move to trash initiated")
    mess_out = 0
    
    if (request.method == 'POST'):
        content = request.get_json(silent=True)
        userid = user_id
        docid  = int(content['DocId'])
        
        try:
            userperm = get_user_permissions(userid, docid)
            if ('W' in userperm):
                session = session_factory()
                sql_stmt=update(Document).where(Document.DocId == docid) .values(IsTrash=1)
                sql_stmt_2 = update(DocumentHistory).where(DocumentHistory.DocId == docid).values(IsTrash = 1)
                sql_stmt_3 = select()
                #("UPDATE Documents SET IsTrash=1 WHERE DocName = file_name,UserId=user_id")
                session.execute(sql_stmt)
                session.execute(sql_stmt_2)
                session.commit()
                session.close()
                mess_out = 200
                data_out = {"message":"success"}
            else:
                raise Exception("Permission to move to trash denied!")
            #return jsonify(message = "File moved to trash successfully")
        except Exception as err:
            data_out = {"message":str(err)}
            #return jsonify(message='Oops! Something went wrong')
            mess_out = 500
            current_app.logger.exception("Failure moving file to trash!")

    current_app.logger.info("Service file/move to trash ended")
    return make_response(jsonify(data_out),mess_out)

'''
Api to mark a file as trash
'''
@fileManagerBlueprint.route('/api/fileretrive', methods = ['GET','POST'])
@authentication
def file_retrive(user_id):
    current_app.logger.info("Service file/retrieve from trash initiated")
    mess_out = 0
    
    if request.method == 'POST':
        content = request.get_json(silent=True)
        userid  = user_id
        docid   = int(content['DocId'])
         
        try:
            userperm = get_user_permissions(userid, docid)
            if ('W' in userperm):
                session = session_factory()
                sql_stmt=update(Document).where(Document.DocId == docid) .values(IsTrash=0)
                sql_stmt_2 = update(DocumentHistory).where(DocumentHistory.DocId == docid).values(IsTrash = 0)
                session.execute(sql_stmt)
                session.execute(sql_stmt_2)
                session.commit()
                session.close()
                data_out = {"message":"success"}
                mess_out = 200
            else:
                raise Exception("Permission to retrieve from trash denied!")
            #return jsonify(message = "File moved to trash successfully")
        except Exception as err:
            #return jsonify(message='Oops! Something went wrong')
            data_out = {"message":str(err)}
            mess_out = 500
            current_app.logger.exception("Failure retrieving file from trash!")

    current_app.logger.info("Service file/retrieve from trash ended")
    return make_response(jsonify(data_out),mess_out)
'''
Api to get Trash list
'''
@fileManagerBlueprint.route('/api/getTrashList', methods=["GET","POST"])
@authentication
def gettrashlist(user_id):
    userid = user_id
    mess_out = 0
    data_out = {}
    trashlist = []
    if request.method == "GET":
        try:
            session = session_factory()
            sql_stmt = (select(Document.DocId, Document.DocName).where(Document.UserId == userid, Document.IsTrash == 1))
            result = session.execute(sql_stmt)
            
            for row in result:
                json_str = {
                    "DocId":row.DocId,
                    "DocName":row.DocName
                }
                trashlist.append(json_str)
            
            data_out = {"Documents": trashlist}
            mess_out = 200
        except Exception as err:
            data_out = {"message":str(err)}
            mess_out = 500
            current_app.logger.exception("Failure getting the list of files! "+str(err))
    else:
        data_out = {"message":"Method not allowed"}
        mess_out = 404        
    return make_response(jsonify(data_out), mess_out)