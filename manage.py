import os
from flask.ext.script import Manager,Server
from config import db,login_manager
from app import create_app
from kutoto.form import NewTopic,ReplyPost,EditPost
from kutoto.models import Post,Topic,User
from flask import redirect,render_template,url_for

app = create_app()
login_manager.init_app(app)
manager = Manager(app)
manager.add_command("runserver",Server("localhost",port=8000))

@login_manager.user_loader
def load_user(userid):
    return User.get(userid)

@app.route("/")
@app.route("/index")
def index():
    topics = Topic.query.order_by(Topic.last_post_id.desc())
    return render_template('index.html',topics=topics)

@app.route("/new_topic",methods=('GET','POST'))
def new_topic():
    form  = NewTopic()
    if form.validate_on_submit():
        form.save()
        return redirect('/index')
    return render_template('form.html',form=form)

@app.route("/topic/<int:topic_id>",methods=('GET','POST'))
def show_topic(topic_id):
    form = ReplyPost()
    posts = Post.query.filter_by(topic_id=topic_id).order_by(Post.date_created)
    topic = Topic.query.get(topic_id)
    if form.validate_on_submit():
        form.save(topic)
        return redirect(url_for('show_topic',topic_id=topic_id))
        #return redirect('/index')
    return render_template('posts.html',posts=posts,form=form)

@app.route('/delete/topic/<int:topic_id>')
def delete_topic(topic_id):
    topic = Topic.query.get(topic_id)
    topic.delete()
    return redirect('/index')

@app.route('/delete/post/<int:post_id>')
def delete_post(post_id):
    post = Post.query.get(post_id)
    topic_id = post.topic_id
    backWhere = post.delete()
    if backWhere:
        return redirect(url_for('show_topic',topic_id=topic_id))
    else:return redirect('/index')

@app.route('/edit/post/<int:post_id>',methods=('GET','POST'))
def edit_post(post_id):
    form = EditPost()
    post = Post.query.get(post_id)
    topic_id = post.topic_id
    if form.validate_on_submit():
        form.save(post)
        #form.populate_obj(post)
        #post.save()
        return redirect(url_for('show_topic',topic_id = topic_id))
    else:
        form.content.data = post.content
    return render_template('edit_post.html',form=form)

@manager.command
def init():
    dfile = 'database.db'
    if os.path.exists(dfile):
        os.remove(dfile)
    db.create_all()

if __name__ == "__main__":
    manager.run()
