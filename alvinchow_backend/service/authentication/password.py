from passlib.context import CryptContext


crypt_context = CryptContext(schemes=['argon2'])


def hash_password(password):
    return crypt_context.hash(password)


def verify_password(password, password_hash):
    return crypt_context.verify(password, password_hash)
