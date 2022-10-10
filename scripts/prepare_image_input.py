#!/usr/bin/env python
import argparse
import os
import re
import shutil
from pathlib import Path


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--image-dir", type=Path, required=True)
    return parser.parse_args()


def prepare_images(image_dir: Path):
    image_files = sorted(
        [f for f in image_dir.glob("*") if re.fullmatch(r"^.*/[0-9]+\.png$", str(f))],
        key=lambda f: int(f.name.split(".")[0]),
    )
    for i in range(len(image_files) - 1):
        dest_dir = image_dir / "input" / str(i + 1).rjust(2, "0")

        os.makedirs(dest_dir)

        print(f"{image_files[i]} -> {dest_dir / 'frame1.png'}")
        shutil.copy(image_files[i], dest_dir / "frame1.png")

        print(f"{image_files[i + 1]} -> {dest_dir / 'frame2.png'}")
        shutil.copy(image_files[i + 1], dest_dir / "frame2.png")


if __name__ == "__main__":
    args = parse_args()
    prepare_images(args.image_dir)
