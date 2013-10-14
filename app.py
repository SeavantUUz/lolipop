from flask import Flask
from database import db

def create_app():
    app = Flask(__name__)
    app.secret_key = '\x03\xedS\x08d`\xb0\x97_\x960x\xac\x12\x87\x88\x9f@x:n`\xeb\xd5'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
    app.debug = True
    db.init_app(app)
    return app
