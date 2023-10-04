#--------------------------------------#
# WebApp for Razorpay
#--------------------------------------#

import razorpay
from flask import Blueprint,  current_app, render_template, request
from random import randint
from datetime import datetime
from dotenv import load_dotenv
import os
from sqlalchemy.sql import text
import sqlalchemy

basedir = os.path.abspath(os.path.dirname(__file__))
env = os.path.join(basedir,'../.env.local')
if os.path.exists(env):
    load_dotenv(env)
url = os.environ.get('DB_URL')
engine = sqlalchemy.create_engine(url)
connect = engine.connect()


# Start flask
# Flask configurations
razorPayBlueprint = Blueprint('razorPayBlueprint', __name__)

# app = Flask(__name__)

# Create a Razorpay client

user_id = ""
#Home page to accept the transaction information
@razorPayBlueprint.route('/api/homeRazor.html')
def home_page():
    return render_template('homeRazor.html')

def create_order(amt,descr):
    pgkeys.r_id = current_app.config["PGKEY_RID"]
    pgkeys.r_key = current_app.config["PGKEY_RKEY"]
    client = razorpay.Client(auth=(pgkeys.r_id, pgkeys.r_key))
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

@razorPayBlueprint.route('/api/razorSubmit', methods = ['POST'])
def app_submit():
    global user_id
    amt_d     = request.form['amt']
    amt       = int(float(amt_d)*100)
    descr     = request.form['orderDescr']
    fname     = request.form['fname']
    lname     = request.form['lname']
    user_id   = request.form['userId']
    cust_name = fname + " " + lname

    c_name = 'Techdocs GL'
#Create an order for transaction before payment

    order_id = create_order(amt,descr)

#Create the checkout/payment collection
    #string  = str(amt) + ' ' + str(descr) + ' ' + str(cust_name)+ ' ' + str(order_id)
    #return string

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


# Return the status of the payment
@razorPayBlueprint.route('/api/razorStatus', methods=['POST'])
def app_status():
    pgkeys.r_id = current_app.config["PGKEY_RID"]
    pgkeys.r_key = current_app.config["PGKEY_RKEY"]
    client = razorpay.Client(auth=(pgkeys.r_id, pgkeys.r_key))
    # Create logical flow and store the details
    # Store the details in transaction table
    payment_id = request.form['razorpay_payment_id']
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
    #orderdetails = client.order.payments(payment_details['order_id'])
    #print(orderdetails)
    payment_details['amount'] = float(payment_details['amount']) / 100
    payment_details['amount_refunded'] = float(payment_details['amount_refunded']) / 100
    payment_details['created_at'] = datetime.fromtimestamp(payment_details['created_at'])
    payment_details['userId'] = user_id

    sql = text()
    db_status = razorpayDB.insert_rec(**payment_details)

    if db_status == 0:
        return "Payment Successful!."
    else:
        return db_status

