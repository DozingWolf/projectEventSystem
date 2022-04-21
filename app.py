from flask import Flask
from konfig import Config
from logging.handlers import TimedRotatingFileHandler
from logging import Formatter,DEBUG,INFO,ERROR,StreamHandler,getLogger
from model import db
from auth.authManager import authManagerBP
from controller.helloPage import helloBP
from controller.getData import getDataBP
from controller.postData import postDataBP
# load parameter
confFile = Config('./conf/para.conf')
# add loghandler and set level and format
selfLogFormat = Formatter('[%(asctime)s] %(levelname)s in %(module)s: %(message)s')
selfLogHandlerFile = TimedRotatingFileHandler(filename='./log/main.log',when='D',
                                           interval=1,backupCount=30,
                                           encoding='UTF-8',delay=False)
selfLogHandlerFile.setLevel(INFO)
selfLogHandlerFile.setFormatter(selfLogFormat)
selfLogHandlerSteam = StreamHandler()
selfLogHandlerSteam.setLevel(DEBUG)
selfLogHandlerSteam.setFormatter(selfLogFormat)
# initial flask
app = Flask(__name__)
rootLogger = getLogger()
for hdl in rootLogger.handlers[:]:
    rootLogger.removeHandler(hdl)
rootLogger.addHandler(selfLogHandlerFile)
rootLogger.addHandler(selfLogHandlerSteam)
app.config.update(confFile.get_map('flask'))
# register blueprint
app.register_blueprint(helloBP,url_prefix='/api/v1.0')
app.register_blueprint(authManagerBP,url_prefix='/api/v1.0/auth')
app.register_blueprint(getDataBP,url_prefix='/api/v1.0/getdata')
app.register_blueprint(postDataBP,url_prefix='/api/v1.0/postdata')
# initial db
db.init_app(app)

if __name__ == '__main__':
    
    app.run()