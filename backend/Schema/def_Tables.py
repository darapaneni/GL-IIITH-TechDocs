# ----------------------------------------------------------------------------------
# Usage:
# This script is used to configure tables on the dataabase
# Ref_Task: 1.3.3
# # ----------------------------------------------------------------------------------
# # Pre requisites:
# # Database connection string, database name, userid & password are to be configured 
# #   as system environment variables 
# # These values are fetched from the environment variables
# # ----------------------------------------------------------------------------------
# # Revision history:
# ## Author        Date       Comment
# ## Shravan       20221005   Initial version
# # ----------------------------------------------------------------------------------

# # ToDo: Defining FK constraints later after the code for Users schema is uploaded

# Import all libraries
import os
import yaml
import os.path
import logging
import mysql.connector
from mysql.connector import connect, errorcode
import os
from dotenv import load_dotenv


##
# Method to store definitions of all the necessary tables into an array
# This array will later be looped and executed to create tables 
def defineTables():
    
    # Table - PaymentAccounts
    # Stores the payment methods of all users
    # Col - AccType, possible values are 'creditcard', 'debitcard', 'personal'
    tbl_array['PaymentAccounts'] = (
        "Create Table if not exists `PaymentAccounts` ("
        "   RecordId        int not null AUTO_INCREMENT,"
        "   UserId          varchar(256),"
        "   IsDefault       bool,"
        "   AccType         varchar(50),"
        "   AccName         varchar(256),"
        "   AccNumber       int(20),"
        "   AccCvv          int(4),"
        "   AccExpiry       date,"
        "   AccIFSC         varchar(128),"
        "   Version         int,"
        "   s_Misc1         varchar(1024),"
        "   s_Misc2         varchar(1024),"
        "   n_Misc1         int,"
        "   n_Misc2         int,"
        "   PRIMARY KEY (RecordId),"
        "   INDEX idx_PA_User (UserId)"
        ")"
    )

    
    # Table - User
    # Store the credentials of the user
    tbl_array['User'] = (
        "Create Table if not exists `User` ("
        "   UserId          varchar(256) NOT NULL UNIQUE,"
        "   UserName        varchar(256) NOT NULL,"
        "   Password        varchar(256),"
        "   IsAdmin         boolean DEFAULT false,"
        "   LoginType       varchar(256),"
        "   PRIMARY KEY (UserId, UserName),"
        "   INDEX idx_User (UserId)"
        ")"
    )

    # Table - UserProfile
    # Store the information of about the user
    tbl_array['UserProfile'] = (
        "Create Table if not exists `UserProfile` ("
        "   UserId          varchar(256) NOT NULL UNIQUE,"
        "   UserName        varchar(256) NOT NULL,"
        "   FirstName       varchar(100),"
        "   LastName        varchar(100),"
        "   StreetAddress   varchar(256),"
        "   State           varchar(256),"
        "   Country         varchar(100),"
        "   Occupation      varchar(256),"
        "   PurposeOfUsage  varchar(256),"
        "   SignUpDate      date,"
        "   LastActiveDate  date,"
        "   PRIMARY KEY (UserId),"
        "   FOREIGN KEY (UserId, UserName) REFERENCES User(UserId, UserName) ON UPDATE CASCADE ON DELETE CASCADE,"
        "   INDEX idx_UserProfile (UserId)"
        ")"
    )

    # Table - Documents
    # Stores all Document info - the latest version only
    tbl_array['Documnents'] = (
        "Create Table if not exists `Documents` ("
        "DocId          int not null AUTO_INCREMENT,"
        "DocName        varchar(256),"
        "UserId         varchar(256),"
        "IsUpload       boolean DEFAULT false,"
        "FilePath       text,"
        "CreatedDate    datetime,"
        "ModifiedDate   datetime,"
        "ModifiedBy     varchar(256),"
        "Version        int,"
        "IsTrash        boolean DEFAULT false,"
        "s_Misc1        varchar(1024),"
        "s_Misc2        varchar(1024),"
        "n_Misc1        int,"
        "n_Misc2        int,"
        "PRIMARY KEY (DocId),"
        "UNIQUE (DocId),"
        "FOREIGN KEY (UserId) REFERENCES User(UserId) ON DELETE CASCADE,"
        "INDEX idx_Doc_ByUserDoc (UserId, DocId),"
        "INDEX idx_Doc_ByUserCreated (UserId, CreatedDate),"
        "INDEX idx_Doc_ByUserModified (UserId, ModifiedDate)"
        ")"
    )


    #Table DocumentHistory
    tbl_array['DocumentHistory'] = (
        "Create Table if not exists `DocumentHistory` ("
        "RecordId       int not null AUTO_INCREMENT,"
        "DocId          int,"
        "DocName        varchar(256),"
        "UserId         varchar(256),"
        "IsUpload       boolean DEFAULT false,"
        "FilePath       text,"
        "CreatedDate    datetime,"
        "ModifiedDate   datetime,"
        "ModifiedBy     varchar(256),"
        "Version        int,"
        "IsTrash        boolean DEFAULT false,"
        "s_Misc1        varchar(1024),"
        "s_Misc2        varchar(1024),"
        "n_Misc1        int,"
        "n_Misc2        int,"
        "PRIMARY KEY (RecordId),"
        "FOREIGN KEY (UserId) REFERENCES User(UserId) ON DELETE CASCADE,"
        "FOREIGN KEY (DocId) REFERENCES Documents(DocId) ON DELETE CASCADE ON UPDATE CASCADE,"
        "INDEX idx_Doc_ByUserDoc (UserId, DocId),"
        "INDEX idx_Doc_ByUserCreated (UserId, CreatedDate),"
        "INDEX idx_Doc_ByUserModified (UserId, ModifiedDate)"
        ")"
    )

    # Table - Permissions
    # Store permission of all documents for all users
    # Col Permission, possible values are (R)ead, (W)rite, (S)hare
    tbl_array['Permissions'] = (
        "Create Table if not exists `Permissions` ("
        "   PermissionId        int not null AUTO_INCREMENT,"
        "   DocId               int,"
        "   UserId              varchar(256),"
        "   UserPermissions     varchar(25),"
        "   GroupPermissions    varchar(25),"
        "   OtherPermissions    varchar(25),"
        "   Version             int,"
        "   s_Misc1             varchar(1024),"
        "   s_Misc2             varchar(1024),"
        "   n_Misc1             int,"
        "   n_Misc2             int,"
        "   PRIMARY KEY (PermissionId),"
        "   FOREIGN KEY (DocId) REFERENCES Documents(DocId) ON DELETE CASCADE,"
        "   FOREIGN KEY (UserId) REFERENCES User(UserId) ON DELETE CASCADE,"
        "   INDEX idx_Perm_ByUserDoc (UserId, DocId)"
        ")"
    )
    # Table - UserPayments
    # Stores the history of all payments of all users
    # Col - PaymentMethod, possible values are 'card', 'netbank', 'UPI'
    # Col - Status, possible values are 'success', 'failed'
    tbl_array['UserPayments'] = (
        "Create Table if not exists `UserPayments` ("
        "   RecordId        int not null AUTO_INCREMENT,"
        "   UserId          varchar(256),"
        "   PaidDate        datetime,"
        "   Amount          decimal(65,30),"
        "   PayAccountId    int,"
        "   PaymentMethod   varchar(128),"
        "   Status          varchar(50),"
        "   Notes           text,"
        "   Version         int,"
        "   s_Misc1         varchar(1024),"
        "   s_Misc2         varchar(1024),"
        "   n_Misc1         int,"
        "   n_Misc2         int,"
        "   PRIMARY KEY (RecordId),"
        "   FOREIGN KEY (UserId) REFERENCES User(UserId) ON DELETE CASCADE,"
        "   INDEX idx_UP_UserDate (UserId, PaidDate)"
        ")"
    )

    # Table - UserSubscriptions
    # Stores the User subscriptions info
    # Col - Type, possible values are (F)ree, (PC) Paid Corporate
    # Col - TypeDesc, possible values are 'Personal', 'Corporate'
    # Col - Status, possible values are (A)ctive', (I)nactive
    tbl_array['UserSubscriptions'] = (
        "Create Table if not exists `UserSubscriptions` ("
        "   RecordId        int not null AUTO_INCREMENT,"
        "   UserId          varchar(256),"
        "   Type            char(5),"
        "   TypeDesc        varchar(128),"
        "   Status          Char(1),"
        "   ExpiryDate      datetime,"
        "   Version         int,"
        "   s_Misc1         varchar(1024),"
        "   s_Misc2         varchar(1024),"
        "   n_Misc1         int,"
        "   n_Misc2         int,"
        "   PRIMARY KEY (RecordId),"
        "   FOREIGN KEY (UserId) REFERENCES User(UserId) ON DELETE CASCADE,"
        "   INDEX idx_US_User (UserId)"
        ")"
    )


    # Table - LinkedAccount
    # Store the details of Accounts to which the user is linked
    tbl_array['LinkedAccount'] = (
        "Create Table if not exists `LinkedAccount` ("
        "   UserId              varchar(256),"
        "   AccountType         varchar(256),"
        "   AccountName         varchar(256),"
        "   AccountPassword     varchar(256),"
        "   PRIMARY KEY (UserId),"
        "   FOREIGN KEY (UserId) REFERENCES User(UserId),"
        "   INDEX idx_LinkedAccount (UserId)"
        ")"
    )

    tbl_array['UserTransactions'] = (
        " CREATE TABLE `UserTransactions` ( "
        "    PaymentId          VARCHAR(255) NOT NULL,"
        "    UserId             VARCHAR(255) NOT NULL,"
        "    Type               VARCHAR(255) ,"
        "    Amount             DECIMAL (6,2) NOT NULL,"
        "    Currency           VARCHAR(10) ,"
        "    Status             VARCHAR(255) ,"
        "    Method             VARCHAR(255) ,"
        "    CardType           VARCHAR(255) ,"
        "    CardNetwork        VARCHAR(255) ,"
        "    CardLast4          VARCHAR(255) ,"
        "    CardIssuer         VARCHAR(255) ,"
        "    CardInternational  VARCHAR(255) ,"
        "    CardEmi            VARCHAR(255) ,"
        "    CardSubType        VARCHAR(255) ,"
        "    CardTokenIin       VARCHAR(255) ,"
        "    OrderId            VARCHAR(255) ,"
        "    Description        VARCHAR(255) ,"
        "    RefundStatus       VARCHAR(255) ,"
        "    AmountRefunded     DECIMAL (6,2) NOT NULL,"
        "    Email              VARCHAR(255) ,"
        "    Contact            VARCHAR(255) ,"
        "    ErrorCode          VARCHAR(255) ,"
        "    DateCreated        TIMESTAMP DEFAULT CURRENT_TIMESTAMP,"
        "    PRIMARY KEY (PaymentId),"
	    "    FOREIGN KEY (UserId) REFERENCES User(UserId) ON DELETE CASCADE"
        "    )"
    )

