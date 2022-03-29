from flask import current_app,request

def markUserIP():
    # 注意，此处使用X-Forwarded_For，因为统御数据中心的nginx上面配置的是这个头:(普通情况下使用X-Forwarded-For
    useruri = request.url
    reqHead = request.headers
    if request.headers.getlist('X-Forwarded_For') is True:
        userip = request.headers.getlist('X-Forwarded_For')[0]
        print('x-forwarded-for :%s'%userip)
    else:
        userip = request.headers.getlist('Host')
        print('host :%s'%userip)
    return ('request_user ip is : %s , source_uri: %s ,reqHead: %s'%(userip,useruri,reqHead))