from data.db_session import create_session
from models import user_types, book_genres, books, authors, issues, users, issue_types, image
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


def get_books(genre_id, author_obj):
    session = create_session()
    cursor = books.Books  # Shortening the path to book
    if genre_id is None and author_obj is None:
        return session.query(cursor).all()
    elif genre_id is None and author_obj is not None:
        return session.query(cursor).filter(cursor.author_id == author_obj.id).all()
    elif genre_id is not None and author_obj is not None:
        return session.query(cursor).filter(cursor.author_id == author_obj.id, cursor.genre_id == genre_id).all()
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


def add_book(name, author_id, barcode, quantity, image_id, description, genre_id):
    session = create_session()
    book = books.Books()
    book.name = name
    book.author_id = author_id
    book.barcode = barcode
    book.quantity = quantity
    book.image_id = image_id
    book.description = description
    book.genre_id = genre_id
    session.add(book)
    session.commit()
    return [0, book.id]  # SUCCESS


def add_genre(name):
    session = create_session()
    genre = book_genres.BookGenre()
    genre.name = name
    session.add(genre)
    session.commit()
    return genre


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


def check_author_presence(author_id):
    session = create_session()
    cursor = authors.Authors  # Shortening the path to user
    author = session.query(cursor).filter(cursor.id == author_id).first()
    return author is not None


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
    cursor = users.User  # Shortening the path to user
    user = session.query(cursor).filter(cursor.id == user_id).update({'cart': user_cart})
    session.commit()
    return 0  # SUCCESS


def get_issues(user_id, issue_status):
    session = create_session()
    cursor = issues.Issues  # Shortening the path to issue
    if issue_status is None:
        user_issues = session.query(cursor).filter(cursor.user_id == user_id).all()
    else:
        user_issues = session.query(cursor).filter(cursor.user_id == user_id, cursor.type == issue_status).all()
    return user_issues


def get_issue_type_name(issue_id):
    session = create_session()
    cursor = issue_types.IssueTypes  # Shortening the path to issue
    issue = session.query(cursor).filter(cursor.id == issue_id).first()
    return issue.name


def get_issue_status_is(issue_status):
    session = create_session()
    cursor = issue_types.IssueTypes  # Shortening the path to issue
    issue = session.query(cursor).filter(cursor.name == issue_status).first()
    return issue


def get_image_id(image_url):
    if image_url is None:
        return 0  # default image
    session = create_session()
    image_obj = image.Image
    image_obj.url = image_url
    session.add(image_obj)
    session.commit()
    return image_obj.id


def get_image_url(image_id):
    session = create_session()
    cursor = image.Image  # Shortening the path to issue
    image_obj = session.query(cursor).filter(cursor.id == image_id).first()
    return image_obj.url


def check_book_available(book_id):
    session = create_session()
    cursor = books.Books  # Shortening the path to book
    book_obj = session.query(cursor).filter(cursor.id == book_id).first()
    return int(book_obj.quantity) > 0


def subtract_book(book_id):
    session = create_session()
    cursor = books.Books  # Shortening the path to book
    book_obj = session.query(cursor).filter(cursor.id == book_id).update({'quantity': '0'})
    session.commit()
    return 0  # SUCCESS


def increase_book(book_id):
    session = create_session()
    cursor = books.Books  # Shortening the path to book
    book_obj = session.query(cursor).filter(cursor.id == book_id).update({'quantity': '1'})
    session.commit()
    return 0  # SUCCESS


def get_books_authors():
    session = create_session()
    authors_objs = session.query(authors.Authors).all()
    return authors_objs


def get_book_id_by_issue(issue_id):
    session = create_session()
    cursor = issues.Issues  # Shortening the path to issue
    book_obj = session.query(cursor).filter(cursor.id == issue_id).first()
    return book_obj.book_id  # SUCCESS


def get_book_id_by_issue(issue_id):
    session = create_session()
    cursor = issues.Issues  # Shortening the path to issue
    book_obj = session.query(cursor).filter(cursor.id == issue_id).first()
    return book_obj.book_id  # SUCCESS


def get_books_by_author(author_id):
    session = create_session()
    cursor = books.Books  # Shortening the path to book
    books_obj = session.query(cursor).filter(cursor.author_id == author_id).all()
    return books_obj
