# coding: utf-8

from flask import Blueprint
from flask import render_template,redirect,abort,url_for,request
from jinja2 import TemplateNotFound
from kutoto.models import Post,Topic,User,Node
from config import force_int
from flask.ext.login import current_user

bp = Blueprint('topic',__name__)

@bp.route('/')
def topics():
    '''To list all topics'''
    page = force_int(request.args.get('page',1),0)
    if not page:
        return abort(404)
    paginator = Topic.query.order_by(Topic.date_created.desc()).paginate(page,7)
    return render_template('topic/topics.html',paginator=paginator,endpoint='topic.topics')

@bp.route('/latest')
def latest():
    '''list all topics by latest time'''
    page = force_int(reqeust.args.get('page',1),0) 
    if not page:
        return abort(404)
    paginator = Topic.query.order_by(Topic.id.desc()).paginate(page,7)
    return render_template('topic/topics.html',paginator=paginator,endpoint='topic.latest')

@bp.route('/<int:uid>',methods=('GET','POST'))
def view(uid):
    page = force_int(request.args.get('page',1),0)
    if not page:
        return abort(404)
    paginator = Post.query.filter_by(topic_id=uid).paginator(page,7)
    form = None
    if current_user is not None and current_user.is_authenticated():
        form = ReplyForm()
    if form.validate_on_submit():
        form.save(current_user,topic)
        redirect(url_for('.view',uid=uid)
    return render_template('topic/view.html',form=form,paginator=paginator)
    
@bp.route('/create/<int:nodename>',methods=('GET','POST'))
def create(nodename):
    node = Node.query.filter(NOde.title == nodename).first_or_404()
    form = NewTopic()
    if form.validate_on_submit():
        form.save(node,current_user)
        return redirect(url_for('.topics'))
    return render_template('topic/create.html',form=form)

@bp.route('/delete/<int:uid>')
def delete(uid):
    topic = Topic.query.get_or_404(uid)
    topic.delete()
    return redirect(url_for('.topics'))

