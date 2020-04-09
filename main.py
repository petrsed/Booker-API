from flask import Flask
from data import db_session
import logging
import sys



app = Flask(__name__)
app.config['SECRET_KEY'] = 'booker_secret_key'


def main():
    logging.basicConfig(stream=sys.stdout, level=logging.INFO)
    logging.info("Program start")
    db_session.global_init("db/booker.sqlite")
    app.run()


if __name__ == '__main__':
    main()