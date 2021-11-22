from sqlalchemy.orm import *
from sqlalchemy import *

Base = declarative_base()


# khoi tao ket noi vao co so du lieu
def connect_to_db():
    engine_ = create_engine('mysql+mysqldb://root:pass@localhost/real-estate-trading?charset=utf8mb4')
    session_ = sessionmaker(bind=engine_)
    return session_


class Post(Base):
    __tablename__ = 'post'
    post_id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, primary_key=True)
    title = Column(String)
    address = Column(String)
    price = Column(Float)
    acreage = Column(String)
    investor = Column(String)
    bedroom = Column(Integer)
    toilet = Column(Integer)
    latitude = Column(Float)
    longitude = Column(Float)
    distance = Column(Float)
    time_upload = Column(DateTime)
    time_priority = Column(DateTime)
    sold = Column(Boolean)
    description = Column(String)


class Image(Base):
    __tablename__ = 'image'
    image_id = Column(Integer, primary_key=True, autoincrement=True)
    post_id = Column(Integer, ForeignKey('post.post_id'))
    image_url = Column(String)
