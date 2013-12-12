# coding:utf-8
from flask import Flask
from _helpers import db,cache,BleepRenderer,login_manager,mark_online
from flask.ext.login import login_required,current_user 
#from _helpers import db,mark_online#,mail
import os,codecs
import misaka as m
import datetime

def create_app():
    app = Flask(__name__)
    app.secret_key = '\x03\xedS\x08d`\xb0\x97_\x960x\xac\x12\x87\x88\x9f@x:n`\xeb\xd5'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
    app.config['ROOTDIR'] = os.getcwd()
    app.config['ONLINEUSERS'] = set()
    app.debug = True

    register_jinja(app)
    register_routes(app)
    db.init_app(app)
    login_manager.init_app(app)
    #mail.init_app(app)

    if not os.path.exists('announcement'):
        os.mknod('announcement')
    cache.init_app(app,config={'CACHE_TYPE': 'simple'})

    @login_required
    @app.before_request
    def mark_current_user_online():
        if current_user is not None and current_user.is_authenticated():
            mark_online(current_user.id)
    return app

def register_jinja(app):
    from views.admin import load_sidebar_notice

    @app.template_filter('renderToGFM')
    def renderToGFM(data):
        renderer = BleepRenderer()
        md = m.Markdown(renderer,
                extensions=m.EXT_FENCED_CODE | m.EXT_NO_INTRA_EMPHASIS)
        return md.render(data)

    @app.template_filter('xmldatetime')
    def xmldatetime(value):
        if not isinstance(value, datetime.datetime):
            return value
        return value.strftime('%Y-%m-%dT%H:%M:%SZ')

    @app.template_filter('timesince')
    def timesince(value):
        now = datetime.datetime.utcnow()
        delta = now - value
        if delta.days > 365:
            return u'{num}年前'.format(num=delta.days / 365)
        if delta.days > 30:
            return u'{num}个月前'.format(num=delta.days / 30)
        if delta.days > 0:
            return u'{num}天前'.format(num=delta.days)
        if delta.seconds > 3600:
            return u'{num}小时前'.format(num=delta.seconds / 3600)
        if delta.seconds > 60:
            return u'{num}个月前'.format(num=delta.seconds / 60)
        return u'刚刚'

    from views.focus import getNodes
    @app.context_processor
    def register_context():
        return dict(
                load_sidebar_notice=load_sidebar_notice,
                getNodes = getNodes,
                )

def register_routes(app):
    from views import index,topic,account,node,admin,user,notice,focus
    app.register_blueprint(topic.bp,url_prefix='/topic')
    app.register_blueprint(account.bp,url_prefix='/account')
    app.register_blueprint(node.bp,url_prefix='/node')
    app.register_blueprint(admin.bp,url_prefix='/admin')
    app.register_blueprint(user.bp,url_prefix='/user')
    app.register_blueprint(notice.bp,url_prefix='/notice')
    app.register_blueprint(focus.bp,url_prefix='/focus')
    app.register_blueprint(index.bp,url_profix='')


