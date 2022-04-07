from flask import Flask
from konfig import Config
from model import db
from controller.helloPage import helloBP
from controller.getData import getDataBP
# load parameter
confFile = Config('./conf/para.conf')
# initial flask
app = Flask(__name__)
app.config.update(confFile.get_map('flask'))
# register blueprint
app.register_blueprint(helloBP,url_prefix='/api/v1.0')
app.register_blueprint(getDataBP,url_prefix='/api/v1.0/getdata')
# initial db
db.init_app(app)

if __name__ == '__main__':
    
    app.run()