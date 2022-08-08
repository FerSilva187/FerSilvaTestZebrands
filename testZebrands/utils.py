def random_password(length, 
allowed_chars = 'abcdefghjkmnpqrstuvwxyzABCDEFGHJKLMNPQRSTUVWXYZ23456789'):
    "Generates a random password with the given length and given allowed_chars"
    from random import choice
    return ''.join([choice(allowed_chars) for i in range(length)])
