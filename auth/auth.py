from flask_httpauth import HTTPTokenAuth
from flask import Blueprint,current_app
from model import db
from model.ormuser import User
from controller.markIP import markUserIP

authBP = Blueprint('authBP',__name__)
httpAut = HTTPTokenAuth(scheme='Bearer')

@httpAut.verify_token
def vefToken(tk:str):
    tokenUser = User.query.filter_by(usertk = tk).first()
    if tokenUser is None:
        return False
    logData = ','.join([markUserIP(),'token user is :%s'%tokenUser.username])
    current_app.logger.info(logData)
    if tokenUser.username is not None:
        return True
    else:
        return False
