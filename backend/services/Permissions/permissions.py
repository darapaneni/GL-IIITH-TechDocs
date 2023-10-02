import os
from sqlalchemy.sql import text
import sqlalchemy
import yaml
from flask import Blueprint,request
from ..UserAuthentication.JWTAuthentication import authentication
from flask import request, jsonify
#creating the Permissions Blueprint
permissions_bp = Blueprint('permissionsBlueprint', __name__)
from dotenv import load_dotenv
import sqlalchemy as db
from sqlalchemy import create_engine, select, update, delete
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from DBConnect import session_factory
from orm_Tables import Permission

basedir = os.path.abspath(os.path.dirname(__file__))
env = os.path.join(basedir,'../.env.local')
if os.path.exists(env):
    load_dotenv(env)
url = os.environ.get('DB_URL')
engine = sqlalchemy.create_engine(url)
connect = engine.connect()


@permissions_bp.route('/api/get_permissions', methods=['GET'])
@authentication
def get_permissions(user_id):
    content = request.get_json(silent=True)
    doc_id = content['DocId']
    user_perm = get_user_permissions(user_id, doc_id)[0]
    return jsonify(UP=user_perm)

@permissions_bp.route('/api/set_permissions', methods=['POST'])
@authentication
def set_permissions(user_id):
    '''
        This function takes share_email,user_id and doc_name as its input arguments.Fetches the
        userId of the sharing person and the DocId which is to be shared using the get_user_id and
        get_doc_id methods.This function helps to set the permissions by giving doc_id and share_user_id
        as inputs for the set permission methods.
    '''
    content = request.get_json(silent=True)
    share_email = content['share_email']
    doc_id = content['DocId']
    permission_type = content['permission_type']
    share_user_id = get_user_id(share_email)
    share_user_id = share_user_id
    sql_query_1 = text("""SELECT PermissionId FROM Permissions WHERE UserId=:UID and DocId=:DID""")
    param_1 = {"UID": share_user_id, "DID": doc_id}
    permission_id = connect.execute(sql_query_1, **param_1).first()
    if permission_type != "remove":
        if permission_id is None:
            sql_query_2 = text("""INSERT into Permissions(UserId,DocId) values (:UID,:DID)""")
            connect.execute(sql_query_2,**param_1)
        
    try: 
        
        if 'S' in get_user_permissions(user_id, doc_id):
            if permission_type == "edit":
                # edit_permissions(share_user_id, doc_id)
                sql_stmt = (update(Permission).where(Permission.UserId == share_user_id, Permission.DocId == doc_id).values({Permission.UserPermissions: "RWD"}))
                session = session_factory()
                session.execute(sql_stmt)
                session.commit()
                session.close()
            elif permission_type == "read":
                sql_stmt = (update(Permission).where(Permission.UserId == share_user_id, Permission.DocId == doc_id).values({Permission.UserPermissions: "R"}))
                session = session_factory()
                session.execute(sql_stmt)
                session.commit()
                session.close()
            elif permission_type == "remove":
                remove_permissions(share_user_id, doc_id)
    except Exception as err:
            data_out = {"message":str(err)}
            mess_out = 500
            return jsonify(data_out, mess_out)
    return jsonify(message="Success, permission (RWD) added to the user")



def get_user_id(user_email):
    '''
        This function takes user_name fields from the User table as its input arguments
        queries the userid for that user_email.
        This function returns the UserId.
    '''
    sql = text("""SELECT UserId FROM User WHERE UserName=:UEMAIL""")
    record = {"UEMAIL": user_email}
    user_id = connect.execute(sql, **record).first()
    return user_id[0]


def get_doc_id(user_id, doc_name):
    '''
        This function takes user_id and doc_name fields from the Documents table as its input arguments
        queries the DocId for that Documents table.
        This function returns the DocId.
    '''
    sql = text("""SELECT DocId FROM Documents WHERE UserId=:UID and DocName=:DNAME""")
    record = {"UID": user_id, "DNAME": doc_name}
    doc_id = connect.execute(sql, **record).first()
    return doc_id[0]


def edit_permissions(user_id, doc_id):
    '''
        This function takes user_id and doc_id fields from the Permissions table as its input arguments
        As edit permissions include the "read, write and delete" operations.Hence, we include the methods
        which sets the "read, write and delete" operations for the user.
    '''
    set_read_user_permission(user_id, doc_id)
    set_write_user_permission(user_id, doc_id)
    set_delete_user_permission(user_id, doc_id)


def remove_permissions(user_id, doc_id):
    '''
        This function takes user_id and doc_id fields from the Permissions table as its input arguments
        As remove permissions include removing all operations.Hence, we include the methods
        which unsets the all operations for the user.
    '''
    # unset_read_user_permission(user_id, doc_id)
    # unset_write_user_permission(user_id, doc_id)
    # unset_delete_user_permission(user_id, doc_id)
    # unset_share_user_permission(user_id, doc_id)
    # unset_analytics_user_permission(user_id, doc_id)
    session = session_factory()
    sql_stmt = (delete(Permission).where(Permission.DocId == doc_id, Permission.UserId==user_id))
    session.execute(sql_stmt)
    session.commit()
    session.close()
