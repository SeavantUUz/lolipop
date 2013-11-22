from flask import Flask
from config import db,BleepRenderer
import misaka as m

def create_app():
    app = Flask(__name__)
    app.secret_key = '\x03\xedS\x08d`\xb0\x97_\x960x\xac\x12\x87\x88\x9f@x:n`\xeb\xd5'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
    app.debug = True
    register_jinja(app)
    db.init_app(app)
    return app

def register_jinja(app):

    @app.template_filter('renderToGFM')
    def renderToGFM(data):
        renderer = BleepRenderer()
        md = m.Markdown(renderer,
                extensions=m.EXT_FENCED_CODE | m.EXT_NO_INTRA_EMPHASIS)
        return md.render(data)
