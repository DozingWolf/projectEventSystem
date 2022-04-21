from flask import Blueprint,current_app,session
from auth.authManager import isLoginCheck,isPermissionCheck
from tool.responseGenerator import responseStructures

helloBP = Blueprint('helloPage',__name__)

@helloBP.route('/hello',methods=['GET'])
@isLoginCheck
@isPermissionCheck
def hello():
    return responseStructures(rstatus='200',
                              rbody={'error_code':2000,
                                     'error_msg':'Hello World! %s'%session.get('user_name'),
                                     'args':session.get('permission')})

@helloBP.route('/hello-2',methods=['GET'])
@isLoginCheck
@isPermissionCheck
def hello_2():
    return responseStructures(rstatus='200',
                              rbody={'error_code':2000,
                                     'error_msg':'Hello World! %s'%session.get('user_name'),
                                     'args':session.get('permission')})