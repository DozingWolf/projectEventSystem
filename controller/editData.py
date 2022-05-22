from crypt import methods
from flask import Blueprint,current_app,request,session
from sqlalchemy import exc
from werkzeug.security import generate_password_hash
from time import strftime,localtime
from traceback import print_exc
from model import db
from tool.responseGenerator import responseStructures
from tool.sqlGenerator import updateSqlGenerator
from controller.dataTraceRecorder import queryTracerLog
from controller.errorlist import PostNoParaError,PostParaEmptyError,AuthNoPermissionError,SqlBuilderError
from auth.authManager import isLoginCheck,isPermissionCheck

editDataBP = Blueprint('editData',__name__)

def valueNoneemptyJudgement(input,argsname:str):
    if len(input) == 0:
        raise PostParaEmptyError(message='post request havent value',
                                 arguname=argsname)

@editDataBP.route('/editPasswd',methods=['POST'])
@queryTracerLog
@isLoginCheck
@isPermissionCheck
def editPasswd():
# 修改用户密码接口
    # 标准sql定义
    updateSQL = '''
            update edm_test_schema.tmstuser set 
            passwd = :passwd , 
            modifyuserid = :modifyuserid , 
            modifydate = to_timestamp(:modifydate,'yyyy-mm-dd hh24:mi:ss')
    '''
    updateWhere = '''
            where userid = :userid
    '''
    updateArg = {}
    # 获取接口变量值
    # 判断是否需要构造新的查询条件
    try:
        # 获取json传递的变量
        inputPara = request.get_json()
        current_app.logger.debug(inputPara)
        if inputPara is not None:
            # 处理需要更新的数据
            # passwd 密码
            if 'passwd' in inputPara:
                current_app.logger.debug(inputPara['passwd'])
                valueNoneemptyJudgement(input=inputPara['passwd'],argsname='passwd')
                updateArg['passwd'] = generate_password_hash(password=inputPara['passwd'],
                                                             method='pbkdf2:sha256',
                                                             salt_length=8)
            else:
                current_app.logger.info('No argument passwd input')
                raise PostNoParaError(message='post request havent enough json payload',
                                      arguname='passwd')
            # userid 用户id
            if 'userid' in inputPara:
                # 此处需要校验一下用户身份，管理员允许修改所有人的密码，普通用户仅可以修改自己的密码
                if session.get('isadmin') is False:
                    if session.get('user_id') != inputPara['userid']:
                        raise AuthNoPermissionError(message='u cant edit other users passwd',
                                                    arguname='passwd')
                else:
                    pass
                valueNoneemptyJudgement(input=str(inputPara['userid']),argsname='userid')
                updateArg['userid'] = inputPara['userid']
                
            else:
                current_app.logger.info('No argument userid input')
                raise PostNoParaError(message='post request havent enough json payload',
                                      arguname='userid')
            # modifyuserid 编辑用户id
            # 从session内取
            updateArg['modifyuserid'] = session.get('user_id')
            # modifydate 编辑时间
            modifyDate = strftime('%Y-%m-%d %H:%M:%S',localtime())
            updateArg['modifydate'] = modifyDate
        else:
            current_app.logger.info('No query para input')
            raise PostNoParaError(message='post request havent json payload',
                                  arguname='passwd')
    except PostParaEmptyError as empvalue:
        return responseStructures(rstatus=empvalue.code,
                                  rbody={'error_code':empvalue.error_code,
                                         'error_msg':empvalue.message,
                                         'args':empvalue.arguname})
    except PostNoParaError as nopara:
        return responseStructures(rstatus=nopara.code,
                                  rbody={'error_code':nopara.error_code,
                                         'error_msg':nopara.message,
                                         'args':nopara.arguname})
    except AuthNoPermissionError as nopms:
        return responseStructures(rstatus=nopms.code,
                                  rbody={'error_code':nopms.error_code,
                                         'error_msg':nopms.message,
                                         'args':nopms.arguname})
    except Exception as err:
        current_app.logger.error('Unknow Error when analyze post requests para, please chack log file to find detail error message')
        current_app.logger.error(err)
        current_app.logger.error(print_exc())
        return responseStructures(rstatus='521',
                                  rbody={'error_code':1699,
                                         'error_msg':'Unknow Error when analyze post requests para, please chack log file to find detail error message',
                                         'args':''})
    updateSQL = ' '.join([updateSQL,updateWhere])
    current_app.logger.debug(updateSQL)
    current_app.logger.debug(updateArg)
    # 执行查询
    try:
        exeSQL = db.session.execute(updateSQL,updateArg)
        db.session.commit()
    except exc.SQLAlchemyError as err:
        current_app.logger.error('SQLAlchemyError, please check log file to find detail error message')
        current_app.logger.error(err)
        current_app.logger.error(print_exc())
        db.session.rollback()
        return responseStructures(rstatus='522',
                                  rbody={'error_code':'1501',
                                         'error_msg':'SQLAlchemyError, please check log file to find detail error message',
                                         'args':''})
    except Exception as err:
        current_app.logger.error('something was wrong, db will rollback this transaction data ')
        current_app.logger.error(err)
        current_app.logger.error(print_exc())
        db.session.rollback()
        return responseStructures(rstatus='522',
                                  rbody={'error_code':'1599',
                                         'error_msg':'DB Unknow Error, data have been rollback, please check log file to find detail error message',
                                         'args':''})
    # 处理数据成为json
    try:
        returnData = {'error_code':'2000','error_msg':'insert success','dataset':'None'}
        return responseStructures(rstatus='200',
                                  rbody=returnData)
    except Exception as err:
        current_app.logger.error('something was wrong, db have been inserted into db, but make response was failed, please check log file to find detail error message')
        current_app.logger.error(err)
        current_app.logger.error(print_exc())
        return responseStructures(rstatus='522',
                                  rbody={'error_code':'1599',
                                         'error_msg':'Server Unknow Error, data have been inserted into db, please check log file to find detail error message',
                                         'args':''})

