from data.db_session import create_session
from models import user_types, book_genres, books, authors, issues, users
import datetime


def get_password_hash(login):
    session = create_session()
    cursor = users.User  # Shortening the path to user
    user = session.query(cursor).filter(cursor.login == login).first()
    if user is None:
        return 2  # UNKNOWN_LOGIN
    return user.hashed_password


def get_user_info(user_id):
    session = create_session()
    cursor = users.User  # Shortening the path to user
    user = session.query(cursor).filter(cursor.id == user_id).first()
    return user.id, user.login, user.name, user.surname, user.type_id, user.cart


def get_user_type(type_id):
    session = create_session()
    cursor = user_types.UserType  # Shortening the path to user type
    type_obj = session.query(cursor).filter(cursor.id == type_id).first()
    return type_obj.name


def get_user_type_id(user_type):
    session = create_session()
    cursor = user_types.UserType  # Shortening the path to user type
    type_obj = session.query(cursor).filter(cursor.name == user_type).first()
    if type_obj is None:
        return 10  # INVALID_TYPE
    return type_obj.id


def add_user(login, password_hash, name, surname, email, type_id):
    session = create_session()
    user = users.User()
    user.login = login
    user.hashed_password = password_hash
    user.name = name
    user.surname = surname
    user.email = email
    user.type_id = type_id
    session.add(user)
    session.commit()
    return [0, user.id]  # SUCCESS


def get_user_id(login):
    session = create_session()
    cursor = users.User  # Shortening the path to user
    user = session.query(cursor).filter(cursor.login == login).first()
    return user.id


def check_login_replay(login):
    session = create_session()
    cursor = users.User  # Shortening the path to user
    user = session.query(cursor).filter(cursor.login == login).first()
    return user is None


def get_books_genres():
    session = create_session()
    genres = session.query(book_genres.BookGenre).all()
    return genres


def get_books(genre_id):
    session = create_session()
    cursor = books.Books  # Shortening the path to book
    if genre_id is None:
        return session.query(cursor).all()
    else:
        return session.query(cursor).filter(cursor.genre_id == genre_id).all()


def get_book_genre_id(genre_name):
    session = create_session()
    cursor = book_genres.BookGenre  # Shortening the path to book genre
    genre = session.query(cursor).filter(cursor.name == genre_name).first()
    if genre is None:
        return 'UNKNOWN_GENRE'
    return genre.id


def get_book_genre_name(genre_id):
    session = create_session()
    cursor = book_genres.BookGenre  # Shortening the path to book genre
    genre = session.query(cursor).filter(cursor.id == genre_id).first()
    return genre.name


def get_book_author_name(author_id):
    session = create_session()
    cursor = authors.Authors  # Shortening the path to authors
    author = session.query(cursor).filter(cursor.id == author_id).first()
    return author.name


def get_book(book_id):
    session = create_session()
    cursor = books.Books  # Shortening the path to book
    book = session.query(cursor).filter(cursor.id == book_id).first()
    return book


def check_barcode_replay(barcode):
    session = create_session()
    cursor = books.Books  # Shortening the path to book
    user = session.query(cursor).filter(cursor.barcode == barcode).first()
    return user is None


def get_book_author_id(author_name):
    session = create_session()
    cursor = authors.Authors  # Shortening the path to authors
    author = session.query(cursor).filter(cursor.name == author_name).first()
    return author


def add_author(name):
    session = create_session()
    author = authors.Authors()
    author.name = name
    session.add(author)
    session.commit()
    return 0  # SUCCESS


def add_book(name, author_id, barcode, quantity):
    session = create_session()
    book = books.Books()
    book.name = name
    book.author_id = author_id
    book.barcode = barcode
    book.quantity = quantity
    session.add(book)
    session.commit()
    return [0, book.id]  # SUCCESS


def get_book_id(book_barcode):
    session = create_session()
    cursor = books.Books  # Shortening the path to book
    book = session.query(cursor).filter(cursor.barcode == book_barcode).first()
    return book.id


def check_book_presence(book_id):
    session = create_session()
    cursor = books.Books  # Shortening the path to book
    book = session.query(cursor).filter(cursor.id == book_id).first()
    return book is not None


def check_user_presence(user_id):
    session = create_session()
    cursor = users.User  # Shortening the path to user
    user = session.query(cursor).filter(cursor.id == user_id).first()
    return user is not None


def give_book(user_id, book_id):
    session = create_session()
    issue = issues.Issues()
    issue.user_id = user_id
    issue.book_id = book_id
    issue.type = "0"  # ISSUED
    session.add(issue)
    session.commit()
    return [0, issue.id]  # SUCCESS


def return_book(issue_id):
    session = create_session()
    cursor = issues.Issues  # Shortening the path to issue
    issue = session.query(cursor).filter(cursor.id == issue_id).update({'type': 1})  # RETURNED
    session.commit()
    return 0  # SUCCESS


def check_issue_presence(issue_id):
    session = create_session()
    cursor = issues.Issues  # Shortening the path to issue
    issue = session.query(cursor).filter(cursor.id == issue_id).first()
    return issue is not None


def get_user_cart(user_id):
    session = create_session()
    cursor = users.User  # Shortening the path to user
    user = session.query(cursor).filter(cursor.id == user_id).first()
    return user.cart


def set_user_cart(user_id, user_cart):
    session = create_session()
    cursor = users.User  # Shortening the path to issue
    user = session.query(cursor).filter(cursor.id == user_id).update({'cart': user_cart})
    session.commit()
    return 0  # SUCCESS