from flask import Flask, request, redirect
import logging
import sys
from services import handler, dbwrapper
from data import db_session
import json
import os
import datetime

app = Flask(__name__)
app.config['SECRET_KEY'] = 'booker_secret_key'
logging.basicConfig(level=logging.INFO, filemode="w", stream=sys.stdout)
base_name = "db/bookertest.sqlite"


def main():
    logging.info("Program start.")
    logging.info("Connect to base - " + base_name)
    db_session.global_init(base_name)
    logging.info("Connect successful")
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
    logging.info("Exit program.")


@app.route('/login', methods=['GET'])
def login():
    authentication_statuses = {0: "SUCCESS", 1: "INVALID_PASSWORD",
                               2: "UNKNOWN_LOGIN", 3: "MISSING_LOGIN",
                               4: "MISSING_PASSWORD_HASH", 5: "MISSING_ARGUMENTS"}
    response = dict()
    request_json = request.json
    log_request("/login", "GET", request_json)
    if request_json is None:
        response["authentication_status"] = authentication_statuses[5]
        log_response(json.dumps(response))
        return json.dumps(response)
    authentication_status = handler.authenticate(request_json)
    response["authentication_status"] = authentication_statuses[authentication_status]
    if authentication_status != 0:
        log_response(json.dumps(response))
        return json.dumps(response)
    user_login = request_json["user"]["login"]
    user_id = dbwrapper.get_user_id(user_login)
    user_id, user_login, user_name, user_surname, user_type, user_cart = handler.get_user_data(user_id)
    response["user"] = {"id": user_id,
                        "login": user_login,
                        "name": user_name,
                        "surname": user_surname,
                        "type": user_type,
                        "cart": user_cart}
    log_response(json.dumps(response))
    return json.dumps(response)


@app.route('/registration', methods=['POST'])
def registration():
    registration_statuses = {0: "SUCCESS", 1: "INVALID_EMAIL",
                             2: "LOGIN_REPLAY", 3: "MISSING_LOGIN",
                             4: "MISSING_NAME", 5: "MISSING_SURNAME",
                             6: "MISSING_PASSWORD_HASH", 7: "MISSING_EMAIL",
                             8: "MISSING_ARGUMENTS", 9: "MISSING_TYPE", 10: "INVALID_TYPE"}
    response = dict()
    request_json = request.json
    log_request("/registration", "POST", request.json)
    if request_json is None:
        response["authentication_status"] = registration_statuses[8]
        log_response(json.dumps(response))
        return json.dumps(response)
    registration_status, user_id = handler.registration(request_json)
    response["authentication_status"] = registration_statuses[registration_status]
    if registration_status != 0:
        log_response(json.dumps(response))
        return json.dumps(response)
    response["user"] = {"id": user_id}
    log_response(json.dumps(response))
    return json.dumps(response)


@app.route('/book/genres', methods=['GET'])
def get_genres():
    log_request("/book/genres", "GET", 'null')
    request_args = request.args
    letters = request_args.get("letters")
    response = dict()
    genres = handler.get_books_genres(request_args)
    response["amount"] = len(genres)
    if letters is None:
        response["genres"] = [{"id": author[0], "name": author[1]} for author in genres]
    else:
        breakdown_authors = handler.breakdown_by_letters(genres)
        print(breakdown_authors)
        response["genres"] = {letter: breakdown_authors[letter] for letter in breakdown_authors}
    log_response(json.dumps(response))
    return json.dumps(response)


@app.route('/book/authors', methods=['GET'])
def get_authors():
    log_request("/book/authors", "GET", 'null')
    letters = request.args.get("letters")
    response = dict()
    authors = handler.get_books_authors()
    response["amount"] = len(authors)
    if letters is None:
        response["authors"] = [{"id": author[0], "name": author[1]} for author in authors]
    else:
        breakdown_authors = handler.breakdown_by_letters(authors)
        response["authors"] = {letter: breakdown_authors[letter] for letter in breakdown_authors}
    log_response(json.dumps(response))
    return json.dumps(response)


@app.route('/books', methods=['GET'])
def get_books():
    response = dict()
    errors = {1: "UNKNOWN_GENRE", 2: "UNKNOWN_AUTHOR"}
    request_args = request.args
    only_amount = request_args.get("onlyAmount")
    log_request("/books", "GET", request_args)
    books = handler.get_books(request_args)
    if str(books).isdigit():
        response["error"] = errors[books]
        log_response(json.dumps(response))
        return json.dumps(response)
    response["amount"] = len(books)
    if only_amount is not None:
        log_response(json.dumps(response))
        return json.dumps(response)
    response["books"] = [
        {"id": book[0], "genre": book[1], "name": book[2], "author": book[3], "barcode": book[4], "quantity": book[5],
         "description": book[6], "image_url": book[7], "icon_url": book[8]}
        for book in books]
    log_response(json.dumps(response))
    return json.dumps(response)