@editDataBP.route('/editProject',methods=['POST'])
def editProject():
# 项目基础信息修改接口
# 项目基础信息可以修改，包括以下几个字段信息
# projectcode项目编码 projectname项目名 prjinitiatorid项目发起人 prjbrif项目简介 prjcreationday项目发起时间
# 设计传参结构
# {'set':{
#         'col_a':'something',
#         'col_b':'something',
#         ['col':'something']
#        },
#  'where':{
#           'col':{
#                  'operation':'equl',
#                  'data':'somevalue'
#                 },
#           'col':{
#                  'operation':'equl',
#                  'data':'somevalue'
#                 },
#           ['col':{
#                  'operation':'equl',
#                  'data':'somevalue'
#                 }]
#          }
# }
# 允许字段不传值
    updateArg = {}
    # localUpdateSet = []
    try:
        # 获取json传递的变量
        inputPara = request.get_json()
        current_app.logger.debug(inputPara)
        if inputPara is not None:
            # 处理需要更新的数据
            updateSQL , updatePara  = updateSqlGenerator(querypara=inputPara,
                                                         setchecklist=['projectcode','projectname','prjinitiatorid','prjbrif','prjcreationday'],
                                                         querychecklist=['projectid','ownerid'],
                                                         tname='edm_test_schema.tprjproject')
            # # 考虑是update语句，需要处理set部分和where部分
            # if 'set' in inputPara:
            #     current_app.logger.debug(inputPara['set'])
            #     # projectcode 项目代码
            #     if 'projectcode' in inputPara['set']:
            #         valueNoneemptyJudgement(input=inputPara['set']['projectcode'],argsname='projectcode')
            #         localUpdateSet.append('projectcode = :projectcode')
            #         updateArg['projectcode'] = inputPara['set']['projectcode']
            #     # projectname 项目名
            #     if 'projectname' in inputPara['set']:
            #         valueNoneemptyJudgement(input=inputPara['set']['projectname'],argsname='projectcode')
            #         localUpdateSet.append('projectname = :projectname')
            #         updateArg['projectname'] = inputPara['set']['projectname']
            #     # prjinitiatorid 项目发起人
            #     # prjbrif 项目简介
            #     # prjcreationday 项目发起时间
            # else:
            #     raise PostNoParaError(message='post request havent enough json payload',
            #                           arguname='set')
            # # modifyuserid 编辑用户id
            # # 从session内取
            # updateArg['modifyuserid'] = session.get('user_id')
            # # modifydate 编辑时间
            # modifyDate = strftime('%Y-%m-%d %H:%M:%S',localtime())
            # updateArg['modifydate'] = modifyDate
            # # 更新查询条件
            # # 项目更新需要考虑多种更新的操作
            # # 可以考虑到的有按照项目编码(id = data)进行更新
            # # 是否存在用户批量更新多个项目的情况？
            # # 此处优先考虑单条数据处理的情况
            # if 'where' in inputPara:
            #     pass
            # else:
            #     raise PostNoParaError(message='post request havent enough json payload',
            #                           arguname='where')
        else:
            current_app.logger.info('No query para input')
            raise PostNoParaError(message='post request havent json payload',
                                  arguname='')
    except PostParaEmptyError as empvalue:
        return responseStructures(rstatus=empvalue.code,
                                  rbody={'error_code':empvalue.error_code,
                                         'error_msg':empvalue.message,
                                         'args':empvalue.arguname})
    except PostNoParaError as nopara:
        return responseStructures(rstatus=nopara.code,
                                  rbody={'error_code':nopara.error_code,
                                         'error_msg':nopara.message,
                                         'args':nopara.arguname})
    except SqlBuilderError as sqlbud:
        return responseStructures(rstatus=sqlbud.code,
                                  rbody={'error_code':sqlbud.error_code,
                                         'error_msg':sqlbud.message,
                                         'args':sqlbud.arguname})
    except Exception as err:
        current_app.logger.error('Unknow Error when analyze post requests para, please chack log file to find detail error message')
        current_app.logger.error(err)
        current_app.logger.error(print_exc())
        return responseStructures(rstatus='521',
                                  rbody={'error_code':1699,
                                         'error_msg':'Unknow Error when analyze post requests para, please chack log file to find detail error message',
                                         'args':''})
    current_app.logger.debug(updateSQL)
    current_app.logger.debug(updatePara)
    # 执行查询
    try:
        exeSQL = db.session.execute(updateSQL,updateArg)
        db.session.commit()
    except exc.SQLAlchemyError as err:
        current_app.logger.error('SQLAlchemyError, please check log file to find detail error message')
        current_app.logger.error(err)
        current_app.logger.error(print_exc())
        db.session.rollback()
        return responseStructures(rstatus='522',
                                  rbody={'error_code':'1501',
                                         'error_msg':'SQLAlchemyError, please check log file to find detail error message',
                                         'args':''})
    except Exception as err:
        current_app.logger.error('something was wrong, db will rollback this transaction data ')
        current_app.logger.error(err)
        current_app.logger.error(print_exc())
        db.session.rollback()
        return responseStructures(rstatus='522',
                                  rbody={'error_code':'1599',
                                         'error_msg':'DB Unknow Error, data have been rollback, please check log file to find detail error message',
                                         'args':''})
    # 处理数据成为json
    try:
        returnData = {'error_code':'2000','error_msg':'insert success','dataset':'None'}
        return responseStructures(rstatus='200',
                                  rbody=returnData)
    except Exception as err:
        current_app.logger.error('something was wrong, db have been inserted into db, but make response was failed, please check log file to find detail error message')
        current_app.logger.error(err)
        current_app.logger.error(print_exc())
        return responseStructures(rstatus='522',
                                  rbody={'error_code':'1599',
                                         'error_msg':'Server Unknow Error, data have been inserted into db, please check log file to find detail error message',
                                         'args':''})

