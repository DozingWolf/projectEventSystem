from flask import Flask
from controller.helloPage import helloBP

app = Flask(__name__)
app.register_blueprint()

if __name__ == '__main__':
    
    app.run()