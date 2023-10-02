from curses import ALL_MOUSE_EVENTS
from datetime import datetime
from decimal import Decimal
# from symbol import not_test
from telnetlib import STATUS
from sqlalchemy import Enum, Column, Integer, String, Text, DateTime, Index, Date, Boolean, DECIMAL, ForeignKey
from sqlalchemy import UniqueConstraint
from sqlalchemy.orm import relationship
from sqlalchemy.dialects import mysql
from DBConnect import Base
from orm_Common import Common
import enum


class ActionEnum(enum.Enum):
    create = "create"
    edit = "edit"
    share = "share"
    delete = "delete"
    rename = "rename"


from sqlalchemy.orm import relationship


#############################
class Document(Common):
    __tablename__ = "Documents"

    UserId          = Column(String(256), ForeignKey("User.UserId"))
    ModifiedDate    = Column(DateTime)
    ModifiedBy      = Column(String(256))  
    User            = relationship('User')    
    
    def __init__(self, UserId, DocName, Filepath, Datetime, Version, IsUpload, IsTrash):
        self.UserId      = UserId
        self.DocName     = DocName
        self.FilePath    = Filepath
        self.CreatedDate = Datetime
        self.Version     = Version
        self.IsUpload    = IsUpload
        self.IsTrash     = IsTrash
  
#############################


class DocumentHistory(Common):
    __tablename__ = "DocumentHistory"

    DocId = Column(Integer, ForeignKey("Documents.DocId"))
    UserId = Column(String(256), ForeignKey("User.UserId"))
    RecordId = Column(Integer, primary_key=True, autoincrement=True)
    User = relationship("User")
    Document = relationship("Document")

    def __init__(self, userid, docid, created_date, document_name, file_path, version):
        self.UserId = userid
        self.DocId = docid
        self.CreatedDate = created_date
        self.DocName = document_name
        self.FilePath = file_path
        self.Version = version


#############################
class UserHistory(Common):
    __tablename__ = "UserHistory"

    RecordId = Column(Integer, primary_key=True, autoincrement=True)
    UserId = Column(String(256), ForeignKey("User.UserId"))
    User = relationship("User")
    DocId = Column(Integer)
    Action = Column(Enum(ActionEnum))

    def __init__(self, userid, docid, time_stamp, document_name, action):
        self.UserId = userid
        self.DocId = docid
        self.CreatedDate = time_stamp
        self.DocName = document_name
        self.Action = action


############################
class Permission(Base):
    __tablename__ = "Permissions"

    PermissionId = Column(Integer, primary_key=True, autoincrement=True)
    DocId = Column(Integer, ForeignKey("Documents.DocId"))
    UserId = Column(String(256), ForeignKey("User.UserId"))
    UserPermissions = Column(String(25))
    GroupPermissions = Column(String(25))
    OtherPermissions = Column(String(25))
    User = relationship("User")
    
    def __init__(self, DocId, UserId, UserPerm):
        self.DocId           = DocId
        self.UserId          = UserId
        self.UserPermissions = UserPerm

#############################
class PaymentAccount(Base):
    __tablename__ = "PaymentAccounts"

    RecordId = Column(Integer, primary_key=True, autoincrement=True)
    UserId = Column(String(256), ForeignKey("User.UserId"))
    IsDefault = Column(Boolean)
    AccType = Column(String(50))
    AccName = Column(String(256))
    AccNumber = Column(mysql.INTEGER(20))
    AccCvv = Column(mysql.INTEGER(4))
    AccExpiry = Column(Date)
    AccIFSC = Column(String(128))
    User = relationship("User")


#############################
class UserPayment(Base):
    __tablename__ = "UserPayments"

    RecordId = Column(Integer, primary_key=True, autoincrement=True)
    UserId = Column(String(256), ForeignKey("User.UserId"))
    PaidDate = Column(DateTime)
    Amount = Column(mysql.DECIMAL(65, 30))
    PayAccountId = Column(Integer)
    PaymentMethod = Column(String(128))
    Status = Column(String(50))
    Notes = Column(Text)
    User = relationship("User")


#############################
class UserSubscription(Base):
    __tablename__ = "UserSubscriptions"

    RecordId = Column(Integer, primary_key=True, autoincrement=True)
    UserId = Column(String(256), ForeignKey("User.UserId"))
    Type = Column(String(5))
    TypeDesc = Column(String(128))
    Status = Column(String(1))
    ExpiryDate = Column(DateTime)
    User = relationship("User")


#############################

class User(Base):
    __tablename__ = "User"

    UserId = Column(String(256), primary_key=True, unique=True)
    UserName = Column(String(256), primary_key=True,nullable=False)
    Password = Column(String(256), nullable=False)
    IsAdmin = Column(Boolean, nullable=False)
    LoginType = Column(String(256), nullable=False)

    # user = relationship("UserPofile",backref = "user", CASCADE = 'all, delete-orphan', lazy = 'dynamic' )

    def __init__(self, UserId, UserName, Password, IsAdmin, LoginType):
        self.UserId = UserId
        self.UserName = UserName
        self.Password = Password
        self.IsAdmin = IsAdmin
        self.LoginType = LoginType


################################

class UserProfile(Base):
    __tablename__ = "UserProfile"

    UserId = Column(String(256), ForeignKey("User.UserId"), primary_key=True, nullable=False, unique=True)
    UserName = Column(String(256), ForeignKey("User.UserName"), nullable=False)
    FirstName = Column(String(100), nullable=True)
    LastName = Column(String(100), nullable=True)
    StreetAddress = Column(String(256), nullable=True)
    State = Column(String(256), nullable=True)
    Country = Column(String(256), nullable=True)
    Occupation = Column(String(256), nullable=True)
    PurposeOfUsage = Column(String(256), nullable=True)
    SignUpDate = Column(Date, nullable=True)
    LastActiveDate = Column(Date, nullable=True)

    def __init__(self, UserId, UserName, FirstName, LastName, StreerAddress, State, Country, Occupation, PurposeOfUsage,
                 SignUpDate, LastActiveDate):
        self.UserId = UserId
        self.UserName = UserName
        self.FirstName = FirstName
        self.LastName = LastName
        self.StreetAddress = StreerAddress
        self.State = State
        self.Country = Country
        self.Occupation = Occupation
        self.PurposeOfUsage = PurposeOfUsage
        self.SignUpDate = SignUpDate
        self.LastActiveDate = LastActiveDate


class LinkedAccount(Base):
    __tablename__ = "LinkedAccount"

    UserId = Column(String(256), ForeignKey("User.UserId"), primary_key=True)
    AccountType = Column(String(256))
    AccountName = Column(String(256))
    AccountPassword = Column(String(256))

    def __init__(self, UserId, AccountType, AccountName, AccountPassword):
        self.UserId = UserId
        self.AccountName = AccountName
        self.AccountType = AccountType
        self.AccountPassword = AccountPassword