@editDataBP.route('/editDept',methods=['POST'])
def editDept():
# 部门基础信息修改接口
# 部门基础信息可以修改，包括以下几个字段信息
# deptname 部门名 status 状态
    updateArg = {}
    try:
        # 获取json传递的变量
        inputPara = request.get_json()
        current_app.logger.debug(inputPara)
        if inputPara is not None:
            # 处理需要更新的数据
            updateSQL , updatePara  = updateSqlGenerator(querypara=inputPara,
                                                         setchecklist=['deptname','status'],
                                                         querychecklist=['deptid','status'],
                                                         tname='edm_test_schema.tmstdept')
        else:
            current_app.logger.info('No query para input')
            raise PostNoParaError(message='post request havent json payload',
                                  arguname='')
    except PostParaEmptyError as empvalue:
        return responseStructures(rstatus=empvalue.code,
                                  rbody={'error_code':empvalue.error_code,
                                         'error_msg':empvalue.message,
                                         'args':empvalue.arguname})
    except PostNoParaError as nopara:
        return responseStructures(rstatus=nopara.code,
                                  rbody={'error_code':nopara.error_code,
                                         'error_msg':nopara.message,
                                         'args':nopara.arguname})
    except SqlBuilderError as sqlbud:
        return responseStructures(rstatus=sqlbud.code,
                                  rbody={'error_code':sqlbud.error_code,
                                         'error_msg':sqlbud.message,
                                         'args':sqlbud.arguname})
    except Exception as err:
        current_app.logger.error('Unknow Error when analyze post requests para, please chack log file to find detail error message')
        current_app.logger.error(err)
        current_app.logger.error(print_exc())
        return responseStructures(rstatus='521',
                                  rbody={'error_code':1699,
                                         'error_msg':'Unknow Error when analyze post requests para, please chack log file to find detail error message',
                                         'args':''})
    current_app.logger.debug(updateSQL)
    current_app.logger.debug(updatePara)
    # 执行查询
    try:
        exeSQL = db.session.execute(updateSQL,updateArg)
        db.session.commit()
    except exc.SQLAlchemyError as err:
        current_app.logger.error('SQLAlchemyError, please check log file to find detail error message')
        current_app.logger.error(err)
        current_app.logger.error(print_exc())
        db.session.rollback()
        return responseStructures(rstatus='522',
                                  rbody={'error_code':'1501',
                                         'error_msg':'SQLAlchemyError, please check log file to find detail error message',
                                         'args':''})
    except Exception as err:
        current_app.logger.error('something was wrong, db will rollback this transaction data ')
        current_app.logger.error(err)
        current_app.logger.error(print_exc())
        db.session.rollback()
        return responseStructures(rstatus='522',
                                  rbody={'error_code':'1599',
                                         'error_msg':'DB Unknow Error, data have been rollback, please check log file to find detail error message',
                                         'args':''})
    # 处理数据成为json
    try:
        returnData = {'error_code':'2000','error_msg':'insert success','dataset':'None'}
        return responseStructures(rstatus='200',
                                  rbody=returnData)
    except Exception as err:
        current_app.logger.error('something was wrong, db have been inserted into db, but make response was failed, please check log file to find detail error message')
        current_app.logger.error(err)
        current_app.logger.error(print_exc())
        return responseStructures(rstatus='522',
                                  rbody={'error_code':'1599',
                                         'error_msg':'Server Unknow Error, data have been inserted into db, please check log file to find detail error message',
                                         'args':''})

