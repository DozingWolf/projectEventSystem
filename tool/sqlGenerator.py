from flask import current_app,session
from sys import exc_info
from time import strftime,localtime
from tool.dataTranser import dateStrTransTimestamp
from controller.errorlist import PostParaError,PostParaEmptyError,PostNoParaError,SqlBuilderError

def valueNoneemptyJudgement(input,argsname:str):
    if len(str(input)) == 0:
        raise PostParaEmptyError(message='post request havent value',
                                 arguname=argsname)

def insertSqlParaGenerator(rpara:list,isexist:list,defaultinsarg:dict):
# insert语句绑定变量字典生成器
# rpara：requests请求所带的参数
# isexist：需要判断的值清单
# rpara构型：{"key":value,"key":value,...}
# isexist构型：[(value,check_flag1,check_flag2,...),(value,check_flag1,check_flag2,...),...]
    # 如果请求参数和判断参数数量不一致，抛出错误
    if len(rpara) != len(isexist):
        raise Exception('rpara <> isexist')
    insertArg = defaultinsarg
    if len(isexist) > 0:
        try:
            current_app.logger.debug(isexist)
            current_app.logger.debug(rpara)
            # 对isexist列表内做循环判断
            for idx,insArg in enumerate(isexist):
                # 如果，给定的值在requests的json报文中，开始判断
                current_app.logger.debug('=======start step %d======='%idx)
                current_app.logger.debug('insArg = %s'%str(insArg))
                if insArg[0] in rpara:
                    # 第一个checkflag，代表是否非空。0为可空，1为非空
                    if insArg[1] == 0:
                        insertArg[insArg[0]] = rpara[insArg[0]] 
                        current_app.logger.debug(rpara[insArg[0]])
                    else:
                        valueNoneemptyJudgement(input=rpara[insArg[0]],argsname=insArg[0])
                        insertArg[insArg[0]] = rpara[insArg[0]] 
                        current_app.logger.debug(rpara[insArg[0]])
                    # 第二个checkflag，代表是否需要处理时间格式。0为不处理，1需要处理
                    # 好像需要考虑下标越界的情况
                    # postgresql用to_timestamp函数解决日期问题了，这个校验其实可以不需要了
                    # 代码不删除了，留给未来如果还要其他需要判断的时候再进行改造吧
                    # if 2 in range(len(insArg)):
                    #     if insArg[2] == 1:
                    #         current_app.logger.debug(insArg)
                    #         insertArg[insArg[0]] = dateStrTransTimestamp(input = rpara[insArg[0]])
                    #     else:
                    #         current_app.logger.debug('no para input, we would not trans timestamp')
                    # else:
                    #     pass
                else:
                    current_app.logger.info('No argument %s input'%insArg[0])
                    raise PostNoParaError(message='post request havent json payload',
                                          arguname=insArg[0])
                current_app.logger.debug('=======end step %d======='%idx)
            return insertArg
        except Exception as err:
            current_app.logger.debug('===================================')
            current_app.logger.error(err.with_traceback)
            current_app.logger.error(exc_info())
            current_app.logger.debug('===================================')
            raise err
    else:
        current_app.logger.info('No argument input')
        return insertArg

