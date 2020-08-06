from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import *
from config import *
import datetime

Base = declarative_base()


class Image(Base):
    __tablename__ = 'image'

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(String(25), nullable=false)
    image_name = Column(String(100))
    image_url = Column(String(100))
    thumb_url = Column(String(100))
    date = Column(DateTime, default=datetime.datetime.utcnow)


class Test(Base):
    __tablename__ = 'test'

    id = Column(Integer, primary_key=True, autoincrement=True)
    test = Column(Boolean, default=True)


Base.metadata.create_all(engine)
