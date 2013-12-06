# coding:utf-8
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.login import LoginManager
from pygments import highlight
from pygments.lexers import get_lexer_by_name
from pygments.formatters import HtmlFormatter
from misaka import HtmlRenderer,SmartyPants
import misaka as m

db = SQLAlchemy()
login_manager = LoginManager()

def force_int(value,default=1):
    try:
        return int(value)
    except:
        return default

class BleepRenderer(HtmlRenderer,SmartyPants):
    ''' code highlight '''
    def block_code(self,text,lang):
        if not lang:
            return '\n<pre><code>%s</code></pre>\n' % \
                    h.escape_html(text.encode("utf8").strip())
        lexer = get_lexer_by_name(lang,stripall=True)
        formatter = HtmlFormatter()
        return highlight(text,lexer,formatter)

class MaxinObject(object):
    pass

from lolipop.models import User,Profile,Node
def fill_with_user(items):
    uids = set([item.user_id for item in items])
    users = User.query.filter(User.id.in_(uids)).all()
    profiles = Profile.query.filter(Profile.id.in_(uids)).all()
    items = fill_object(items,users,'username',attr='user_id')
    items = fill_object(items,profiles,'avatar',attr='user_id')
    return items

def fill_with_node(items):
    uids = set([item.node_id for item in items])
    nodes = Node.query.filter(Node.id.in_(uids)).all()
    return fill_object(items,nodes,'title',attr='node_id')

## you could pass a attr='xxx' in kwargs
## which to indicate which attr be seached
## in item
def fill_object(items,objects,*args,**kwargs):
    objects_dict = {}
    attr = kwargs.get('attr','id')
    for o in objects:
       objects_dict[o.id] = o
    for arg in args:
        items = map(lambda o:_add_attr(o,objects_dict,arg,attr),items)
    return items

def _add_attr(item,objects_dict,arg,attr):
    _object = objects_dict.get(getattr(item,attr))
    item.__setattr__(arg,getattr(_object,arg))
    return item

