from crypt import methods
from flask import Blueprint,current_app,request,make_response,g
from sqlalchemy import exc
from model import db
from tool.dataTranser import dateStrTransTimestamp
from tool.sqlGenerator import insertSqlParaGenerator
from controller.errorlist import PostNoParaError,PostParaEmptyError

postDataBP = Blueprint('postData',__name__)

def responseStructures(rstatus:str,rbody):
    resp = make_response(rbody)
    resp.status = rstatus
    return resp

def valueNoneemptyJudgement(input,argsname:str):
    if len(input) == 0:
        raise PostParaEmptyError(message='post request havent value',
                                 arguname=argsname)


@postDataBP.route('/postCreateUser',methods=['POST'])
def postCreateUser():
# 新增用户接口
    # 标准SQL和变量定义
    insertSQL = '''
            insert into edm_test_schema.tmstuser (userid, username, passwd, isadmin,createuserid)
            values (nextval('edm_test_schema.seq_tmstuser_userid'), :username, :passwd, :isadmin, :createuserid)
    '''
    insertArg = {'createuserid':0}
    # 获取用户传递的变量数据并判断    
    try:
        # 获取json传递的变量
        inputPara = request.get_json()
        if inputPara is not None:
            # 处理需要插入的数据
            # username 用户名
            if 'username' in inputPara:
                valueNoneemptyJudgement(input=inputPara['username'],argsname='username')
                insertArg['username'] = inputPara['username']
            else:
                current_app.logger.info('No argument username input')
                raise PostNoParaError(message='post request havent json payload',
                                      arguname='username')
            # passwd 用户密码
            if 'passwd' in inputPara:
                valueNoneemptyJudgement(input=inputPara['passwd'],argsname='passwd')
                insertArg['passwd'] = inputPara['passwd']
            else:
                current_app.logger.info('No argument passwd input')
                raise PostNoParaError(message='post request havent json payload',
                                      arguname='passwd')
            # isadmin 管理员状态
            if 'isadmin' in inputPara:
                valueNoneemptyJudgement(input=inputPara['isadmin'],argsname='isadmin')
                insertArg['isadmin'] = inputPara['isadmin']
            else:
                current_app.logger.info('No argument isadmin input')
                raise PostNoParaError(message='post request havent json payload',
                                      arguname='isadmin')
        else:
            current_app.logger.info('No query para input')
            raise PostNoParaError(message='post request havent json payload',
                                  arguname='username,passwd,isadmin')
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
    except Exception as err:
        current_app.logger.error('Unknow Error when analyze post requests para, please chack log file to find detail error message')
        current_app.logger.error(err)
        return responseStructures(rstatus='521',
                                  rbody={'error_code':1699,
                                         'error_msg':'Unknow Error when analyze post requests para, please chack log file to find detail error message',
                                         'args':''})
    # 记录insert数据
    current_app.logger.debug(insertSQL)
    current_app.logger.debug(insertArg)
    # 执行查询
    try:
        exeSQL = db.session.execute(insertSQL,insertArg)
        db.session.commit()
    except exc.SQLAlchemyError as err:
        current_app.logger.error('SQLAlchemyError, please check log file to find detail error message')
        current_app.logger.error(err)
        return responseStructures(rstatus='522',
                                  rbody={'error_code':'1501',
                                         'error_msg':'SQLAlchemyError, please check log file to find detail error message',
                                         'args':''})
    except Exception as err:
        current_app.logger.error('something was wrong, db will rollback this transaction data ')
        current_app.logger.error(err)
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
        current_app.logger.debug(err)
        return responseStructures(rstatus='522',
                                  rbody={'error_code':'1599',
                                         'error_msg':'Server Unknow Error, data have been inserted into db, please check log file to find detail error message',
                                         'args':''})
    