@app.route('/book/<id>', methods=['GET'])
def get_book(id):
    log_request("/book/<id>", "GET", id)
    response = dict()
    book = handler.get_book(id)
    if book == 1:
        response["error"] = "UNKNOWN_BOOK_ID"
        log_response(json.dumps(response))
        return json.dumps(response)
    response["book"] = {"id": book[0],
                        "genre": book[1],
                        "name": book[2],
                        "author": book[3],
                        "barcode": book[4],
                        "quantity": book[5],
                        "description": book[6],
                        "image_url": book[7],
                        "icon_url": book[8]}
    log_response(json.dumps(response))
    return json.dumps(response)


@app.route('/book', methods=['POST'])
def add_book():
    statuses_of_the_add = {0: "SUCCESS", 1: "INVALID_BARCODE",
                           2: "BARCODE_REPLAY", 3: "MISSING_NAME",
                           4: "MISSING_AUTHOR", 5: "MISSING_BARCODE",
                           6: "MISSING_QUANTITY", 7: "MISSING_ARGUMENTS",
                           8: "MISSING_GENRE", 9: "MISSING_DESCRIPTION"}
    response = dict()
    request_json = request.json
    log_request("/book", "POST", request_json)
    if request_json is None:
        response["authentication_status"] = statuses_of_the_add[7]
        log_response(json.dumps(response))
        return json.dumps(response)
    add_book_status, book_id = handler.add_book(request_json)
    response["add_status"] = statuses_of_the_add[add_book_status]
    if add_book_status != 0:
        log_response(json.dumps(response))
        return json.dumps(response)
    response["book"] = {"id": book_id}
    log_response(json.dumps(response))
    return json.dumps(response)


@app.route('/issue/', methods=['PUT'])
def issue():
    issued_statuses = {0: "SUCCESS", 1: "UNKNOWN_USER_ID",
                       2: "UNKNOWN_BOOK_ID", 3: "MISSING_USER_ID",
                       4: "MISSING_BOOK_ID", 5: "MISSING_ARGUMENTS",
                       6: "BOOK_NOT_AVAILABLE"}
    response = dict()
    request_args = request.args
    log_request("/issue", "PUT", request_args)
    issue_status, issue_id = handler.issue_book(request_args)
    response["issue_status"] = issued_statuses[issue_status]
    if issue_status != 0:
        log_response(json.dumps(response))
        return json.dumps(response)
    response["issue_id"] = issue_id
    log_response(json.dumps(response))
    return json.dumps(response)


@app.route('/issue/return/<issue_id>', methods=['POST'])
def return_book(issue_id):
    log_request("/issue/return/<issue_id>", "POST", issue_id)
    return_statuses = {0: "SUCCESS", 1: "UNKNOWN_ISSUE_ID"}
    response = dict()
    return_status = handler.return_book(issue_id)
    response["return_status"] = return_statuses[return_status]
    log_response(json.dumps(response))
    return json.dumps(response)


@app.route('/cart', methods=['POST'])
def add_boot_to_cart():
    add_to_cart_statuses = {0: "SUCCESS", 1: "UNKNOWN_USER_ID",
                            2: "UNKNOWN_BOOK_ID", 3: "MISSING_USER_ID",
                            4: "MISSING_BOOK_ID", 5: "MISSING_ARGUMENTS"}
    response = dict()
    request_json = request.json
    log_request("/cart", "POST", request_json)
    if request_json is None:
        response["add_status"] = add_to_cart_statuses[5]
        log_response(json.dumps(response))
        return json.dumps(response)
    add_to_cart_status = handler.add_to_cart(request.json)
    response["add_status"] = add_to_cart_statuses[add_to_cart_status]
    log_response(json.dumps(response))
    return json.dumps(response)


@app.route('/user/<user_id>', methods=['GET'])
def get_user_data(user_id):
    log_request("/user/<user_id>", "GET", user_id)
    response = dict()
    if not dbwrapper.check_user_presence(user_id):
        response["error"] = "UNKNOWN_USER_ID"
        log_response(json.dumps(response))
        return json.dumps(response)
    user_id, user_login, user_name, user_surname, user_type, user_cart = handler.get_user_data(user_id)
    response["user"] = {"id": user_id,
                        "login": user_login,
                        "name": user_name,
                        "surname": user_surname,
                        "type": user_type,
                        "cart": user_cart}
    log_response(json.dumps(response))
    return json.dumps(response)