# functions to set the permissions

# User/Owner level permissions
def set_read_user_permission(user_id, doc_id):
    '''
        This function takes user_id and doc_id fields from the Permissions table as its input arguments
        and queries the PermissionId and UserPermissions details. If UserPermissions is not set, then it'll
        set to "read". However, if it is already set then the "read" permission is added to the existing
        permission set. This function gives a user "read" permissions of a file.
    '''
    sql_query_1 = text("""SELECT PermissionId FROM Permissions WHERE UserId=:UID and DocId=:DID""")
    param_1 = {"UID": user_id, "DID": doc_id}
    permission_id = connect.execute(sql_query_1, **param_1).first()
    sql_query_2 = text("""SELECT UserPermissions from Permissions WHERE PermissionId=:PID""")
    param_2 = {"PID": permission_id[0]}
    user_permission = connect.execute(sql_query_2, **param_2).first()
    if user_permission[0] is None:
        up = "R"
    else:
        up = user_permission[0] 
        up += "R"

    sql_query_3 = text("""UPDATE Permissions SET UserPermissions=:UP WHERE PermissionId=:PID""")
    param_3 = {"UP": up, "PID": permission_id[0]}
    connect.execute(sql_query_3, **param_3)


def set_write_user_permission(user_id, doc_id):
    '''
        This function takes user_id and doc_id fields from the Permissions table as its input arguments
        and queries the PermissionId and UserPermissions details. If UserPermissions is not set, then it'll
        set to "write". However, if it is already set then the "write" permission is added to the existing
        permission set. This function gives a user "write" permissions of a file.
    '''
    sql_query_1 = text("""SELECT PermissionId FROM Permissions WHERE UserId=:UID and DocId=:DID""")
    param_1 = {"UID": user_id, "DID": doc_id}
    permission_id = connect.execute(sql_query_1, **param_1).first()
    sql_query_2 = text("""SELECT UserPermissions from Permissions WHERE PermissionId=:PID""")
    param_2 = {"PID": permission_id[0]}
    user_permission = connect.execute(sql_query_2, **param_2).first()
    if user_permission[0] is None:
        up = "W"
    else:
        up = user_permission[0] 
        up += "W"
    sql_query_3 = text("""UPDATE Permissions SET UserPermissions=:UP WHERE PermissionId=:PID""")
    param_3 = {"UP": up, "PID": permission_id[0]}
    connect.execute(sql_query_3, **param_3)


def set_share_user_permission(user_id, doc_id):
    '''
        This function takes user_id and doc_id fields from the Permissions table as its input arguments
        and queries the PermissionId and UserPermissions details. If UserPermissions is not set, then it'll
        set to "share". However, if it is already set then the "share" permission is added to the existing
        permission set. This function gives a user "share" permissions of a file.
    '''
    sql_query_1 = text("""SELECT PermissionId FROM Permissions WHERE UserId=:UID and DocId=:DID""")
    param_1 = {"UID": user_id, "DID": doc_id}
    permission_id = connect.execute(sql_query_1, **param_1).first()
    sql_query_2 = text("""SELECT UserPermissions from Permissions WHERE PermissionId=:PID""")
    param_2 = {"PID": permission_id[0]}
    user_permission = connect.execute(sql_query_2, **param_2).first()
    if user_permission[0] is None:
        up = "S"
    else:
        up = user_permission[0] 
        up += "S" 
    sql_query_3 = text("""UPDATE Permissions SET UserPermissions=:UP WHERE PermissionId=:PID""")
    param_3 = {"UP": up, "PID": permission_id[0]}
    connect.execute(sql_query_3, **param_3)


def set_delete_user_permission(user_id, doc_id):
    '''
        This function takes user_id and doc_id fields from the Permissions table as its input arguments
        and queries the PermissionId and UserPermissions details. If UserPermissions is not set, then it'll
        set to "delete". However, if it is already set then the "delete" permission is added to the existing
        permission set. This function gives a user "delete" permissions of a file.
    '''
    sql_query_1 = text("""SELECT PermissionId FROM Permissions WHERE UserId=:UID and DocId=:DID""")
    param_1 = {"UID": user_id, "DID": doc_id}
    permission_id = connect.execute(sql_query_1, **param_1).first()
    sql_query_2 = text("""SELECT UserPermissions from Permissions WHERE PermissionId=:PID""")
    param_2 = {"PID": permission_id[0]}
    user_permission = connect.execute(sql_query_2, **param_2).first()
    if user_permission[0] is None:
        up = "D"
    else:
        up = user_permission[0] 
        up += "D"
    sql_query_3 = text("""UPDATE Permissions SET UserPermissions=:UP WHERE PermissionId=:PID""")
    param_3 = {"UP": up, "PID": permission_id[0]}
    connect.execute(sql_query_3, **param_3)