@postDataBP.route('/postCreateDept',methods=['POST'])
def postCreateDept():
# 新增用户接口
    # 标准SQL和变量定义
    insertSQL = '''
            insert into edm_test_schema.tmstdept (deptid, deptname, createuserid)
            values (nextval('edm_test_schema.seq_tmstdept_deptid'), :deptname, :createuserid)
    '''
    insertArg = {'createuserid':0}
    # 获取用户传递的变量数据并判断    
    try:
        # 获取json传递的变量
        inputPara = request.get_json()
        if inputPara is not None:
            # 处理需要插入的数据
            # deptname 部门名
            if 'deptname' in inputPara:
                valueNoneemptyJudgement(input=inputPara['deptname'],argsname='deptname')
                insertArg['deptname'] = inputPara['deptname']
            else:
                current_app.logger.info('No argument username input')
                raise PostNoParaError(message='post request havent json payload',
                                      arguname='deptname')
        else:
            current_app.logger.info('No query para input')
            raise PostNoParaError(message='post request havent json payload',
                                  arguname='deptname')
    except Exception as err:
        current_app.logger.error('Unknow Error when analyze post requests para, please chack log file to find detail error message')
        current_app.logger.error(err)
        return responseStructures(rstatus='521',
                                  rbody={'error_code':1699,
                                         'error_msg':'Unknow Error when analyze post requests para, please chack log file to find detail error message',
                                         'args':''})
    # 记录insert数据
    current_app.logger.debug(insertSQL)
    current_app.logger.debug(insertArg)
    # 执行查询
    try:
        exeSQL = db.session.execute(insertSQL,insertArg)
        db.session.commit()
    except exc.SQLAlchemyError as err:
        current_app.logger.error('SQLAlchemyError, please check log file to find detail error message')
        current_app.logger.error(err)
        return responseStructures(rstatus='522',
                                  rbody={'error_code':'1501',
                                         'error_msg':err.args[0],
                                         'args':''})
    except Exception as err:
        current_app.logger.error('something was wrong, db will rollback this transaction data ')
        current_app.logger.error(err)
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
        current_app.logger.debug(err)
        return responseStructures(rstatus='522',
                                  rbody={'error_code':'1599',
                                         'error_msg':'Server Unknow Error, data have been inserted into db, please check log file to find detail error message',
                                         'args':''})