def insertSqlParaGenerator_batch(insertpara:dict,checklist:list,tname:str):
# 新写一个insert构造器
# insert into tablename (col_a,col_b,col_c[,col_n]) values (v_1,v_2,v_3[,v_n])
# 设计传参结构
# {'column':[col_a,col_b,col_c],
#  'values':[
#            [v_1,v_2,v_3],
#            [v_1,v_2,v_3],
#            [v_1,v_2,v_3]
#           ]
# }
    queryModel = ['insert into %s ('%tname]
    queryValueModel = ['values (']
    queryParameter = []
    # current_app.logger.debug(queryModel)
    if not insertpara.get('column'):
        # 如果传入的column部分字典值为空，抛出错误
        raise PostNoParaError(message='post request havent json payload',
                              arguname='column')
    if not insertpara.get('values'):
        # 如果传入的column部分字典值为空，抛出错误
        raise PostNoParaError(message='post request havent json payload',
                              arguname='values')
    if len(insertpara.get('values')) == 0:
        # 如果values没有任何数据，报个错
        raise PostParaEmptyError(message='empty payload',
                                 arguname='values')
    if len(insertpara.get('column')) != len(insertpara.get('values')[0]):
        # 如果column定义的字段数量和values提供的数值数量不一致，报个错
        raise PostParaError(message='the numbers of column not equl the number of values',
                            arguname='column,values')
    for insColValue in insertpara.get('column'):
        # 处理insert段
        # 代码收尾用createuserid进行，这样就不需要判断逗号的问题了
        # 发现一个问题，如果数据有sequence序列怎么处理？
        queryModel.append('%s,'%insColValue)
        queryValueModel.append(':insColValue,')
    queryModel.append('createuserid)')
    queryValueModel.append(':createuserid)')
    queryModel.extend(queryValueModel)
    current_app.logger.debug(queryModel)
    for insKey,insValue in enumerate(insertpara.get('values')):
        # 构造一个接受批量插入的数据集
        current_app.logger.debug('insValue is:')
        current_app.logger.debug(insValue)
        insValue.append(session.get('user_id'))
        queryParameter.append(insValue)
    return ' '.join(queryModel) , queryParameter

def selectSqlGenerator(querypara:dict,querychecklist:list,tname:str):
# 设计一个查询构造器
# 基本可以借用update构造器的where部分
# select有时候是count计算，是不是考虑处理一下？
# 或者构造器保持简洁，count与否由上层代码来处理？
# {
#  'type':'count'|'select',
#  'col':['col_a','col_b'],
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
    pass

