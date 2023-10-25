import hashlib


def key_builder(index: str, params: dict) -> str:
    return hashlib.md5(f'{index}:{params}'.encode()).hexdigest()