def set_analytics_user_permission(user_id, doc_id):
    '''
        This function takes user_id and doc_id fields from the Permissions table as its input arguments
        and queries the PermissionId and UserPermissions details. If UserPermissions is not set, then it'll
        set to "analytics". However, if it is already set then the "analytics" permission is added to the existing
        permission set. This function gives a user "analytics" permissions of a file.
    '''
    sql_query_1 = text("""SELECT PermissionId FROM Permissions WHERE UserId=:UID and DocId=:DID""")
    param_1 = {"UID": user_id, "DID": doc_id}
    permission_id = connect.execute(sql_query_1, **param_1).first()
    sql_query_2 = text("""SELECT UserPermissions from Permissions WHERE PermissionId=:PID""")
    param_2 = {"PID": permission_id[0]}
    user_permission = connect.execute(sql_query_2, **param_2).first()
    if user_permission[0] is None:
        up = "A"
    else:
        up = user_permission[0] 
        up += "A"
    sql_query_3 = text("""UPDATE Permissions SET UserPermissions=:UP WHERE PermissionId=:PID""")
    param_3 = {"UP": up, "PID": permission_id[0]}
    connect.execute(sql_query_3, **param_3)


# Group level permissions
def set_read_group_permission(user_id, doc_id):
    '''
        This function takes user_id and doc_id fields from the Permissions table as its input arguments
        and queries the PermissionId and GroupPermissions details. If GroupPermissions is not set, then it'll
        set to "read". However, if it is already set then the "read" permission is added to the existing
        permission set. This function gives a group "read" permissions of a file.
    '''
    sql_query_1 = text("""SELECT PermissionId FROM Permissions WHERE UserId=:UID and DocId=:DID""")
    param_1 = {"UID": user_id, "DID": doc_id}
    permission_id = connect.execute(sql_query_1, **param_1).first()
    sql_query_2 = text("""SELECT GroupPermissions from Permissions WHERE PermissionId=:PID""")
    param_2 = {"PID": permission_id[0]}
    group_permission = connect.execute(sql_query_2, **param_2).first()
    if group_permission is None:
        group_permission = "R"
    else:
        group_permission += "R"
    sql_query_3 = text("""UPDATE Permissions SET GroupPermissions=:GP WHERE PermissionId=:PID""")
    param_3 = {"GP": group_permission, "PID": permission_id[0]}
    connect.execute(sql_query_3, **param_3).first()


def set_write_group_permission(user_id, doc_id):
    '''
        This function takes user_id and doc_id fields from the Permissions table as its input arguments
        and queries the PermissionId and GroupPermissions details. If GroupPermissions is not set, then it'll
        set to "write". However, if it is already set then the "write" permission is added to the existing
        permission set. This function gives a group "write" permissions of a file.
    '''
    sql_query_1 = text("""SELECT PermissionId FROM Permissions WHERE UserId=:UID and DocId=:DID""")
    param_1 = {"UID": user_id, "DID": doc_id}
    permission_id = connect.execute(sql_query_1, **param_1).first()
    sql_query_2 = text("""SELECT GroupPermissions from Permissions WHERE PermissionId=:PID""")
    param_2 = {"PID": permission_id[0]}
    group_permission = connect.execute(sql_query_2, **param_2).first()
    if group_permission is None:
        group_permission = "W"
    else:
        group_permission += "W"
    sql_query_3 = text("""UPDATE Permissions SET GroupPermissions=:GP WHERE PermissionId=:PID""")
    param_3 = {"GP": group_permission, "PID": permission_id[0]}
    connect.execute(sql_query_3, **param_3).first()


def set_share_group_permission(user_id, doc_id):
    '''
    This function takes user_id and doc_id fields from the Permissions table as its input arguments
    and queries the PermissionId and GroupPermission details. If GroupPermission is not set, then it'll
    set to "share". However, if it is already set then the "share" permission is added to the existing
    permission set. This function gives a group "share" permissions of a file.
    '''
    sql_query_1 = text("""SELECT PermissionId FROM Permissions WHERE UserId=:UID and DocId=:DID""")
    params_1 = {"UID": user_id, "DID": doc_id}
    permission_id = connect.execute(sql_query_1, **params_1)
    sql_query_2 = text("""SELECT GroupPermissions from Permissions WHERE PermissionId=:PID""")
    params_2 = {"PID": permission_id[0]}
    group_permission = connect.execute(sql_query_2, **params_2)
    if group_permission is None:
        group_permission = "S"
    else:
        group_permission += "S"
    sql_query_3 = text("""UPDATE Permissions SET GroupPermissions=:GP WHERE PermissionId=:PID""")
    params_3 = {"GP": group_permission, "PID": permission_id[0]}
    connect.execute(sql_query_3, **params_3)


def set_delete_group_permission(user_id, doc_id):
    '''
    This function takes user_id and doc_id fields from the Permissions table as its input arguments
    and queries the PermissionId and GroupPermission details. If GroupPermission is not set, then it'll
    set to "delete". However, if it is already set then the "delete" permission is added to the existing
    permission set. This function gives a group "delete" permissions of a file.
    '''
    sql_query_1 = text("""SELECT PermissionId FROM Permissions WHERE UserId=:UID and DocId=:DID""")
    params_1 = {"UID": user_id, "DID": doc_id}
    permission_id = connect.execute(sql_query_1, **params_1)
    sql_query_2 = text("""SELECT UserPermissions from Permissions WHERE PermissionId=:PID""")
    params_2 = {"PID": permission_id[0]}
    group_permission = connect.execute(sql_query_2, **params_2)
    if group_permission is None:
        group_permission = "D"
    else:
        group_permission += "D"
    sql_query_3 = text("""UPDATE Permissions SET UserPermissions=:GP WHERE PermissionId=:PID""")
    params_3 = {"GP": group_permission, "PID": permission_id[0]}
    connect.execute(sql_query_3, **params_3)


