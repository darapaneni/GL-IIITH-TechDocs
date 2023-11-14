# Import all libraries
import os
import yaml
import os.path
import logging
import mysql.connector
from mysql.connector import connect, errorcode
import os
from dotenv import load_dotenv
from flask import Flask
from flask_bcrypt import Bcrypt

app = Flask(__name__)
bcrypt = Bcrypt(app)


# Get details from configuration file
basedir = os.path.abspath(os.path.dirname(__file__))
env = os.path.join(basedir,'../backend/.env.local')
load_dotenv(env)
print(os.environ.get('DB_URL'))

db_conn =   os.environ.get('DB_CONN')
db_database = os.environ.get('DB_NAME')
db_user = os.environ.get('DB_USER')
db_pass = os.environ.get('DB_PASS')
# log_path = os.environ.get('DIR_ROOT') + os.environ.get('DIR_LOG')
# # Initiate logging 
# logging.basicConfig(filename=log_path)

def insert_varibles_into_table(UserId, UserName, Password, LoginType):
    try:
        connection = mysql.connector.connect(host=db_conn,
                                            database=db_database,
                                            user=db_user,
                                            password=db_pass)
        cursor = connection.cursor()
        mySql_insert_query = """INSERT INTO glcaptest.User (UserId,UserName,Password,LoginType) 
                                VALUES (%s, %s, %s, %s) """

        record = (UserId, UserName, Password, LoginType)
        cursor.execute(mySql_insert_query, record)
        connection.commit()
        print("Record inserted successfully into Users table")
        if connection.is_connected():
            cursor.close()
            connection.close()
    

    except mysql.connector.Error as error:
        print("Failed to insert into MySQL table {}".format(error))
        
    print("MySQL connection is closed")

insert_varibles_into_table('Test1', 'Test1@Test', bcrypt.generate_password_hash('Test123').decode('utf-8'), 'email')
insert_varibles_into_table('Test2', 'Test2@Test', bcrypt.generate_password_hash('Test123').decode('utf-8'), 'email')
insert_varibles_into_table('sai.dappu@gmail.com', 'sai.dappu@gmail.com', bcrypt.generate_password_hash('Test123').decode('utf-8'), 'email')