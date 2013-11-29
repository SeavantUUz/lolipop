# coding:utf-8
from flask import Blueprint,request,render_template,flash
from views.account import admin_required
from config import force_int,fill_object
from kutoto.models import User,Profile
from kutoto.form import NodeForm

bp = Blueprint('admin',__name__)

@bp.route('/',methods=['GET','POST'])
@admin_required
def dashboard():
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
