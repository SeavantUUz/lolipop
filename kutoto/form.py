# coding:utf-8
from flask_wtf import Form
from wtforms import TextField,TextAreaField,PasswordField,BooleanField
from wtforms.validators import DataRequired,Required,EqualTo
from kutoto.models import Post,Topic,User,Node,Profile,Notice
from datetime import datetime

class CreateForm(Form):
    subject = TextField(u'标题',validators=[DataRequired(message=u'标题')],description=u'这里填写标题哦')
    content = TextAreaField(u'内容',validators=[DataRequired(u'内容')],description=u'这里填写内容的说')

    def save(self,node,user):
        topic = Topic(title = self.subject.data)
        post = Post(content = self.content.data)
        return topic.save(node=node,user = user,post = post)

class NoticeForm(Form):
    subject = TextField(u'标题',validators=[DataRequired(message=u'标题')],description=u'这里填写标题哦')
    content = TextAreaField(u'内容',validators=[DataRequired(u'内容')],description=u'这里填写内容的说')

    def save(self):
        notice = Notice(title = self.subject.data,content = self.content.data)
        return notice.save()

class ReplyForm(Form):
    content = TextAreaField(u'内容',validators=[DataRequired(u'内容')])
    def save(self,user,topic):
        post = Post(content = self.content.data)
        return post.save(user = user,topic = topic)

class EditPost(Form):
    content = TextAreaField(u'内容',validators=[DataRequired(u'内容')])
    def save(self,post):
        post.content = self.content.data
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
                description = self.description.data,
                )
        return node.save()

class ProfileForm(Form):
    username = TextField(u'昵称',description = u'您的昵称')
    email = TextField(u'email',description = u'您的电子邮箱地址')
    avatar = TextField(u'头像',description = u'请告知我您头像的外链地址?')
    website = TextField(u'website',description=u'您的私人网站(博客)?')
    weibo = TextField(u'新浪微博',description = u'您的新浪微博用户名?')
    twitter = TextField(u'twitter',description = u'您的twitter号?不需要@')
    description = TextAreaField(u'简介',description = u'附上您的简介么?')
    significant = TextAreaField(u'签名',description = u'您的签名？支持markdown')

    def save(self,user):
        profile = Profile(id=user.id,
                avatar = self.avatar.data,
                website = self.website.data,
                weibo = self.weibo.data,
                twitter = self.twitter.data,
                description = self.description.data,
                significant = self.significant.data)
        return profile.save()
