import os
import sys
from sqlalchemy import Column, ForeignKey, Integer, String, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()

class Category(Base):
    __tablename__ = 'category'

    name = Column(String(50), nullable=False)
    id = Column(Integer, primary_key=True)

class Item(Base):
    __tablename__ = 'item'

    title = Column(String(80), nullable=False)
    desc = Column(String(500), nullable=False)
    id = Column(Integer, primary_key=True)
    cat_id = Column(Integer, ForeignKey(Category.id))
    category = relationship(Category)



engine = create_engine(
    'sqlite:///itemcatalog.db'
)

Base.metadata.create_all(engine)