def updateSqlGenerator(querypara:dict,setchecklist:list,querychecklist:list,tname:str):
# update tablename set col_1 = something , col_2 = something where col_3 = something and col_4 = something
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
# 设计传参json如上，设想，如果想要用一个自动方式处理，就需要对set部分和where部分做遍历
# 遍历的时候，为了确定这个参数是否正确，可能需要给一个参数列表用于确定这个数据的正确名称
# where条件也同理
    queryModel = ['update %s set'%tname]
    queryParameter = {}
    # current_app.logger.debug(queryModel)
    if not querypara.get('set'):
        # 如果传入的set部分字典值为空，抛出错误
        # 用exception占个位，后续改成自定义错误值
        raise PostNoParaError(message='post request havent json payload',
                              arguname='set')
    if not querypara.get('where'):
        # 如果传入的query部分字典值为空，抛出错误
        # 用exception占个位，后续改成自定义错误值
        raise PostNoParaError(message='post request havent json payload',
                              arguname='where')
    # setPartFlag = len(querypara.get('set').items())
    # calcFlag = 0
    for setKey,setValue in querypara.get('set').items():
        current_app.logger.debug(setKey)
        current_app.logger.debug(setValue)
        if setKey in setchecklist:
            # set部分，因为是更新，每个值都不应该是空值，所以都要做非空校验
            valueNoneemptyJudgement(input=setValue,argsname=setKey)
            # 完成非空校验后进行sql构造和传参
            # 此处需要考虑，最后一个set之后，是没有逗号的
            # 或者，只有一个set条件之后，也是没有逗号的
            # 不需要考虑了，因为还有默认的修改日期和修改人条件，让那两个条件处理语句收口
            # 新增两种情况，1是传入的是一个list，需要考虑；2是传入是一个日期，需要考虑校验
            queryModel.extend([setKey,'= :%s ,'%setKey])
            queryParameter[setKey] = setValue
        else:
            # 如果给定的set值不存在于检查list，其实可以不用管？
            # 先不抛出任何错误，写个日志吧
            current_app.logger.debug('set.%s is not in checklist'%setKey)
            # 用exception占个位，后续改成自定义错误值
            # raise PostNoParaError(message='post request havent json payload',
            #                       arguname='set.%s'%setKey)
        # 原本处理语句收口的代码因为要考虑默认的修改人和修改时间，就不需要特意处理了
        # if setPartFlag == 1:
        #     # 当只有一个set值时，不需要拼接逗号符
        #     pass
        # else:
        #     if calcFlag+1 == setPartFlag:
        #         # 当有多个set值时，最后一个set不要拼接逗号符号
        #         pass
        #     else:
        #         calcFlag += 1
        #         queryModel.append(',')
    # 加上更新人和更新时间的默认值
    queryModel.append('modifydate = to_timestamp(:modifydate,\'yyyy-mm-dd hh24:mi:ss\') ,')
    queryParameter['modifydate'] = strftime('%Y-%m-%d %H:%M:%S',localtime())
    queryModel.append('modifyuserid = :modifyuserid')
    queryParameter['modifyuserid'] = session.get('user_id')
    # 此处要考虑一个问题，where条件的where字符，什么时候拼上去？
    queryModel.append('where 1=1')
    for whereKey,whereValue in querypara.get('where').items():
        current_app.logger.debug(whereKey)
        current_app.logger.debug(whereValue)
        if whereKey in querychecklist:
            # where部分的校验
            # where是一个嵌套的二层字典，需要定位到值和运算符kv对进行校验
            valueNoneemptyJudgement(input=whereValue.get('data'),argsname=whereKey)
            # 构造where条件第一部分
            queryModel.extend(['and %s'%whereKey])
            # 为防止set和where条件有同一个字段，需要对绑定变量名进行别名处理
            newWhereParaName = 'where_'+whereKey
            # 判断计算条件 > < >= <= != 等
            if whereValue.get('operation') == 'equl':
                # = 计算
                queryModel.append('=')
            elif whereValue.get('operation') == 'gret':
                # > 计算
                queryModel.append('>')
            elif whereValue.get('operation') == 'lest':
                # < 计算
                queryModel.append('<')
            elif whereValue.get('operation') == 'neql':
                # != 计算
                queryModel.append('<>')
            elif whereValue.get('operation') == 'greteq':
                # >= 计算
                queryModel.append('>=')
            elif whereValue.get('operation') == 'lesteq':
                # <= 计算
                queryModel.append('<=')
            elif whereValue.get('operation') == 'in':
                # in 计算
                queryModel.append('in')
            elif whereValue.get('operation') == 'like':
                # like 计算
                queryModel.append('like')
            else:
                # 不支持的运算符，抛出错误
                raise SqlBuilderError(message='mismatch mathematical symbol',
                                      arguname='key:where.%s.operation value:%s'%(whereKey,whereValue.get('operation')))
            # 构造where条件数值部分
            queryModel.extend([':%s'%newWhereParaName])
            # 根据sqlalchemy的奇怪特性，需要把list的参数转为tuple才可以绑定变量
            if isinstance(whereValue.get('data'),list):
                queryParameter[newWhereParaName] = tuple(whereValue.get('data'))
            else:
                queryParameter[newWhereParaName] = whereValue.get('data')
        else:
            # 如果给定的where值不存在于检查list，存在安全性风险
            # 抛出错误
            raise SqlBuilderError(message='error \'where\' condition',
                                  arguname=whereKey)
    current_app.logger.debug(' '.join(queryModel))
    current_app.logger.debug(queryParameter)
    return ' '.join(queryModel) , queryParameter
        
def deleteSqlGenerator(querypara:dict,querychecklist:list,tname:str):
# 删除语句构造器
# delete from table where col_1 = something and col_2 = something 
# 设计传参结构
# {
#     'where':{
#         'col_1':'someting',
#         'col_2':2,
#         'col_3':[1,2,3,4]
#     }
# }
# 理论上不建议做任何的物理删除操作
# 用逻辑删除标记来进行替代比较合适
    pass
