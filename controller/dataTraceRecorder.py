from flask import current_app,session,request
from functools import wraps

def queryTracerLog(func):
# 建立一个追踪日志
# 用来追踪每一次用户请求url并记录每次的请求负载内容
    @wraps(func)
    def traceLog(*args, **kwargs):
        if session.get('user_id'):
            userID = str(session.get('user_id'))
        else:
            userID = 'Anonymous user'
        queryMethod = request.method
        queryUrl = request.path
        queryPayload = request.get_json()
        queryUA = request.headers.get('User-Agent')
        logString = ' : '.join(['[Tracer LOG]',queryUA,userID,queryMethod,queryUrl,str(queryPayload)])
        current_app.logger.info(logString)
        return func(*args, **kwargs)
    return traceLog