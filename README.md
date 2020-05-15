# Project 1

Web Programming with Python and JavaScript

# Author
Gordan Gjerapic, e-mail: ggjerapic@gmail.com

<!-- #Table of contents -->

# 1.0 Overview
This project creates a web-site for book reviews using `PostgreSQL` and `Flask`
as a requirement for EdX - Project1. 

# 2.0 Initial Setup
To set-up Project 1, the following items were required:
1) Python installation - use Python 3.6.8
2) PostgreSQL database - use Heroku web-site to set-up hosting requirements
3) Set environment variables required to run Flask
4) Install python packages required for Flask/SQL support
5) Get access to `Goodreads` api
6) Load `books.csv` items (list of books) to Heroku database

## 2.1 Python Installation
There were problems with running `Flask` using `Python 3.8.1`.  
After `Google`-ing comments by other users reporting the same problem, 
`Python 3.6.8` was selected as an interpreter for the `Book Review` project.

## 2.2 PostgreSQL Database
The PostgreSQL database was set-up on https://www.heroku.com using "Hobby Dev - Free" plan 
resulting in the following credentials where URI was used as a DATABASE_URL for the
 `Book Review` Flask application.
 

**Table 2.1:   Heroku credentials**

| Heroku   <br>(database credentials)    |    Value   |
|----------------------------------------|:----------:|
| Host                                   | <my_value> |
| Database                               | <my_value> |
| User                                   | <my_value> |
| Port                                   | <my_value> |
| Password                               | <my_value> |
| URI<br>(Universal Resource Identifier) | <my_value> |
| Heroku CLI                             | <my_value> |

## 2.3 Environment Variables
Environment variables were set as follows

**Table 2.2:  Environment variables**

| Environment  variable |          Value          |
|-----------------------|:-----------------------:|
| FLASK_APP             |      application.py     |
| DEBUG                 |            1            |
| DATABASE_URL          | Heroku URI   <my_value> |

## 2.4 Python Packages
The following Python packages/libraries were used:
* `Flask`
* `Flask-Session`
* `psycopg2-binary`
* `SQLAlchemy`
* `requests`

The package `werkzeug` was reloaded using the version `0.16.0` after encountering problems
with the program execution.

## 2.5 Goodreads API
To use `Goodreads` api, https://www.goodreads.com/api, one needs to register and obtain the `key`.

## 2.6 Import of 'books.csv' Data and Uploading Data to Heroku Database 
The content of `books.csv` file was uploaded to heroku using packages `os`, `csv`, 
`SQLalchemy` and `SQLaclhemy.orm`. In python file `import.py`use the SQL command:


        INSERT INTO books (book_isbn, book_title, book_author, book_year) VALUES 
                   (:book_isbn, :book_title, :book_author, :book_year)                  


where `:book_isbn`, `:book_title`, `:book_author` and `:book_year` are individual attributes for the single book item 
in `books.csv` file.
 
# 3.0 Website Organization and File Structure
The program `application.py` is used to provide WSGI (Web Server Gateway Interface) using Flask. The  
functionality for different URLs is provided using `@app.route` decorators and associated functions.

## 3.1 Python Files
Python files `validate_credentials.py` and `books_api.py` are used by the main program 
`application.py` (Flask application). 

The program `validate_credentials.py` is used to validate user's credentials (username and password) during the registration 
and the login process. The program `books_api.py` is used to provide the number of ratings 
and the average rating for a book from `Goodreads` with a specific ISBN.

## 3.2 HTML files
The following HTML files were utilized for the `Book Review - Project 1` application

**Table 3.1: HTML files**

| HTML file       | Purpose                                                      |
|-----------------|--------------------------------------------------------------|
| layout.html     | Header/Extender file for other pages                         |
| **index.html**  | Start-up/registration page                                   |
| **login.html**  | Login page                                                   |
| **search.html** | page for book search using "Author", "Title" and "ISBN" keys |
| **logout.html** | Logout page                                                  |
| book.html       | page w/ individual book data and for book review             |
| error.html      | page to send warning or errors to user                       |
| success.html    | page informing user of successful task completion            |

## 3.3 SQL tables
The following tables were used to perform the requirements of the `Book Review` application.

**Table 3.2: SQL tables**

| Table<br>Name | Col 1 Name<br>Primary Key | Col 2<br>Name | Col 3<br>Name | Col 4<br>Name | Col 5<br>Name |
|:-------------:|:-------------------------:|:-------------:|:-------------:|:-------------:|:-------------:|
| books         |            book_id        |    book_isbn  |   book_title  |   book_author |    book_year  |
| users         |            usr_id         |    usr_name   |    usr_psswd  |       n/a     |       n/a     |
| reviews       |            rev_id         |     usr_id    |     book_id   |    rev_rate   |     rev_txt   |

## 3.3 Application Requirements
The website uses the landing page `index.html` for registration and three other main pages 
`login.html`, `search.html` and `logout.html` to facilitate the following requirements:
* Registration   
* Login
* Search 
* Logout

Note that the requirement 
* Import
was addressed separately as discussed in Section 2.6. 

The requirements for 
* Book Page
* Review Submission and
* Goodreads Review Data

were addressed using the page `book.html` and the associated application routes and functions 
implemented in (or called from) `application.py`.

The requirement
* API access 
 
was addressed in `application.py` allowing for the JSON return
for the web-link defined in Flask as `@app.route("/api/<book_isbn>")`. The API is defined 
by the corresponding function `my_books_api(book_isbn)`.  E.g., the API returns the dictionary 

    {
        "author":"Isaac Asimov", 
        "average_score":5.0, 
        "isbn":"553803700", 
        "review_count":3, 
        "title":"I, Robot",
        "year":1950 
    } <br>
    
for the book with the ISBN = 553803700.  For the book without reviews, the API returns
the `"average score" = -9999`.
    
    
  

