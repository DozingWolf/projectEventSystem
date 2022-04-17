from flask import current_app
from sys import exc_info
from tool.dataTranser import dateStrTransTimestamp
from controller.errorlist import PostParaEmptyError,PostNoParaError

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
