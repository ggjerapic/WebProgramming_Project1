/*  Reference:
    http://www.sqlcourse.com/
    Note: use -- to comment individual lines
    create table */
CREATE TABLE reviews (
    rev_id SERIAL PRIMARY KEY,
    usr_id INTEGER NOT NULL,
    book_id INTEGER NOT NULL,
    rev_rate INTEGER NOT NULL,
    rev_txt VARCHAR NOT NULL
);
-- SELECT * FROM reviews;
-- DELETE FROM reviews where usr_id=4;
/* delete users */
-- DELETE FROM users;
-- --
-- /* remove users table */
-- DROP TABLE users;

/* delete all records */
-- DELETE FROM users;

/* delete table
   drop table is different from deleting all of the records in the table.
   Deleting all of the records in the table leaves the table
   including column and constraint information.
   Dropping the table removes the table definition as well as all of
   its rows.*/
-- DROP TABLE users;

/* check that everything works by retrieving records */
-- select * from users WHERE usr_name='xxxxx'