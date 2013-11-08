import os,string
from flask.ext.script import Manager,Server
from flask.ext.login import current_user,login_user,login_required,logout_user
from config import db,login_manager
from app import create_app
#from kutoto.form import ,EditPost,AddNodeForm
from kutoto.models import Post,Topic,User,Node
from flask import redirect,render_template,url_for,request,flash,abort,current_app
from functools import wraps

app = create_app()
login_manager.init_app(app)
manager = Manager(app)
manager.add_command("runserver",Server("localhost",port=8000))

from views import topic,account
app.register_blueprint(topic.bp,url_prefix='/topic')
app.register_blueprint(account.bp,url_prefix='/account')

@app.route("/")
@app.route("/index")
def index():
    #nodes = Nodes.query.order_by(Topic.last_post_id.desc())
    return render_template('index.html')

##@app.route('/delete/<int:node_id>/post/<int:post_id>')
##def deletePost(node_id,post_id):
##    node = Node.query.get(node_id)
##    node_title = node.title
##    post = Post.query.get(post_id)
##    topic_id = post.topic_id
##    isNotBackToIndex = post.delete()
##    if isNotBackToIndex:
##        return redirect(url_for('listPosts',node_title=node_title,topic_id=topic_id))
##    else:return redirect('/index')

##@app.route('/edit/<int:node_id>/post/<int:post_id>',methods=('GET','POST'))
##def editPost(node_id,post_id):
##    form = EditPost()
##    node = Node.query.get(post_id)
##    node_title = node.title
##    post = Post.query.get(post_id)
##    topic_id = post.topic_id
##    if form.validate_on_submit():
##        form.save(post)
##        return redirect(url_for('listPosts',node_title=node_title,topic_id = topic_id))
##    else:
##        form.content.data = post.content
##    return render_template('edit_post.html',form=form)

#@app.route('/admin')
#@admin_required
#def admin():
#    nodes = Node.query.all()
#    return render_template('admin.html',nodes=nodes)

## @app.route('/admin/<Objects>')
## @admin_required
## def adminObjects(Objects):
##     scope = {}
##     if Objects == 'Topic':
##         scope[Objects]=Topic
##     elif Objects == 'User':
##         scope[Objects]=User
##     exec 'Objects = ' + Objects in scope
##     objects = scope['Objects'].query.all()
##     return render_template('objects.html',objects = objects,objects_name=Objects)
 
## @app.route('/delete/topic/<int:topic_id>')
## @admin_required
## def deleteTopic(topic_id):
##     topic = Topic.query.get(topic_id)
##     topic.delete()
##     return redirect(url_for('admin'))
## 
## @app.route('/delete/user/<int:user_id>')
## @admin_required
## def delelteUser(user_id):
##     user = User.query.get(user_id)
##     user.delete()
##     return redirect(url_for('admin'))
## 
## @app.route('/addNode',methods=('GET','POST'))
## @admin_required
## def addNode():
##     form = AddNodeForm()
##     if form.validate_on_submit():
##         form.save()
##         return redirect(url_for('index'))
##     return render_template('addNode.html',form=form)

@manager.command
def init():
    dfile = 'database.db'
    if os.path.exists(dfile):
        os.remove(dfile)
    db.create_all()


if __name__ == "__main__":
    manager.run()