@app.route('/author/<author_id>', methods=['GET'])
def get_author_data(author_id):
    log_request("/author/<author_id>", "GET", author_id)
    response = dict()
    if not dbwrapper.check_author_presence(author_id):
        response["error"] = "UNKNOWN_AUTHOR_ID"
        log_response(json.dumps(response))
        return json.dumps(response)
    author_name, books_id = handler.get_author_data(author_id)
    response["author"] = {"id": author_id,
                          "name": author_name,
                          "books": books_id}
    log_response(json.dumps(response))
    return json.dumps(response)


@app.route('/genre/<genre_id>', methods=['GET'])
def get_genre_data(genre_id):
    log_request("/author/<author_id>", "GET", genre_id)
    response = dict()
    if not dbwrapper.check_genre_presence(genre_id):
        response["error"] = "UNKNOWN_GENRE_ID"
        log_response(json.dumps(response))
        return json.dumps(response)
    author_name, books_id = handler.get_genre_data(genre_id)
    response["genre"] = {"id": genre_id,
                         "name": author_name,
                         "books": books_id}
    log_response(json.dumps(response))
    return json.dumps(response)


@app.route('/cart', methods=["PUT", 'DELETE'])
def cart():
    if request.method == "PUT":
        request_args = request.args
        log_request("/cart", "PUT", request_args)
        add_to_cart_statuses = {0: "SUCCESS", 1: "UNKNOWN_USER_ID",
                                2: "UNKNOWN_BOOK_ID", 3: "MISSING_USER_ID",
                                4: "MISSING_BOOK_ID", 5: "BOOK_NOT_AVAILABLE"}
        response = dict()
        add_to_cart_status = handler.add_to_cart(request_args)
        response["add_status"] = add_to_cart_statuses[add_to_cart_status]
        log_response(json.dumps(response))
        return json.dumps(response)
    elif request.method == "DELETE":
        request_args = request.args
        log_request("/cart", "DELETE", request_args)
        add_to_cart_statuses = {0: "SUCCESS", 1: "UNKNOWN_USER_ID",
                                2: "UNKNOWN_BOOK_ID", 3: "MISSING_USER_ID",
                                4: "MISSING_BOOK_ID", 5: "BOOK_IS_NOT_IN_CART"}
        response = dict()
        add_to_cart_status = handler.delete_from_cart(request_args)
        response["delete_status"] = add_to_cart_statuses[add_to_cart_status]
        log_response(json.dumps(response))
        return json.dumps(response)


@app.route('/issues', methods=['GET'])
def get_issues():
    response = dict()
    request_args = request.args
    log_request("/issues", "GET", request_args)
    error_codes = {1: "UNKNOWN_USER_ID", 2: "MISSING_USER_ID", 3: "UNKNOWN_ISSUE_STATUS", 4: "MISSING_ARGUMENTS"}
    if request_args is None:
        response["error"] = error_codes[4]
        log_response(json.dumps(response))
        return json.dumps(response)
    issues = handler.get_issues(request)
    try:
        response["error"] = error_codes[issues]
    except TypeError:
        response["amount"] = len(issues)
        response["issues"] = [
            {"id": issue[0], "book_id": issue[1], "date": issue[2], "type": issue[3]} for issue in issues]
    log_response(json.dumps(response))
    return json.dumps(response)


@app.route('/documentation')
@app.route('/docs')
@app.route('/index')
@app.route('/')
def redirect_to_documentation():
    logging.info("--------------------")
    logging.info("-REDIRECT TO DOCS-")
    logging.info("--------------------")
    return redirect("https://www.notion.so/Booker-API-96e582c8325b40948997babe674acac1")


@app.route('/git')
def redirect_to_git():
    logging.info("--------------------")
    logging.info("-REDIRECT TO GIT-")
    logging.info("--------------------")
    return redirect("https://github.com/PetrSed/Booker-API")


def log_request(address, method, request_data):
    logging.info("--------------------")
    logging.info(f"New Request to {address}. Method: {method}")
    logging.info(f"Request time: {datetime.datetime.now()}")
    logging.info(
        f"Request data: {str(request_data)}")


def log_response(response_data):
    logging.info(
        f"Response data: {str(response_data)[:80]}")
    logging.info(f"Response time: {datetime.datetime.now()}")
    logging.info("--------------------")


if __name__ == '__main__':
    main()
