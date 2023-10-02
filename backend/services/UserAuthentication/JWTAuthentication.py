from flask import Blueprint, current_app, jsonify
from flask import request,make_response
#from app.databases.database import *
from flask_bcrypt import Bcrypt
from . import *
import jwt
from flask import jsonify
from datetime import datetime
from functools import wraps
import sqlalchemy as db
from sqlalchemy import create_engine, select, update
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from DBConnect import session_factory
from orm_Tables import User
from flask import request,make_response


authTokenDecode_bp = Blueprint('AuthTokenDecode',__name__)

## Below is the decorator for the authentication if the JWT token is send in header
def authentication(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token=None
        if 'authToken' in request.headers:
            token = request.headers['authToken']
            key = current_app.config["SECRET"]
        if not token:
            data_sent={"message": "token missing"}
            return make_response(jsonify(data_sent), 400)
        try:
            data= jwt.decode(token, key, algorithms=["HS256"])
            session = session_factory()
            sql_stmt = (select(User.UserId) .where (User.UserName == data["Email"]))
            user_id = session.execute(sql_stmt).first()
            
            if not user_id[0]:
                data_sent = {"message":"Invalid token"}
                return make_response(jsonify(data_sent,401))
        except:
            data_sent = {"message":"error while decoding"}
            return jsonify(data_sent,401)
        return f(user_id[0], *args, **kwargs)
    return decorated


##Below is the decorator for the authentication if JWT token in send in json
# def authentication(f):
#     @wraps(f)
#     def decorated(*args, **kwargs):
#         token=None
#         key=current_app.config["SECRET"]
#         content = request.get_json(silent=True)
#         if content["token"]:
#             token = content["token"]
#         if not token:
#             return jsonify(message="token missing")
#         try:
#             data= jwt.decode(token, key, algorithms=["HS256"])
#             session = session_factory()
#             sql_stmt = (select(User.UserId) .where (User.UserName == data["Email"]))
#             user_id = session.execute(sql_stmt).first()
#             session.close()
#             if not user_id[0]:
#                 return jsonify(message="invalid token")

#         except:
#             return jsonify(message="error while decoding")
#         return f(user_id[0], *args, **kwargs)
#     return decorated