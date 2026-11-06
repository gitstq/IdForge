"""UUID v7 实现（RFC 9562）。

布局（128 bit）：
- 48 bit：unix 毫秒时间戳（unix_ts_ms）
- 4 bit：版本号 = 0b0111 (7)
- 12 bit：rand_a
- 2 bit：变体位 = 0b10
- 62 bit：rand_b

按时间排序，时间戳可直接解析。
"""

import time

from ._random import random_bytes

_VERSION = 0x7
_VARIANT = 0b10


def _build(ms: int, rng: int) -> int:
    rand_a = (rng >> 62) & 0xFFF
    rand_b = rng & ((1 << 62) - 1)
    value = (ms << 80) | (_VERSION << 76) | (rand_a << 64) \
        | (_VARIANT << 62) | rand_b
    return value


def _format(value: int) -> str:
    h = f"{value:032x}"
    return f"{h[0:8]}-{h[8:12]}-{h[12:16]}-{h[16:20]}-{h[20:32]}"


def generate(ms: int | None = None, rng: int | None = None) -> str:
    if ms is None:
        ms = int(time.time() * 1000)
    if rng is None:
        rng = int.from_bytes(random_bytes(10), "big")  # 80 bit，取高 74 位
    return _format(_build(ms, rng))


def parse(uuid: str) -> tuple:
    """解析 UUIDv7，返回 (timestamp_ms, int_value)。"""
    norm = uuid.replace("-", "").lower()
    if len(norm) != 32 or any(c not in "0123456789abcdef" for c in norm):
        raise ValueError("UUID 格式非法")
    value = int(norm, 16)
    version = (value >> 76) & 0xF
    if version != _VERSION:
        raise ValueError(f"非 UUIDv7（版本={version}）")
    ts = value >> 80
    return ts, value


def timestamp_ms(uuid: str) -> int:
    return parse(uuid)[0]


def validate(uuid: str) -> bool:
    try:
        parse(uuid)
        return True
    except ValueError:
        return False
