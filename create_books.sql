/*  Reference:
    http://www.sqlcourse.com/
    Note: use -- to comment individual lines
    create table */
CREATE TABLE books (
    book_id SERIAL PRIMARY KEY,
    book_isbn VARCHAR NOT NULL,
    book_title VARCHAR NOT NULL,
    book_author VARCHAR NOT NULL,
    book_year VARCHAR NOT NULL
);

/* delete all records */
-- DELETE FROM books;

/* delete table
   drop table is different from deleting all of the records in the table.
   Deleting all of the records in the table leaves the table
   including column and constraint information.
   Dropping the table removes the table definition as well as all of
   its rows.*/
-- DROP TABLE books;

/* check that everything works by retrieving records */
-- select * from books WHERE book_author='Isaac Asimov'