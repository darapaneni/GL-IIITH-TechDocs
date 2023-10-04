#login.py
'''
This file is used for checking the authentication of the user. 
Here the user can login either through google account or by entering the registered email and password.
On request for login, the login type is intially checked. 
For Either of the login type (google or Email)", the UserAuthentication database is checked if user credentials.
if the credenials are authentic a JWT token is generated and returned.
Else the corresponding error message is generated.
'''

from flask import Blueprint, current_app, jsonify
from flask import request,make_response
from . import *
import jwt
from flask import jsonify
from DBConnect import session_factory
from orm_Tables import User
from orm_Tables import UserProfile
from flask_bcrypt import Bcrypt
from sqlalchemy import create_engine, select, update

userLogin_bp = Blueprint('login',__name__)

@userLogin_bp.route('/api/signin', methods=['GET', 'POST'])
def signin():
    bcrypt = Bcrypt(current_app)
    if request.method == 'POST':
        loginType = request.form.get('loginType')
        username  = request.form.get('email')
        # content = request.get_json(silent=True)
        # loginType = content["loginType"]
        # username = content["email"]
        # Checking for the Login Type
        if loginType == 'google':
            session = session_factory()
            sql_stmt = (select(User.UserId, User.IsAdmin, User.LoginType).where (User.UserName == username))
            sql_stmt_2 = (select(UserProfile.FirstName, UserProfile.LastName).where(UserProfile.UserName == username))
            result_2 = session.execute(sql_stmt_2).first()
            result = session.execute(sql_stmt).first()
            session.close()
        #if user is registered
        
            if result:
                if result[2] == 'google':
                    key = current_app.config["SECRET"]
                    admin = result[1]
                    firstname = result_2[0]
                    lastname = result_2[1]
                    data_sent = {"Email": username,
                                "isAdmin": admin,
                                "loginType":loginType
                                }
                    # generate the JWT Token
                    JWT_Token = jwt.encode(data_sent, key, algorithm="HS256")
                    jsondata = {"userAuthToken":JWT_Token,
                                "isAdmin":admin,
                                "FirstName":firstname,
                                "LastName":lastname}
                    return make_response(jsonify(jsondata), 200)
                else:
                    data_sent = {"message":"User not Registered"} 
                    return make_response(jsonify(data_sent),401)
            else:
                    data_sent = {"message":"User not Registered"} 
                    return make_response(jsonify(data_sent),401)

# checking for the login type 
        elif loginType == "email":
            password = request.form.get('password')
            # password = content["password"]
            if password:
                session = session_factory()
                sql_stmt = (select(User.UserId, User.IsAdmin, User.Password, User.LoginType).where (User.UserName == username))
                sql_stmt_2 = (select(UserProfile.FirstName, UserProfile.LastName).where(UserProfile.UserName == username))
                result_2 = session.execute(sql_stmt_2).first()
                result = session.execute(sql_stmt).first()
                session.close()

                if result:
            
                    if result[3] == "google":
                        data_sent = {"message":"User registered with google please login via google"} 
                        return make_response(jsonify(data_sent),401)

        # if the user is registered
                    if result[0]:   
                        if bcrypt.check_password_hash(result[2], password):
                            key = current_app.config["SECRET"]
                            admin = result[1]
                            firstname = result_2[0]
                            lastname = result_2[1]
                            data_sent = {"Email": username,
                                        "isAdmin": admin,
                                        "loginType":loginType
                                            }
                            JWT_Token = jwt.encode(data_sent, key, algorithm="HS256")
                            data_sent  =  {"userAuthToken" : JWT_Token,     
                                                "isAdmin":admin,
                                                "FirstName":firstname,
                                                "LastName":lastname}
                            return make_response(jsonify(data_sent), 200) 
                        else:
                            data_sent = {"message":"Invalid Password"} 
                            return make_response(jsonify(data_sent),401)
                    else:
                        data_sent = {"message":"User not Registered"} 
                        return make_response(jsonify(data_sent),401)
                else:
                    data_sent = {"message": "User not Registered"}
                    return make_response(jsonify(data_sent), 401)            
            else:
                data_sent = {"message":"User not Registered"}
                return make_response(jsonify(data_sent), 401)
        else:
            data_sent = {"message":"User not Registered"} 
            return make_response(jsonify(data_sent),401)
        
    else:
        data_sent = {"message":"Invalid method"} 
        return make_response(jsonify(data_sent),401)