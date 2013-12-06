# coding:utf-8

from datetime import datetime
#from run import db
from werkzeug import generate_password_hash,check_password_hash
from config import db
from flask.ext.login import UserMixin

class Node(db.Model):
    __tablename__ = "nodes"
    id = db.Column(db.Integer,primary_key = True)
    title = db.Column(db.String(120),unique=True)
    description = db.Column(db.String)
    topics = db.relationship("Topic",backref="node",lazy="joined")
    
    @property
    def post_count(self):
        return Post.query.filter(Topic.node_id == self.id).filter(Post.topic_id == Topic.node_id).count()

    @property
    def topic_count(self):
        return Topic.query.filter(Topic.node_id == self.id).count()

    def save(self):
        db.session.add(self)
        db.session.commit()
        return self

    def delete(self):
        db.session.delete(self)
        db.session.commit()
        return self

class User(db.Model,UserMixin):
    '''User account'''
    __tablename__ = "users"
    id = db.Column(db.Integer,primary_key = True)
    email = db.Column(db.String(120),unique=True)
    username = db.Column(db.String(80),unique=True)
    _password = db.Column('password',db.String(80),nullable=False)
    date_joined = db.Column(db.DateTime,default=datetime.utcnow)
    #care_nodes = db.Column(db.String,nullable = True)
    posts = db.relationship("Post",backref="user",lazy="dynamic")
    topics = db.relationship("Topic",backref="user",lazy="dynamic")
    
    # synonym method replace a column by another name
    # descriptor is a parameter in sqlalchemy
    # property is python build-in method
    #def __init__(self):
        # It is a list which record all nodes you care

    #def add_care_node(self,node_id):
    #    self.care_nodes_list.append(node_id)
    #    self.save_care_nodes()

   # def remove_care_node(self,node_id):
   #     self.care_nodes_list.remove(node_id)
   #     self.save_care_nodes()

   # def get_care_nodes(self):
   #     return self.care_nodes_list

   # def save_care_nodes(self):
   #     self.care_nodes = ','.join(self.care_nodes_list)

    def _set_password(self,password):
        self._password = generate_password_hash(password)

    def _get_password(self):
        return self._password

    def get_name(self):
        return self.username


    password = db.synonym('_password',descriptor = property(_get_password,_set_password))

    def __repr__(self):
        return "%s" % self.username

    def __str__(self):
        return "%s" % self.username

    def check_password(self,password):
        if self.password is None:
            return False
        return check_password_hash(self.password,password)

    def get_all_posts(self):
        return Post.query.filter(Post.user_id == self.id)

    def get_all_topics(self):
        return Topic.query.filter(Topic.user_id == self.id)

    @classmethod
    def authenticate(cls,login,password):
        user = cls.query.filter(db.or_(User.username == login,User.email == login)).first()
        if user:
            authenticated = user.check_password(password)
        else:
            authenticated = False
        return user,authenticated

    def save(self):
        db.session.add(self)
        db.session.commit()
        return self

    def delete(self):
        db.session.delete(self)
        db.session.commit()
        return self

class Profile(db.Model):
    __tablename__ = "profiles"
    id = db.Column(db.Integer,primary_key=True)
    avatar = db.Column(db.String(200))
    website = db.Column(db.String(400),nullable=True)
    weibo = db.Column(db.String(100),nullable=True)
    twitter = db.Column(db.String(100),nullable=True)
    description = db.Column(db.Text)
    significant = db.Column(db.Text,nullable = True)
    rankPoint = db.Column(db.Integer,default = 0)
    
    @classmethod
    def get_or_create(cls,uid):
        item = cls.query.get(uid)
        if item:
            return item
        item = cls(id=uid)
        db.session.add(item)
        db.session.commit()
        return item

    def save(self):
        db.session.add(self)
        db.session.commit()
        return self

