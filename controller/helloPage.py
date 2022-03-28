from crypt import methods
import imp
from flask import Blueprint

helloBP = Blueprint('helloPage',__name__,url_prefix='/api/v1.0')

@helloBP.route('/hello',methods=['POST'])
def hello():
    return 'Hello World!'