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


if __name__ == '__main__':
    main()