def set_analytics_group_permission(user_id, doc_id):
    '''
    This function takes user_id and doc_id fields from the Permissions table as its input arguments
    and queries the PermissionId and GroupPermission details. If GroupPermission is not set, then it'll
    set to "analytics". However, if it is already set then the "analytics" permission is added to the existing
    permission set. This function gives a group "analytics" permissions of a file.
    '''
    sql_query_1 = text("""SELECT PermissionId FROM Permissions WHERE UserId=:UID and DocId=:DID""")
    params_1 = {"UId": user_id, "DId": doc_id}
    permission_id = connect.execute(sql_query_1, **params_1)
    sql_query_2 = text("""SELECT UserPermissions from Permissions WHERE PermissionId=:PID""")
    params_2 = {"PID": permission_id[0]}
    group_permission = connect.execute(sql_query_2, **params_2)
    if group_permission is None:
        group_permission = "A"
    else:
        group_permission += "A"
    sql_query_3 = text("""UPDATE Permissions SET UserPermissions=:GP WHERE PermissionId=:PID""")
    params_3 = {"GP": group_permission, "PID": permission_id[0]}
    connect.execute(sql_query_3, **params_3)


# Others level permissions
def set_read_others_permission(user_id, doc_id):
    '''
    This function takes user_id and doc_id fields from the Permissions table as its input arguments
    and queries the PermissionId and GroupPermission details. If OtherPermissions is not set, then it'll
    set to "read". However, if it is already set then the "read" permission is added to the existing
    permission set. This function gives others(anyone other than owner and group) "read" permissions of a file.
    '''
    sql_query_1 = text("""SELECT PermissionId FROM Permissions WHERE UserId=:UID and DocId=:DID""")
    params_1 = {"UID": user_id, "DID": doc_id}
    permission_id = connect.execute(sql_query_1, **params_1)
    sql_query_2 = text("""SELECT OtherPermissions from Permissions WHERE PermissionId=:PID""")
    params_2 = {"PID": permission_id[0]}
    others_permission = connect.execute(sql_query_2, **params_2)
    if others_permission == None:
        others_permission = "R"
    else:
        others_permission += "R"
    sql_query_3 = text("""UPDATE Permissions SET OtherPermissions=:OP WHERE PermissionId=:PID""")
    params_3 = {"OP": others_permission, "PID": permission_id[0]}
    connect.execute(sql_query_3, **params_3)


def set_write_others_permission(user_id, doc_id):
    '''
    This function takes user_id and doc_id fields from the Permissions table as its input arguments
    and queries the PermissionId and GroupPermission details. If OtherPermissions is not set, then it'll
    set to "write". However, if it is already set then the "write" permission is added to the existing
    permission set. This function gives others(anyone other than owner and group) "write" permissions of a file.
    '''
    sql_query_1 = text("""SELECT PermissionId FROM Permissions WHERE UserId=:UID and DocId=:DID""")
    params_1 = {"UID": user_id, "DID": doc_id}
    permission_id = connect.execute(sql_query_1, **params_1)
    sql_query_2 = text("""SELECT UserPermissions from Permissions WHERE PermissionId=:PID""")
    params_2 = {"PId": permission_id[0]}
    others_permission = connect.execute(sql_query_2, **params_2)
    if others_permission == None:
        others_permission = "W"
    else:
        others_permission += "W"
    sql_query_3 = text("""UPDATE Permissions SET OtherPermissions=:OP WHERE PermissionId=:PID""")
    params_3 = {"OP": others_permission, "PID": permission_id[0]}
    connect.execute(sql_query_3, **params_3)


def set_share_others_permission(user_id, doc_id):
    '''
    This function takes user_id and doc_id fields from the Permissions table as its input arguments
    and queries the PermissionId and GroupPermission details. If OtherPermissions is not set, then it'll
    set to "share". However, if it is already set then the "share" permission is added to the existing
    permission set. This function gives others(anyone other than owner and group) "share" permissions of a file.
    '''
    sql_query_1 = text("""SELECT PermissionId FROM Permissions WHERE UserId=:UID and DocId=:DID""")
    params_1 = {"UID": user_id, "DID": doc_id}
    permission_id = connect.execute(sql_query_1, **params_1)
    sql_query_2 = text("""SELECT UserPermissions from Permissions WHERE PermissionId=:PID""")
    params_2 = {"PId": permission_id[0]}
    others_permission = connect.execute(sql_query_2, **params_2)
    if others_permission is None:
        others_permission = "S"
    else:
        others_permission += "S"
    sql_query_3 = text("""UPDATE Permissions SET OtherPermissions=:OP WHERE PermissionId=:PID""")
    params_3 = {"OP": others_permission, "PID": permission_id[0]}
    connect.execute(sql_query_3, **params_3)


