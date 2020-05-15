import csv
import os

from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

engine = create_engine(os.getenv("DATABASE_URL"))
db = scoped_session(sessionmaker(bind=engine))

def main():
    f = open("books.csv")
    reader = csv.reader(f)

    for isbn, title, author, year in reader:
        db.execute("INSERT INTO books (book_isbn, book_title, book_author, book_year) VALUES "
                   "(:book_isbn, :book_title, :book_author, :book_year)",
                    {"book_isbn": isbn, "book_title": title, "book_author": author, "book_year": year})
        print(f"Added book from {author} published in {year} - {title}.")
    db.commit()

if __name__ == "__main__":
    # db.execute("CREATE TABLE IF NOT EXISTS books (book_id SERIAL PRIMARY KEY, book_isbn VARCHAR NOT NULL,"
    #        "book_title VARCHAR NOT NULL, book_author VARCHAR NOT NULL, book_year VARCHAR NOT NULL")
    main()
