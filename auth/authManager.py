from flask import current_app,request,session,Blueprint,g
from time import time
from model import db
from model.user import User
from tool.responseGenerator import responseStructures,responseStructureswithCookie
from controller.errorlist import AuthNoPermissionError,AuthError,DBDataError

authManagerBP = Blueprint('authUser',__name__)

@authManagerBP.route('/loginUser',methods=['POST'])
def loginUser():
    if session.get('logged_in') is True:
        return responseStructures(rstatus='200',
                                  rbody={'error_code':2000,
                                         'error_msg':'u have already login by account %s'%session.get('user_name')})                               
    rtnMsg = ''
    loginTime = time()
    try:
        # 检查入参情况
        loginPara = request.get_json()
        if loginPara is None:
            rtnMsg = 'No login para input'
            current_app.logger.error(rtnMsg)
            raise AuthError(message=rtnMsg,arguname='userid, username, passwd')
        if 'userid' in loginPara:
            current_app.logger.debug('userid %s'%loginPara['userid'])
        else:
            rtnMsg = 'No userid'
            current_app.logger.info(rtnMsg)
            raise AuthError(message=rtnMsg,arguname='userid')
        if 'username' in loginPara:
            current_app.logger.debug('username %s'%loginPara['username'])
        else:
            rtnMsg = 'No username'
            current_app.logger.info(rtnMsg)
            raise AuthError(message=rtnMsg,arguname='username')
        if 'passwd' in loginPara:
            current_app.logger.debug('passwd %s'%loginPara['passwd'])
        else:
            rtnMsg = 'No passwd'
            current_app.logger.info(rtnMsg)
            raise AuthError(message=rtnMsg,arguname='passwd')
    except AuthError as err:
        return responseStructures(rstatus=err.code,
                                  rbody={'error_code':err.error_code,
                                         'error_msg':err.message,
                                         'args':err.arguname})
    except Exception as err:
        current_app.logger.error('Unknow Error when analyze post requests para, please chack log file to find detail error message')
        current_app.logger.error(err)
        return responseStructures(rstatus='521',
                                  rbody={'error_code':1699,
                                         'error_msg':'Unknow Error when analyze post requests para, please chack log file to find detail error message',
                                         'args':''})
    # 保留一段用于处理密码加解密
    # …………
    # …………
    # 开始查询并验证用户信息
    # 构造验证用户sql
    current_app.logger.debug('start execute sql')
    countNumSQL = '''select count(1) from edm_test_schema.tmstuser t 
                     where 1=1 
                       and t.username = :username 
                       and t.userid = :userid
                       and t.passwd = :passwd'''
    countNumPara = {'username':loginPara['username'],
                    'userid':loginPara['userid'],
                    'passwd':loginPara['passwd']}
    # 构造获取用户权限sql

    # 开始执行查询
    try:
        countExeSql = db.session.execute(countNumSQL,countNumPara)
        countRtn = countExeSql.fetchall()
        current_app.logger.debug(countRtn)
        if countRtn[0][0] == 1:
            newUser = User(userid=loginPara['userid'],username=loginPara['username'],pcode='001')
            # 加上session看看
            session['logged_in'] = True
            session['user_id'] = newUser.getUserID()
            session['user_name'] = newUser.getUserName()
            session['user_pcode'] = newUser.getUserPermissions()
            session['login_time'] = loginTime
            # 把g也加上试试
            g.user = newUser
            g.login_time = loginTime
        else:
            raise DBDataError(message='no user data found',
                              arguname='')
    except DBDataError as err:
        return responseStructures(rstatus=err.code,
                                  rbody={'error_code':err.error_code,
                                         'error_msg':err.message,
                                         'args':err.arguname})
    except Exception as err:
        current_app.logger.error('Unknow Error when analyze post requests para, please chack log file to find detail error message')
        current_app.logger.error(err)
        return responseStructures(rstatus='521',
                                  rbody={'error_code':1699,
                                         'error_msg':'Unknow Error when analyze post requests para, please chack log file to find detail error message',
                                         'args':''})

    # 反馈cookie给前端
    return responseStructureswithCookie(rstatus='200',
                                        rbody={'error_code':2000,
                                               'error_msg':'success'},
                                        cookieitem=[['cookie_1','1234255325'],['cookie_2','kbfawdouifqnbwelkjbncilsudfnb'],['cookie_3','i am your father']])

@authManagerBP.route('/logoutUser',methods=['POST'])
def logoutUser():
    current_app.logger.debug('=================start log out====================')
    current_app.logger.debug(session.get('logged_in'))
    try:
        if session.get('logged_in'):
            current_app.logger.debug('current user %s will louout'%session.get('user_name'))
            current_app.logger.debug(session.get('user_id'))
            current_app.logger.debug(session.get('user_name'))
            session['logged_in'] = False
            return {'msg':'user logout success!'}
        else:
            return {'msg':'u havent login!'}
    except Exception as err:
        current_app.logger.error(err)
        return {'msg':'error!'}