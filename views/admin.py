from flask import Blueprint,request,render_template,flash
from views.account import admin_required
from config import force_int
from kutoto.models import User

bp = Blueprint('admin',__name__)

@bp.route('/',methods=['GET','POST'])
@admin_required
def dashboard():
    page = force_int(request.args.get('page', 1), 0)
    if not page:
        return abort(404)

    paginator = User.query.order_by(User.id.desc()).paginate(page)
    return render_template(
        'admin/dashboard.html',
        paginator=paginator,
    )
