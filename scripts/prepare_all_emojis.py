#!/usr/bin/env python
import argparse
import csv
import os
import shutil
from pathlib import Path
from string import ascii_lowercase
from typing import Dict


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--src-dir", type=Path, required=True)
    parser.add_argument("--dst-dir", type=Path, required=True)
    parser.add_argument("--mapping-file", type=Path, required=True)
    return parser.parse_args()


def build_code_to_name_map(mapping_file: Path) -> Dict[str, str]:
    code_to_name = {}

    with open(mapping_file) as f:
        field_names = f.readline().strip().split(",")

        reader = csv.DictReader(f, fieldnames=field_names)
        for line in reader:
            if line["category"] not in {"people", "nature"} or (line["category"] == "nature" and int(line["index"]) > 124):
                continue

            # fe0f is not used in noto-emoji filenames
            code = line["code"].lower().replace("u+", "").replace(", ", "_").replace("_fe0f", "")
            name = "".join(filter(lambda c: c in ascii_lowercase + "_", line["name"].lower().replace(" ", "_")))
            code_to_name[f"emoji_u{code}.png"] = name

    return code_to_name


def move_emojis(src_dir: Path, dst_dir: Path, mapping: Dict[str, str]):
    os.makedirs(dst_dir)

    image_list = src_dir.glob("emoji_*.png")
    for image in image_list:
        try:
            dst_file = dst_dir / f"{mapping[image.name]}.png"
        except KeyError as e:
            # print(f"Emoji not found in mapping: {e}, skipping")
            continue

        print(f"Copying {image} to {dst_file}")
        shutil.copy(image, dst_file)


if __name__ == "__main__":
    args = parse_args()
    mappings = build_code_to_name_map(args.mapping_file)
    move_emojis(args.src_dir, args.dst_dir, mappings)
