from flask import Flask
from config import db,BleepRenderer
import os,codecs
import misaka as m

def create_app():
    app = Flask(__name__)
    app.secret_key = '\x03\xedS\x08d`\xb0\x97_\x960x\xac\x12\x87\x88\x9f@x:n`\xeb\xd5'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
    app.config['ROOTDIR'] = os.getcwd()
    app.debug = True
    register_jinja(app)
    db.init_app(app)
    if not os.path.exists('announcement'):
        os.mknod('announcement')
    return app

def register_jinja(app):
    from views.admin import load_sidebar_notice

    @app.template_filter('renderToGFM')
    def renderToGFM(data):
        renderer = BleepRenderer()
        md = m.Markdown(renderer,
                extensions=m.EXT_FENCED_CODE | m.EXT_NO_INTRA_EMPHASIS)
        return md.render(data)

    @app.context_processor
    def register_context():
        return dict(
                load_sidebar_notice=load_sidebar_notice,
                )

