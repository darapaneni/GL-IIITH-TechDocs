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
# from .mail import send_reset_email, verify_reset_token
from sqlalchemy import create_engine, null, select, delete, update

changepassword_bp = Blueprint('changepassword',__name__)
@changepassword_bp.route('/api/changePassword', methods=["GET", "POST"])
# To check the JWT Token
@authentication
def changepassword(user_id):  
    bcrypt = Bcrypt(current_app)       
    if request.method == 'POST':
        # Receiving Current password and new password
        currentPassword = request.form.get('currentPassword')
        newPassword = request.form.get('newPassword')
        if currentPassword:
            session = session_factory()
            sql_stmt = (select(User.Password, User.LoginType).where (User.UserId == user_id))
            result = session.execute(sql_stmt).first()
            session.close()
            if result:
                if result[0]:
                    # checking if the current and existing password are same. If true updating the new password after encrypting
                    if bcrypt.check_password_hash(result[0], currentPassword):
                        if newPassword:
                            encryptPassword = bcrypt.generate_password_hash(newPassword)
                            session = session_factory()
                            sql_stmt = (update(User).where(User.UserId == user_id).values(Password=encryptPassword))
                            session.execute(sql_stmt)
                            session.commit()
                            check_stmt = (select(User.Password).where(User.UserId==user_id))
                            check = session.execute(check_stmt).first()[0]
                            session.close()
                            if bcrypt.check_password_hash(check,newPassword):
                                data_sent = {"message": "OK"}
                                return make_response((jsonify(data_sent), 200))
                            else:
                                data_sent = {"message": "Unable to update password, error in retrieving data"}
                                return make_response((jsonify(data_sent), 401))
                        else:
                            data_sent = {"message": "New Password is null"}
                            return make_response(jsonify(data_sent), 401)
                    else:
                        data_sent = {"message": " Error in current password"}
                        return make_response(jsonify(data_sent), 401)
                else:
                    data_sent = {"message": "current Password is null"}
                    return make_response(jsonify(data_sent), 401)
            else:
                    data_sent = {"message": "Error in retrieving Data"}
                    return make_response(jsonify(data_sent), 401)
        else:
                data_sent = {"message": "No password received, password can't be null"}
                return make_response(jsonify(data_sent), 401)
    else:
        data_sent = {"message": "method not allowed"}
        return make_response(jsonify(data_sent), 405)