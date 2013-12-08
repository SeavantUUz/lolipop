# coding:utf-8
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.login import LoginManager
from flask.ext.cache import Cache
from pygments import highlight
from pygments.lexers import get_lexer_by_name
from pygments.formatters import HtmlFormatter
from misaka import HtmlRenderer,SmartyPants
import misaka as m

db = SQLAlchemy()
cache = Cache()
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
    items = fill_object(items,users,'username',name='user_id')
    items = fill_object(items,profiles,'avatar',name='user_id')
    return items

def fill_with_node(items):
    uids = set([item.node_id for item in items])
    nodes = Node.query.filter(Node.id.in_(uids)).all()
    return fill_object(items,nodes,'title',name='node_id',rename='node_title')

## you could pass a attr='xxx' in kwargs
## which to indicate which attr be seached
## in item
def fill_object(items,objects,*args,**kwargs):
    objects_dict = {}
    for o in objects:
       objects_dict[o.id] = o
    for arg in args:
        items = map(lambda o:_add_attr(o,objects_dict,arg,kwargs),items)
    return items

# to solve rename,I import a ugly method.
def _add_attr(item,objects_dict,arg,kwargs):
    # use the attr of item's name to get special object
    name = kwargs.get('name','id')
    # attributeName is the name from the special object
    attributeName = arg
    _object = objects_dict.get(getattr(item,name))
    # if the unique key has emerged in item.__dict__
    # modify the unique key to an other string
    if arg in item.__dict__.keys():
        arg = kwargs['rename']
    item.__setattr__(arg,getattr(_object,attributeName))
    return item

