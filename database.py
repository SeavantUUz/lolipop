from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Table,Column,Integer,String,MetaData
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session,sessionmaker

engine = create_engine('sqlite:///foo.db',convert_unicode=True)
db_session = scoped_session(sessionmaker(autocommit=False,
                                        autoflush=False,
                                        bind=engine))

Base = declarative_base()
Base.query = db_session.query_property()

class Filesystem(Base):
    __tablename__ = 'filesystem'

    path = Column(String,primary_key = True)
    name = Column(String)

    def __init__(self,path,name):
        self.path = path
        self.name = name

    def __repr__(self):
        return "<Metadata('%s','%s')>" % (self.path,self.name)

Base.metadata.create_all(bind=engine)
