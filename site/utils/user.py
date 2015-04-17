import hashlib

def make_username(first_name, last_name, email):

    hash_user = hashlib.sha1()

    hash_user.update("-".join([first_name, last_name, email]))
    username = hash_user.hexdigest()

    return username
