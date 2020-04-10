from . import dbwrapper


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
