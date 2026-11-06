"""IdForge 库调用示例。"""

from idforge import ulid, uuid7, uuid4


def demo():
    u, _ = ulid()
    print("ULID :", u)
    print("UUIDv7:", uuid7())
    print("UUIDv4:", uuid4())


if __name__ == "__main__":
    demo()
