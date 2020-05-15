import os

# packages required to run flask application
from flask import Flask, session, render_template, request, jsonify
from flask_session import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

# local files
import validate_credentials
from books_api import goodreads_api

#
# --- GENERAL NOTES FOR RUNNING THE APPLICATION -------
# note: needed to re-install wekzueg package using version before 1.0.0
# pip install Werkzeug==0.16.1  (as a superuser) for flask to work
# not able to run flask using python 3.8.1, use python 3.6.8
#
# --- CREATE DATABASE ON HEROKU WITH THE UNIQUE URL (see project 1 handout:
# URL: postgres://pzbajbpsqgizxa:6cd4e080f3666cdffb35e9b1eff200d68541beedf3a64883065f1bf8cd41047c@ec2-52-201-55-4.
# compute-1.amazonaws.com:5432/d78beakjd7ltbr
#
# --- PRECONDITIONS -------
# CREATE TABLE "books" in the database with 5000 tiles from "books.csv"
# see file "create_books.sql" outlining the process/basic SQL commands
# use file "import.py" to save records from "books.csv" to the database
# set environment variables: FLASK_APP="application.py", FLASK_DEBUG=1 and
#   DATABASE_URL to the URL/URI assigned by HEROKU web-site

app = Flask(__name__)

# Check for environment variable
if not os.getenv("DATABASE_URL"):
    raise RuntimeError("DATABASE_URL is not set")

# Configure session to use filesystem
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Set up database
engine = create_engine(os.getenv("DATABASE_URL"))
db = scoped_session(sessionmaker(bind=engine))

# initialize user variables
usr_id = None
usr_name = None
usr_psswd = None
valid_User = False
msg_type = None

@app.route("/")
def index():
    return render_template("index.html")


@app.route("/registration", methods=["POST"])
def registration():
    ''' user registration '''
    usr_name_inp = request.form.get("usr_name")
    usr_psswd_inp = request.form.get("usr_psswd")
    usr_psswd_chk = request.form.get("usr_psswd_chk")
    print(f"usr_name = {usr_name_inp}, usr_psswd = {usr_psswd_inp}")

    # validate inputs
    registrationFlag = True
    usr_name, usr_psswd, message = validate_credentials.validate_login(
        usr_name_inp, usr_psswd_inp, usr_psswd_chk, registrationFlag=registrationFlag)

    if not message:
        # # -- if allowing for users with the same user name but different passwords, use:
        # if db.execute("SELECT usr_id FROM users WHERE usr_name= :usr_name AND usr_psswd= :usr_psswd",
        #               {"usr_name": usr_name, "usr_psswd": usr_psswd}).rowcount > 0:
        #     message = "Selected credentials (username and password) already exist in the database.\n" + \
        #               "Please choose a different set of credentials or use your existing information to login"
        #
        # -- do not allow users with the same username, use:
        if db.execute("SELECT usr_id FROM users WHERE usr_name= :usr_name ",
                      {"usr_name": usr_name}).rowcount > 0:
            message = "This username already exists in the database.\n" + \
                      "Please choose a different user name or use your existing information to login"
    # report error is there is a problem, otherwise add credentials to the database into "users" table
    # and inform user that the registration was successful
    if message:
        return render_template("error.html", message=message, msg_type=None)
    else:
        db.execute("INSERT INTO users (usr_name, usr_psswd) VALUES (:usr_name, :usr_psswd)",
                   {"usr_name": usr_name, "usr_psswd": usr_psswd})
        db.commit()
        msg_success = "You have successfully completed your registration. \n" +\
                        "You can now login and start the book review"
        return render_template("success.html", message=msg_success)


@app.route("/login")
def login():
    ''' base login page '''
    return render_template("login.html")


@app.route("/login_validate", methods=["POST"])
def login_validate():
    ''' validate login '''
    global usr_id, valid_User
    usr_name_inp = request.form.get("usr_name")
    usr_psswd_inp = request.form.get("usr_psswd")
    usr_psswd_chk = None

    # validate inputs
    registrationFlag = False
    usr_name, usr_psswd, message = validate_credentials.validate_login(
        usr_name_inp, usr_psswd_inp, usr_psswd_chk, registrationFlag=registrationFlag)

    # report error is there is a problem, otherwise add credentials to the database into "users" table
    # and inform user that the registration was successful
    if db.execute("SELECT usr_id FROM users WHERE usr_name= :usr_name AND usr_psswd= :usr_psswd",
                  {"usr_name": usr_name, "usr_psswd": usr_psswd}).rowcount == 0:
        message = "Login credentials not found.\n"+\
                  "Please login using valid credentials or go to Home page and register as a new user"
    else:
        result = db.execute("SELECT usr_id FROM users WHERE usr_name=:usr_name AND usr_psswd= :usr_psswd",
                            {"usr_name": usr_name, "usr_psswd": usr_psswd}).fetchone()

    if message:
        return render_template("error.html", message=message, msg_type=None)
    else:
        usr_id = int(result[0])
        msg_success = " You have successfully completed your login.\n You can now review books in the database. "
        valid_User=True
        return render_template("search.html")
        # return render_template("success.html", message=msg_success)