def set_delete_others_permission(user_id, doc_id):
    '''
    This function takes user_id and doc_id fields from the Permissions table as its input arguments
    and queries the PermissionId and GroupPermission details. If OtherPermissions is not set, then it'll
    set to "delete". However, if it is already set then the "delete" permission is added to the existing
    permission set. This function gives others(anyone other than owner and group) "delete" permissions of a file.
    '''
    sql_query_1 = text("""SELECT PermissionId FROM Permissions WHERE UserId=:UID and DocId=:DID""")
    params_1 = {"UID": user_id, "DID": doc_id}
    permission_id = connect.execute(sql_query_1, **params_1)
    sql_query_2 = text("""SELECT UserPermissions from Permissions WHERE PermissionId=:PID""")
    params_2 = {"PId": permission_id[0]}
    others_permission = connect.execute(sql_query_2, **params_2)
    if others_permission is None:
        others_permission = "D"
    else:
        others_permission += "D"
    sql_query_3 = text("""UPDATE Permissions SET OtherPermissions=:OP WHERE PermissionId=:PID""")
    params_3 = {"OP": others_permission, "PID": permission_id[0]}
    connect.execute(sql_query_3, **params_3)


def set_analytics_others_permission(user_id, doc_id):
    '''
    This function takes user_id and doc_id fields from the Permissions table as its input arguments
    and queries the PermissionId and OtherPermissions details. If OtherPermissions is not set, then it'll
    set to "analytics". However, if it is already set then the "analytics" permission is added to the existing
    permission set. This function gives others(anyone other than owner and group) "analytics" permissions of a file.
    '''
    sql_query_1 = text("""SELECT PermissionId FROM Permissions WHERE UserId=:UID and DocId=:DID""")
    params_1 = {"UID": user_id, "DID": doc_id}
    permission_id = connect.execute(sql_query_1, **params_1)
    sql_query_2 = text("""SELECT UserPermissions from Permissions WHERE PermissionId=:PID""")
    params_2 = {"PID": permission_id[0]}
    others_permission = connect.execute(sql_query_2, **params_2)
    if others_permission is None:
        others_permission = "A"
    else:
        others_permission += "A"
    sql_query_3 = text("""UPDATE Permissions SET OtherPermissions=:OP WHERE PermissionId=:PID""")
    params_3 = {"OP": others_permission, "PID": permission_id[0]}
    connect.execute(sql_query_3, **params_3)


# functions to get the permissions
def get_user_permissions(user_id, doc_id):
    session = session_factory()
    userid = user_id
    '''
        This function takes user_id and doc_id fields from the Permissions table as its input arguments
        and queries the PermissionId and UserPermissions details.
        This function returns the UserPermissions set to the user.
    '''
    # sql_query_1 = text("""SELECT PermissionId FROM Permissions WHERE UserId=:UID and DocId=:DID""")
    # param_1 = {"UID": userid, "DID": doc_id}
    # permission_id = connect.execute(sql_query_1, **param_1).first()
    # sql_query_2 = text("""SELECT UserPermissions from Permissions WHERE PermissionId=:PID""")
    # param_2 = {"PID": permission_id[0]}
    # user_permission = connect.execute(sql_query_2, **param_2).first()
    # return list(user_permission)
    sql_stmt = (select (Permission.UserPermissions).where(Permission.UserId == userid ,Permission.DocId == doc_id))
    user_permissions = session.execute(sql_stmt).first()[0]
    return list(user_permissions)



def get_group_permissions(user_id, doc_id):
    '''
        This function takes user_id and doc_id fields from the Permissions table as its input arguments
        and queries the PermissionId and GroupPermissions details.
        This function returns the GroupPermissions set to the user.
    '''
    sql_query_1 = text("""SELECT PermissionId FROM Permissions WHERE UserId=:UID and DocId=:DID""")
    param_1 = {"UID": user_id, "DID": doc_id}
    permission_id = connect.execute(sql_query_1, **param_1).first()
    sql_query_2 = text("""SELECT GroupPermissions from Permissions WHERE PermissionId=:PID""")
    param_2 = {"PID": permission_id[0]}
    group_permission = connect.execute(sql_query_2, **param_2).first()
    return list(group_permission)


def get_others_permissions(user_id, doc_id):
    '''
    This function takes user_id and doc_id fields from the Permissions table as its input arguments
    and queries the PermissionId and OtherPermissions details.
    This function returns the OtherPermissions set to the user.
    '''
    sql_query_1 = text("""SELECT PermissionId FROM Permissions WHERE UserId=:UID and DocId=:DID""")
    params_1 = {"UID": user_id, "DID": doc_id}
    permission_id = connect.execute(sql_query_1, **params_1)
    sql_query_2 = text("""SELECT UserPermissions from Permissions WHERE PermissionId=:PID""")
    params_2 = {"PID": permission_id[0]}
    other_permission = connect.execute(sql_query_2, **params_2)
    return list(other_permission)


# functions to unset/remove permissions

