# Updateprofile.py 
''' this file receives json file containing the  user profile details to be updated. This includes 
firstname, lastname, street address, state, country, occupation and purpose of use. 
Process: When the post method is called, first the user authentication is verified.
After the JWT token is verified, the entered userdetails are obtained and updated in the UserProfile Database.
On succesful Updation "OK" is being sent, else "error message" is sent.
'''

from flask import Blueprint, current_app, jsonify
from flask import request,make_response
from flask_bcrypt import Bcrypt
from . import *
import jwt
from flask import jsonify
from datetime import datetime
import pytz,json
from DBConnect import session_factory
from orm_Tables import User
from sqlalchemy import create_engine, select, update
from flask_bcrypt import Bcrypt
from orm_Tables import UserProfile
from ..UserAuthentication.JWTAuthentication import authentication


updateUserProfile_bp = Blueprint('updateprofile',__name__)


@updateUserProfile_bp .route('/api/updateProfile',methods=['GET', 'POST'])
#check for user authorisation
@authentication
def updateProfile(user_id):
    if request.method == 'POST':
        requestparams = json.loads(request.data) #reading the parameters to update
        userData = requestparams["userData"]
        userId= user_id
        firstName = userData["firstName"]
        lastName = userData["lastName"]
        if len(firstName) > 10:
            data_sent = {"message":"First name length should be less than 10"}
            return make_response(jsonify(data_sent), 401)
        if not firstName and not lastName:
            data_sent = {"message":"Both first name and last name cannot be empty"}
            return make_response(jsonify(data_sent), 400)
        address = userData["address"]
        streetAddress = address["streetAddress"]
        state = address["state"]
        country = address["country"]
        occupation = userData["occupation"]
        purposeOfUsage = userData["purposeOfUse"]
        #Updating to database
        session = session_factory()
        sql_stmt = (update(UserProfile).where(UserProfile.UserId == userId).values(FirstName=firstName,LastName = lastName,StreetAddress = streetAddress,State = state, Country = country, Occupation = occupation, PurposeOfUsage = purposeOfUsage))
        result = session.execute(sql_stmt)
        session.commit()
        session.close()
        if result:
            message = {"message":"OK"}
            return make_response(jsonify(message), 200)
        else:
            data_sent = {"message":"Update Error Message"} 
            return make_response(jsonify(data_sent),404)
            
    else:
            data_sent = {"message":"Error Message"} 
            return make_response(jsonify(data_sent),404)