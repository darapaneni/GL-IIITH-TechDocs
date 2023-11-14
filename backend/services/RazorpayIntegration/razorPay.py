#--------------------------------------#
# WebApp for Razorpay
#--------------------------------------#

import razorpay
from flask import Blueprint,  current_app, render_template, request
from flask import jsonify
from random import randint
from datetime import datetime
from dotenv import load_dotenv
import os
from sqlalchemy.sql import text
import sqlalchemy
import yaml
import os.path
import logging
import mysql.connector
from mysql.connector import connect, errorcode

basedir = os.path.abspath(os.path.dirname(__file__))
env = os.path.join(basedir,'../../.env.local')
load_dotenv(env)
url = os.environ.get('DB_URL')
engine = sqlalchemy.create_engine(url)
connect = engine.connect()
print(url)
db_conn = os.environ.get('DB_CONN')
db_database = os.environ.get('DB_NAME')
db_user = os.environ.get('DB_USER')
db_pass = os.environ.get('DB_PASS')

# Start flask
# Flask configurations
razorPayBlueprint = Blueprint('razorPayBlueprint', __name__)

##app = Flask(__name__)

# Create a Razorpay client

##user_id = "81577282-11fe-4db5-b52a-e833e64352f5"
#Home page to accept the transaction information
@razorPayBlueprint.route('/homeRazor/')
def home_page():
    return render_template('homeRazor.html')

def create_order(amt,descr):
   ## pgkeys.r_id = current_app.config["PGKEY_RID"]
   ## pgkeys.r_id = ProdConfig.PGKEY_RID
    r_id = current_app.config["PGKEY_RID"]
    r_key = current_app.config["PGKEY_RKEY"]
    client = razorpay.Client(auth=(r_id, r_key))
    order_currency ='INR'
    #create receipt id from random number
    order_receipt = 'receipt_'+ str(randint(1,1000))

    notes = {'description': descr}
    data={'amount':amt,
          'currency':order_currency,
          'receipt': order_receipt,
          'notes': notes }
    response = client.order.create(data)
    order_id = response['id']
    return(order_id)

@razorPayBlueprint.route('/submit/', methods = ['POST'])
def app_submit():
    global user_id
    # Receiving Current password and new password
    amt_d     = request.form['amt']
    ##content   = request.get_json(silent=True)
    ##amt_d     = content["amt"]
    amt       = int(float(amt_d)*100)
    descr     = request.form['orderDescr']
    fname     = request.form['fname']
    lname     = request.form['lname']
    user_id   = request.form['userId']
    ##descr     = content["orderDesc"]
    ##fname     = content["fname"]
    ##lname     = content["lname"]
    ##user_id   = content["userId"]
    cust_name = fname + " " + lname

    c_name = 'Techdocs GL'
#Create an order for transaction before payment
    print(c_name)
    order_id = create_order(amt,descr)
    print(order_id)

#Create the checkout/payment collection
    string  = str(amt) + ' ' + str(descr) + ' ' + str(cust_name)+ ' ' + str(order_id)
    ##return string
    print(string)

    return render_template('checkout.html',
                           custName=cust_name,
                           descr=descr,
                           amtD=amt_d,
                           amt=amt,
                           key=current_app.config['PGKEY_RID'],
                           currency='INR',
                           name=c_name,
                           orderId=order_id
                           )
    ##payment_id = request.form.get("razorpay_payment_id")
    ##print(payment_id)
