#getprofile.py
'''
This file is used to get the user profile details from the database.
This includes firstname, lastname, street address, state, country, occupation, purpose of use, sign up date and last active date.
On receiving a request for getting the profile of the user, the JWT is verfied. On successful authentication 
the user profile parameters are sent.  
'''
from flask import Blueprint, current_app, jsonify
from flask import request,make_response
from . import *
import jwt
from flask import jsonify
from DBConnect import session_factory
from sqlalchemy import create_engine, select, update
from orm_Tables import UserProfile
from orm_Tables import User
from flask_bcrypt import Bcrypt
from ..UserAuthentication.JWTAuthentication import authentication



getUserProfile_bp = Blueprint('getprofile',__name__)
#check for user authorisation

@getUserProfile_bp.route('/api/getProfile',methods=['GET','POST'])
@authentication
def getProfile(user_id):
    if request.method == 'POST':
        #Obtain the data from registered user profile from UserProfile Database
        
        session = session_factory()
        sql_stmt_1 = (select(User.UserName).where (User.UserId == user_id))
        getProfileusername = session.execute(sql_stmt_1).first()[0]
        sql_stmt = (select(UserProfile.FirstName, UserProfile.LastName, UserProfile.StreetAddress,
                        UserProfile.State,UserProfile.Country,UserProfile.Occupation,UserProfile.PurposeOfUsage,
                        UserProfile.SignUpDate,UserProfile.LastActiveDate).where (UserProfile.UserName == getProfileusername))
        result = session.execute(sql_stmt).first()
        session.close()
        if result:
            Data_Send = {
            "userData":{"firstName": result[0],
                        "lastName" : result[1],
                        "address": {"streetAddress" : result[2], 
                                    "state" : result[3],
                                    "country" : result[4]},
                        "occupation" : result[5],
                        "purposeOfUse": result[6]},
            "usageStats":{"signUpDate": str(result[7]),
                        "lastActiveDate" : str(result[8])}
            }
            return make_response(jsonify(Data_Send), 200)
        else:
            data_sent = {"message":"Not Found"} 
            return make_response(jsonify(data_sent),404)
    else:
        data_sent = {'message':'Method not allowed'}
        return make_response(jsonify(data_sent),400)