# User/Owner functions
def unset_read_user_permission(user_id, doc_id):
    '''
        This function takes user_id and doc_id fields from the Permissions table as its input arguments
        and queries the PermissionId.get_user_permissions method helps to get the UserPermissions assigned for
        that particular user_id and doc_id.Removed the "read" permission from the UserPermissions.Then
        updated the UserPermissions.This function removes a user "read" permissions of a file.
    '''
    user_permissions = get_user_permissions(user_id, doc_id)
    user_permissions.remove('R')
    user_permissions = "".join(user_permissions)
    sql_query_1 = text("""SELECT PermissionId FROM Permissions WHERE UserId=:UID and DocId=:DID""")
    param_1 = {"UID": user_id, "DID": doc_id}
    permission_id = connect.execute(sql_query_1, **param_1).first()
    sql_query_2 = text("""UPDATE Permissions SET UserPermissions=:UP WHERE PermissionId=:PID""")
    param_2 = {"UP": user_permissions, "PID": permission_id[0]}
    connect.execute(sql_query_2, **param_2).first()


def unset_write_user_permission(user_id, doc_id):
    '''
        This function takes user_id and doc_id fields from the Permissions table as its input arguments
        and queries the PermissionId.get_user_permissions method helps to get the UserPermissions assigned for
        that particular user_id and doc_id.Removed the "write" permission from the UserPermissions.Then
        updated the UserPermissions.This function removes a user "write" permissions of a file.
    '''
    user_permissions = get_user_permissions(user_id, doc_id)
    user_permissions.remove('W')
    user_permissions = "".join(user_permissions)
    sql_query_1 = text("""SELECT PermissionId FROM Permissions WHERE UserId=:UID and DocId=:DID""")
    param_1 = {"UID": user_id, "DID": doc_id}
    permission_id = connect.execute(sql_query_1, **param_1).first()
    sql_query_2 = text("""UPDATE Permissions SET UserPermissions=:UP WHERE PermissionId=:PID""")
    param_2 = {"UP": user_permissions, "PID": permission_id[0]}
    connect.execute(sql_query_2, **param_2).first()


def unset_share_user_permission(user_id, doc_id):
    '''
        This function takes user_id and doc_id fields from the Permissions table as its input arguments
        and queries the PermissionId.get_user_permissions method helps to get the UserPermissions assigned for
        that particular user_id and doc_id.Removed the "share" permission from the UserPermissions.Then
        updated the UserPermissions.This function removes a user "share" permissions of a file.
    '''
    user_permissions = get_user_permissions(user_id, doc_id)
    user_permissions.remove('S')
    user_permissions = "".join(user_permissions)
    sql_query_1 = text("""SELECT PermissionId FROM Permissions WHERE UserId=:UID and DocId=:DID""")
    param_1 = {"UID": user_id, "DID": doc_id}
    permission_id = connect.execute(sql_query_1, **param_1).first()
    sql_query_2 = text("""UPDATE Permissions SET UserPermissions=:UP WHERE PermissionId=:PID""")
    param_2 = {"UP": user_permissions, "PID": permission_id[0]}
    connect.execute(sql_query_2, **param_2).first()


def unset_delete_user_permission(user_id, doc_id):
    '''
        This function takes user_id and doc_id fields from the Permissions table as its input arguments
        and queries the PermissionId.get_user_permissions method helps to get the UserPermissions assigned for
        that particular user_id and doc_id.Removed the "delete" permission from the UserPermissions.Then
        updated the UserPermissions.This function removes a user "delete" permissions of a file.
    '''
    user_permissions = get_user_permissions(user_id, doc_id)
    user_permissions.remove('D')
    user_permissions = "".join(user_permissions)
    sql_query_1 = text("""SELECT PermissionId FROM Permissions WHERE UserId=:UID and DocId=:DID""")
    param_1 = {"UID": user_id, "DID": doc_id}
    permission_id = connect.execute(sql_query_1, **param_1).first()
    sql_query_2 = text("""UPDATE Permissions SET UserPermissions=:UP WHERE PermissionId=:PID""")
    param_2 = {"UP": user_permissions, "PID": permission_id[0]}
    connect.execute(sql_query_2, **param_2).first()


def unset_analytics_user_permission(user_id, doc_id):
    '''
        This function takes user_id and doc_id fields from the Permissions table as its input arguments
        and queries the PermissionId.get_user_permissions method helps to get the UserPermissions assigned for
        that particular user_id and doc_id.Removed the "analytics" permission from the UserPermissions.Then
        updated the UserPermissions.This function removes the user level "analytics" permissions of a file.
    '''
    user_permissions = get_user_permissions(user_id, doc_id)
    user_permissions.remove('A')
    user_permissions = "".join(user_permissions)
    sql_query_1 = text("""SELECT PermissionId FROM Permissions WHERE UserId=:UID and DocId=:DID""")
    param_1 = {"UID": user_id, "DID": doc_id}
    permission_id = connect.execute(sql_query_1, **param_1).first()
    sql_query_2 = text("""UPDATE Permissions SET UserPermissions=:UP WHERE PermissionId=:PID""")
    param_2 = {"UP": user_permissions, "PID": permission_id[0]}
    connect.execute(sql_query_2, **param_2).first()


# Group functions

