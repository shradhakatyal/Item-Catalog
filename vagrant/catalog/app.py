from database_setup import Base, Category, Item
from flask import Flask, render_template, request, redirect, jsonify, url_for, flash
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from oauth2client.client import flow_from_clientsecrets
from oauth2client.client import FlowExchangeError
import httplib2
import json
from flask import make_response
import requests
import random
import string
from flask import session as login_session

app = Flask(__name__)


CLIENT_ID = json.loads(
    open('client_secrets.json', 'r').read())['web']['client_id']
APPLICATION_NAME = "Item Catalog"


engine = create_engine('sqlite:///itemcatalog.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()


# Create anti-forgery state token
@app.route('/login')
def showLogin():
    state = ''.join(random.choice(string.ascii_uppercase + string.digits)
                    for x in xrange(32))
    login_session['state'] = state
    return render_template('login.html', STATE=state)


@app.route('/gconnect', methods=['POST'])
def gconnect():
    # Validate state token
    if request.args.get('state') != login_session['state']:
        response = make_response(json.dumps('Invalid state parameter.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    # Obtain authorization code
    code = request.data

    try:
        # Upgrade the authorization code into a credentials object
        oauth_flow = flow_from_clientsecrets('client_secrets.json', scope='')
        oauth_flow.redirect_uri = 'postmessage'
        credentials = oauth_flow.step2_exchange(code)
    except FlowExchangeError:
        response = make_response(
            json.dumps('Failed to upgrade the authorization code.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Check that the access token is valid.
    access_token = credentials.access_token
    url = ('https://www.googleapis.com/oauth2/v1/tokeninfo?access_token=%s'
           % access_token)
    h = httplib2.Http()
    result = json.loads(h.request(url, 'GET')[1])
    # If there was an error in the access token info, abort.
    if result.get('error') is not None:
        response = make_response(json.dumps(result.get('error')), 500)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Verify that the access token is used for the intended user.
    gplus_id = credentials.id_token['sub']
    if result['user_id'] != gplus_id:
        response = make_response(
            json.dumps("Token's user ID doesn't match given user ID."), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Verify that the access token is valid for this app.
    if result['issued_to'] != CLIENT_ID:
        response = make_response(
            json.dumps("Token's client ID does not match app's."), 401)
        print "Token's client ID does not match app's."
        response.headers['Content-Type'] = 'application/json'
        return response

    stored_access_token = login_session.get('access_token')
    stored_gplus_id = login_session.get('gplus_id')
    if stored_access_token is not None and gplus_id == stored_gplus_id:
        response = make_response(json.dumps('Current user is already connected.'),
                                 200)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Store the access token in the session for later use.
    login_session['access_token'] = credentials.access_token
    login_session['gplus_id'] = gplus_id

    # Get user info
    userinfo_url = "https://www.googleapis.com/oauth2/v1/userinfo"
    params = {'access_token': credentials.access_token, 'alt': 'json'}
    answer = requests.get(userinfo_url, params=params)

    data = answer.json()

    login_session['username'] = data['name']
    login_session['picture'] = data['picture']
    login_session['email'] = data['email']

    user_id = getUserID(login_session['email'])
    if not user_id:
        user_id = createUser(login_session)
    login_session['user_id'] = user_id

    output = ''
    output += '<h1>Welcome, '
    output += login_session['username']
    output += '!</h1>'
    output += '<img src="'
    output += login_session['picture']
    output += ' " style = "width: 300px; height: 300px;border-radius: 150px;-webkit-border-radius: 150px;-moz-border-radius: 150px;"> '
    flash("you are now logged in as %s" % login_session['username'])
    print "done!"
    return output


# User Helper Functions
def createUser(login_session):
    newUser = User(name=login_session['username'], email=login_session[
                   'email'], picture=login_session['picture'])
    session.add(newUser)
    session.commit()
    user = session.query(User).filter_by(email=login_session['email']).one()
    return user.id


def getUserInfo(user_id):
    user = session.query(User).filter_by(id=user_id).one()
    return user


def getUserID(email):
    try:
        user = session.query(User).filter_by(email=email).one()
        return user.id
    except:
        return None


# App routes
@app.route('/')
@app.route('/catalog')
def getAllCategories():
    categories = session.query(Category)
    latest_items = session.query(Item).order_by(Item.id.desc()).limit(5)
    if 'username' in login_session:
        return render_template('privateCatalog.html', categories=categories, items=latest_items)
    return render_template('catalog.html', categories=categories, items=latest_items)


# To display all items in a catgeory
@app.route('/catalog/<string:cat_name>/items')
def getItemsFromCategory(cat_name):
    categories = session.query(Category)
    q = session.query(Category).filter_by(name=cat_name.title()).one()
    cat_id = q.id
    items = session.query(Item).filter_by(cat_id=cat_id).all()
    if 'username' in login_session:
        return render_template('privateItems.html', categories=categories, items=items)
    return render_template('items.html', categories=categories, items=items)


# To display information about a single item
@app.route('/catalog/<string:cat_name>/<string:item_title>')
def getItemDetails(cat_name, item_title):
    # item = session.query(Item).join(Category).filter(Item.title == item_title.title())
    # .filter(Category.name == cat_name.title()).one()
    q = session.query(Category).filter_by(name=cat_name).one()
    cat_id = q.id
    item = session.query(Item).filter_by(cat_id=cat_id).filter_by(title=item_title.title()).one()
    if 'username' in login_session:
        return render_template('privateItemDetail.html', item=item)
    return render_template('itemdetail.html', item=item)

@app.route('/catalog/<string:cat_name>/<string:item_title>/edit', methods=['GET', 'POST'])
def editItem(cat_name, item_title):
    editedItem = session.query(Item).filter_by(title=item_title).one()
    if request.method == 'POST':
        editedItem.name = request.form['title']
        editedItem.desc = request.form['desc']
        cat_id = session.query(Category).filter_by(name=request.form['cat_name']).one().id
        editedItem.cat_id = cat_id
        session.add(editedItem)
        session.commit()
        return redirect(url_for('getItemsFromCategory', cat_name=cat_name))
    else:
        item_desc = session.query(Item).filter_by(title=item_title).one().desc
        return render_template('edititem.html',cat_name=cat_name, item_title=item_title, item_desc=item_desc)


@app.route('/catalog/<string:cat_name>/<string:item_title>/delete', methods=['GET', 'POST'])
def deleteItem(cat_name, item_title):
    deletedItem = session.query(Item).filter_by(title=item_title).one()
    if request.method == 'POST':
        session.delete(deletedItem)
        session.commit()
        return redirect(url_for('getItemsFromCategory', cat_name=cat_name))
    else:
        return render_template('deleteitem.html',cat_name=cat_name, item_title=item_title)

@app.route('/catalog/add', methods=['GET', 'POST'])
def addNewItem():
    if request.method == 'POST':
        if(session.query(Category).filter_by(name=request.form['cat_name']).scalar() is not None):
            cat_id = session.query(Category).filter_by(name=request.form['cat_name']).one().id
            newItem = Item(title=request.form['title'], desc=request.form['desc'], cat_id=cat_id)
        else:
            newCat = Category(name=request.form['cat_name'])
            session.add(newCat)
            cat_id = session.query(Category).filter_by(name=newCat.name).one().id
            newItem = Item(title=request.form['title'], desc=request.form['desc'], cat_id=cat_id)
        
        session.add(newItem)
        session.commit()
        return redirect(url_for('getAllCategories'))
    else:
        return render_template('additem.html')
    

if __name__ == '__main__':
    app.secret_key = 'super_secret_key'
    app.debug = True
    app.run(host='0.0.0.0', port=5000)
