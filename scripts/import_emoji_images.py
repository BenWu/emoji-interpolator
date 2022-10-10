#!/usr/bin/env python
import argparse
import os
import shutil
from pathlib import Path


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--src-dir", type=Path, required=True)
    parser.add_argument("--dst-dir", type=Path, required=True)
    parser.add_argument("--unicode-list", nargs="+", required=True)
    return parser.parse_args()


def code_to_image_name(code: str) -> str:
    return f"emoji_u{code.lower()}.png"


def validate_list(src_dir: Path, unicode_list: list[str]):
    missing_codes = set()

    for code in unicode_list:
        if not (src_dir / code_to_image_name(code)).exists():
            missing_codes.add(code)

    if len(missing_codes) > 0:
        raise ValueError(f"Emoji codes missing from image files: {missing_codes}")


def import_images(src_dir: Path, dst_dir: Path, unicode_list: list[str]):
    os.makedirs(dst_dir)
    for i, code in enumerate(unicode_list, start=1):
        print(f"{src_dir / code_to_image_name(code)} -> {dst_dir / f'{i}.png'}")
        shutil.copy(src_dir / code_to_image_name(code), dst_dir / f"{i}.png")


if __name__ == "__main__":
    args = parse_args()
    validate_list(args.src_dir, args.unicode_list)
    import_images(args.src_dir, args.dst_dir, args.unicode_list)
