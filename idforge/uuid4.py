"""UUID v4 实现（RFC 4122），纯标准库、随机版本。"""

from ._random import random_bytes


def _format(value: int) -> str:
    h = f"{value:032x}"
    return f"{h[0:8]}-{h[8:12]}-{h[12:16]}-{h[16:20]}-{h[20:32]}"


def generate() -> str:
    b = bytearray(random_bytes(16))
    # 版本 4（位 6 高 4 位 = 0100）
    b[6] = (b[6] & 0x0F) | 0x40
    # 变体 RFC 4122（位 8 高 2 位 = 10）
    b[8] = (b[8] & 0x3F) | 0x80
    return _format(int.from_bytes(b, "big"))


def validate(uuid: str) -> bool:
    norm = uuid.replace("-", "").lower()
    if len(norm) != 32 or any(c not in "0123456789abcdef" for c in norm):
        return False
    return norm[12] == "4" and norm[16] in "89ab"