##
# Method to run the table definitions defined in the earlier call in a loop
# Creates a connection to the Database and then executes the create query
def createTables():
    # Get all details of the DB from the environment variables
    # db_conn     = os.environ.get('MYSQL_CONNECTION')
    # db_database = os.environ.get('MYSQL_DB')
    # db_user     = os.environ.get('MYSQL_USER')
    # db_pass     = os.environ.get('MYSQL_PASS')

    # Get details from configuration file
    basedir = os.path.abspath(os.path.dirname(__file__))
    env = os.path.join(basedir,'../.env.local')
    load_dotenv(env)
    print(os.environ.get('DB_URL'))
    

    db_conn = os.environ.get('DB_CONN')
    db_database = os.environ.get('DB_NAME')
    db_user = os.environ.get('DB_USER')
    db_pass = os.environ.get('DB_PASS')
    # log_path = os.environ.get('DIR_ROOT') + os.environ.get('DIR_LOG')
    # # Initiate logging 
    # logging.basicConfig(filename=log_path)

    try:
        cnx = mysql.connector.connect(
            host=db_conn,
            database=db_database,
            user=db_user,
            password=db_pass
        )
    except mysql.connector.Error as err:
        logging.exception(err)
    else:
        cursor = cnx.cursor()

    for tbl_name in tbl_array:
        tbl_def = tbl_array[tbl_name]
        try:
            print("Running table def: {}: ".format(tbl_name), end='')
            logging.info("Running table def: {}: ".format(tbl_name), end='')
            # print("\n Table def: ",tbl_def)
            cursor.execute(tbl_def)
        except mysql.connector.Error as err:
            if err.errno == errorcode.ER_TABLE_EXISTS_ERROR:
                logging.error("Table already exists.")
            else:
                logging.exception(err.msg)
        else:
            print("...Passed")
            logging.info("...Passed")

    cursor.close()
    cnx.close()


#########################
# Main Call
#########################
if __name__ == '__main__':
    # Variable to store all table definitions
    tbl_array = {}
    # Table definitions
    defineTables()
    # Open connection and run table defitions
    createTables()
