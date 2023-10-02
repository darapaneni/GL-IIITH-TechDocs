# Libraries
import warnings
import logging
import yaml
import requests
import timeago
from datetime import datetime
from flask import Flask, request, jsonify, json, Blueprint, current_app, make_response
import sqlalchemy as db
from DBConnect import session_factory
from ..UserAuthentication.JWTAuthentication import authentication

from orm_Tables import UserHistory, ActionEnum, Document, User

# Suppress warnings
warnings.filterwarnings("ignore")

import sys
sys.path.append('../')

userHistoryManagerBlueprint = Blueprint('userHistoryManagerBlueprint', __name__)


@userHistoryManagerBlueprint.route('/api/userhistorymanagerhealth')
def filemanagerhealth():
    print(current_app.config)
    return jsonify({'health':'good'}) 

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

def get_user_record_by_email(email):
    try: 
        session = session_factory()
        user_query = session.query(User).filter(User.username == email).all()
        session.close()
        if len(user_query) > 0:
            return user_query[0]
        current_app.logger.info("User record for email Id - " + str(email) + " doesn't exist")
        return False
    except Exception:
        current_app.logger.exception("Failure getting user record!")
        return False

##############################################################################
# Home API for historymanager
# Check on HistoryManager service
@userHistoryManagerBlueprint.route('/api/userHistory', methods = ['GET', 'POST'])
def home():
    if(request.method == 'GET'):
        data = "HistoryManager home. Allowed endpoints are /history/get; /history/create;"
        return jsonify({'data': data})

# API to create a new user history
# Input: UserId, DocumentId, Action, AdditionalInfo(JSON containing more info based on Action)
# For Action = share -> AdditionalInfo = {'email_id': 'abc@xyz.com'}
# Processing: 
# 1. Create an entry into UserHistory table
# Output: UserHistoryId
@userHistoryManagerBlueprint.route('/api/historyCreate', methods = ['GET', 'POST'])
def create_user_history():
    data_out = ''
    mess_out = ''
    additionalInfo = {}
    
    current_app.logger.info("Service history/create initiated")
    if(request.method == 'POST'):
        # request data
        content  = request.get_json(silent=True)
        user_id   = content['UserId']
        document_id  = content['DocumentId']
        action = content['Action']
        if "AdditionalInfo" in content:
            additionalInfo = content['AdditionalInfo']
        # processing request
        
        # Save it in the database - by using UserHistory object
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
                document_name = document.DocName

            user_history_record = UserHistory(user, document, datetime.now(), document_name, action)
            if action == ActionEnum.share.value:
                user_history_record.s_Misc1 = additionalInfo["email_id"]

            session.add(user_history_record)
            session.flush()
            record_id = user_history_record.RecordId
            session.commit()
            session.close()

            data_out = json.dumps({'UserHistoryId':record_id})
            mess_out = 'success'

        except Exception:
            mess_out = 'fail'
            current_app.logger.exception("Failure Creating UserHistory!")
    current_app.logger.info("Service history/create ended")
    
    #Return the json object to the caller
    return jsonify(message=mess_out, data=data_out)

# API to get user history
# Inputs: Email, PageNumber(if)
# Processing: 
# 1. Gets the user record for the email
# 2. Retrieves the user history records based on offset and pagesize
# 3. Convert time stamp to timeago format
# 4. If action is share, get the shared email id
# Output:
# UserId, DocId, DocName, DocText
@userHistoryManagerBlueprint.route('/api/historyGet', methods = ['GET', 'POST'])
@authentication
def get_user_history(user_id):
    current_app.logger.info("Service history/get initiated")
    data_out = ''
    mess_out = ''
    history_records = []

    if(request.method == 'POST'):
        # retrieve data inputs from the request
        page_size = 100
        content   = request.get_json(silent=True)
        user_email   = user_id
        page_number = 0

        try :
            session = session_factory()
            # sql_stmt = (select(User.UserName).where(User.UserId == user_id))
            user_history_query = session.query(UserHistory).filter(UserHistory.UserId == user_id).order_by(UserHistory.CreatedDate.desc()).offset(page_number*page_size).limit(page_size).all()
            session.close()
            for user_history_record in user_history_query:
                action = user_history_record.Action
                if not action:
                    continue
                document_name = user_history_record.DocName
                time_stamp = timeago.format(user_history_record.CreatedDate, datetime.now())

                history_record = {
                    "action": action.value,
                    "time": time_stamp,
                    "doc_name": document_name
                }
                if action == ActionEnum.share:
                    history_record["shared_to"] = user_history_record.s_Misc1
                history_records.append(history_record)

            data_out = {'items':history_records}
            mess_out = "success"

        except Exception:
            mess_out = "failed to send"
    
    current_app.logger.info("Service history/get ended")
    return make_response(jsonify(data_out),mess_out)

#################
# Main Call
# if __name__ == "__main__":
#     app.run(debug=True)
