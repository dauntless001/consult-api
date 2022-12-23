import re

def validate_email(email):
    regex = "^[a-zA-Z0-9-_]+@[a-zA-Z0-9]+\.[a-z]{1,3}$"
    if not re.match(regex,email):
        raise ValueError('Invalid Email')
    return email

def validate_password(password):
    if len(password) < 8 :
        raise ValueError('Password Must be more than 8 characters')
    return password

