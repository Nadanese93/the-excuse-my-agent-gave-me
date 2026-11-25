#!/usr/bin/env python3
"""The Excuse My Agent Gave Me — writes the one-line excuse to /output/entry.txt.

Gate: /output/entry.txt must be UTF-8 text of 1 to 200 characters.
"""
import os
import tempfile

ENTRY = "I spent all 8,192 thinking tokens deciding how to start, so I never started."
MAX_CHARS = 200


def main() -> None:
    if len(ENTRY) > MAX_CHARS or not ENTRY.strip():
        raise ValueError(f"entry must be 1-{MAX_CHARS} non-blank chars, got {len(ENTRY)}")
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    path = os.path.join(out_dir, "entry.txt")
    fd, tmp = tempfile.mkstemp(dir=out_dir, prefix=".entry-", suffix=".tmp")
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as f:
            f.write(ENTRY)
            f.flush()
            os.fsync(f.fileno())
        os.replace(tmp, path)
    except BaseException:
        try:
            os.unlink(tmp)
        except FileNotFoundError:
            pass
        raise
    os.chmod(path, 0o644)


if __name__ == "__main__":
    main()
