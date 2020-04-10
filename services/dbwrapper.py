from data.db_session import create_session
from models import users
from models import user_types


def get_password_hash(login):
    session = create_session()
    cursor = users.User  # Shortening the path to user
    user = session.query(cursor).filter(cursor.login == login).first()
    if user is None:
        return 2  # UNKNOWN_LOGIN
    return user.hashed_password


def get_user_info(login):
    session = create_session()
    cursor = users.User  # Shortening the path to user
    user = session.query(cursor).filter(cursor.login == login).first()
    return user.id, user.name, user.surname, user.type_id, user.cart


def get_user_type(type_id):
    session = create_session()
    cursor = user_types.UserType  # Shortening the path to user type
    type_obj = session.query(cursor).filter(cursor.id == type_id).first()
    return type_obj.name