class Post(db.Model):
    __tablename__="posts"

    # when two tables reference each other,you alway should
    # use the properity use_alter
    # if set up ondelete properity when parent row change,
    # the children row will change too
    id = db.Column(db.Integer,primary_key = True)
    # foreignkey's first parameter is the table's column name
    topic_id = db.Column(db.Integer,db.ForeignKey("topics.id",use_alter = True,name="fk_topic_id",ondelete="CASCADE"))
    user_id =  db.Column(db.Integer,db.ForeignKey("users.id"))
    content = db.Column(db.Text)
    date_created = db.Column(db.DateTime,default=datetime.utcnow)
    dete_modified = db.Column(db.DateTime)

    def save(self,user=None,topic=None):
        #def save(self,topic=None):
        # edit the post

        if self.id:
            db.session.add(self)
            db.session.commit()
            return self

        # new post
        if user and topic:
        #if topic:
            self.user_id = user.id
            self.topic_id = topic.id
            self.date_created = datetime.utcnow()

            db.session.add(self)
            db.session.commit()

            topic.last_post_id = self.id
            
            #user.score += 1
            topic.post_count += 1
            
            db.session.add(topic)
            db.session.commit()
            return self

    def delete(self):
        if self.topic.first_post_id == self.id:
            self.topic.delete()
            return False
        if self.topic.last_post_id == self.id:
            self.topic.last_post_id = self.topic.second_last_post_id
            db.session.commit()

            # Here's self.user and self.topic
            # is the backref which define in
            # User class and Topic class
            
            #self.user.score -= 1
            self.topic.post_count -= 1
            
            db.session.delete(self)
            db.session.commit()
            return True

class Notice(db.Model):
    __tablename__ = 'notice'
    id = db.Column(db.Integer,primary_key = True)
    title = db.Column(db.String)
    content = db.Column(db.Text)
    date_create = db.Column(db.DateTime,default = datetime.utcnow)
    viewed = db.Column(db.Integer,default=0)

    def __str__(self):
        return self.title

    def save(self):
        db.session.add(self)
        db.session.commit()
        return self

    def delete(self):
        db.session.delete(self)
        db.session.commit()
        return self

class Topic(db.Model):
    __tablename__ = 'topics'
    id = db.Column(db.Integer,primary_key = True)
    title = db.Column(db.String)
    node_id = db.Column(db.Integer,db.ForeignKey("nodes.id",use_alter=True,name="fk_node_id"))
    user_id = db.Column(db.Integer,db.ForeignKey("users.id"))
    date_created = db.Column(db.DateTime,default=datetime.utcnow)
    viewed = db.Column(db.Integer,default = 0)
    post_count = db.Column(db.Integer,default = 0)

    # when two table reference each other and one-to-one
    # set uselist = False
    first_post_id = db.Column(db.Integer,db.ForeignKey("posts.id",ondelete="CASCADE"))
    first_post = db.relationship("Post",backref="first_post",foreign_keys=[first_post_id],uselist=False)

    last_post_id = db.Column(db.Integer,db.ForeignKey("posts.id",ondelete="CASCADE",onupdate="CASCADE"))
    last_post = db.relationship("Post",backref="last_post",foreign_keys=[last_post_id],uselist=False)

    posts = db.relationship("Post",backref="topic",lazy="joined",primaryjoin="Post.topic_id == Topic.id",cascade="all,delete-orphan",post_update=True)

    def __init__(self,title=None):
        if title:
            self.title = title

    def get_name(self):
        return self.title

    def __str__(self):
        return self.title

    def __repr__(self):
        return '<Topic:%s>' % self.id

    @property
    def second_last_post_id(self):
        return self.posts[-2].id

    def save(self,node=None,user=None,post=None):
        #def save(self,post=None):
        # edit title
        if self.id:
            db.session.add(self)
            db.session.commit()

        self.node_id = node.id
        self.user_id = user.id
        db.session.add(self)
        db.session.commit()

        post.save(user,self)
        self.first_post_id = post.id
        db.session.commit()
        return self

    def delete(self):
        #count = Post.query.filter(topic_id == self.id).filter(user_id == self.user_id).count()
        #self.user.score -= count
        db.session.delete(self)
        db.session.commit()