@editDataBP.route('/editProjectEvent',methods=['POST'])
def editProjectEvent():
# 项目事件修改接口
# 项目事件可以修改，包括以下几个字段信息
# eventtime 事件时间 eventcreationid 事件发起人 eventstatus 事件状态 eventmsg 事件信息 status 状态
# 需要考虑时间字段如何处理？前台报文过来的时候多加一个标记？还是如何做逻辑判断？
# 同时要考虑前台传过来的时间字段，是字符串还是时间戳？需要定一个规则
    updateArg = {}
    try:
        # 获取json传递的变量
        inputPara = request.get_json()
        current_app.logger.debug(inputPara)
        if inputPara is not None:
            # 处理需要更新的数据
            updateSQL , updatePara  = updateSqlGenerator(querypara=inputPara,
                                                         setchecklist=['eventtime','eventcreationid','eventstatus','eventmsg','status'],
                                                         querychecklist=['projectid','eventid'],
                                                         tname='edm_test_schema.tmstdept')
        else:
            current_app.logger.info('No query para input')
            raise PostNoParaError(message='post request havent json payload',
                                  arguname='')
    except PostParaEmptyError as empvalue:
        return responseStructures(rstatus=empvalue.code,
                                  rbody={'error_code':empvalue.error_code,
                                         'error_msg':empvalue.message,
                                         'args':empvalue.arguname})
    except PostNoParaError as nopara:
        return responseStructures(rstatus=nopara.code,
                                  rbody={'error_code':nopara.error_code,
                                         'error_msg':nopara.message,
                                         'args':nopara.arguname})
    except SqlBuilderError as sqlbud:
        return responseStructures(rstatus=sqlbud.code,
                                  rbody={'error_code':sqlbud.error_code,
                                         'error_msg':sqlbud.message,
                                         'args':sqlbud.arguname})
    except Exception as err:
        current_app.logger.error('Unknow Error when analyze post requests para, please chack log file to find detail error message')
        current_app.logger.error(err)
        current_app.logger.error(print_exc())
        return responseStructures(rstatus='521',
                                  rbody={'error_code':1699,
                                         'error_msg':'Unknow Error when analyze post requests para, please chack log file to find detail error message',
                                         'args':''})
    current_app.logger.debug(updateSQL)
    current_app.logger.debug(updatePara)
    # 执行查询
    try:
        exeSQL = db.session.execute(updateSQL,updateArg)
        db.session.commit()
    except exc.SQLAlchemyError as err:
        current_app.logger.error('SQLAlchemyError, please check log file to find detail error message')
        current_app.logger.error(err)
        current_app.logger.error(print_exc())
        db.session.rollback()
        return responseStructures(rstatus='522',
                                  rbody={'error_code':'1501',
                                         'error_msg':'SQLAlchemyError, please check log file to find detail error message',
                                         'args':''})
    except Exception as err:
        current_app.logger.error('something was wrong, db will rollback this transaction data ')
        current_app.logger.error(err)
        current_app.logger.error(print_exc())
        db.session.rollback()
        return responseStructures(rstatus='522',
                                  rbody={'error_code':'1599',
                                         'error_msg':'DB Unknow Error, data have been rollback, please check log file to find detail error message',
                                         'args':''})
    # 处理数据成为json
    try:
        returnData = {'error_code':'2000','error_msg':'insert success','dataset':'None'}
        return responseStructures(rstatus='200',
                                  rbody=returnData)
    except Exception as err:
        current_app.logger.error('something was wrong, db have been inserted into db, but make response was failed, please check log file to find detail error message')
        current_app.logger.error(err)
        current_app.logger.error(print_exc())
        return responseStructures(rstatus='522',
                                  rbody={'error_code':'1599',
                                         'error_msg':'Server Unknow Error, data have been inserted into db, please check log file to find detail error message',
                                         'args':''})