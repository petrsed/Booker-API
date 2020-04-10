from flask import Flask, request
import logging
import sys
from services import handler, dbwrapper
from data import db_session
import json

app = Flask(__name__)
app.config['SECRET_KEY'] = 'booker_secret_key'


def main():
    logging.basicConfig(stream=sys.stdout, level=logging.INFO)
    logging.info("Program start.")
    db_session.global_init("db/booker.sqlite")
    app.run()
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
    user_id, user_name, user_surname, user_type, user_cart = handler.get_user_data(user_login)
    response["user"] = {"id": user_id,
                        "name": user_name,
                        "surname": user_surname,
                        "type": user_type,
                        "cart": user_cart}
    return json.dumps(response)


@app.route('/registration', methods=['PUT'])
def registration():
    registration_statuses = {0: "SUCCESS", 1: "INVALID_EMAIL",
                             2: "LOGIN_REPLAY", 3: "MISSING_LOGIN",
                             4: "MISSING_NAME", 5: "MISSING_SURNAME",
                             6: "MISSING_PASSWORD_HASH", 7: "MISSING_EMAIL",
                             8: "MISSING_ARGUMENTS", 9: "MISSING_TYPE", 10: "INVALID_TYPE"}
    response = dict()
    logging.info(f'Request: {request.json!r}')
    registration_status = handler.registration(request.json)
    response["authentication_status"] = registration_statuses[registration_status]
    if registration_status != 0:
        return json.dumps(response)
    user_login = request.json["user"]["login"]
    user_id = dbwrapper.get_user_id(user_login)
    response["user"] = {"id": user_id}
    return json.dumps(response)


@app.route('/book/genres', methods=['GET'])
def get_genres():
    response = dict()
    genres = handler.get_books_genres()
    response["amount"] = len(genres)
    response["genres"] = [{"id": genre[0], "name": genre[1]} for genre in genres]
    return json.dumps(response)


@app.route('/book', methods=['GET'])
def get_books():
    response = dict()
    books = handler.get_books(request.json)
    if books == 1:
        response["error"] = "UNKNOWN_GENRE"
        return json.dumps(response)
    response["amount"] = len(books)
    response["books"] = [
        {"id": book[0], "genre": book[1], "name": book[2], "author": book[3], "barcode": book[4], "quantity": book[5]}
        for book in books]
    return json.dumps(response)


if __name__ == '__main__':
    main()
