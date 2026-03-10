from __future__ import annotations

import struct
import sys
from pathlib import Path


def build_ico(png_bytes: bytes) -> bytes:
    # ICO header + one image directory entry. Modern Windows accepts PNG payloads inside ICO.
    header = struct.pack("<HHH", 0, 1, 1)
    size = len(png_bytes)
    entry = struct.pack(
        "<BBBBHHII",
        0,  # 256 px width
        0,  # 256 px height
        0,  # palette
        0,  # reserved
        1,  # color planes
        32,  # bits per pixel
        size,
        6 + 16,  # header + dir entry
    )
    return header + entry + png_bytes


def main() -> int:
    if len(sys.argv) != 3:
        print("Usage: generate_windows_icon.py <input_png> <output_ico>")
        return 1

    input_png = Path(sys.argv[1])
    output_ico = Path(sys.argv[2])
    png_bytes = input_png.read_bytes()
    output_ico.write_bytes(build_ico(png_bytes))
    print(output_ico)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