@postDataBP.route('/postCreatePrject',methods=['POST'])
def postCreatePrject():
# 新增项目接口
    # 标准SQL和变量定义
    insertSQL = '''
            insert into edm_test_schema.tprjproject 
            (projectid, ownerid, projectcode, projectname, prjinitiatorid,
             prjbrif, prjcreationday, createuserid)
            values 
            (nextval('edm_test_schema.seq_tprjproject_projectid'), :ownerid, :projectcode, :projectname, :prjinitiatorid,
             :prjbrif, :prjcreationday, :createuserid)
    '''
    insertArg = {'createuserid':0}
    # 获取用户传递的变量数据并判断    
    try:
        # 获取json传递的变量
        inputPara = request.get_json()
        if inputPara is not None:
            # 处理需要插入的数据
            # ownerid 所属部门
            if 'ownerid' in inputPara:
                valueNoneemptyJudgement(input=inputPara['ownerid'],argsname='username')
                insertArg['username'] = inputPara['ownerid']
            else:
                current_app.logger.info('No argument ownerid input')
                raise PostNoParaError(message='post request havent json payload',
                                      arguname='ownerid')
            # projectcode 项目编码
            if 'projectcode' in inputPara:
                valueNoneemptyJudgement(input=inputPara['projectcode'],argsname='projectcode')
                insertArg['projectcode'] = inputPara['projectcode']
            else:
                current_app.logger.info('No argument projectcode input')
                raise PostNoParaError(message='post request havent json payload',
                                      arguname='projectcode')
            # projectname 项目名
            if 'projectname' in inputPara:
                valueNoneemptyJudgement(input=inputPara['projectname'],argsname='projectname')
                insertArg['projectname'] = inputPara['projectname']
            else:
                current_app.logger.info('No argument projectname input')
                raise PostNoParaError(message='post request havent json payload',
                                      arguname='projectname')
            # prjinitiatorid 项目发起人id
            if 'prjinitiatorid' in inputPara:
                valueNoneemptyJudgement(input=inputPara['prjinitiatorid'],argsname='prjinitiatorid')
                insertArg['prjinitiatorid'] = inputPara['prjinitiatorid']
            else:
                current_app.logger.info('No argument prjinitiatorid input')
                raise PostNoParaError(message='post request havent json payload',
                                      arguname='prjinitiatorid')
            # prjbrif 项目简介文字
            if 'prjbrif' in inputPara:
                # 项目简介可以为空，是否可以不控制了？
                # valueNoneemptyJudgement(input=inputPara['prjbrif'],argsname='prjbrif')
                insertArg['prjbrif'] = inputPara['prjbrif']
            else:
                current_app.logger.info('No argument prjbrif input')
                raise PostNoParaError(message='post request havent json payload',
                                      arguname='prjbrif')
            # prjcreationday 项目发起时间
            # json入参需要考虑时间格式的处理问题
            if 'prjcreationday' in inputPara:
                valueNoneemptyJudgement(input=inputPara['prjcreationday'],argsname='prjcreationday')
                transData = dateStrTransTimestamp(input = inputPara['prjcreationday'])
                insertArg['prjcreationday'] = transData
            else:
                current_app.logger.info('No argument prjcreationday input')
                raise PostNoParaError(message='post request havent json payload',
                                      arguname='prjcreationday')
        else:
            current_app.logger.info('No query para input')
            raise PostNoParaError(message='post request havent json payload',
                                  arguname='ownerid,projectcode,projectname,prjinitiatorid,prjbrif')
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
    except Exception as err:
        current_app.logger.error('Unknow Error when analyze post requests para, please chack log file to find detail error message')
        current_app.logger.error(err)
        return responseStructures(rstatus='521',
                                  rbody={'error_code':1699,
                                         'error_msg':'Unknow Error when analyze post requests para, please chack log file to find detail error message',
                                         'args':''})
    # 记录insert数据
    current_app.logger.debug(insertSQL)
    current_app.logger.debug(insertArg)
    # 执行查询
    try:
        exeSQL = db.session.execute(insertSQL,insertArg)
        db.session.commit()
    except exc.SQLAlchemyError as err:
        current_app.logger.error('SQLAlchemyError, please check log file to find detail error message')
        current_app.logger.error(err)
        return responseStructures(rstatus='522',
                                  rbody={'error_code':'1501',
                                         'error_msg':'SQLAlchemyError, please check log file to find detail error message',
                                         'args':''})
    except Exception as err:
        current_app.logger.error('something was wrong, db will rollback this transaction data ')
        current_app.logger.error(err)
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
        current_app.logger.debug(err)
        return responseStructures(rstatus='522',
                                  rbody={'error_code':'1599',
                                         'error_msg':'Server Unknow Error, data have been inserted into db, please check log file to find detail error message',
                                         'args':''})


