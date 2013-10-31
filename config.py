from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.login import LoginManager
from pygments import highlight
from pygments.lexers import get_lexer_by_name
from pygments.formatters import HtmlFormatter
from misaka import HtmlRenderer,SmartyPants

db = SQLAlchemy()
login_manager = LoginManager()

class BleepRenderer(HtmlRenderer,SmartyPants):
    ''' code highlight '''
    def block_code(self,text,lang):
        if not lang:
            return '\n<pre><code>%s</code></pre>\n' % \
                    h.escape_html(text.encode("utf8").strip())
        lexer = get_lexer_by_name(lang,stripall=True)
        formatter = HtmlFormatter()
        return highlight(text,lexer,formatter)

