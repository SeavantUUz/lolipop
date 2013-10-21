# coding:utf-8
from flask_wtf import Form
from wtforms import TextField,TextAreaField,PasswordField,BooleanField
from wtforms.validators import DataRequired,Required,EqualTo
from kutoto.models import Post,Topic,User
from datetime import datetime

class NewTopic(Form):
    subject = TextField(u'标题',validators=[DataRequired(message=u'标题')])
    content = TextAreaField(u'内容',validators=[DataRequired(u'内容')])
    def save(self):
        topic = Topic(title = self.subject.data)
        post = Post(content = self.content.data)
        return topic.save(post = post)

class ReplyPost(Form):
    content = TextAreaField(u'内容',validators=[DataRequired(u'内容')])
    def save(self,topic):
        post = Post(content = self.content.data)
        return post.save(topic = topic)

class EditPost(Form):
    content = TextAreaField(u'内容',validators=[DataRequired(u'内容')])
    def save(self,post):
        post.content = self.content.data
        return post.save()

class RegisterUser(Form):
    username = TextField(u"用户名",validators=[Required(message=u"填写用户名")])
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
        user = User(username=self.username.data,
                email=self.email.data,
                password=self.password.data,
                date_joined = datetime.utcnow(),
                )
        return user.save()

class LoginUser(Form):
    username = TextField(u"用户名",validators=[Required(message=u"填写用户名")])
    password = PasswordField(u'密码',validators = [Required(message=u"填写密码")])
    remember_me = BooleanField(u'记住我',default = False)
