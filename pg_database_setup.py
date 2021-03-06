import os
import sys
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine
import os
from urllib import parse

PG_URL = parse.urlparse(os.environ["DATABASE_URL"])

PG_DATABASE = PG_URL.path[1:]
PG_USER = PG_URL.username
PG_PASSWD = PG_URL.password
PG_HOST = PG_URL.hostname
PG_PORT = str(PG_URL.port)
PG_CONN = 'postgresql+psycopg2://'+PG_USER+':'+PG_PASSWD+'@'+PG_HOST+':'+PG_PORT+'/'+PG_DATABASE

Base = declarative_base()


class User(Base):
    __tablename__ = 'userinfo'

    id = Column(Integer, primary_key=True)
    name = Column(String(80), nullable=False)
    email = Column(String(250), nullable=False)
    picture = Column(String(250))


class Restaurant(Base):
    __tablename__ = 'restaurant'

    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)
    user_id = Column(Integer, ForeignKey('userinfo.id'))
    user = relationship(User)

    @property
    def serializeRestaurant(self):
        #returns object data in serialized format
        return {
            "name": self.name,
            "id":   self.id,
        }

class MenuItem(Base):
    __tablename__ = 'menu_item'

    name = Column(String(80), nullable=False)
    id = Column(Integer, primary_key=True)
    description = Column(String(250))
    price = Column(String(8))
    course = Column(String(250))
    restaurant_id = Column(Integer, ForeignKey('restaurant.id'))
    restaurant = relationship(Restaurant)
    user_id = Column(Integer, ForeignKey('userinfo.id'))
    user = relationship(User)

    @property
    def serialize(self):
        #returns object data in serialized format
        return {
            "name": self.name,
            "id":   self.id,
            "price": self.price,
            "description": self.description,
            "course": self.course,
        }

# engine = create_engine('sqlite:///restaurantmenu.db')
engine = create_engine(PG_CONN)

Base.metadata.create_all(engine)
