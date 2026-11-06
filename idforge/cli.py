"""IdForge 命令行入口。

子命令：
  idforge ulid   [--monotonic] [--count N]
  idforge uuid7  [--count N]
  idforge uuid4  [--count N]
  idforge parse  <id>            检测类型并解析时间戳
"""

import argparse
import sys
import time

from . import ulid, uuid4, uuid7
from .ulid import validate as ulid_valid, timestamp_ms as ulid_ts
from .uuid7 import validate as uuid7_valid, timestamp_ms as uuid7_ts
from .uuid4 import validate as uuid4_valid


def _emit(values):
    for v in values:
        print(v)


def cmd_ulid(args):
    if args.monotonic:
        state = None
        out = []
        for _ in range(args.count):
            s, state = ulid(monotonic_last=state)
            out.append(s)
        _emit(out)
    else:
        _emit([ulid()[0] for _ in range(args.count)])
    return 0


def cmd_uuid7(args):
    _emit([uuid7() for _ in range(args.count)])
    return 0


def cmd_uuid4(args):
    _emit([uuid4() for _ in range(args.count)])
    return 0


def cmd_parse(args):
    ident = args.id.strip()
    if ulid_valid(ident):
        ts = ulid_ts(ident)
        print(f"type : ULID")
        print(f"time : {ts} ms  ({time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime(ts / 1000))} UTC)")
        return 0
    if uuid7_valid(ident):
        ts = uuid7_ts(ident)
        print(f"type : UUIDv7")
        print(f"time : {ts} ms  ({time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime(ts / 1000))} UTC)")
        return 0
    if uuid4_valid(ident):
        print("type : UUIDv4 (random, no embedded timestamp)")
        return 0
    sys.stderr.write("Unrecognized identifier format.\n")
    return 1


def build_parser():
    p = argparse.ArgumentParser(
        prog="idforge",
        description="IdForge: zero-dependency sortable unique ID generator (ULID/UUIDv7/UUIDv4).",
    )
    sub = p.add_subparsers(dest="command", required=True)

    u = sub.add_parser("ulid", help="Generate ULID(s).")
    u.add_argument("--monotonic", action="store_true", help="Monotonic within same ms.")
    u.add_argument("--count", type=int, default=1)
    u.set_defaults(func=cmd_ulid)

    v = sub.add_parser("uuid7", help="Generate UUIDv7(s).")
    v.add_argument("--count", type=int, default=1)
    v.set_defaults(func=cmd_uuid7)

    w = sub.add_parser("uuid4", help="Generate UUIDv4(s).")
    w.add_argument("--count", type=int, default=1)
    w.set_defaults(func=cmd_uuid4)

    x = sub.add_parser("parse", help="Detect type and show timestamp of an ID.")
    x.add_argument("id", help="ULID or UUID string.")
    x.set_defaults(func=cmd_parse)

    return p


def main(argv=None):
    args = build_parser().parse_args(argv)
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())
