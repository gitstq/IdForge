"""ULID 实现（RFC 都不存在，但遵循广泛采用的 ULID 规范）。

ULID = 26 字符 Crockford Base32：
- 前 10 字符：48 位毫秒时间戳（按字典序可排序）
- 后 16 字符：80 位随机熵

特性：按字符串排序 == 按时间排序；可解析出创建时间戳。
"""

import time

from ._random import random_bytes

_CROCKFORD = "0123456789ABCDEFGHJKMNPQRSTVWXYZ"
_ENCODE = _CROCKFORD
# 解码表：标准 Crockford 仅含 32 个字符；为容错额外接受 I/L->1, O->0, U->2
_DECODE = {c: i for i, c in enumerate(_CROCKFORD)}
_DECODE.update({"I": 1, "L": 1, "O": 0, "U": 2})


def _encode_base32(value: int, length: int) -> str:
    chars = []
    for i in range(length - 1, -1, -1):
        chars.append(_ENCODE[(value >> (i * 5)) & 0x1F])
    return "".join(chars)


def _decode_base32(s: str) -> int:
    value = 0
    for ch in s:
        value = (value << 5) | _DECODE[ch]
    return value


def encode_time(ms: int) -> str:
    return _encode_base32(ms, 10)


def encode_random(rand80: int) -> str:
    return _encode_base32(rand80, 16)


def generate(ms: int | None = None, randomness: int | None = None,
             monotonic_last: tuple | None = None) -> tuple:
    """生成一个 ULID 字符串。

    返回 (ulid_str, (timestamp_ms, randomness))，便于单调模式维护状态。
    monotonic_last: 上一轮的 (ms, randomness)，用于保证同一毫秒内严格递增。
    """
    if ms is None:
        ms = int(time.time() * 1000)
    if randomness is None:
        randomness = int.from_bytes(random_bytes(10), "big")  # 80 bit

    if monotonic_last is not None:
        last_ms, last_rand = monotonic_last
        if ms <= last_ms:
            ms = last_ms
            randomness = max(randomness, last_rand + 1)
            if randomness >= (1 << 80):
                ms += 1
                randomness = 0

    ulid_str = encode_time(ms) + encode_random(randomness)
    return ulid_str, (ms, randomness)


def parse(ulid: str) -> tuple:
    """解析 ULID，返回 (timestamp_ms, randomness)。"""
    if not isinstance(ulid, str) or len(ulid) != 26:
        raise ValueError("ULID 必须为 26 个字符")
    upper = ulid.upper()
    try:
        ms = _decode_base32(upper[:10])
        rand = _decode_base32(upper[10:])
    except KeyError as e:
        raise ValueError(f"ULID 含非法字符: {e}") from e
    return ms, rand


def timestamp_ms(ulid: str) -> int:
    return parse(ulid)[0]


def validate(ulid: str) -> bool:
    try:
        parse(ulid)
        return True
    except ValueError:
        return False
