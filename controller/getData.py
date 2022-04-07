from flask import Blueprint,current_app,request
from json import dumps as jdump
from model import db
from tool import dataTranser

getDataBP = Blueprint('getData',__name__)

@getDataBP.route('/getProjectMember',methods=['GET'])
def getProjectMember():
# 获取项目所对应的项目成员和项目所属部门
    # 标准查询和变量定义
    selectSQL = '''
            select 
            p.projectcode,p.projectname,u.username,m.memberstatus,d.deptname
            from edm_test_schema.trltprjmember m 
            inner join edm_test_schema.tmstuser u on m.userid = u.userid
            inner join edm_test_schema.tprjproject p on p.projectid = m.projectid
            inner join edm_test_schema.tmstdept d on p.ownerid = d.deptid
            where 1=1
            and p.status = :status
    '''
    selectArg = {'status':0}
    
    # 获取用户传递的变量数据并判断    
    try:
        # 获取json传递的变量
        inputPara = request.get_json()
        if inputPara is None:
            current_app.logger.info('No query para input')
        else:
            querySet = [selectSQL]
            # 处理各个查询的条件
            # prjcode 项目编码
            if 'prjcode' in inputPara:
                querySet.append('and p.projectcode = :prjcode')
                selectArg['prjcode'] = inputPara['prjcode']
            # prjname 项目名
            if 'prjname' in inputPara:
                querySet.append('and p.projectname = :prjname')
                selectArg['prjname'] = inputPara['prjname']
            # deptname 所属部门
            if 'deptname' in inputPara:
                querySet.append('and d.deptname = :deptname')
                selectArg['deptname'] = inputPara['deptname']
            # membername 项目成员 
            if 'username' in inputPara:
                querySet.append('and u.username = :username')
                selectArg['username'] = inputPara['username']
    except Exception as err:
        current_app.logger.debug(err)
        raise err
    # 构造新的查询
    selectSQL = ' '.join(querySet)
    current_app.logger.debug(selectSQL)
    current_app.logger.debug(selectArg)
    # 执行查询
    try:
        exeSQL = db.session.execute(selectSQL,selectArg)
        rtn = exeSQL.fetchall()
    except Exception as err:
        raise err
    # 处理数据成为json
    try:
        returnData = {'status':'1000','msg':'query success','dataset':dataTranser.dbDataTransJson(inputdata=rtn)}
        returnData = jdump(returnData,ensure_ascii=False)
    except Exception as err:
        current_app.logger.debug(err)
        returnData = {'status':'4000','msg':'query error','detailmsg':err}
        raise err
    return returnData

@getDataBP.route('/getProjectEvent',methods=['GET'])
def getProjectEvent():
# 获取项目包含的事件情况
    # 标准查询和变量定义
    selectSQL = '''
            select
            p.projectcode,p.projectname,e.eventtime,e.eventmsg,u.username as recorder,
            d.deptname as prjowner
            from edm_test_schema.tprjproject p 
            inner join edm_test_schema.tprjevent e on p.projectid = e.projectid and e.status = 0
            inner join edm_test_schema.tmstuser u on p.prjinitiatorid = u.userid
            inner join edm_test_schema.tmstdept d on p.ownerid = d.deptid
            where 1=1
            and p.status = :status
    '''
    selectArg = {'status':0} 
    # 获取用户传递的变量数据并判断 
    try:
        inputPara = request.get_json()
        if inputPara is None:
            current_app.logger.info('No query para input')
        else:
            querySet = [selectSQL]
            # 处理各个查询的条件
            # prjcode 项目编码
            if 'prjcode' in inputPara:
                querySet.append('and p.projectcode = :prjcode')
                selectArg['prjcode'] = inputPara['prjcode']
            # prjname 项目名
            if 'prjname' in inputPara:
                querySet.append('and p.projectname = :prjname')
                selectArg['prjname'] = inputPara['prjname']
            # membername 项目成员 
            if 'username' in inputPara:
                querySet.append('and u.username = :username')
                selectArg['username'] = inputPara['username']
            # ...............
    except Exception as err:
        raise err
    # 构造新的查询
    selectSQL = ' '.join(querySet)
    current_app.logger.debug(selectSQL)
    current_app.logger.debug(selectArg)
    # 执行查询
    try:
        exeSQL = db.session.execute(selectSQL,selectArg)
        rtn = exeSQL.fetchall()
    except Exception as err:
        raise err
    # 处理数据成为json
    try:
        returnData = {'status':'1000','msg':'query success','dataset':dataTranser.dbDataTransJson(inputdata=rtn)}
        returnData = jdump(returnData,ensure_ascii=False)
    except Exception as err:
        current_app.logger.debug(err)
        returnData = {'status':'4000','msg':'query error','detailmsg':err}
        raise err
    return returnData

@getDataBP.route('/getProjectList',methods=['GET'])
def getProjectList():
# 获取项目列表
    # 标准查询和变量定义
    selectSQL = '''
            select 
            p.projectid ,d.deptname ,p.projectcode ,p.projectname ,u.username ,
            prjbrif ,p.prjcreationday ,p.createdate ,c.username ,p.modifydate ,
            m.username ,p.status 
            from tprjproject p 
            inner join tmstdept d on p.ownerid = d.deptid  
            inner join tmstuser u on p.prjinitiatorid = u.userid 
            inner join tmstuser c on p.createuserid = c.userid 
            inner join tmstuser m on p.modifyuserid = m.userid 
            where 1=1
            and p.status = 0
    '''