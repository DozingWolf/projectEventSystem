from flask import Blueprint,current_app

helloBP = Blueprint('helloPage',__name__)

@helloBP.route('/hello',methods=['GET'])
def hello():
    return 'Hello World!'