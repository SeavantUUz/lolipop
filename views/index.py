from flask import Blueprint,render_template
from lolipop.models import Notice,Topic
from _helpers import fill_with_user,fill_with_node,cache

bp = Blueprint('index',__name__)

@bp.route("/")
@bp.route("/index")
@cache.cached(timeout=1000)
def index():
    notices = Notice.query.order_by(Notice.id.desc())
    topics = Topic.query.order_by(Topic.last_post_id.desc()).limit(15)
    topics = fill_with_node(fill_with_user(topics))
    return render_template('index.html',topics=topics,notices=notices)
    #return 'hello world'
