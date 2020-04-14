from flask import Flask, request
import logging
import sys
from services import handler, dbwrapper
from data import db_session
import json
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = 'booker_secret_key'


def main():
    logging.basicConfig(stream=sys.stdout, level=logging.INFO)
    logging.info("Program start.")
    db_session.global_init("db/bookertest.sqlite")
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
    logging.info("Exit program.")


@app.route('/login', methods=['GET'])
def login():
    authentication_statuses = {0: "SUCCESS", 1: "INVALID_PASSWORD",
                               2: "UNKNOWN_LOGIN", 3: "MISSING_LOGIN",
                               4: "MISSING_PASSWORD_HASH", 5: "MISSING_ARGUMENTS"}
    response = dict()
    logging.info(f'Request: {request.json!r}')
    authentication_status = handler.authenticate(request.json)
    response["authentication_status"] = authentication_statuses[authentication_status]
    if authentication_status != 0:
        return json.dumps(response)
    user_login = request.json["user"]["login"]
    user_id = dbwrapper.get_user_id(user_login)
    user_id, user_login, user_name, user_surname, user_type, user_cart = handler.get_user_data(user_id)
    response["user"] = {"id": user_id,
                        "login": user_login,
                        "name": user_name,
                        "surname": user_surname,
                        "type": user_type,
                        "cart": user_cart}
    return json.dumps(response)


@app.route('/registration', methods=['POST'])
def registration():
    registration_statuses = {0: "SUCCESS", 1: "INVALID_EMAIL",
                             2: "LOGIN_REPLAY", 3: "MISSING_LOGIN",
                             4: "MISSING_NAME", 5: "MISSING_SURNAME",
                             6: "MISSING_PASSWORD_HASH", 7: "MISSING_EMAIL",
                             8: "MISSING_ARGUMENTS", 9: "MISSING_TYPE", 10: "INVALID_TYPE"}
    response = dict()
    logging.info(f'Request: {request.json!r}')
    registration_status, user_id = handler.registration(request.json)
    response["authentication_status"] = registration_statuses[registration_status]
    if registration_status != 0:
        return json.dumps(response)
    response["user"] = {"id": user_id}
    return json.dumps(response)


@app.route('/book/genres', methods=['GET'])
def get_genres():
    response = dict()
    genres = handler.get_books_genres()
    response["amount"] = len(genres)
    response["genres"] = [{"id": genre[0], "name": genre[1]} for genre in genres]
    return json.dumps(response)


@app.route('/books', methods=['GET'])
def get_books():
    response = dict()
    books = handler.get_books(request)
    if books == 1:
        response["error"] = "UNKNOWN_GENRE"
        return json.dumps(response)
    response["amount"] = len(books)
    response["books"] = [
        {"id": book[0], "genre": book[1], "name": book[2], "author": book[3], "barcode": book[4], "quantity": book[5]}
        for book in books]
    return json.dumps(response)


@app.route('/book/<id>', methods=['GET'])
def get_book(id):
    response = dict()
    book = handler.get_book(id)
    if book == 1:
        response["error"] = "UNKNOWN_BOOK_ID"
        return json.dumps(response)
    response["book"] = {"id": book[0],
                        "genre": book[1],
                        "name": book[2],
                        "author": book[3],
                        "barcode": book[4],
                        "quantity": book[5]}
    return json.dumps(response)


@app.route('/book', methods=['POST'])
def add_book():
    statuses_of_the_add = {0: "SUCCESS", 1: "INVALID_BARCODE",
                           2: "BARCODE_REPLAY", 3: "MISSING_NAME",
                           4: "MISSING_AUTHOR", 5: "MISSING_BARCODE",
                           6: "MISSING_QUANTITY", 7: "MISSING_ARGUMENTS"}
    response = dict()
    logging.info(f'Request: {request.json!r}')
    add_book_status, book_id = handler.add_book(request.json)
    response["add_status"] = statuses_of_the_add[add_book_status]
    if add_book_status != 0:
        return json.dumps(response)
    response["book"] = {"id": book_id}
    return json.dumps(response)


@app.route('/issue/', methods=['POST'])
def issue():
    issued_statuses = {0: "SUCCESS", 1: "UNKNOWN_USER_ID",
                       2: "UNKNOWN_BOOK_ID", 3: "MISSING_USER_ID",
                       4: "MISSING_BOOK_ID"}
    response = dict()
    logging.info(f'Request: {request.json!r}')
    issue_status, issue_id = handler.issue_book(request.json)
    response["issue_status"] = issued_statuses[issue_status]
    if issue_status != 0:
        return json.dumps(response)
    response["issue_id"] = issue_id
    return json.dumps(response)


@app.route('/issue/return/<issue_id>', methods=['POST'])
def return_book(issue_id):
    return_statuses = {0: "SUCCESS", 1: "UNKNOWN_ISSUE_ID"}
    response = dict()
    return_status = handler.return_book(issue_id)
    response["return_status"] = return_statuses[return_status]
    return json.dumps(response)


@app.route('/cart', methods=['POST'])
def add_boot_to_cart():
    add_to_cart_statuses = {0: "SUCCESS", 1: "UNKNOWN_USER_ID",
                            2: "UNKNOWN_BOOK_ID", 3: "MISSING_USER_ID",
                            4: "MISSING_BOOK_ID"}
    response = dict()
    logging.info(f'Request: {request.json!r}')
    add_to_cart_status = handler.add_to_cart(request.json)
    response["add_status"] = add_to_cart_statuses[add_to_cart_status]
    return json.dumps(response)


@app.route('/user/<user_id>', methods=['GET'])
def get_user_data(user_id):
    response = dict()
    user_id, user_login, user_name, user_surname, user_type, user_cart = handler.get_user_data(user_id)
    response["user"] = {"id": user_id,
                        "login": user_login,
                        "name": user_name,
                        "surname": user_surname,
                        "type": user_type,
                        "cart": user_cart}
    return json.dumps(response)


@app.route('/cart', methods=["POST", 'DELETE'])
def cart():
    if request.method == "POST":
        add_to_cart_statuses = {0: "SUCCESS", 1: "UNKNOWN_USER_ID",
                                2: "UNKNOWN_BOOK_ID", 3: "MISSING_USER_ID",
                                4: "MISSING_BOOK_ID"}
        response = dict()
        logging.info(f'Request: {request.json!r}')
        add_to_cart_status = handler.add_to_cart(request.json)
        response["add_status"] = add_to_cart_statuses[add_to_cart_status]
        return json.dumps(response)
    elif request.method == "DELETE":
        add_to_cart_statuses = {0: "SUCCESS", 1: "UNKNOWN_USER_ID",
                                2: "UNKNOWN_BOOK_ID", 3: "MISSING_USER_ID",
                                4: "MISSING_BOOK_ID", 5: "BOOK_IS_NOT_IN_CART"}
        response = dict()
        add_to_cart_status = handler.delete_from_cart(request.args)
        response["delete_status"] = add_to_cart_statuses[add_to_cart_status]
        return json.dumps(response)


@app.route('/issues', methods=['GET'])
def get_issues():
    error_codes = {1: "UNKNOWN_USER_ID", 2: "MISSING_USER_ID", 3: "UNKNOWN_ISSUE_STATUS"}
    response = dict()
    issues = handler.get_issues(request)
    try:
        response["error"] = error_codes[issues]
    except TypeError:
        response["amount"] = len(issues)
        response["issues"] = [
            {"id": issue[0], "book_id": issue[1], "date": issue[2], "type": issue[3]} for issue in issues]
    return json.dumps(response)


if __name__ == '__main__':
    main()
