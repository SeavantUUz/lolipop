# coding:utf-8
from flask import Blueprint,request,render_template,flash,current_app,redirect,url_for
from views.account import admin_required
from config import force_int,fill_object
from kutoto.models import User,Profile
from kutoto.form import NodeForm
import codecs,os

bp = Blueprint('admin',__name__)

@bp.route('/',methods=['GET','POST'])
@admin_required
def dashboard():
    if request.method == 'POST':
        save_sidebar_notice(request.form.get('content',None))
        return redirect(url_for('.dashboard'))
    page = force_int(request.args.get('page', 1), 0)
    if not page:
        return abort(404)
    form = NodeForm()
    paginator = User.query.order_by(User.id.desc()).paginate(page)
    profiles = Profile.query.order_by(Profile.id).paginate(page).items
    paginator.itmes = fill_object(paginator.items,profiles,'avatar')

    return render_template(
        'admin/dashboard.html',
        paginator=paginator,
        form = form,
    )

def save_sidebar_notice(content):
    with codecs.open(os.path.join(current_app.config['ROOTDIR'],'announcement'),'w','utf-8','strict') as f:
        f.write(content)

def load_sidebar_notice():
    with codecs.open(os.path.join(current_app.config['ROOTDIR'],'announcement'),'r','utf-8','strict') as f: 
        content = f.read()
        return content

