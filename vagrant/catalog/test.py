from flask import Flask
from database_setup import Category, Item, Base

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


engine = create_engine('sqlite:///itemcatalog.db')
Base.metadata.bind = engine

app = Flask(__name__)

DBSession = sessionmaker()
DBSession.configure(bind=engine)
session = DBSession()

@app.route('/')
def testDb():
    testCat = Category(name = "Soccer")
    session.add(testCat)
    session.commit()
    rows = session.query(Category.name).count()
    return str(rows)



if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port=5000)