#logout.py
'''
This File is responsible for signing out. On receiving a request for sign out, the jwt is verified.
On successful verification, the last active date in the UserProfile database is updated with the current date.
on succesfull Updation of database JWT is sent. Else Error message is sent
'''

from flask import Blueprint, current_app, jsonify
from flask import request,make_response
from . import *
from flask import jsonify
from DBConnect import session_factory
from orm_Tables import UserProfile
from flask_bcrypt import Bcrypt
from .JWTAuthentication import authentication
import pytz
from datetime import datetime
from sqlalchemy import create_engine, select, update

userLogout_bp = Blueprint('logout',__name__)

@userLogout_bp.route('/api/signout', methods=["GET", "POST"])
#check for user authorisation
@authentication
def signout(user_id):
    if request.method == 'POST':
        #updating the lastactive time of the user in  UserProfile Database
            logoutUsername = user_id 
            currentDateTime = datetime.now(pytz.timezone('Asia/Kolkata'))
            currentDate = currentDateTime.today()
            session = session_factory()
            sql_stmt = (update(UserProfile).where(UserProfile.UserName == logoutUsername).values(LastActiveDate=currentDate))
            session.execute(sql_stmt)
            session.close()
        #sending the JWT Token after updating the database
            # JWT_Encode_Token = (request.form.get('userAuthToken'))
            JWT_Encode_Token = request.headers["authToken"]
            data_sent = {"userAuthToken":JWT_Encode_Token} 
            return make_response(jsonify(data_sent),200)
    else:
            data_sent = {"message":"Invalid Request/No User Session"} 
            return make_response(jsonify(data_sent),400)