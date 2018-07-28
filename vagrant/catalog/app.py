from flask import Flask, render_template, request, redirect, url_for
from sqlalchemy import create_engine, and_
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Category, Item

app = Flask(__name__)

engine = create_engine('sqlite:///itemcatalog.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()

#App routes

@app.route('/')
@app.route('/catalog')
def getAllCategories():
    categories = session.query(Category)
    latest_items = session.query(Item).order_by(Item.id.desc()).limit(5)
    return render_template('catalog.html', categories=categories, items=latest_items)

#To display all items in a catgeory
@app.route('/catalog/<string:cat_name>/items')
def getItemsFromCategory(cat_name):
    categories = session.query(Category)
    q = session.query(Category).filter_by(name=cat_name.title()).one()
    cat_id = q.id
    items = session.query(Item).filter_by(cat_id=cat_id).all()
    return render_template('items.html', categories=categories, items=items)

#To display information about a single item
# @app.route('/catalog/<string:cat_name>/<string:item_title>')
# def getItemDetails(cat_name, item_title):
#     q = session.query(Category).filter_by(name=cat_name.title()).one()
#     cat_id = q.id
#     item = session.query(Item).filter_by(title = "Snowboard")
    # print(item_title.title())
    # return render_template('itemdetail.html', item=item)

if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port=5000)
