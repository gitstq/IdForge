"""IdForge —— 零依赖·可排序唯一 ID 生成引擎。

纯 Python 标准库实现，支持三种主流可排序 / 随机唯一标识符：
- ULID     ：26 字符 Crockford Base32，时间可排序
- UUID v7  ：RFC 9562，毫秒时间戳 + 随机，时间可排序
- UUID v4  ：RFC 4122，纯随机

全部离线、零第三方依赖、密码学安全随机源。
"""

from .ulid import generate as ulid, parse as parse_ulid, timestamp_ms as ulid_ts, validate as validate_ulid
from .uuid7 import generate as uuid7, parse as parse_uuid7, timestamp_ms as uuid7_ts, validate as validate_uuid7
from .uuid4 import generate as uuid4, validate as validate_uuid4

__version__ = "1.0.0"

__all__ = [
    "ulid", "parse_ulid", "ulid_ts", "validate_ulid",
    "uuid7", "parse_uuid7", "uuid7_ts", "validate_uuid7",
    "uuid4", "validate_uuid4",
    "__version__",
]