# Return the status of the payment
@razorPayBlueprint.route('/status/', methods=['POST'])
def app_status():
    basedir = os.path.abspath(os.path.dirname(__file__))
    env = os.path.join(basedir,'../../.env.local')
    load_dotenv(env)
    url = os.environ.get('DB_URL')
    engine = sqlalchemy.create_engine(url)
    connect = engine.connect()
    db_conn = os.environ.get('DB_CONN')
    db_database = os.environ.get('DB_NAME')
    db_user = os.environ.get('DB_USER')
    db_pass = os.environ.get('DB_PASS')
    print(url)
    print(db_conn)
    print(db_database)
    print(db_user)
    print(db_pass)


    r_id = current_app.config["PGKEY_RID"]
    r_key = current_app.config["PGKEY_RKEY"]
    client = razorpay.Client(auth=(r_id, r_key))
    # Create logical flow and store the details
    # Store the details in transaction table
    payment_id = request.form.get("razorpay_payment_id")
    print(payment_id)
    ##content   = request.get_json(silent=True)
    ##payment_id = content["razorpay_payment_id"]
    payment_details = client.payment.fetch(payment_id)
    print( payment_details)
    if payment_details['method']=='card':
        card_details = client.payment.fetchCardDetails(payment_id)
        print(card_details)
        payment_details['card_type ']=card_details['type']
        payment_details['card_network'] = card_details['network']
        payment_details['card_last4'] = card_details['last4']
        payment_details['card_issuer'] = card_details['issuer']
        payment_details['card_international'] = card_details['international']
        payment_details['card_emi'] = card_details['emi']
        payment_details['card_sub_type'] = card_details['sub_type']
        payment_details['card_token_iin'] = card_details['token_iin']
    else:
        payment_details['card_type '] = None
        payment_details['card_network'] = None
        payment_details['card_last4'] = None
        payment_details['card_issuer'] = None
        payment_details['card_international'] = None
        payment_details['card_emi'] = None
        payment_details['card_sub_type'] = None
        payment_details['card_token_iin'] = None
        #To check order details
    ##orderdetails = client.order.payments(payment_details['order_id'])
    ##print(orderdetails)
    payment_details['amount'] = float(payment_details['amount']) / 100
    payment_details['amount_refunded'] = float(payment_details['amount_refunded']) / 100
    payment_details['created_at'] = datetime.fromtimestamp(payment_details['created_at'])
    payment_details['userId'] = user_id
    print( payment_details)
   ## sql = text()
    print( payment_details)
    cnx = mysql.connector.connect(
        host=db_conn,
        database=db_database,
        user=db_user,
        password=db_pass
    )
    cursor = cnx.cursor()
    print("...Passed")
    sql = """ INSERT INTO UserTransactions
               (PaymentId,
                UserId,
                Type,
                Amount,
                Currency,
                Status,
                Method,
                OrderId,
                Description,
                RefundStatus,
                AmountRefunded,
                Email,
                Contact,
                ErrorCode,
                DateCreated,
                CardType,
                CardNetwork,
                CardLast4,
                CardIssuer,
                CardInternational,
                CardEmi,
                CardSubType,                
                CardTokenIin
                ) 
               VALUES (%s,
                       %s,
                       %s,
                       %s,
                       %s,
                       %s,
                       %s,
                       %s,
                       %s,
                       %s,
                       %s,
                       %s,
                       %s,
                       %s,
                       %s,
                       %s,
                       %s,
                       %s,
                       %s,
                       %s,
                       %s,
                       %s,
                       %s
                       )"""
    values = (payment_details['id'],
              payment_details['userId'],
              payment_details['entity'],
              payment_details['amount'],
              payment_details['currency'],
              payment_details['status'],
              payment_details['method'],
              payment_details['order_id'],
              payment_details['description'],
              payment_details['refund_status'],
              payment_details['amount_refunded'],
              payment_details['email'],
              payment_details['contact'],
              payment_details['error_code'],
              payment_details['created_at'],
              payment_details['card_type '],
              payment_details['card_network'],
              payment_details['card_last4'],
              payment_details['card_issuer'],
              payment_details['card_international'],
              payment_details['card_emi'],
              payment_details['card_sub_type'],
              payment_details['card_token_iin']
              )
    
    try:
        cursor.execute(sql, values)

    except Exception as error:
        cnx.rollback()
        cnx.close()
        return error
    else:
        cnx.commit()
        cursor.close()
        cnx.close()
        print(".....Passed.")
        return "Payment Successfull."

    

    #db_status = razorpayDB.insert_rec(**payment_details)

    #if db_status == 0:
     #   return "Payment Successful!."
    #else:
     #   return db_status

