# coding: utf-8
from flask import Blueprint,render_template,redirect,abort,url_for,request
from flask.ext.login import current_user,login_required
from jinja2 import TemplateNotFound
from lolipop.models import Post,Topic,User,Node
from lolipop.form import ReplyForm,CreateForm
from config import force_int,fill_with_user,fill_with_node,cache
from views.account import admin_required

bp = Blueprint('topic',__name__)

#def fill_with_user(items):
#    uids = [1]
#    users = User.query.filter(User.id.in_([1])).all()
#    for i in users:
#        print i.username

@bp.route('/')
@cache.cached(timeout=50)
def topics():
    '''To list all topics'''
    page = force_int(request.args.get('page',1),0)
    if not page:
        return abort(404)
    paginator = Topic.query.order_by(Topic.date_created.desc()).paginate(page,15)
    paginator.items=fill_with_node(fill_with_user(paginator.items))
    return render_template('topic/topics.html',paginator=paginator,endpoint='topic.topics')

@bp.route('/latest')
@cache.cached(timeout=50)
def latest():
    '''list all topics by latest time'''
    page = force_int(request.args.get('page',1),0) 
    if not page:
        return abort(404)
    paginator = Topic.query.order_by(Topic.id.desc()).paginate(page,15)
    paginator.items=fill_with_node(fill_with_user(paginator.items))
    return render_template('topic/topics.html',paginator=paginator,endpoint='topic.latest')

@bp.route('/<int:uid>',methods=('GET','POST'))
@cache.cached(timeout=50)
def view(uid):
    page = force_int(request.args.get('page',1),0)
    if not page:
        return abort(404)
    paginator = Post.query.filter_by(topic_id=uid).paginate(page,15)
    paginator.items = fill_with_user(paginator.items)
    topic = Topic.query.get_or_404(uid)
    form = None
    if current_user is not None and current_user.is_authenticated():
        form = ReplyForm()
    return render_template('topic/view.html',form=form,topic=topic,paginator=paginator)
    
@bp.route('/create/<urlname>',methods=('GET','POST'))
@login_required
def create(urlname):
    node = Node.query.filter(Node.title == urlname).first_or_404()
    form = CreateForm()
    if form.validate_on_submit():
        form.save(node,current_user)
        return redirect(url_for('.topics'))
    return render_template('topic/create.html',form=form)

@bp.route('/<int:uid>/reply',methods=['GET','POST'])
def reply(uid):
    topic = Topic.query.get_or_404(uid)
    form = ReplyForm()
    if form.validate_on_submit():
        form.save(current_user,topic)
    else:
        flash(('Missing content'),'error')
    return redirect(url_for('.view',uid=uid))

@bp.route('/delete/<int:uid>')
@admin_required
def delete(uid):
    topic = Topic.query.get_or_404(uid)
    topic.delete()
    return redirect(url_for('.topics'))

