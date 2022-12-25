def validate_password(password):
    if len(password) < 8 :
        raise ValueError('Password Must be more than 8 characters')
    return password

