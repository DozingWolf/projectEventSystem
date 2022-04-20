from flask import Blueprint,current_app
from auth.authManager import isLoginCheck

helloBP = Blueprint('helloPage',__name__)

@helloBP.route('/hello',methods=['GET'])
@isLoginCheck
def hello():
    return 'Hello World!'