import re


def is_valid_username(username):
    if len(username) > 20 or len(username) < 8:
        return False
    if not re.match(r"(^[a-zA-Z0-9]+([_-]?[a-zA-Z0-9])*$)", username):
        return False
    return True


def is_valid_email(email):
    return re.match(r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)", email)


def is_valid_password(password):
    return len(password) >= 8
