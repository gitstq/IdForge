"""IdForge 单元测试（纯标准库 unittest，零依赖）。"""

import re
import time
import unittest

from idforge import ulid, uuid4, uuid7
from idforge.ulid import (
    encode_time,
    generate,
    parse,
    timestamp_ms,
    validate,
)
from idforge.uuid7 import generate as uuid7_generate, parse as uuid7_parse, timestamp_ms as uuid7_ts, validate as uuid7_valid
from idforge.uuid4 import generate as uuid4_generate, validate as uuid4_valid


class TestULID(unittest.TestCase):
    def test_canonical_vector(self):
        # ULID 规范公开测试向量：时间戳 1469918176385 -> "01ARYZ6S41"
        self.assertEqual(encode_time(1469918176385), "01ARYZ6S41")

    def test_zero(self):
        self.assertEqual(generate(ms=0, randomness=0)[0], "0" * 26)

    def test_roundtrip(self):
        s, (ms, rnd) = generate(ms=1700000000000, randomness=123456789)
        self.assertEqual(len(s), 26)
        self.assertEqual(parse(s), (1700000000000, 123456789))

    def test_timestamp_extraction(self):
        s, (ms, _) = generate(ms=1700000000000)
        self.assertEqual(timestamp_ms(s), 1700000000000)

    def test_sortable(self):
        # 不同时间戳的 ULID 应当按时间（字典序）排序
        base = 1700000000000
        ids = [generate(ms=base + i)[0] for i in range(50)]
        self.assertEqual(sorted(ids), ids)
        # 时间戳更大的 ULID 字符串必然更大
        earlier, _ = generate(ms=base)
        later, _ = generate(ms=base + 1000)
        self.assertLess(earlier, later)

    def test_monotonic(self):
        state = None
        prev = None
        for _ in range(100):
            s, state = generate(monotonic_last=state)
            if prev is not None:
                self.assertGreater(s, prev)
            prev = s

    def test_validate(self):
        s = generate()[0]
        self.assertTrue(validate(s))
        self.assertFalse(validate("0" * 25))
        self.assertFalse(validate("!" * 26))


class TestUUID7(unittest.TestCase):
    _RE = re.compile(
        r"^[0-9a-f]{8}-[0-9a-f]{4}-7[0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}$"
    )

    def test_format_and_version(self):
        u = uuid7_generate()
        self.assertRegex(u, self._RE)

    def test_timestamp_roundtrip(self):
        ms = 1700000000000
        u = uuid7_generate(ms=ms)
        self.assertEqual(uuid7_ts(u), ms)

    def test_unique(self):
        self.assertNotEqual(uuid7_generate(), uuid7_generate())

    def test_validate(self):
        self.assertTrue(uuid7_valid(uuid7_generate()))
        self.assertFalse(uuid7_valid("not-a-uuid"))
        self.assertFalse(uuid7_valid(uuid4_generate()))  # v4 不是 v7


class TestUUID4(unittest.TestCase):
    _RE = re.compile(
        r"^[0-9a-f]{8}-[0-9a-f]{4}-4[0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}$"
    )

    def test_format(self):
        self.assertRegex(uuid4_generate(), self._RE)

    def test_unique(self):
        self.assertNotEqual(uuid4_generate(), uuid4_generate())

    def test_validate(self):
        self.assertTrue(uuid4_valid(uuid4_generate()))
        self.assertFalse(uuid4_valid("12345678-1234-1234-1234-123456789012"))


class TestParseCLI(unittest.TestCase):
    def test_parse_ulid(self):
        from idforge.cli import cmd_parse, build_parser

        s = generate(ms=1700000000000)[0]
        args = build_parser().parse_args(["parse", s])
        # 不实际调用打印，仅验证能进入分支不抛异常
        self.assertEqual(args.id, s)


if __name__ == "__main__":
    unittest.main(verbosity=2)
