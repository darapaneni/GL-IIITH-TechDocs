# Libraries
import os
import warnings
import logging
import yaml
import requests
from datetime import datetime
from flask import request, jsonify, json, Blueprint, current_app,make_response
from DBConnect import session_factory
from ..UserAuthentication.JWTAuthentication import authentication
from orm_Tables import Document, DocumentHistory, User


# Suppress warnings
warnings.filterwarnings("ignore")

import sys
sys.path.append('../')

documentVersionManagerBlueprint = Blueprint('documentVersionManagerBlueprint', __name__)

@documentVersionManagerBlueprint.route('/api/documentversionmanagerhealth')
def filemanagerhealth():
    print(current_app.config)
    return jsonify({'health':'good'}) 

# Class to handle common version file related processes
class VersionManage:
    v_file_name =''
    v_file_path =''
        
    @classmethod
    def createNewVersionFile(cls, user_id, document_name, version, current_file_path):

        data_path = current_app.config["DIR_ROOT"] + current_app.config["DIR_DATA"] 
        log_path = current_app.config['DIR_ROOT'] + current_app.config['DIR_LOG']
        logging.basicConfig(filename=log_path)
        file_directory = data_path + '/' + str(user_id)
        if (document_name == ""):
            datestr  = datetime.today().strftime('%Y%m%d%H%M%S')
            document_name = 'untitled_' + datestr #+ 'v_' + str(version) + '.tex'
        # else :
        #     index = document_name.index('.tex')
        #     document_name = document_name[:index]

        file_path = file_directory + '/' + document_name + '_v_' + str(version) + '.tex'

        if not os.path.exists(file_directory):
            print(file_path)
            print(file_directory)
            os.makedirs(file_directory)
        
        if current_file_path == "":
            with open(file_path,"w") as f:
                f.write("")
        else:
            # TODO: copy contents from old file to new file
            with open(current_file_path) as f:
                with open(file_path, "w") as f1:
                    for line in f:
                        f1.write(line)

        cls.v_file_name = document_name
        cls.v_file_path = file_path


def get_document_record(document_id):
    try: 
        session = session_factory()
        document_query = session.query(Document).filter(Document.DocId == document_id).all()
        session.close()
        if len(document_query) > 0:
            return document_query[0]
        current_app.logger.info("Document record for document Id - " + str(document_id) + " doesn't exist")
        return False
    except Exception:
        current_app.logger.exception("Failure getting document id!")
        return False

def get_user_record(user_id):
    try: 
        session = session_factory()
        user_query = session.query(User).filter(User.Id == user_id).all()
        session.close()
        if len(user_query) > 0:
            return user_query[0]
        current_app.logger.info("User record for user Id - " + str(user_id) + " doesn't exist")
        return False
    except Exception:
        current_app.logger.exception("Failure getting user record!")
        return False

def get_latest_document_version_record(document_id):
    try: 
        session = session_factory()
        document_version_query = session.query(DocumentHistory).filter(DocumentHistory.DocId==document_id).order_by(DocumentHistory.Version.desc()).first()
        session.close()
        if document_version_query:
            return document_version_query[0]
        current_app.logger.info("Document version for doc Id - " + str(document_id) + " doesn't exist")
        return False
    except Exception:
        current_app.logger.exception("Failure getting document version!")
        return False



##############################################################################
# Home API for document_version_manager
# Check on DocumentVersionManager service
@documentVersionManagerBlueprint.route('/api/version', methods = ['GET', 'POST'])
def home():
    if(request.method == 'GET'):
        data = "DocumentVersionManager home. Allowed endpoints are /version/create ; /version/get"
        return jsonify({'data': data})


# API to create a new version
# Input: UserId, DocumentId (if)
# Processing: 
# 1. Creates a sub folder with UserId in the destination directory 
# 2. Creates a file name suffixed with date time string 
# 3. Copies this file name to the above folder
# 4. Copies the content of Document to new file
# 5. Create an entry into Document version table
# Output: UserId, DocId, DocName

@documentVersionManagerBlueprint.route('/api/versionCreate', methods = ['GET', 'POST'])
def create_document_version():
    
    current_app.logger.info("Service version/create initiated")
    data_out = ''
    mess_out = ''
    if(request.method == 'POST'):
        # request data
        content  = request.get_json(silent=True)
        user_id   = content['UserId']
        document_id  = content['DocumentId']

        # processing request
        try: 
            session = session_factory()

            user = get_user_record(user_id)
            if not user:
                mess_out = "User record doesn't exist"
                return jsonify(message=mess_out, data=data_out)

            document = get_document_record(document_id)
            if (not document):
                mess_out = "Document record doesn't exist"
                return jsonify(message=mess_out, data=data_out)
            else:
                document_version = document.Version
                document_name = document.DocName
                file_path = document.FilePath
            file_version_object = VersionManage()
            file_version_object.createNewVersionFile(user_id, document_name, document_version, file_path)
            document_version_record = DocumentHistory(user, document, datetime.now(), file_version_object.v_file_name, file_version_object.v_file_path, document_version)

            session.add(document_version_record)
            session.commit()
            session.close()
            data_out = json.dumps({'UserId': user_id, 'DocId':document_id, 'DocName':file_version_object.v_file_name})

        except Exception as e:
            print(e)
            mess_out = 'fail'
            current_app.logger.exception("Failure Creating Version!")

    current_app.logger.info("Service version/create ended")
    
    #Return the json object to the caller
    return jsonify(message=mess_out, data=data_out)

# API to get latest version of a doc id
# Inputs:  DocumentId
# Processing: 
# 1. Retrieves the latest document version for the given document id
# Output:
# Version
@documentVersionManagerBlueprint.route('/api/versionGet', methods = ['GET', 'POST'])
@authentication
def get_latest_document_version(user_id):
    current_app.logger.info("Service version/get initiated")
    data_out = ''
    mess_out = ''

    if(request.method == 'POST'):
        # retrieve data inputs from the request
        content = request.get_json(silent=True)
        document_id = content['DocId']
        
        version_record = get_latest_document_version_record(document_id)
        if (not version_record):
            version =  0
        else:
            version =  version_record.Version
    
    data_out = {'DocumentId':document_id, 'Version':version}
    current_app.logger.info("Service version/get ended")
    return make_response(jsonify(data_out),200)

#################
# Main Call
# if __name__ == "__main__":
#     app.run(debug=True)
    
