from . import dbwrapper
from re import *
from random import sample


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


def get_user_data(user_id):
    user_id, user_login, user_name, user_surname, user_type_id, user_cart = dbwrapper.get_user_info(user_id)
    user_type = dbwrapper.get_user_type(user_type_id)
    return user_id, user_login, user_name, user_surname, user_type, user_cart


def registration(request):
    if "user" not in request:
        return [8, None]  # MISSING_ARGUMENTS
    user = request["user"]
    if "login" not in user:
        return [3, None]  # MISSING_LOGIN
    elif "name" not in user:
        return [4, None]  # MISSING_NAME
    elif "surname" not in user:
        return [5, None]  # MISSING_SURNAME
    elif "email" not in user:
        return [7, None]  # MISSING_EMAIL
    elif "password_hash" not in user:
        return [6, None]  # MISSING_PASSWORD_HASH
    elif "type" not in user:
        return [9, None]  # MISSING_TYPE
    login, password_hash = user["login"], user["password_hash"]
    name, surname = user["name"], user["surname"]
    email, type = user["email"], user["type"]
    if not dbwrapper.check_login_replay(login):
        return [2, None]  # LOGIN_REPLAY
    if not check_email_valid(email):
        return [1, None]  # INVALID_EMAIL
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


def get_books(args):
    random, start, author = args.get("random"), args.get("start"), args.get("author")
    genre_name, amount = args.get("genre"), args.get("amount")
    if genre_name is None:
        genre_id = None
    else:
        genre_id = dbwrapper.get_book_genre_id(genre_name)
        if genre_id == 'UNKNOWN_GENRE':
            return 1  # UNKNOWN_GENRE
    books = list()
    if author is not None:
        author_obj = dbwrapper.get_book_author_id(author)
        if author_obj == None:
            return 2  # UNKNOWN_AUTHOR
    else:
        author_obj = None
    books_objects = dbwrapper.get_books(genre_id, author_obj)
    for book_object in books_objects:
        book_genre = dbwrapper.get_book_genre_name(book_object.genre_id)
        book_author = dbwrapper.get_book_author_name(book_object.author_id)
        image_url = dbwrapper.get_image_url(book_object.image_id)
        icon_url = dbwrapper.get_image_url(book_object.icon_id)
        books.append(
            (book_object.id, book_genre, book_object.name, book_author, book_object.barcode, book_object.quantity,
             book_object.description, image_url, icon_url))
    if random is not None and len(books) >= int(random):
        return sample(books, len(books))[:int(random)]
    elif start is not None and amount is not None and len(books) >= int(start) and int(amount):
        return books[int(start):int(start) + int(amount)]
    elif amount is not None and start is None:
        return books[:int(amount)]
    elif amount is None and start is not None:
        return books[int(start):]
    else:
        return books


def get_book(id):
    book_object = dbwrapper.get_book(id)
    if book_object is None:
        return 1  # UNKNOWN_BOOK_ID
    else:
        book_genre = dbwrapper.get_book_genre_name(book_object.genre_id)
        book_author = dbwrapper.get_book_author_name(book_object.author_id)
        book_image_url = dbwrapper.get_image_url(book_object.image_id)
        book_icon_url = dbwrapper.get_image_url(book_object.icon_id)
        return [book_object.id, book_genre, book_object.name, book_author, book_object.barcode, book_object.quantity,
                book_object.description, book_image_url, book_icon_url]


def add_book(request):
    if "book" not in request:
        return [7, None]  # MISSING_ARGUMENTS
    book = request["book"]
    if "name" not in book:
        return [3, None]  # MISSING_NAME
    elif "genre" not in book:
        return [8, None]  # MISSING_GENRE
    elif "description" not in book:
        return [9, None]  # MISSING_DESCRIPTION
    elif "author" not in book:
        return [4, None]  # MISSING_AUTHOR
    elif "barcode" not in book:
        return [5, None]  # MISSING_BARCODE
    elif "quantity" not in book:
        return [6, None]  # MISSING_QUANTITY
    name, author = book["name"], book["author"]
    barcode, quantity = book["barcode"], book["quantity"]
    description, genre_name = book["description"], book["genre"]
    if "image_url" in book:
        image_url = book["image_url"]
    else:
        image_url = None
    if not dbwrapper.check_barcode_replay(barcode):
        return [2, None]  # BARCODE_REPLAY
    if not check_barcode_valid(barcode):
        return [1, None]  # INVALID_BARCODE
    genre_obj = dbwrapper.get_book_genre_id(genre_name)
    if genre_obj is None:
        genre_obj = dbwrapper.add_genre(genre_name)
    genre_id = genre_obj.id
    author_obj = dbwrapper.get_book_author_id(author)
    if author_obj is None:
        dbwrapper.add_author(author)
        author_obj = dbwrapper.get_book_author_id(author)
    author_id = author_obj.id
    image_id = dbwrapper.get_image_id(image_url)
    return dbwrapper.add_book(name, author_id, barcode, quantity, image_id, description, genre_id)