def unset_read_group_permission(user_id, doc_id):
    '''
        This function takes user_id and doc_id fields from the Permissions table as its input arguments
        and queries the PermissionId.get_group_permissions method helps to get the GroupPermissions assigned for
        that particular user_id and doc_id.Removed the "read" permission from the GroupPermissions.Then
        updated the GroupPermissions.This function removes the group level "read" permissions of a file.
    '''
    group_permissions = get_group_permissions(user_id, doc_id)
    group_permissions.remove('R')
    group_permissions = "".join(group_permissions)
    sql_query_1 = text("""SELECT PermissionId FROM Permissions WHERE UserId=:UID and DocId=:DID""")
    param_1 = {"UID": user_id, "DID": doc_id}
    permission_id = connect.execute(sql_query_1, **param_1).first()
    sql_query_2 = text("""UPDATE Permissions SET GroupPermissions=:GP WHERE PermissionId=:PID""")
    param_2 = {"GP": group_permissions, "PID": permission_id[0]}
    connect.execute(sql_query_2, **param_2).first()


def unset_write_group_permission(user_id, doc_id):
    '''
        This function takes user_id and doc_id fields from the Permissions table as its input arguments
        and queries the PermissionId.get_group_permissions method helps to get the GroupPermissions assigned for
        that particular user_id and doc_id.Removed the "write" permission from the GroupPermissions.Then
        updated the GroupPermissions.This function removes the group level "write" permissions of a file.
    '''
    group_permissions = get_group_permissions(user_id, doc_id)
    group_permissions.remove('W')
    group_permissions = "".join(group_permissions)
    sql_query_1 = text("""SELECT PermissionId FROM Permissions WHERE UserId=:UID and DocId=:DID""")
    param_1 = {"UID": user_id, "DID": doc_id}
    permission_id = connect.execute(sql_query_1, **param_1).first()
    sql_query_2 = text("""UPDATE Permissions SET GroupPermissions=:GP WHERE PermissionId=:PID""")
    param_2 = {"GP": group_permissions, "PID": permission_id[0]}
    connect.execute(sql_query_2, **param_2).first()



def unset_share_group_permission(user_id, doc_id):
    '''
        This function takes user_id and doc_id fields from the Permissions table as its input arguments
        and queries the PermissionId.get_group_permissions method helps to get the GroupPermissions assigned for
        that particular user_id and doc_id.Removed the "share" permission from the GroupPermissions.Then
        updated the GroupPermissions.This function removes the group level "share" permissions of a file.
    '''
    group_permissions = get_group_permissions(user_id, doc_id)
    group_permissions.remove('S')
    group_permissions = "".join(group_permissions)
    sql_query_1 = text("""SELECT PermissionId FROM Permissions WHERE UserId=:UID and DocId=:DID""")
    param_1 = {"UID": user_id, "DID": doc_id}
    permission_id = connect.execute(sql_query_1, **param_1).first()
    sql_query_2 = text("""UPDATE Permissions SET GroupPermissions=:GP WHERE PermissionId=:PID""")
    param_2 = {"GP": group_permissions, "PID": permission_id[0]}
    connect.execute(sql_query_2, **param_2).first()


def unset_delete_group_permission(user_id, doc_id):
    '''
        This function takes user_id and doc_id fields from the Permissions table as its input arguments
        and queries the PermissionId.get_group_permissions method helps to get the GroupPermissions assigned for
        that particular user_id and doc_id.Removed the "delete" permission from the GroupPermissions.Then
        updated the GroupPermissions.This function removes the group level "delete" permissions of a file.
    '''
    group_permissions = get_group_permissions(user_id, doc_id)
    group_permissions.remove('D')
    group_permissions = "".join(group_permissions)
    sql_query_1 = text("""SELECT PermissionId FROM Permissions WHERE UserId=:UID and DocId=:DID""")
    param_1 = {"UID": user_id, "DID": doc_id}
    permission_id = connect.execute(sql_query_1, **param_1).first()
    sql_query_2 = text("""UPDATE Permissions SET GroupPermissions=:GP WHERE PermissionId=:PID""")
    param_2 = {"GP": group_permissions, "PID": permission_id[0]}
    connect.execute(sql_query_2, **param_2).first()


def unset_analytics_group_permission(user_id, doc_id):
    '''
        This function takes user_id and doc_id fields from the Permissions table as its input arguments
        and queries the PermissionId.get_group_permissions method helps to get the GroupPermissions assigned for
        that particular user_id and doc_id.Removed the "analytics" permission from the GroupPermissions.Then
        updated the GroupPermissions.This function removes the group level "analytics" permissions of a file.
    '''
    group_permissions = get_group_permissions(user_id, doc_id)
    group_permissions.remove('A')
    group_permissions = "".join(group_permissions)
    sql_query_1 = text("""SELECT PermissionId FROM Permissions WHERE UserId=:UID and DocId=:DID""")
    param_1 = {"UID": user_id, "DID": doc_id}
    permission_id = connect.execute(sql_query_1, **param_1).first()
    sql_query_2 = text("""UPDATE Permissions SET GroupPermissions=:GP WHERE PermissionId=:PID""")
    param_2 = {"GP": group_permissions, "PID": permission_id[0]}
    connect.execute(sql_query_2, **param_2).first()

# Others permissions

