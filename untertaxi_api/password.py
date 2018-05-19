import hashlib


def hash_password(password: str, secret_key: str) -> str:
    m = hashlib.sha256()
    m.update(secret_key.encode())
    m.update(password.encode())
    return m.hexdigest()