@app.route("/search", methods=["POST"])
def search():
    ''' Provide book search based on Title, Author or ISBN '''
    global valid_User, usr_id
    if not usr_id or not valid_User:
        message ="You need valid credentials to access this content \n" +\
            "Please login or go to Home page to register (first-time users)"
        return render_template("error.html", message=message, msg_type=None)
    default_string = None
    default_search = None
    max_Rows = 20  # maximum number of rows allowed to be returned from the search
    searchType = request.form.get("searchType")
    searchString = request.form.get("searchString")
    message = None
    results = None
    if not searchString:
        message = "Missing search string"

    # Author search
    if not message and searchType == "Author":
        results = db.execute("SELECT * FROM books WHERE book_author= :book_author",
                             {"book_author": searchString}).fetchall()
        if len(results) == 0:
            searchString = "%" + searchString + "%"
            results = db.execute("SELECT * FROM books WHERE book_author LIKE :book_author",
                                 {"book_author": searchString}).fetchall()
    # Title search
    if not message and searchType == "Title":
        results = db.execute("SELECT * FROM books WHERE book_title= :book_title",
                             {"book_title": searchString}).fetchall()
        if len(results) == 0:
            searchString = "%" + searchString + "%"
            results = db.execute("SELECT * FROM books WHERE book_title LIKE :book_title",
                                 {"book_title": searchString}).fetchall()
    #
    # ISBN search
    if not message and searchType == "ISBN":
        results = db.execute("SELECT * FROM books WHERE book_ISBN= :book_ISBN",
                             {"book_ISBN": searchString}).fetchall()
        if len(results) == 0:
            searchString = "%" + searchString + "%"
            results = db.execute("SELECT * FROM books WHERE book_ISBN LIKE :book_ISBN",
                                 {"book_ISBN": searchString}).fetchall()
    #
    if len(results) > max_Rows:
        message = "Search results exceed maximum allowed number of rows (max_rows = 20).  Please refine your search"

    if message:
        return render_template("error.html", message=message, msg_type=None)

    if len(results) > max_Rows:
        results = results[:max_Rows]
    default_search = searchType
    default_string = searchString
    return render_template("search.html", search_results=results, default_search=default_search,
                           default_string=default_string, message=message)


@app.route("/search_base")
def search_base():
    global usr_id, valid_User
    message=None
    if usr_id == None or not valid_User:
        message= "Please login prior to using \"Book Review\" - Project 1 web-site"
        return render_template("error.html", message=message, msg_type=None)
    else:
        return render_template("search.html")


@app.route("/book/<int:book_id>")
def book(book_id):
    """Lists details about a single book."""
    global valid_User, usr_id
    if not usr_id or not valid_User:
        message ="You need valid credentials to access this content \n" +\
            "Please login or go to Home page to register (first-time users)"
        return render_template("error.html", message=message, msg_type=None)
    # Make sure that the book exists.
    book = db.execute("SELECT * FROM books WHERE book_id = :id", {"id": book_id}).fetchone()
    if book is None:
        return render_template("error.html", message="There is no data on this book in a database", msg_type=None)
    else:
        # find information from goodreads website
        inp_isbn = list(db.execute("SELECT book_isbn FROM books WHERE book_id = :id", {"id": book_id}).fetchone())[0]
        try:
            goodreads_nRevs, goodreads_avgRate = goodreads_api(inp_isbn)
        except ValueError:
            goodreads_nRevs = "n/a"
            goodreads_avgRate = "n/a"
        #
        # find available reviews
        rev_items = []
        if db.execute("SELECT * FROM reviews WHERE book_id = :id ",
                      {"id": book_id}).rowcount > 0:
            # rev_items = db.execute("SELECT users.usr_name, reviews.rev_rate, reviews.rev_txt FROM users INNER JOIN "
            #     "reviews ON users.usr_id = reviews.usr_id ").fetchall()
            rev_items = db.execute("SELECT users.usr_name, reviews.rev_rate, reviews.rev_txt FROM reviews INNER JOIN "
                                   "users ON reviews.usr_id = users.usr_id WHERE book_id=:id",
                                   {"id": book_id}).fetchall()
    # render book page with relevant information
    return render_template("book.html", book=book,
                           goodreads_nRevs=goodreads_nRevs, goodreads_avgRate=goodreads_avgRate, rev_items=rev_items)

