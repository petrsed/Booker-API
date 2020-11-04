from config import MySQL
from services import dbwrapper
import logging
import sys
import pymysql
import os


def get_commands(filename):
    with open(filename, "r") as sql_file:
        return [command.replace("\n", "") for command in sql_file.read().split(';')]


def get_files():
    current_path = os.path.abspath(os.curdir)
    db_scripts_path = current_path.split("\\")
    db_scripts_path = db_scripts_path[:len(db_scripts_path) - 1]
    db_scripts_path.append("db")
    db_scripts_path = "\\".join(db_scripts_path)
    files = os.listdir(db_scripts_path)
    return [f"{db_scripts_path}\\{file}" for file in files]


def init():
    db = pymysql.connect(MySQL.MYSQL_DB_ADDRESS, MySQL.MYSQL_DB_USER, MySQL.MYSQL_DB_PASSWORD, MySQL.MYSQL_DB_NAME)
    cursor = db.cursor()
    for file in get_files():
        if not file.endswith(".sql"):
            continue
        for command in get_commands(file):
            if command != '':
                print(command)
                cursor.execute(command)
    db.commit()


def main():
    logging.info("Script start.")
    dbwrapper.check_connection()
    init()
    logging.info("Script exits.")


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO, filemode="w", stream=sys.stdout)
    main()
