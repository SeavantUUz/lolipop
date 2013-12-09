from flask import redirect,render_template,url_for,abort,request,Blueprint,current_app
from flask.ext.login import current_user
from config import force_int,fill_object,cache,get_online_users
from lolipop.models import User,Topic,Profile


bp = Blueprint("user",__name__)

@bp.route('/')
def users():
    uids = get_online_users()
    print uids
    page = force_int(request.args.get('page',1),0)
    if not page:
        return abort(404)
    paginator = User.query.filter(User.id.in_(uids)).order_by(User.id).paginate(page)
    profiles = Profile.query.filter(Profile.id.in_(uids)).order_by(Profile.id).paginate(page).items
    paginator.items = fill_object(paginator.items,profiles,'avatar','twitter')
    return render_template('user/users.html',paginator=paginator)

@bp.route('/<int:uid>')
def view(uid):
    user = User.query.filter_by(id=uid).first_or_404()
    profile = Profile.query.filter_by(id=uid).first_or_404()
    topics = Topic.query.filter_by(user_id=uid).order_by(Topic.id.desc()).limit(15)
    return render_template('user/view.html',user=user,profile=profile,topics=topics)
