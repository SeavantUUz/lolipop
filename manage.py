import os
from flask.ext.script import Manager,Server
from flask.ext.login import current_user,login_user,login_required,logout_user
from config import db,login_manager
from app import create_app
from kutoto.form import NewTopic,ReplyPost,EditPost,RegisterUser,LoginUser,AddNodeForm
from kutoto.models import Post,Topic,User,Node
from flask import redirect,render_template,url_for,request,flash,abort
from functools import wraps

app = create_app()
login_manager.init_app(app)
manager = Manager(app)
manager.add_command("runserver",Server("localhost",port=8000))

def admin_required(func):
    @wraps(func)
    def decorated_view(*args,**kwargs):
        try:
            if not current_user.id == 1:
                abort(403)
            return func(*args,**kwargs)
        except AttributeError:
            abort(403)
    return decorated_view

@login_manager.user_loader
def load_user(userid):
    return User.query.get(userid)

@app.route("/")
@app.route("/index")
def index():
    #nodes = Nodes.query.order_by(Topic.last_post_id.desc())
    nodes = Node.query.all()
    return render_template('index.html',nodes = nodes)

@app.route("/node/<node_title>")
def listTopics(node_title):
    topics = Node.query.filter(Topic.node.title == node_title).order_by(Topic.last_post.desc())
    return render_template('node.html',node_title=node_title,topics = topics)
    
@app.route("/node/<node_title>/new_topic",methods=('GET','POST'))
@login_required
def newTopic(node_title):
    node = Node.query.filter(Node.title == node_title).first()
    form  = NewTopic()
    if form.validate_on_submit():
        form.save(node,current_user)
        return redirect(url_for('listTopics',node_title=node_title))
    return render_template('form.html',form=form)

@app.route("/node/<node_title>/topic/<int:topic_id>",methods=('GET','POST'))
## where we can see the different between filter and filter_by
## the filter allow use the pythonic way to filter data
## and filter_by use the column name to filter
def listPosts(node_title,topic_id):
    node = Node.query.filter_by(tilte = node_title)
    form = ReplyPost()
    posts = Post.query.filter_by(topic_id=topic_id).order_by(Post.date_created)
    topic = Topic.query.get(topic_id)
    if current_user is not None and current_user.is_authenticated() and form.validate_on_submit():
        form.save(node,current_user,topic)
        return redirect(url_for('listPosts',node_title=node_title,topic_id=topic_id))
    elif form.validate_on_submit():
        return redirect(url_for('login'))
    return render_template('posts.html',posts=posts,form=form)

@app.route('/register',methods=["GET","POST"])
def register():
    if current_user is not None and current_user.is_authenticated():
        return redirect(url_for('profile',user_id = current_user.id))
    form = RegisterUser(request.form)
    if form.validate_on_submit():
        user = form.save()
        login_user(user)
        flash(("Thanks for your registering"),"success")
        return redirect(url_for('index'))
    return render_template('register.html',form=form)

@app.route('/login',methods=["GET","POST"])
def login():
    if current_user is not None and current_user.is_authenticated():
        return redirect(url_for('profile',user_id=current_user.id))
    form = LoginUser()
    if form.validate_on_submit():
        user,authenticated = User.authenticate(form.username.data,form.password.data)
        if user and authenticated:
            login_user(user,remember = form.remember_me.data)
            return redirect(request.args.get("next") or url_for('index'))
    return render_template("login.html",form=form)

@app.route('/profile/<int:user_id>')
def profile(user_id):
    user = User.query.get(user_id)
    return render_template('profile.html',user = user)

@app.route("/logout")
@login_required
def logout():
    logout_user()
    flash(("Logged out"),"success")
    return redirect(url_for('index'))

@app.route('/delete/<int:node_id>/post/<int:post_id>')
def deletePost(post_id):
    node = Node.query.get(node_id)
    node_title = node.title
    post = Post.query.get(post_id)
    topic_id = post.topic_id
    isNotBackToIndex = post.delete()
    if isNotBackToIndex:
        return redirect(url_for('listPosts',node_title=node_title,topic_id=topic_id))
    else:return redirect('/index')

@app.route('/edit/<int:node_id>/post/<int:post_id>',methods=('GET','POST'))
def editPost(post_id):
    form = EditPost()
    node = Node.query.get(post_id)
    node_title = node.title
    post = Post.query.get(post_id)
    topic_id = post.topic_id
    if form.validate_on_submit():
        form.save(post)
        return redirect(url_for('listPosts',node_title=node_title,topic_id = topic_id))
    else:
        form.content.data = post.content
    return render_template('edit_post.html',form=form)

@app.route('/admin')
@admin_required
def admin():
    posts = Post.query.all()
    topics = Topic.query.all()
    users = User.query.filter(User.id != 1).all()
    return render_template('admin.html',posts = posts,topics = topics,users = users)

@app.route('/delete/topic/<int:topic_id>')
@admin_required
def deleteTopic(topic_id):
    topic = Topic.query.get(topic_id)
    topic.delete()
    return redirect(url_for('admin'))

@app.route('/delete/user/<int:user_id>')
@admin_required
def delelteUser(user_id):
    user = User.query.get(user_id)
    user.delete()
    return redirect(url_for('admin'))

@app.route('/addNode',methods=('GET','POST'))
@admin_required
def addNode():
    form = AddNodeForm()
    if form.validate_on_submit():
        form.save()
        return redirect(url_for('index'))
    return render_template('addNode.html',form=form)

@manager.command
def init():
    dfile = 'database.db'
    if os.path.exists(dfile):
        os.remove(dfile)
    db.create_all()


if __name__ == "__main__":
    manager.run()