def unset_read_others_permission(user_id, doc_id):
    '''
        This function takes user_id and doc_id fields from the Permissions table as its input arguments
        and queries the PermissionId.get_others_permissions method helps to get the OtherPermissions assigned for
        that particular user_id and doc_id.Removed the "read" permission from the OtherPermissions.Then
        updated the OtherPermissions.This function removes the others level "read" permissions of a file.
    '''
    other_permissions = get_others_permissions(user_id, doc_id)
    other_permissions.remove('R')
    other_permissions = "".join(other_permissions)
    sql_query_1 = text("""SELECT PermissionId FROM Permissions WHERE UserId=:UID and DocId=:DID""")
    param_1 = {"UID": user_id, "DID": doc_id}
    permission_id = connect.execute(sql_query_1, **param_1).first()
    sql_query_2 = text("""UPDATE Permissions SET OtherPermissions=:OP WHERE PermissionId=:PID""")
    param_2 = {"OP": other_permissions, "PID": permission_id[0]}
    connect.execute(sql_query_2, **param_2).first()


def unset_write_others_permission(user_id, doc_id):
    '''
        This function takes user_id and doc_id fields from the Permissions table as its input arguments
        and queries the PermissionId.get_others_permissions method helps to get the OtherPermissions assigned for
        that particular user_id and doc_id.Removed the "write" permission from the OtherPermissions.Then
        updated the OtherPermissions.This function removes the others level "write" permissions of a file.
    '''
    other_permissions = get_others_permissions(user_id, doc_id)
    other_permissions.remove('W')
    other_permissions = "".join(other_permissions)
    sql_query_1 = text("""SELECT PermissionId FROM Permissions WHERE UserId=:UID and DocId=:DID""")
    param_1 = {"UID": user_id, "DID": doc_id}
    permission_id = connect.execute(sql_query_1, **param_1).first()
    sql_query_2 = text("""UPDATE Permissions SET OtherPermissions=:OP WHERE PermissionId=:PID""")
    param_2 = {"OP": other_permissions, "PID": permission_id[0]}
    connect.execute(sql_query_2, **param_2).first()



def unset_share_others_permission(user_id, doc_id):
    '''
        This function takes user_id and doc_id fields from the Permissions table as its input arguments
        and queries the PermissionId.get_others_permissions method helps to get the OtherPermissions assigned for
        that particular user_id and doc_id.Removed the "share" permission from the OtherPermissions.Then
        updated the OtherPermissions.This function removes the others level "share" permissions of a file.
    '''
    other_permissions = get_others_permissions(user_id, doc_id)
    other_permissions.remove('S')
    other_permissions = "".join(other_permissions)
    sql_query_1 = text("""SELECT PermissionId FROM Permissions WHERE UserId=:UID and DocId=:DID""")
    param_1 = {"UID": user_id, "DID": doc_id}
    permission_id = connect.execute(sql_query_1, **param_1).first()
    sql_query_2 = text("""UPDATE Permissions SET OtherPermissions=:OP WHERE PermissionId=:PID""")
    param_2 = {"OP": other_permissions, "PID": permission_id[0]}
    connect.execute(sql_query_2, **param_2).first()


def unset_delete_others_permission(user_id, doc_id):
    '''
        This function takes user_id and doc_id fields from the Permissions table as its input arguments
        and queries the PermissionId.get_others_permissions method helps to get the OtherPermissions assigned for
        that particular user_id and doc_id.Removed the "delete" permission from the OtherPermissions.Then
        updated the OtherPermissions.This function removes the others level "delete" permissions of a file.
    '''
    other_permissions = get_others_permissions(user_id, doc_id)
    other_permissions.remove('D')
    other_permissions = "".join(other_permissions)
    sql_query_1 = text("""SELECT PermissionId FROM Permissions WHERE UserId=:UID and DocId=:DID""")
    param_1 = {"UID": user_id, "DID": doc_id}
    permission_id = connect.execute(sql_query_1, **param_1).first()
    sql_query_2 = text("""UPDATE Permissions SET OtherPermissions=:OP WHERE PermissionId=:PID""")
    param_2 = {"OP": other_permissions, "PID": permission_id[0]}
    connect.execute(sql_query_2, **param_2).first()


def unset_analytics_others_permission(user_id, doc_id):
    '''
        This function takes user_id and doc_id fields from the Permissions table as its input arguments
        and queries the PermissionId.get_others_permissions method helps to get the OtherPermissions assigned for
        that particular user_id and doc_id.Removed the "analytics" permission from the OtherPermissions.Then
        updated the OtherPermissions.This function removes the others level "analytics" permissions of a file.
    '''
    other_permissions = get_others_permissions(user_id, doc_id)
    other_permissions.remove('A')
    other_permissions = "".join(other_permissions)
    sql_query_1 = text("""SELECT PermissionId FROM Permissions WHERE UserId=:UID and DocId=:DID""")
    param_1 = {"UID": user_id, "DID": doc_id}
    permission_id = connect.execute(sql_query_1, **param_1).first()
    sql_query_2 = text("""UPDATE Permissions SET OtherPermissions=:OP WHERE PermissionId=:PID""")
    param_2 = {"OP": other_permissions, "PID": permission_id[0]}
    connect.execute(sql_query_2, **param_2).first()