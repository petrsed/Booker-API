from . import dbwrapper
from re import *


def entry(login, received_password_hash):
    valid_password_hash = dbwrapper.get_password_hash(login)
    if valid_password_hash == 2:
        return 2  # UNKNOWN_LOGIN
    if valid_password_hash == received_password_hash:
        return 0  # SUCCESS
    else:
        return 1  # INVALID_PASSWORD


def authenticate(request):
    if "user" not in request:
        return 5  # MISSING_ARGUMENTS
    user = request["user"]
    if "login" not in user:
        return 3  # MISSING_LOGIN
    elif "password_hash" not in user:
        return 4  # MISSING_PASSWORD_HASH
    login, password_hash = user["login"], user["password_hash"]
    return entry(login, password_hash)


def get_user_data(login):
    user_id, user_name, user_surname, user_type_id, user_cart = dbwrapper.get_user_info(login)
    user_type = dbwrapper.get_user_type(user_type_id)
    return user_id, user_name, user_surname, user_type, user_cart


def registration(request):
    if "user" not in request:
        return 8  # MISSING_ARGUMENTS
    user = request["user"]
    if "login" not in user:
        return 3  # MISSING_LOGIN
    elif "name" not in user:
        return 4  # MISSING_NAME
    elif "surname" not in user:
        return 5  # MISSING_SURNAME
    elif "email" not in user:
        return 7  # MISSING_EMAIL
    elif "password_hash" not in user:
        return 6  # MISSING_PASSWORD_HASH
    elif "type" not in user:
        return 9  # MISSING_TYPE
    login, password_hash = user["login"], user["password_hash"]
    name, surname = user["name"], user["surname"]
    email, type = user["email"], user["type"]
    if not dbwrapper.check_login_replay(login):
        return 2  # LOGIN_REPLAY
    if not check_email_valid(email):
        return 1  # INVALID_EMAIL
    type_id = dbwrapper.get_user_type_id(type)
    if type_id == 10:
        return 10  # INVALID_TYPE
    return dbwrapper.add_user(login, password_hash, name, surname, email, type_id)


def check_email_valid(address):
    pattern = compile('(^|\s)[-a-z0-9_.]+@([-a-z0-9]+\.)+[a-z]{2,6}(\s|$)')
    return pattern.match(address)


def get_books_genres():
    genres = list()
    genre_objects = dbwrapper.get_books_genres()
    for genre_object in genre_objects:
        genres.append([genre_object.id, genre_object.name])
    return genres


def get_books(request):
    if "genre" not in request:
        genre_id = None
    else:
        genre_name = request["genre"]
        genre_id = dbwrapper.get_book_genre_id(genre_name)
        if genre_id == 'UNKNOWN_GENRE':
            return 1  # UNKNOWN_GENRE
    books = list()
    books_objects = dbwrapper.get_books(genre_id)
    for book_object in books_objects:
        book_genre = dbwrapper.get_book_genre_name(book_object.genre_id)
        book_author = dbwrapper.get_book_author_name(book_object.author_id)
        books.append(
            [book_object.id, book_genre, book_object.name, book_author, book_object.barcode, book_object.quantity])
    return books


def get_book(id):
    book_object = dbwrapper.get_book(id)
    if book_object is None:
        return 1  # UNKNOWN_BOOK_ID
    else:
        book_genre = dbwrapper.get_book_genre_name(book_object.genre_id)
        book_author = dbwrapper.get_book_author_name(book_object.author_id)
        return [book_object.id, book_genre, book_object.name, book_author, book_object.barcode, book_object.quantity]


def add_book(request):
    if "book" not in request:
        return 7  # MISSING_ARGUMENTS
    book = request["book"]
    if "name" not in book:
        return 3  # MISSING_NAME
    elif "author" not in book:
        return 4  # MISSING_AUTHOR
    elif "barcode" not in book:
        return 5  # MISSING_BARCODE
    elif "quantity" not in book:
        return 6  # MISSING_QUANTITY
    name, author = book["name"], book["author"]
    barcode, quantity = book["barcode"], book["quantity"]
    if not dbwrapper.check_barcode_replay(barcode):
        return 2  # BARCODE_REPLAY
    if not check_barcode_valid(barcode):
        return 1  # INVALID_BARCODE
    author_obj = dbwrapper.get_book_author_id(author)
    if author_obj is None:
        dbwrapper.add_author(author)
        author_obj = dbwrapper.get_book_author_id(author)
    author_id = author_obj.id
    return dbwrapper.add_book(name, author_id, barcode, quantity)


def check_barcode_valid(barcode):
    return barcode.isdigit()



