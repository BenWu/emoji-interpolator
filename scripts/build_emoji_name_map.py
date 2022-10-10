#!/usr/bin/env python
import argparse
import csv
from pathlib import Path

from bs4 import BeautifulSoup, Tag
import requests


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--dst-dir", type=Path, required=True)
    return parser.parse_args()


def create_mappings(dst_dir: Path):
    html_doc = requests.get("https://emojipedia.org/emoji/").text

    soup = BeautifulSoup(html_doc, "html.parser")

    codepoint_table = [child for child in soup.html.body if isinstance(child, Tag) and "container" in child.attrs.get("class", [])][0].div.article.table

    mapping_list = []

    for row in codepoint_table.children:
        if row.name != "tr":
            continue

        contents = [c for c in row.contents if isinstance(c, Tag)]

        emoji_char, emoji_name = contents[0].text.split(" ", 1)
        emoji_code = contents[1].text
        mapping_list.append({"char": emoji_char, "name": emoji_name, "code": emoji_code})

    dst_file = dst_dir / "emoji_char_codes.csv"

    with open(dst_file, "w") as f:
        writer = csv.DictWriter(f, fieldnames=mapping_list[0].keys())
        writer.writeheader()
        writer.writerows(mapping_list)

    print(f"Wrote {len(mapping_list)} rows to {dst_file}")


if __name__ == "__main__":
    args = parse_args()
    create_mappings(dst_dir=args.dst_dir)