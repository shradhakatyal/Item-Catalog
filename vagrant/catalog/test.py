from flask import Flask
from database_setup import Category, Item, Base

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


engine = create_engine('sqlite:///itemcatalog.db')
Base.metadata.bind = engine

app = Flask(__name__)

DBSession = sessionmaker(bind=engine)
session = DBSession()
testCat = Category(name="Soccer")
session.add(testCat)
session.commit()

@app.route('/')
@app.route('/home')
def testDb():
    rows = session.query(Category)
    str = ""
    for row in rows:
        print (row.name)
        str += row.name + " "

    return str



if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port=5000)