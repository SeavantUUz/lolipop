from flask import Flask
from config import db,BleepRenderer,login_manager
import os,codecs
import misaka as m

def create_app():
    app = Flask(__name__)
    app.secret_key = '\x03\xedS\x08d`\xb0\x97_\x960x\xac\x12\x87\x88\x9f@x:n`\xeb\xd5'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
    app.config['ROOTDIR'] = os.getcwd()
    app.debug = True

    register_jinja(app)
    register_routes(app)
    db.init_app(app)
    login_manager.init_app(app)
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

def register_routes(app):
    from views import index,topic,account,node,admin,user,notice
    app.register_blueprint(topic.bp,url_prefix='/topic')
    app.register_blueprint(account.bp,url_prefix='/account')
    app.register_blueprint(node.bp,url_prefix='/node')
    app.register_blueprint(admin.bp,url_prefix='/admin')
    app.register_blueprint(user.bp,url_prefix='/user')
    app.register_blueprint(notice.bp,url_prefix='/notice')
    app.register_blueprint(index.bp,url_profix='')


