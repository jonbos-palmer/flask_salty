import hashlib, uuid

def hash_pass(password):
    return hashlib.sha512(password).hexdigest()

def salt_gen():
    return uuid.uuid4().hex

def verify_password(password, salt, hashed_pass):
    return hash_pass(str.encode(password+salt))== hashed_pass