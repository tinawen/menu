from sqlalchemy import (
    Column,
    Integer,
    Text,
    Date,
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

    def __init__(self, name, description, menu_id):
        self.name = name
        self.description = description
        self.menu_id = menu_id
        
class Menu(Base):
    __tablename__ = 'menus'
    id = Column(Integer, primary_key=True)
    name = Column(Text)
    date = Column(Date)
    time_sort_key = Column(Integer)
    menus = Column(Text)

    def __init__(self, name, date, time_sort_key, menus):
        self.name = name
        self.date = date
        self.time_sort_key = time_sort_key
        self.menus = menus

class Allergen(Base):
    __tablename__ = 'allergens'
    id = Column(Integer, primary_key=True)
    menu_item_id = Column(Integer)
    allergen = Column(Text)

    def __init__(self, menu_item_id, allergen):
        self.menu_item_id = menu_item_id
        self.allergen = allergen

    
