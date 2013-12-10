from flask import Blueprint,redirect,url_for,abort
from flask.ext.login import current_user,login_required
from lolipop.models import Node
from config import redis

bp = Blueprint("focus",__name__)

@login_required
def nodes_id():
    if current_user is not None and current_user.is_authenticated():
        user_key = 'user-nodes/%d' % current_user.id
        return redis.smembers(user_key)

@login_required
def getNodes():
    uids = nodes_id()
    nodes = Node.query.filter(Node.id.in_(uids))
    return nodes

@bp.route('/add/<int:node_id>')
@login_required
def add(node_id):
    if current_user is not None and current_user.is_authenticated():
        user_key = 'user-nodes/%d' % current_user.id
        p = redis.pipeline()
        p.sadd(user_key,node_id)
        p.execute()
    return redirect(url_for('node.nodes'))

@bp.route('/remove/<int:node_id>')
@login_required
def remove(node_id):
    if current_user is not None and current_user.is_autheneticated():
        user_key = 'user-nodes/%d' % current_user.id
        p = redis.pipeline()
        p.srem(user_key,node_id)
        p.execute()
    return redirect(url_for('node.nodes'))

