import os,string
from flask.ext.script import Manager,Server
from flask.ext.login import current_user,login_user,login_required,logout_user
from config import db,login_manager
from app import create_app,register_jinja
#from kutoto.form import ,EditPost,AddNodeForm
from kutoto.models import Post,Topic,User,Node
from flask import redirect,render_template,url_for,request,flash,abort,current_app
from functools import wraps

app = create_app()
login_manager.init_app(app)
manager = Manager(app)
manager.add_command("runserver",Server("localhost",port=8000))

from views import topic,account,node,admin,user
app.register_blueprint(topic.bp,url_prefix='/topic')
app.register_blueprint(account.bp,url_prefix='/account')
app.register_blueprint(node.bp,url_prefix='/node')
app.register_blueprint(admin.bp,url_prefix='/admin')
app.register_blueprint(user.bp,url_prefix='/user')

@app.route("/")
@app.route("/index")
def index():
    topics = Topic.query.order_by(Topic.last_post_id.desc()).limit(15)
    return render_template('index.html',topics=topics)

@manager.command
def init():
    dfile = 'database.db'
    if os.path.exists(dfile):
        os.remove(dfile)
    db.create_all()


if __name__ == "__main__":
    manager.run()
