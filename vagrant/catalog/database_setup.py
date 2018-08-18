import os
import sys
from sqlalchemy import Column, ForeignKey, Integer, String, create_engine, Boolean, Text, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
import datetime

Base = declarative_base()


class User(Base):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True)
    email = Column(String(100), unique=True, nullable=False)
    name = Column(String(100), nullable=True)
    avatar = Column(String(200))
    active = Column(Boolean, default=False)
    tokens = Column(Text)
    created_at = Column(DateTime, default=datetime.datetime.utcnow())


class Category(Base):
    __tablename__ = 'category'

    name = Column(String(50), nullable=False)
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey(User.id))
    user = relationship(User)

    
class Item(Base):
    __tablename__ = 'item'

    title = Column(String(80), nullable=False)
    desc = Column(String(500), nullable=False)
    id = Column(Integer, primary_key=True)
    cat_id = Column(Integer, ForeignKey(Category.id))
    category = relationship(Category)
    user_id = Column(Integer, ForeignKey(User.id))
    user = relationship(User)

    
engine = create_engine(
    'sqlite:///itemcatalog.db'
)

Base.metadata.create_all(engine)