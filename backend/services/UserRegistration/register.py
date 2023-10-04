from flask import Blueprint, current_app,jsonify
from flask import request,make_response
from orm_Tables import User
from flask_bcrypt import Bcrypt
from datetime import datetime
from flask import request,make_response
from . import *
from DBConnect import session_factory
from orm_Tables import User,UserProfile
from sqlalchemy import create_engine, select, insert
import pytz
import uuid

register_bp = Blueprint('UserRegister',__name__)




@register_bp.route('/api/register', methods=['GET','POST'])
def register():
    currentDateTime = datetime.now(pytz.timezone('Asia/Kolkata'))
    currentDate = currentDateTime.today()
    bcrypt = Bcrypt(current_app)
    content  = request.get_json(silent=True)
    res=''
    if request.method=='POST':
        userId=str(uuid.uuid4())
        userName=content['email']
        password=content['password']
        firstname=content["FirstName"]
        lastname=content["LastName"]
        IsAdmin=False
        loginType=content['loginType']
        secure_password = bcrypt.generate_password_hash(password) 
        session = session_factory()
        sql_stmt = (select(User.UserId, User.IsAdmin, User.UserName ).where (User.UserName == userName))
        result = session.execute(sql_stmt).first()
        session.close()
        
        #usernamedata=str(usernamedata)
        if result==None:
            session = session_factory()
            sql_statement1= insert(User).values(UserId=userId,UserName=userName,Password=secure_password,IsAdmin=IsAdmin,LoginType=loginType)
            sql_statement2= insert(UserProfile).values(UserId=userId,UserName=userName,FirstName=firstname, LastName=lastname,SignUpDate=currentDate,LastActiveDate=currentDate)
            result1=session.execute(sql_statement1)
            result2=session.execute(sql_statement2)
            session.commit()
            check_stmt = (select(User) .where(User.UserId==userId))
            check_stmt_2 = (select(UserProfile) .where(UserProfile.UserId==userId))
            check = session.execute(check_stmt)
            check_2 = session.execute(check_stmt_2)
            session.close() 
            if check and check_2:
                res={"message":'You are registered and can now login'}
                mess_out=make_response(jsonify(res), 200)
            else:
                res={"message":'Registeration error-Cannot add user'}
                mess_out=make_response(jsonify(res), 401)
        
        
        else:
            res={"message":'user already existed, please login or contact admin'}
            #return redirect(url_for('login'))
            mess_out=make_response(jsonify(res), 401)
    
    return mess_out        
    #return render_template('register.html')