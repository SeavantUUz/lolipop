from flask import redirect,render_template,url_for,flash,abort,Blueprint
from config import force_int
from kutoto.form import NodeForm

bp = Blueprint("node",__name__)

@bp.route('/'):
def nodes():
    nodes = Node.query.order_by(Node.id.desc()).all()
    return render_template('node/nodes.html',nodes = nodes)

@bp.route('/<urlname>')
def view():
   node = Node.query.filter_by(title=urlname).first_or_404() 
   page = force_int(request.args.get('page',1),0)
   if not page:
       return abort(404)
   paginator = Topic.query.order_by(Topic.id.desc()).paginate(page,7)
   return render_template('node/view.html',node=node,paginate=paginate)

@bp.route('/create',methods=['GET','POST'])
def create():
    form = NodeForm()
    if form.validate_on_submit():
        node = form.save()
        return redirect(url_for('.view',urlname=node.title))
    return render_template('node/create.html',form=form)

@bp.route('/<urlname>/edit',methods=['GET','POST'])
def edit(urlname):
    node = Node.query.filter_by(title=urlname).first_or_404()
    form = NodeForm(obj=node)
    if form.validate_on_submit():
        form.populate_obj(node)
        node.save()
        return redirect(url_for('.view',urlname=node.title))
    return render_template('node/edit.html',form=form,node=node)
