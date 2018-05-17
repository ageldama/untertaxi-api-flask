import hashlib


def digested_str(password: str) -> str:
    m = hashlib.sha256()
    m.update(password.encode())
    return m.hexdigest()


def eq(hash_hex: str, password: str) -> bool:
    hash2 = digested_str(password)
    return hash_hex == hash2
