# coding:utf-8
from flask_wtf import Form
from wtforms import TextField,TextAreaField
from wtforms.validators import DataRequired
from kutoto.models import Post,Topic

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
