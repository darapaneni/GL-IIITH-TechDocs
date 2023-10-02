# DB Connector library
import mysql.connector

# Function to insert the record in transactions table
def insert_rec(**payment_details):
    # Connect to the MySQL database
    mydb = mysql.connector.connect(
        host="44.197.242.29",
        user="latexdb",
        password="Latexdb123!",
        database="latexdb"
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









