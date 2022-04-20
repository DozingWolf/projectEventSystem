from flask import make_response

def responseStructures(rstatus:str,rbody):
    resp = make_response(rbody)
    resp.status = rstatus
    return resp

def responseStructureswithCookie(rstatus:str,rbody,cookieitem:list):
    resp = make_response(rbody)
    resp.status = rstatus
    for idx,citem in enumerate(cookieitem):
        resp.set_cookie(citem[0],citem[1])
    return resp