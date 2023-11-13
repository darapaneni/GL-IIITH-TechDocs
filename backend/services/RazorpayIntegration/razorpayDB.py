# DB Connector library
import os
import yaml
import os.path
import logging
import mysql.connector
from mysql.connector import connect, errorcode
import os
from dotenv import load_dotenv

# Function to insert the record in transactions table
def insert_rec(**payment_details):
    basedir = os.path.abspath(os.path.dirname(__file__))
    env = os.path.join(basedir,'../../.env.local')
    if os.path.exists(env):
        load_dotenv(env)
    url = os.environ.get('DB_URL')
    db_conn = os.environ.get('DB_CONN')
    db_database = os.environ.get('DB_NAME')
    db_user = os.environ.get('DB_USER')
    db_pass = os.environ.get('DB_PASS')
    print(db_user)
    # Connect to the MySQL database
    mydb = mysql.connector.connect(
        host=db_conn,
        database=db_database,
        user=db_user,
        password=db_pass
    )

    # Define a Cursor
    mycursor = mydb.cursor()

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
        mycursor.execute(sql, values)

    except Exception as error:
        mydb.rollback()
        mydb.close()
        return error
    else:
        mydb.commit()
        mydb.close()
        return 0