@postDataBP.route('/postCreateEvent',methods=['POST'])
def postCreateEvent():
# 新增项目事件接口
    # 标准SQL和变量定义
    insertSQL = '''
            insert into edm_test_schema.tprjevent 
            (eventid, projectid, eventtime, eventcreationid, eventstatus, 
             eventmsg, createuserid)
            values 
            (nextval('edm_test_schema.seq_tprjevent_eventid'), :projectid, to_timestamp(:eventtime,'yyyy-mm-dd hh24:mi:ss'), :eventcreationid, :eventstatus, 
             :eventmsg, :createuserid)
    '''
    insertArg = {'createuserid':0}
    argList = [('projectid',1),('eventtime',1),('eventcreationid',1),('eventstatus',1),('eventmsg',0)]
    # 获取用户传递的变量数据并判断 
    try:
        # 获取json传递的变量
        inputPara = request.get_json()
        if inputPara is not None:
            # 处理需要插入的数据
            insertArg = insertSqlParaGenerator(rpara=inputPara,isexist=argList,defaultinsarg=insertArg)
        else:
            current_app.logger.info('No query para input')
            raise PostNoParaError(message='post request havent json payload',
                                  arguname='projectid, eventtime, eventcreationid, eventstatus, eventmsg, createuserid')
        current_app.logger.debug('===================================')
        current_app.logger.debug(insertArg)
        current_app.logger.debug('===================================')
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
    except Exception as err:
        current_app.logger.error('Unknow Error when analyze post requests para, please chack log file to find detail error message')
        current_app.logger.error(err)
        return responseStructures(rstatus='521',
                                  rbody={'error_code':1699,
                                         'error_msg':'Unknow Error when analyze post requests para, please chack log file to find detail error message',
                                         'args':''})
    # 记录insert数据
    current_app.logger.debug(insertSQL)
    current_app.logger.debug(insertArg)
    # 执行查询
    try:
        exeSQL = db.session.execute(insertSQL,insertArg)
        db.session.commit()
    except exc.SQLAlchemyError as err:
        current_app.logger.error('SQLAlchemyError, please check log file to find detail error message')
        current_app.logger.error(err)
        return responseStructures(rstatus='522',
                                  rbody={'error_code':'1501',
                                         'error_msg':'SQLAlchemyError, please check log file to find detail error message',
                                         'args':''})
    except Exception as err:
        current_app.logger.error('something was wrong, db will rollback this transaction data ')
        current_app.logger.error(err)
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
        current_app.logger.debug(err)
        return responseStructures(rstatus='522',
                                  rbody={'error_code':'1599',
                                         'error_msg':'Server Unknow Error, data have been inserted into db, please check log file to find detail error message',
                                         'args':''})


@postDataBP.route('/postCreatePrjMember',methods=['POST'])
def postCreatePrjMember():
# 新增项目成员接口
    # 标准SQL和变量定义
    insertSQL = '''
            insert into edm_test_schema.trltprjmember 
            (projectid, userid, memberstatus, createuserid)
            values 
            (:projectid, :userid, :memberstatus, :createuserid)
    '''
    insertArg = {'createuserid':0}
    argList = [('projectid',1),('userid',1),('memberstatus',1)]
    # 获取用户传递的变量数据并判断 
    try:
        # 获取json传递的变量
        inputPara = request.get_json()
        if inputPara is not None:
            # 处理需要插入的数据
            insertArg = insertSqlParaGenerator(rpara=inputPara,isexist=argList,defaultinsarg=insertArg)
        else:
            current_app.logger.info('No query para input')
            raise PostNoParaError(message='post request havent json payload',
                                  arguname='projectid, userid, memberstatus')
        current_app.logger.debug('===================================')
        current_app.logger.debug(insertArg)
        current_app.logger.debug('===================================')
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
    except Exception as err:
        current_app.logger.error('Unknow Error when analyze post requests para, please chack log file to find detail error message')
        current_app.logger.error(err)
        return responseStructures(rstatus='521',
                                  rbody={'error_code':1699,
                                         'error_msg':'Unknow Error when analyze post requests para, please chack log file to find detail error message',
                                         'args':''})
    # 记录insert数据
    current_app.logger.debug(insertSQL)
    current_app.logger.debug(insertArg)
    # 执行查询
    try:
        exeSQL = db.session.execute(insertSQL,insertArg)
        db.session.commit()
    except exc.SQLAlchemyError as err:
        current_app.logger.error('SQLAlchemyError, please check log file to find detail error message')
        current_app.logger.error(err)
        return responseStructures(rstatus='522',
                                  rbody={'error_code':'1501',
                                         'error_msg':'SQLAlchemyError, please check log file to find detail error message',
                                         'args':''})
    except Exception as err:
        current_app.logger.error('something was wrong, db will rollback this transaction data ')
        current_app.logger.error(err)
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
        current_app.logger.debug(err)
        return responseStructures(rstatus='522',
                                  rbody={'error_code':'1599',
                                         'error_msg':'Server Unknow Error, data have been inserted into db, please check log file to find detail error message',
                                         'args':''})