/*  Reference:
    http://www.sqlcourse.com/
    Note: use -- to comment individual lines
    create table */
CREATE TABLE users (
    usr_id SERIAL PRIMARY KEY,
    usr_name VARCHAR NOT NULL,
    usr_psswd VARCHAR NOT NULL,
);
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