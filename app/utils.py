import hashlib


def shorten_url(url: str) -> str:
    hash_object = hashlib.md5(url.encode())
    return hash_object.hexdigest()[:8]
