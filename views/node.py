from flask import redirect,render_template,url_for,flash,abort,request,Blueprint
from _helpers import force_int,cache,fill_with_user,fill_with_node
from lolipop.form import NodeForm,CreateForm
from lolipop.models import Node,Topic
from flask.ext.login import current_user
from views.account import admin_required

bp = Blueprint("node",__name__)

@bp.route('/')
def nodes():
    nodes = Node.query.order_by(Node.id.desc()).all()
    return render_template('node/nodes.html',nodes = nodes)

@bp.route('/<urlname>',methods=('GET','POST'))
@cache.cached(timeout=50)
def view(urlname):
   node = Node.query.filter_by(title=urlname).first_or_404() 
   page = force_int(request.args.get('page',1),0)
   if not page:
       return abort(404)
   paginator = Topic.query.filter_by(node_id=node.id).order_by(Topic.id.desc()).paginate(page,10)
   paginator.items = fill_with_node(fill_with_user(paginator.items))
   form = None
   if current_user is not None and current_user.is_authenticated():
       form = CreateForm()
   return render_template('node/view.html',form=form,node=node,paginator=paginator)

@bp.route('/create',methods=['GET','POST'])
@admin_required
def create():
    form = NodeForm()
    if form.validate_on_submit():
        node = form.save()
        cache.clear()
        return redirect(url_for('.view',urlname=node.title))
    return render_template('node/create.html',form=form,current_user = current_user)

@bp.route('/<urlname>/edit',methods=['GET','POST'])
@admin_required
def edit(urlname):
    node = Node.query.filter_by(title=urlname).first_or_404()
    form = NodeForm(obj=node)
    if form.validate_on_submit():
        form.populate_obj(node)
        node.save()
        cache.clear()
        return redirect(url_for('.view',urlname=node.title))
    return render_template('node/edit.html',form=form,node=node,current_user=current_user)
