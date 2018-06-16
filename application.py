import random
import string
import httplib2
import requests
import json
from db_setup import Users, Base, Category, BookDetails
from flask import session as login_session
from oauth2client.client import flow_from_clientsecrets
from oauth2client.client import FlowExchangeError
from oauth2client.client import GoogleCredentials
from flask import Flask, render_template, request
from flask import redirect,  url_for, jsonify, flash, make_response
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

app = Flask(__name__)

CLIENT_ID = json.loads(
    open('client_secrets.json', 'r').read())['web']['client_id']
APPLICATION_NAME = "BookShelf"

engine = create_engine('sqlite:///bookstore.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()


@app.route('/login/')
def showLogin():
    state = ''.join(random.choice(string.ascii_uppercase+string.digits)
                    for x in xrange(32))
    login_session['state'] = state
    return render_template('loginpage.html', STATE=state)


@app.route('/gconnect', methods=['POST', 'GET'])
def gconnect():
    if request.args.get('state') != login_session['state']:
        response = make_response(json.dumps('Invalid State Parameter'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    code = request.data
    try:
        oauth_flow = flow_from_clientsecrets('client_secrets.json', scope='')
        oauth_flow.redirect_uri = 'postmessage'
        credentials = oauth_flow.step2_exchange(code)
    except FlowExchangeError:
        response = make_response(json.dumps('Failed to upgrade auth code'),
                                 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    # is access_token valid
    access_token = credentials.access_token
    url = ('https://www.googleapis.com/oauth2/v1/tokeninfo?access_token=%s'
           % access_token)
    h = httplib2.Http()
    # result of request are stored
    result = json.loads(h.request(url, 'GET')[1])
    # the message is sent to server if any result contains any errors
    if result.get('error') is not None:
        response = make_response(json.dumps(result.get('error')), 500)
        response.headers['Content-Type'] = 'application/json'
    # checking the right access_token
    gplus_id = credentials.id_token['sub']
    if result['user_id'] != gplus_id:
        response = make_response(json.dumps('Users ids do not match'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    # the token was issued for this app
    if result['issued_to'] != CLIENT_ID:
        response = make_response(json.dumps('Token id does not match app id'),
                                 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    # it is checking the user is  already logged in not to reset all info
    stored_access_token = login_session.get('access_token')
    stored_gplus_id = login_session.get('gplus_id')
    if stored_access_token is not None and gplus_id == stored_gplus_id:
        response = make_response(json.dumps('User is already connected'), 200)
        response.headers['Content-Type'] = 'application/json'
        return response
    login_session['access_token'] = credentials.access_token
    login_session['gplus_id'] = gplus_id
    # user info
    userinfo_url = "https://www.googleapis.com/oauth2/v1/userinfo"
    params = {'access_token': credentials.access_token, 'alt': 'json'}
    answer = requests.get(userinfo_url, params=params)
    data = answer.json()
    login_session['username'] = data['name']
    login_session['picture'] = data['picture']
    login_session['email'] = data['email']
    login_session['provider'] = 'google'
    user_id = getUserID(data['email'])
    if not user_id:
        user_id = createUser(login_session)
    login_session['user_id'] = user_id
    output = ''
    output += '<h1>Welcome, '
    output += login_session['username']
    output += '</h1>'
    return output


@app.route('/gdisconnect/')
def gdisconnect():
    access_token = login_session.get('access_token')
    print access_token
    if access_token is None:
        response = make_response(json.dumps('User is not connected'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    url = 'https://accounts.google.com/o/oauth2/revoke?token=%s' % access_token
    h = httplib2.Http()
    result = h.request(url, 'GET')[0]
    print result
    if result['status'] == '200':
        del login_session['access_token']
        del login_session['gplus_id']
        del login_session['username']
        del login_session['picture']
        del login_session['email']
        response = make_response(json.dumps("You are disconnected"), 200)
        response.headers['Content-Type'] = 'application/json'
        return redirect('/categories')
    else:
        response = make_response(json.dumps("Error occured"), 400)
        response.headers['Content-Type'] = 'application/json'
        return redirect('/categories')


# creates the new user details

def createUser(login_session):
    '''
    this function creates new user information
    session.add() is add the user
    session.commit() is commit the session
    '''
    user = Users(name=login_session['username'],
                 email=login_session['email'],
                 picture=login_session['picture'])
    session.add(user)
    session.commit()
    user_db = session.query(Users).filter_by(
        email=login_session['email']).one()
    return user_db.id


def getUserInfo(user_id):
    '''
    this function getting the user information
    '''
    user = session.query(User).filter_by(id=user_id).one()
    return user


def getUserID(email):
    '''
    this function is getting the userid
    '''
    try:
        user = session.query(Users).filter_by(email=email).one()
        return user.id
    except:
        return None


@app.route('/')
@app.route('/categories/')
def showcategories():
    '''
   @app.route('/categories/') opens the categories.html or
   public_categories.html based on checking the condition.
    '''
    categories = session.query(Category).all()
    if 'username' not in login_session:
        return render_template('public_categories.html', categories=categories)
    else:
        return render_template('categories.html', categories=categories,
                               user=login_session['email'],
                               picture=login_session['picture'])


@app.route('/categories/<int:categories_id>/')
@app.route('/categories/<int:categories_id>/books/')
def showBooks(categories_id):
    '''
    this function is shows the book details
    if user not login then public_books.html page will opened
    if login it opens the books.html and then shows the book details
    '''
    categories = session.query(Category).filter_by(
        id=categories_id).one_or_none()
    if categories is None:
        return "No such element"
    books = session.query(BookDetails).filter_by(
        categories_id=categories_id).all()
    if 'username' not in login_session:
        return render_template('public_books.html',
                               categories=categories, books=books)
    return render_template('books.html', books=books,
                           categories=categories, user=login_session['email'])


@app.route('/categories/new/', methods=['GET', 'POST'])
def newcategories():
    '''
    this function is used to add the new category
    if user not login it will goto the login page
    the user fill the all the details
    and submit it shows the Category was successfully added to the catalog
    if this function is executed the newcategories.html page is opened
    '''
    if 'username' not in login_session:
        return redirect('/login')
    if request.method == 'POST':
        newcategories = Category(name=request.form['name'],
                                 description=request.form['description'],
                                 user_id=login_session['user_id'])
        session.add(newcategories)
        session.commit()
        flash('Category was successfully added to the catalog')
        return redirect(url_for('showcategories'))
    else:
        return render_template('newcategories.html')


@app.route('/categories/<int:categories_id>/books/new/',
           methods=['GET', 'POST'])
def newBook(categories_id):
    '''
    this function is used to add the new book details
    if user not login it will goto the login page
    newBook is takes new book details
    after submited "Book was successfully added to the list" message will shoen
    if this function is executed the newBook.html page is opened
    '''
    if 'username' not in login_session:
        return redirect('/login')
    if request.method == 'POST':
        if 'type' not in request.form:
            type = 'eBook'
        else:
            type = request.form['type']
        newBook = BookDetails(name=request.form['name'],
                              author=request.form['author'],
                              description=request.form['description'],
                              price=request.form['price'],
                              user_id=login_session['user_id'],
                              categories_id=categories_id)
        session.add(newBook)
        session.commit()
        flash('Book was successfully added to the list')
        return redirect(url_for('showBooks', categories_id=categories_id))
    else:
        return render_template('newBook.html', categories_id=categories_id)


@app.route('/categories/<int:categories_id>/edit/', methods=['GET', 'POST'])
def editcategories(categories_id):
    '''
    if user not login it will goto the login page
    this function is used for edit the categories
    the first six categories only user1 will edit
    if any other user opened and click edit it will shows the alert
    after edit category "Category was successfully edited" message will shown
    if this function is executed the editcategories.html page is opened
    '''
    if 'username' not in login_session:
        return redirect('/login')
    categoriesToEdit = session.query(Category).filter_by(
        id=categories_id).one_or_none()
    if categoriesToEdit is None:
        return ("<script>function myFunction() {alert('No such element');"
                "window.history.back();}</script>"
                "<body onload='myFunction()''>")
    if categoriesToEdit.user_id != login_session['user_id']:
        return ("<script>function myFunction() {alert('No access');"
                "window.history.back();}</script>"
                "<body onload='myFunction()''>")
    if request.method == 'POST':
        if request.form['name']:
            categoriesToEdit.name = request.form['name']
        if request.form['description']:
            categoriesToEdit.description = request.form['description']
        session.add(categoriesToEdit)
        session.commit()
        flash('Category %s was successfully edited' % categoriesToEdit.name)
        return redirect(url_for('showcategories'))
    else:
        return render_template(
            'editcategories.html', categories=categoriesToEdit)


@app.route('/categories/<int:categories_id>/books/<int:book_id>/edit/',
           methods=['GET', 'POST'])
def editBook(categories_id, book_id):
    '''
    this function is used for edit the book details
    if user not login it will goto the login page
    redirects to the method that shows the listof books of
    the categories if successful
    only user1 is edit first six categories book details
    if any other user clicks the edit button it shows the alert
    if this function is executed the editBook.html page is opened
    '''
    if 'username' not in login_session:
        return redirect('/login')
    bookToEdit = session.query(BookDetails).filter_by(id=book_id).one_or_none()
    if bookToEdit is None:
        return ("<script>function myFunction() {alert('No such element');"
                "window.history.back();}</script>"
                "<body onload='myFunction()''>")
    if bookToEdit.user_id != login_session['user_id']:
        return ("<script>function myFunction()"
                "{alert('No access');window.history.back();}"
                "</script><body onload='myFunction()''>")
    if request.method == 'POST':
        if request.form['name']:
            bookToEdit.name = request.form['name']
        if request.form['description']:
            bookToEdit.description = request.form['description']
        if request.form['price']:
            bookToEdit.price = request.form['price']
        if request.form['type']:
            bookToEdit.type = request.form['type']
        if request.form['author']:
            bookToEdit.author = request.form['author']
        bookToEdit.id = book_id
        bookToEdit.categories_id = categories_id
        session.add(bookToEdit)
        session.commit()
        flash('Book %s was successfully edited' % bookToEdit.name)
        return redirect(url_for('showBooks', categories_id=categories_id))
    else:
        return render_template('editBook.html', categories_id=categories_id,
                               book_id=book_id, book=bookToEdit)


@app.route('/categories/<int:categories_id>/delete/', methods=['GET', 'POST'])
def deletecategories(categories_id):
    '''
    if user not login it will goto the login page
    this function is used for deleting the category
    only user1 is delete first six categories
    if any other user clicks the delete button it shows the alert
    if this function is executed the deletecategories.html page is opened
    '''
    if 'username' not in login_session:
        return redirect('/login')
    categoriesToDelete = session.query(Category).filter_by(
        id=categories_id).one_or_none()
    if categoriesToDelete is None:
        return ("<script>function myFunction() {alert('No such element');"
                "window.history.back();}</script>"
                "<body onload='myFunction()''>")
    if categoriesToDelete.user_id != login_session['user_id']:
        return ("<script>function myFunction()"
                "{alert('No access');"
                "window.history.back();"
                "}</script><body onload='myFunction()''>")
    if request.method == 'POST':
        session.delete(categoriesToDelete)
        session.commit()
        flash('Category was successfully deleted from the catalog')
        return redirect(url_for('showcategories', categories_id=categories_id))
    else:
        return render_template(
            'deletecategories.html', categories=categoriesToDelete)


@app.route('/categories/<int:categories_id>/books/<int:book_id>/delete/',
           methods=['GET', 'POST'])
def deleteBook(categories_id, book_id):
    '''
    if user not login it will goto the login page
    this function is used for deleting the book details
    only user1 is delete first six categories book details
    if any other user clicks the delete button it shows the alert
    if this function is executed the deleteBook.html page is opened
    '''
    if 'username' not in login_session:
        return redirect('/login')
    bookToDelete = session.query(
        BookDetails).filter_by(id=book_id).one_or_none()
    if bookToDelete is None:
        return ("<script>function myFunction() {alert('No such element');"
                "window.history.back();"
                "window.history.back();}</script>"
                "<body onload='myFunction()''>")
    if bookToDelete.user_id != login_session['user_id']:
        return ("<script>function myFunction()"
                "{alert('No access');}</script><body onload='myFunction()''>")
    if request.method == 'POST':
        session.delete(bookToDelete)
        session.commit()
        flash('Book was successfully deleted from the list')
        return redirect(url_for('showBooks', categories_id=categories_id))
    else:
        return render_template('deleteBook.html', book=bookToDelete)


# json api endpoints
@app.route('/categories/JSON/')
def categoriesJSON():
    '''
    tis function is used for json api endpoints
    '''
    categories = session.query(Category).all()
    return jsonify(categories=[g.serialize for g in categories])


@app.route('/categories/<int:categories_id>/books/JSON/')
def showBooksJSON(categories_id):
    '''
    this function is used for json api endpoints
    '''
    categories = session.query(Category).filter_by(
        id=categories_id).one_or_none()
    if categories is None:
        return "No such element."
    books = session.query(
        BookDetails).filter_by(categories_id=categories_id).all()
    return jsonify(books=[b.serialize for b in books])


@app.route('/categories/<int:categories_id>/books/<int:book_id>/JSON/')
def showBookItemJSON(categories_id, book_id):
    '''
    this function is used for json api endpoints
    '''
    Book_Item = session.query(BookDetails).filter_by(id=book_id).one_or_none()
    if Book_Item is None:
        return "No such element."
    return jsonify(Book_Item=Book_Item.serialize)


if __name__ == '__main__':
    app.secret_key = 'some_very_difficult_key_to_protect_data'
    app.debug = True
    app.run(host='0.0.0.0', port=8888)
