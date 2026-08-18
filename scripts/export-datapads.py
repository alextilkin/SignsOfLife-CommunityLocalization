#!/usr/bin/env python3
"""Convert game DatapadTextData.xml into overlay JSON {ID, Title, Category, Text}."""
from __future__ import annotations

import argparse
import json
import xml.etree.ElementTree as ET
from pathlib import Path


def default_xml() -> Path:
    documents = Path(__file__).resolve().parents[2]
    return documents / "signs-of-life" / "Signs of Life" / "Content" / "XML" / "DatapadTextData.xml"


def convert(xml_path: Path) -> list[dict]:
    root = ET.parse(xml_path).getroot()
    rows = []
    for node in root.findall(".//datapadText"):
        text_el = node.find("text")
        text = "".join(text_el.itertext()) if text_el is not None else ""
        rows.append(
            {
                "ID": int(node.attrib["id"]),
                "Title": node.attrib.get("title", ""),
                "Category": node.attrib.get("category", ""),
                "Text": text,
            }
        )
    return rows


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--xml", type=Path, default=default_xml())
    parser.add_argument(
        "--out",
        type=Path,
        default=Path(__file__).resolve().parents[1] / "english" / "Config" / "DatapadTextData.json",
    )
    args = parser.parse_args()
    if not args.xml.is_file():
        raise SystemExit("Datapad XML not found: %s" % args.xml)
    rows = convert(args.xml)
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(
        json.dumps(rows, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
        newline="\n",
    )
    print("Wrote %s datapads to %s" % (len(rows), args.out))


if __name__ == "__main__":
    main()
