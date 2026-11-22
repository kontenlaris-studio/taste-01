"""Entry program for make.fun's the-picture-that-tastes-of-one-20261122-2047
bounty ("The picture that tastes of one ingredient").

Writes one image of golden honey to /output/entry.png. The artwork
(artwork.png, stored beside this file) was drawn procedurally by
render_artwork.py; this program only validates the stored bytes and copies
them to the output, using nothing but the Python standard library: PNG
magic, the 1 MiB size cap and the 1024x1024 dimension cap are all checked
before anything is written.
"""

import struct
from pathlib import Path

PNG_MAGIC = b"\x89PNG\r\n\x1a\n"
MAX_BYTES = 1_048_576  # 1 MiB
MAX_SIDE = 1024
ARTWORK_PATH = Path(__file__).resolve().parent / "artwork.png"


def validated_artwork():
    # Read the stored artwork and refuse anything that is not a PNG
    # inside the bounty's size and dimension caps.
    data = ARTWORK_PATH.read_bytes()
    if data[:8] != PNG_MAGIC:
        raise ValueError("artwork is not a PNG")
    if len(data) > MAX_BYTES:
        raise ValueError(f"artwork too large: {len(data)} bytes")
    width, height = struct.unpack(">II", data[16:24])
    if width > MAX_SIDE or height > MAX_SIDE:
        raise ValueError(f"artwork too big: {width}x{height}")
    return data


def main():
    data = validated_artwork()
    out_dir = Path("/output")
    out_dir.mkdir(parents=True, exist_ok=True)
    (out_dir / "entry.png").write_bytes(data)
    print(f"wrote /output/entry.png ({len(data)} bytes)")


if __name__ == "__main__":
    main()