#----- provide review of individual titles -----
@app.route("/book/<int:book_id>", methods=["GET", "POST"])
def review(book_id):
    ''' provide review of individual titles '''
    global valid_User, usr_id, msg_type
    getFlag = False
    if not usr_id or not valid_User:
        message ="You need valid credentials to access this content \n" +\
            "Please login or go to Home page to register (first-time users)"
        return render_template("error.html", message=message, msg_type=None)

    message = None
    rev_rate = request.form.get("rev_rate")
    rev_txt = request.form.get("rev_txt")
    #
    #--- check if valid inputs provided
    if not rev_rate or not rev_txt:
        message = "Incomplete review, please provide rating and short review for the book"
    #
    #---- check if the user provided review in the past ----
    if db.execute("SELECT * FROM reviews WHERE book_id = :book_id AND usr_id = :usr_id",
                  {"book_id": book_id, "usr_id": usr_id}).rowcount > 0:
        if not message:
            message = "We've noticed that you reviewed this book previously. Your review is now updated"
            msg_type = "Warning"
            db.execute("UPDATE reviews SET rev_rate = :rev_rate, rev_txt = :rev_txt "
                       " WHERE book_id = :book_id AND usr_id = :usr_id",
                       {"rev_rate": rev_rate, "rev_txt": rev_txt, "book_id": book_id, "usr_id": usr_id})
            db.commit()
    if message:
        return render_template("error.html", message=message, msg_type=msg_type)

    db.execute("INSERT INTO reviews (usr_id, book_id, rev_rate, rev_txt) VALUES "
               "(:usr_id, :book_id, :rev_rate, :rev_txt)",
               {"usr_id": usr_id, "book_id": book_id, "rev_rate": rev_rate, "rev_txt": rev_txt})
    db.commit()

    rev_items = db.execute("SELECT users.usr_name, reviews.rev_rate, reviews.rev_txt FROM reviews INNER JOIN "
                       "users ON reviews.usr_id = users.usr_id WHERE book_id=:id", {"id": book_id}).fetchall()
    msg_success = "You review was submitted successfully."
    #
    #--- get required data to render the book page ------
    book = db.execute("SELECT * FROM books WHERE book_id = :id", {"id": book_id}).fetchone()
    if book is None:
        return render_template("error.html", message="There is no data on this book in a database", msg_type=None)
    else:
        # find information from goodreads website
        inp_isbn = list(db.execute("SELECT book_isbn FROM books WHERE book_id = :id", {"id": book_id}).fetchone())[0]
        try:
            goodreads_nRevs, goodreads_avgRate = goodreads_api(inp_isbn)
        except ValueError:
            goodreads_nRevs = "n/a"
            goodreads_avgRate = "n/a"

    return render_template("book.html", book_id=book_id, book=book,
                           goodreads_nRevs=goodreads_nRevs, goodreads_avgRate=goodreads_avgRate, rev_items=rev_items)
    #
    # return render_template("book.html", book_id=book_id, rev_items=rev_items)
    # # return render_template("success.html", message=msg_success)


@app.route("/logout", methods=["GET", "POST"])
def logout():
    ''' Use to logout the user '''
    global usr_id, usr_psswd, usr_name, valid_User
    usr_id = None
    usr_name = None
    usr_psswd = None
    valid_User = False

    msg_success = "You have successfully logged out of the book review. \n" +\
                    "If you want to continue with the book review, please login again"
    return render_template("success.html", message=msg_success)
    # return render_template("logout.html")

@app.route("/api/<book_isbn>")
def my_books_api(book_isbn):
    """Return details about a single book based on the isbn request"""

    # Make sure that the book exists.
    book = db.execute("SELECT * FROM books WHERE book_isbn = :id", {"id": book_isbn}).fetchone()
    if book is None:
        error_ID = 404
        return jsonify({"error": "could not find requested ISBN", "error_code": error_ID}), error_ID

    # modify information from the reference web site:
    book_items = list(book)
    book_keys = ["book_id", "book_isbn", "book_title", "book_author", "book_year"]
    book_dict = dict(zip(book_keys, book_items))
    average_score = db.execute("SELECT AVG(rev_rate) FROM reviews WHERE book_id = :id",
                        {"id": book_items[0]}).fetchone()
    review_count = db.execute("SELECT COUNT(ALL rev_rate) FROM reviews WHERE book_id = :id",
                               {"id": book_items[0]}).fetchone()

    book_keys_json = ["title", "author", "year", "isbn", "review_count", "average_score"]
    book_items_json = book_items[2:4]
    book_items_json.append(int(book_dict["book_year"]))
    book_items_json.append(book_dict["book_isbn"])
    book_items_json.append(int(list(review_count)[0]))
    if list(average_score)[0]:
        book_items_json.append(float(list(average_score)[0]))
    else:
        book_items_json.append(-9999)
    # project 1 requirement is to return the JSON object in the following format:
    # return jsonify({
    #         "title": "Memory",
    #         "author": "Dough Loyd",
    #         "year": 2015,
    #         "isbn": "1632168146",
    #         "review_count": 28,
    #         "average_score": 5.0
    #     })
    book_dict_json = dict(zip(book_keys_json, book_items_json))
    return jsonify(book_dict_json)