def check_barcode_valid(barcode):
    return barcode.isdigit()


def issue_book(request):
    user_id = request.get("user_id")
    book_id = request.get("book_id")
    if user_id is None:
        return [3, None]  # MISSING_USER_ID
    elif book_id is None:
        return [4, None]  # MISSING_BOOK_ID
    if not dbwrapper.check_book_presence(book_id):
        return [1, None]  # UNKNOWN_USER_ID
    if not dbwrapper.check_user_presence(user_id):
        return [2, None]  # UNKNOWN_BOOK_ID
    if not dbwrapper.check_book_available(book_id):
        return [6, None]  # BOOK_NOT_AVAILABLE
    remove_from_cart(user_id, book_id)
    dbwrapper.subtract_book(book_id)
    return dbwrapper.give_book(user_id, book_id)


def return_book(issue_id):
    if not dbwrapper.check_issue_presence(issue_id):
        return 1  # UNKNOWN_ISSUE_ID
    book_id = dbwrapper.get_book_id_by_issue(issue_id)
    dbwrapper.increase_book(book_id)
    return dbwrapper.return_book(issue_id)


def add_to_cart(request):
    user_id = request.get("user_id")
    book_id = request.get("book_id")
    if user_id is None:
        return 3  # MISSING_USER_ID
    elif book_id is None:
        return 4  # MISSING_BOOK_ID
    if not dbwrapper.check_book_presence(book_id):
        return 2  # UNKNOWN_BOOK_ID
    if not dbwrapper.check_user_presence(user_id):
        return 1  # UNKNOWN_USER_ID
    user_cart = dbwrapper.get_user_cart(user_id)
    if user_cart is not None:
        books = user_cart.split(";")
        books.append(str(book_id))
        new_user_cart = ";".join(set(books))
    else:
        new_user_cart = str(book_id)
    return dbwrapper.set_user_cart(user_id, new_user_cart)


def remove_from_cart(user_id, book_id):
    user_cart = dbwrapper.get_user_cart(user_id)
    books = user_cart.split(";")
    try:
        del books[books.index(str(book_id))]
    except ValueError:
        return 5  # BOOK_IS_NOT_IN_CART
    new_user_cart = ";".join(set(books))
    return dbwrapper.set_user_cart(user_id, new_user_cart)


def delete_from_cart(request):
    user_id = request.get("user_id")
    book_id = request.get("book_id")
    if user_id is None:
        return 3  # MISSING_USER_ID
    elif book_id is None:
        return 4  # MISSING_BOOK_ID
    if not dbwrapper.check_book_presence(book_id):
        return 2  # UNKNOWN_BOOK_ID
    if not dbwrapper.check_user_presence(user_id):
        return 1  # UNKNOWN_USER_ID
    return remove_from_cart(user_id, book_id)


def get_issues(request):
    issue_status = request.args.get("issue_status")
    user_id = request.args.get("user_id")
    if issue_status is not None:
        issue_status_obj = dbwrapper.get_issue_status_is(issue_status)
        if issue_status_obj is None:
            return 3  # UNKNOWN_ISSUE_STATUS
        else:
            issue_status_id = issue_status_obj.id
    else:
        issue_status_id = issue_status  # set none
    if user_id is None:
        return 2  # MISSING_USER_ID
    if not dbwrapper.check_user_presence(user_id):
        return 1  # UNKNOWN_USER_ID
    user_issues = dbwrapper.get_issues(user_id, issue_status_id)
    issues = list()
    for issue_obj in user_issues:
        type = dbwrapper.get_issue_type_name(issue_obj.type)
        issues.append([issue_obj.id, issue_obj.book_id, str(issue_obj.date), type])
    return issues


def get_books_authors():
    authors = list()
    author_objects = dbwrapper.get_books_authors()
    for author_object in author_objects:
        authors.append([author_object.id, author_object.name])
    return authors


def breakdown_by_letters(authors):
    letters = {}
    sorted_authors = sorted(authors, key=lambda x: x[1])
    for author in sorted_authors:
        letter = author[1][0]
        if letter in letters:
            authors = letters[letter]
            authors.append({"id": author[0], "name": author[1]})
            letters[letter] = authors
        else:
            letters[letter] = [{"id": author[0], "name": author[1]}]
    print(letters)
    return letters


def get_author_data(author_id):
    books = dbwrapper.get_books_by_author(author_id)
    ids = ";".join([str(book.id) for book in books])
    name = dbwrapper.get_book_author_name(author_id)
    return (name, ids)


def get_genre_data(genre_id):
    books = dbwrapper.get_books_by_genre(genre_id)
    ids = ";".join([str(book.id) for book in books])
    name = dbwrapper.get_book_genre_name(genre_id)
    return (name, ids)
