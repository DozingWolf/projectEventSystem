from flask import current_app
from datetime import datetime

def dbDataTransJson(inputdata:list):
    # sqlalchemy数据代理转dict,反馈给业务服务一个dict结构的数据，转json由业务代码进行
    # 不直接转json的原因是外部还需要拼装状态码、说明等信息，多次编码转换不优雅
    current_app.logger.debug(inputdata)
    countRowNum = len(inputdata)
    rtnData = {'rownum':-1,'rowdata':[]}
    rtnData['rownum'] = countRowNum
    if countRowNum >= 1:
        for rid,row in enumerate(inputdata):
            colList = []
            # 当数据出现datetime类型时，需要处理一下
            for cid,col in enumerate(row):
                if isinstance(col,datetime):
                    col = str(col)
                colList.append(col)
            rtnData['rowdata'].append([rid+1,colList])
    else:
        pass
    current_app.logger.debug(rtnData)
    return rtnData