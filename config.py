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

def fill_object(items,profiles,*args):
    profiles_dict = {}
    for profile in profiles:
        profiles_dict[profile.id] = profile
    for arg in args:
        items = map(lambda o:_add_attr(o,profiles_dict,arg),items)
    return items

def _add_attr(item,profiles_dict,arg):
    profile = profiles_dict.get(item.id)
    item.__setattr__(arg,getattr(profile,arg))
    return item
