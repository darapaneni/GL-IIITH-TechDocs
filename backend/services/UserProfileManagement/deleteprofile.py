from flask import make_response, jsonify, request, abort
import getpass
import json 
import jwt
#from frontend.app import User, db
from flask import Flask, jsonify, request, render_template, url_for
from flask import make_response
#from sqlalchemy.sql import text
from flask_bcrypt import Bcrypt
from flask import Blueprint, current_app, jsonify
from DBConnect import session_factory
from orm_Tables import User
from ..UserAuthentication.JWTAuthentication import authentication
from ..ForgotPassword.mail import send_reset_email, verify_reset_token
from sqlalchemy import create_engine, select, delete

deletecode_bp = Blueprint('deletecode',__name__)
@deletecode_bp.route('/api/deleteAccount', methods=["GET", "POST"])
@authentication
#@login_required
def delete_account(user_id):  
    bcrypt = Bcrypt(current_app)       
    if request.method == 'POST':
        #JWT_Encode_Token = json.loads(request.form.get('userAuthToken'))
        #key = 'secret'
        #JWT_Decode_Token = jwt.decode(JWT_Encode_Token, key, algorithms="HS256")
        #password = request.form.get('password')
        #user = User.query.filter_by(User.username == auth.username).first()
        #user = User.query.filter_by(username=JWT_Decode_Token.value()).first()
        login_type = request.form.get('loginType')
        if login_type == 'email':
            password = request.form.get('currentPassword')
            # password = getpass.getpass('Confirm Password: ')
            if password:
                session = session_factory()
                sql_stmt = (select(User.UserId, User.IsAdmin, User.Password, User.LoginType).where (User.UserId == user_id))
                result = session.execute(sql_stmt).first()
                session.close()
                if result:
                    if result[2]:
                        if bcrypt.check_password_hash(result[2], password):
                            session = session_factory()
                            sql_stmt = (delete(User).where(User.UserId == user_id))
                            session.execute(sql_stmt)
                            session.commit()
                            check_stmt = (select(User).where(User.UserId == user_id))
                            check = session.execute(check_stmt).first()
                            session.close()
                            if check is None:
                                data_sent = {"message": "User Deleted Successfully!!"}
                                return make_response((jsonify(data_sent), 200))
                            else:
                                data_sent = {"message": "User Not Deleted Successfully!!"}
                                return make_response((jsonify(data_sent), 401))
                        else:
                            #check if the user actually exists, take the user-supplied password, hash it, and compare it to the hashed password in the database
                            data_sent = {"message": "Can't Delete User, User or Password is wrong!!"}
                            return make_response(jsonify(data_sent), 401)
                    else:
                        data_sent = {"message": "password is null"}
                        return make_response(jsonify(data_sent), 401)
                else:
                    data_sent = {"message": "Error in retrieving data"}
                    return make_response(jsonify(data_sent), 401)
            else:
                data_sent = {"message": "No password received, password can't be null"}
                return make_response(jsonify(data_sent), 401)
                           
            #else:
                #db.session.delete(user)
                #db.session.commit()
                #data_sent = {"message": "User Deleted Successfully!!"}
                #return make_response((jsonify(data_sent), 200))
        elif login_type == 'google':
            #db.session.delete(user)
            #db.session.commit()
            session = session_factory()
            sql_stmt = (delete(User).where(User.UserId == user_id))
            session.execute(sql_stmt)
            session.commit()
            check_stmt = (select(User).where(User.UserId == user_id))
            check = session.execute(check_stmt).first()
            session.close()
            if check is None:
                data_sent = {"message": "User Deleted Successfully!!"}
                return make_response((jsonify(data_sent), 200))
            else:
                data_sent = {"message": "User Not Deleted Successfully!!"}
                return make_response((jsonify(data_sent), 401))
        else:
            data_sent = {"message":"Not valid"}
            return make_response((jsonify(data_sent), 401))    
    else:
        data_sent = {"message":"Method not allowed"}
        return make_response((jsonify(data_sent), 401))   
             
   
   
   
   
   
   
   
   
   
   
    # password = getpass.getpass('Confirm Password: ')
    
    # if not user or not check_password_hash(user.password, password):    #check if the user actually exists, take the user-supplied password, hash it, and compare it to the hashed password in the database
    #     data_sent = {"message": "Can't Delete User, User or Password is wrong!!"}
    #     return make_response(jsonify(data_sent), 401)
    # else:
    #     db.session.delete(user)
    #     db.session.commit()
    #     data_sent = {"message": "User Deleted Successfully!!"}
    #     return make_response((jsonify(data_sent), 200))

