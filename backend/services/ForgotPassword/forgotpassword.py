from flask import Flask, jsonify, request, render_template, url_for
from flask import make_response
from flask_mail import Mail, Message
from sqlalchemy import update
#from sqlalchemy.sql import text
from flask_bcrypt import Bcrypt
from flask import Blueprint, current_app, jsonify
from DBConnect import session_factory
from orm_Tables import User
from ..UserAuthentication.JWTAuthentication import authentication
from .mail import send_reset_email, verify_reset_token
from sqlalchemy import create_engine, select, update


forgotpassword_bp = Blueprint('forgotpassword',__name__)

@forgotpassword_bp.route('/api/forgot-password', methods=['GET','POST'])

def forgot_password():
    req = request.json
    if not req :
        req = request.form 

    if request.method == "POST":
        data = req['email_id']

        #user = User.query.filter_by(username=data).first()
        session = session_factory()
        sql_stmt = (select(User.UserId, User.IsAdmin, User.LoginType).where (User.UserName == data))
        result = session.execute(sql_stmt).first()
        session.close()
        print(result)
        if result is None:
            return make_response(jsonify({'message':'There is no account with that email. You must register first'}), 401)
        else:
            
            #print(user.Id)
            if result[2] == 'email':
                send_reset_email(result[0], data)
                return make_response(jsonify({'message': 'You have been sent an email to complete your password reset'}), 200)
            elif result[2] == 'google':
                return make_response(
                    jsonify({'message': 'Please use google account to reset your password'}), 401)
    else:
        return jsonify(({"message":"Method not allowed"}),404)


@forgotpassword_bp.route('/api/reset-password', methods=['GET','POST'])

def reset_password():
    bcrypt = Bcrypt(current_app)
    req = request.json
    if not req :
        req = request.form 

    if request.method == "POST":
        key = current_app.config['SECRET']
        token = (req["token"])
        new_password = (req["new_password"])
        user_id = verify_reset_token(token)
        new_password = bcrypt.generate_password_hash(new_password)
        #print(new_password)
        print('user_id:'+user_id)
        if user_id == None:
            return make_response(jsonify({'message': 'Error'}), 401)
        else:
            #data = User.query.filter_by(Id=user_id).first()
            #data.password = new_password
            #db.session.commit()
            session = session_factory()
            sql_stmt = (update(User).where(User.UserId == user_id).values(Password=new_password))
            session.execute(sql_stmt)
            session.commit()
            session.close()
            return make_response(jsonify({'message': 'Success'}), 200)
    else:
        return jsonify(({"message":"Method not allowed"}),404)




@forgotpassword_bp.route('/api/validate-token', methods=['GET', 'POST'])

def validate_token():
    req = request.json
    if not req :
        req = request.form 

    if request.method == "POST":
        data = (req["token"])
        print(data)
        user_id = verify_reset_token(data)
        print(user_id)
        if user_id is None:
            return make_response(jsonify({'message': 'Error'}), 404)
        else:
            return make_response(jsonify({'message': 'Success'}), 200)
    else:
        return jsonify(({"message":"Method not allowed"}),404)