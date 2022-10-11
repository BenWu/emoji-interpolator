#!/usr/bin/env python
import argparse
import csv
from pathlib import Path
from typing import Dict, Tuple

from bs4 import BeautifulSoup, Tag
import requests


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--dst-dir", type=Path, required=True)
    return parser.parse_args()


def create_categories() -> Dict[str, Tuple[str, int]]:
    category_urls = {
        "people": "https://emojipedia.org/people/",
        "nature": "https://emojipedia.org/nature/",
        "food": "https://emojipedia.org/food-drink/",
        "activity": "https://emojipedia.org/activity/",
        "travel": "https://emojipedia.org/travel-places",
        "objects": "https://emojipedia.org/objects/",
        "symbols": "https://emojipedia.org/symbols/",
        "flags": "https://emojipedia.org/flags/",
    }
    name_to_category = {}

    for category, url in category_urls.items():
        html_doc = requests.get(url).text
        soup = BeautifulSoup(html_doc, "html.parser")

        emoji_list = [
            child for child in soup.html.body if isinstance(child, Tag) and "container" in child.attrs.get("class", [])
        ][0].div.ul

        i = 0
        for row in emoji_list.children:
            if row.name != "li":
                continue

            emoji_name = row.text.split(" ", 1)[1]
            name_to_category[emoji_name] = (category, i)
            i += 1

    return name_to_category


def create_mappings(dst_dir: Path, name_to_category_map: Dict[str, Tuple[str, int]]):
    html_doc = requests.get("https://emojipedia.org/emoji/").text
    soup = BeautifulSoup(html_doc, "html.parser")

    codepoint_table = [
        child for child in soup.html.body if isinstance(child, Tag) and "container" in child.attrs.get("class", [])
    ][0].div.article.table

    mapping_list = []

    for row in codepoint_table.children:
        if row.name != "tr":
            continue

        contents = [c for c in row.contents if isinstance(c, Tag)]

        emoji_char, emoji_name = contents[0].text.split(" ", 1)
        emoji_code = contents[1].text
        mapping_list.append({
            "char": emoji_char,
            "name": emoji_name,
            "code": emoji_code,
            "category": name_to_category_map.get(emoji_name, ("other",))[0],
            "index": name_to_category_map.get(emoji_name, (0, 0))[1],
        })

    dst_file = dst_dir / "emoji_char_codes.csv"

    with open(dst_file, "w") as f:
        writer = csv.DictWriter(f, fieldnames=mapping_list[0].keys())
        writer.writeheader()
        writer.writerows(mapping_list)

    print(f"Wrote {len(mapping_list)} rows to {dst_file}")


if __name__ == "__main__":
    args = parse_args()
    name_to_category = create_categories()
    create_mappings(dst_dir=args.dst_dir, name_to_category_map=name_to_category)