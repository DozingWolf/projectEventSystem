from crypt import methods
from flask import Blueprint,current_app,request
from sqlalchemy import exc
from werkzeug.security import generate_password_hash
from model import db
from tool.dataTranser import dateStrTransTimestamp
from tool.sqlGenerator import insertSqlParaGenerator
from tool.responseGenerator import responseStructures
from controller.errorlist import PostNoParaError,PostParaEmptyError
from auth.authManager import isLoginCheck,isPermissionCheck

editDataBP = Blueprint('editData',__name__)

def valueNoneemptyJudgement(input,argsname:str):
    if len(input) == 0:
        raise PostParaEmptyError(message='post request havent value',
                                 arguname=argsname)

@editDataBP.route('editPasswd',methods=['POST'])
def editPasswd():
# 修改用户密码接口
    # 标准sql定义
    updateSQL = '''
            update edm_test_schema.tmstuser u set 
            u.passwd = :passwd
    '''
    updateWhere = '''
            where u.userid = :userid
    '''
    # 获取接口变量值
    # 判断是否需要构造新的查询条件
    