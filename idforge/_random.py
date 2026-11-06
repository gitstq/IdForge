"""安全随机源封装（密码学安全，纯标准库）。"""

import secrets


def random_bytes(n: int) -> bytes:
    """返回 n 个密码学安全的随机字节。"""
    return secrets.token_bytes(n)
