# coding:utf-8
from flask_wtf import Form
from wtforms import TextField,TextAreaField,PasswordField,BooleanField
from wtforms.validators import DataRequired,Required,EqualTo
from kutoto.models import Post,Topic,User,Node
from datetime import datetime
import misaka as m
from config import BleepRenderer
from jinja2 import Markup

def _renderToGFM(data):
    renderer = BleepRenderer()
    md = m.Markdown(renderer,
            extensions=m.EXT_FENCED_CODE | m.EXT_NO_INTRA_EMPHASIS)
    return md.render(data)

class CreateForm(Form):
    subject = TextField(u'标题',validators=[DataRequired(message=u'标题')],description=u'这里填写标题哦')
    content = TextAreaField(u'内容',validators=[DataRequired(u'内容')],description=u'这里填写内容的说')

    def save(self,node,user):
        topic = Topic(title = self.subject.data)
        post = Post(content = _renderToGFM(self.content.data))
        return topic.save(node=node,user = user,post = post)

class ReplyForm(Form):
    content = TextAreaField(u'内容',validators=[DataRequired(u'内容')])
    def save(self,user,topic):
        post = Post(content = _renderToGFM(self.content.data))
        return post.save(user = user,topic = topic)

class EditPost(Form):
    content = TextAreaField(u'内容',validators=[DataRequired(u'内容')])
    def save(self,post):
        post.content = _renderToGFM(self.content.data)
        return post.save()

class RegisterForm(Form):
    account = TextField(u"用户名",validators=[Required(message=u"填写用户名")])
    email = TextField(u"电子邮箱",validators = [Required(message=u"填写电子邮箱")])
    password = PasswordField(u'密码',validators = [Required(message=u"填写密码")])
    confirm_password = PasswordField(u'重新输入密码',validators = [Required(message=u"重新输入密码"),EqualTo("password",message=u'密码不匹配')])

    def validate_username(self,field):
        user = User.query.filter_by(username=field.data).first()
        if user:
            raise ValidationError("This username is token")

    def validate_email(self,field):
        email = User.query.filter_by(email = field.data).first()
        if email:
            raise ValidationError("This email is token")

    def save(self):
        user = User(username=self.account.data,
                email=self.email.data,
                password=self.password.data,
                date_joined = datetime.utcnow(),
                )
        return user.save()

class LoginForm(Form):
    account = TextField(u"用户名",validators=[Required(message=u"填写用户名")])
    password = PasswordField(u'密码',validators = [Required(message=u"填写密码")])
    remember_me = BooleanField(u'记住我',default = False)

class NodeForm(Form):
    title = TextField(u'Node Name',validators = [Required(message=u'填写Node的名字')])
    description = TextAreaField(u'Node 描述',validators = [Required(message=u'请填写描述')])
    
    def save(self):
        node = Node(title=self.title.data,
                description = _renderToGFM(self.description.data),
                )
        return node.save()
