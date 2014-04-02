from sqlalchemy import (
    Column,
    Integer,
    Text,
    Date,
    Boolean,
    )

from sqlalchemy.ext.declarative import declarative_base

from sqlalchemy.orm import (
    scoped_session,
    sessionmaker,
    )

from zope.sqlalchemy import ZopeTransactionExtension

DBSession = scoped_session(sessionmaker(extension=ZopeTransactionExtension()))
Base = declarative_base()

class MenuItem(Base):
    __tablename__ = 'menu_items'
    id = Column(Integer, primary_key=True)
    name = Column(Text)
    description = Column(Text)
    menu_id = Column(Integer)
    healthy = Column(Integer)

    def __init__(self, name, description, menu_id, healthy):
        self.name = name
        self.description = description
        self.menu_id = menu_id
        self.healthy = healthy

class Menu(Base):
    __tablename__ = 'menus'
    id = Column(Integer, primary_key=True)
    cafe_id = Column(Integer)
    name = Column(Text)
    date = Column(Date)
    time_sort_key = Column(Integer)
    menus = Column(Text)
    sent = Column(Boolean)
    images_id = Column(Text)

    def __init__(self, cafe_id, name, date, time_sort_key, menus, sent, images_id=None):
        self.cafe_id = cafe_id
        self.name = name
        self.date = date
        self.time_sort_key = time_sort_key
        self.menus = menus
        self.sent = sent
        self.images_id = images_id

    @staticmethod
    def get_by_date_time(cafe_id, date, time_sort_key):
        filters = [
            Menu.cafe_id == cafe_id,
            Menu.date == date,
            Menu.time_sort_key == time_sort_key,
            ]
        return DBSession.query(Menu).filter(*filters).first()

class Allergen(Base):
    __tablename__ = 'allergens'
    id = Column(Integer, primary_key=True)
    menu_item_id = Column(Integer)
    allergen = Column(Text)

    def __init__(self, menu_item_id, allergen):
        self.menu_item_id = menu_item_id
        self.allergen = allergen

class Image(Base):
    __tablename__ = 'images'
    id = Column(Integer, primary_key=True)
    image_url = Column(Text)
    thumb_url = Column(Text)

    def __init__(self, image_url, thumb_url):
        self.image_url = image_url
        self.thumb_url = thumb_url

class Cafe(Base):
    __tablename__ = 'cafes'
    id = Column(Integer, primary_key=True)
    name = Column(Text)
    
    def __init__(self, name):
        self.name = name
