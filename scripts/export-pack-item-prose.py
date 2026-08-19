#!/usr/bin/env python3
"""Fill english/Config/InventoryItemData.json sol.* Name/Description from pack JSON.

English pack-item prose stays in LoadedContent item_*.json. The game
InventoryItemData.json sol.* rows are overlay hooks only (Complexity /
AutoOrganizeString). This snapshot merge is the translator-facing copy, same
idea as export-datapads.py.

Does not invent InventoryItemData rows. Warns when a vanilla item_*.json has
no hook, or a sol.* hook has no matching pack item.
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

IDENTIFIER_TRUNCATION = 32


def default_game_root() -> Path:
    documents = Path(__file__).resolve().parents[2]
    return documents / "signs-of-life" / "Signs of Life"


def default_inventory() -> Path:
    return default_game_root() / "Content" / "Config" / "InventoryItemData.json"


def default_items_root() -> Path:
    return default_game_root() / "Content" / "LoadedContent" / "VanillaContent"


def truncate(value: str) -> str:
    return value[:IDENTIFIER_TRUNCATION]


def fix_leading_decimals(text: str) -> str:
    """Newtonsoft accepts `.3`; Python json does not."""
    out = []
    in_str = False
    escape = False
    prev_nonspace = ""
    i = 0
    n = len(text)
    while i < n:
        ch = text[i]
        if in_str:
            out.append(ch)
            if escape:
                escape = False
            elif ch == "\\":
                escape = True
            elif ch == '"':
                in_str = False
            i += 1
            continue
        if ch == '"':
            in_str = True
            out.append(ch)
            prev_nonspace = ch
            i += 1
            continue
        if (
            ch == "."
            and i + 1 < n
            and text[i + 1].isdigit()
            and not prev_nonspace.isdigit()
        ):
            out.append("0")
        if not ch.isspace():
            prev_nonspace = ch
        out.append(ch)
        i += 1
    return "".join(out)


def strip_trailing_commas(text: str) -> str:
    out = []
    in_str = False
    escape = False
    i = 0
    n = len(text)
    while i < n:
        ch = text[i]
        if in_str:
            out.append(ch)
            if escape:
                escape = False
            elif ch == "\\":
                escape = True
            elif ch == '"':
                in_str = False
            i += 1
            continue
        if ch == '"':
            in_str = True
            out.append(ch)
            i += 1
            continue
        if ch == ",":
            j = i + 1
            while j < n and text[j] in " \t\r\n":
                j += 1
            if j < n and text[j] in "}]":
                i += 1
                continue
        out.append(ch)
        i += 1
    return "".join(out)


def loads_lenient(text: str):
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        return json.loads(fix_leading_decimals(strip_trailing_commas(text)))


def shallowest_str(node, key: str, depth: int = 0):
    found = None
    found_depth = None

    def walk(value, current_depth):
        nonlocal found, found_depth
        if isinstance(value, dict):
            raw = value.get(key)
            if isinstance(raw, str) and (found_depth is None or current_depth < found_depth):
                found = raw
                found_depth = current_depth
            for child in value.values():
                walk(child, current_depth + 1)
        elif isinstance(value, list):
            for child in value:
                walk(child, current_depth + 1)

    walk(node, depth)
    return found


def object_span(text: str, marker: str):
    idx = text.find(marker)
    if idx < 0:
        return None
    start = text.rfind("{", 0, idx)
    if start < 0:
        return None
    depth = 0
    in_str = False
    escape = False
    i = start
    while i < len(text):
        ch = text[i]
        if in_str:
            if escape:
                escape = False
            elif ch == "\\":
                escape = True
            elif ch == '"':
                in_str = False
        else:
            if ch == '"':
                in_str = True
            elif ch == "{":
                depth += 1
            elif ch == "}":
                depth -= 1
                if depth == 0:
                    return start, i + 1
        i += 1
    return None


def json_literal(value) -> str:
    return json.dumps(value, ensure_ascii=False)


def format_row(row: dict, name: str | None, description: str | None, newline: str) -> str:
    keys = [("ItemID", row["ItemID"]), ("Complexity", row["Complexity"])]
    if name:
        keys.append(("Name", name))
    auto = row.get("AutoOrganizeString")
    if isinstance(auto, str) and auto:
        keys.append(("AutoOrganizeString", auto))
    if description:
        keys.append(("Description", description))
    templates = row.get("Templates")
    if isinstance(templates, dict) and templates:
        keys.append(("Templates", templates))

    lines = ["{"]
    last = len(keys) - 1
    for index, (key, value) in enumerate(keys):
        comma = "" if index == last else ","
        lines.append("        \"%s\":  %s%s" % (key, json_literal(value), comma))
    lines.append("    }")
    return newline.join(lines)


def load_pack_prose(items_root: Path) -> tuple[dict, list[str]]:
    warnings = []
    modinfo_path = items_root / "modinfo.json"
    if not modinfo_path.is_file():
        raise SystemExit("modinfo.json not found: %s" % modinfo_path)
    modinfo = loads_lenient(modinfo_path.read_text(encoding="utf-8-sig"))
    prefix = truncate(str(modinfo.get("UniqueModName") or "sol"))

    prose = {}
    for path in sorted(items_root.rglob("item_*.json")):
        try:
            data = loads_lenient(path.read_text(encoding="utf-8-sig"))
        except Exception as exc:
            warnings.append("failed to parse %s: %s" % (path, exc))
            continue
        unique = shallowest_str(data, "UniqueIdentifier")
        if not unique:
            warnings.append("no UniqueIdentifier in %s" % path)
            continue
        full_id = prefix + "." + truncate(unique)
        prose[full_id] = {
            "Name": (shallowest_str(data, "Name") or "").strip() or None,
            "Description": (shallowest_str(data, "Description") or "").strip() or None,
            "path": str(path),
        }
    return prose, warnings


def merge(inventory_text: str, prose: dict) -> tuple[str, dict]:
    newline = "\r\n" if "\r\n" in inventory_text else "\n"
    rows = json.loads(inventory_text)
    stats = {
        "filled_name": 0,
        "filled_description": 0,
        "hooks": 0,
        "missing_hooks": [],
        "orphan_hooks": [],
    }

    hook_ids = []
    for row in rows:
        item_id = row.get("ItemID")
        if not isinstance(item_id, str) or not item_id.startswith("sol."):
            continue
        hook_ids.append(item_id)
        stats["hooks"] += 1
        pack = prose.get(item_id)
        if pack is None:
            stats["orphan_hooks"].append(item_id)
            continue
        marker = '"ItemID":  "%s"' % item_id
        span = object_span(inventory_text, marker)
        if span is None:
            raise SystemExit("could not find InventoryItemData object for %s" % item_id)
        start, end = span
        original = json.loads(inventory_text[start:end])
        name = pack["Name"]
        description = pack["Description"]
        if name:
            stats["filled_name"] += 1
        if description:
            stats["filled_description"] += 1
        replacement = format_row(original, name, description, newline)
        inventory_text = inventory_text[:start] + replacement + inventory_text[end:]

    for pack_id in sorted(prose):
        if pack_id not in hook_ids:
            stats["missing_hooks"].append(pack_id)
    return inventory_text, stats


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--inventory", type=Path, default=default_inventory())
    parser.add_argument("--items-root", type=Path, default=default_items_root())
    parser.add_argument(
        "--out",
        type=Path,
        default=Path(__file__).resolve().parents[1] / "english" / "Config" / "InventoryItemData.json",
    )
    args = parser.parse_args()
    if not args.inventory.is_file():
        raise SystemExit("InventoryItemData.json not found: %s" % args.inventory)
    if not args.items_root.is_dir():
        raise SystemExit("VanillaContent not found: %s" % args.items_root)

    raw = args.inventory.read_bytes()
    has_bom = raw.startswith(b"\xef\xbb\xbf")
    inventory_text = raw.decode("utf-8-sig")
    prose, parse_warnings = load_pack_prose(args.items_root)
    merged, stats = merge(inventory_text, prose)

    args.out.parent.mkdir(parents=True, exist_ok=True)
    encoded = merged.encode("utf-8")
    if has_bom:
        encoded = b"\xef\xbb\xbf" + encoded
    args.out.write_bytes(encoded)

    for warning in parse_warnings:
        print(warning, file=sys.stderr)
    for item_id in stats["missing_hooks"]:
        print("pack item has no InventoryItemData hook: %s" % item_id, file=sys.stderr)
    for item_id in stats["orphan_hooks"]:
        print("InventoryItemData sol.* hook has no pack item: %s" % item_id, file=sys.stderr)

    print(
        "Wrote %s Name and %s Description fields across %s sol.* hooks to %s"
        % (stats["filled_name"], stats["filled_description"], stats["hooks"], args.out)
    )
    if stats["missing_hooks"] or stats["orphan_hooks"] or parse_warnings:
        print(
            "(%s missing hooks, %s orphan hooks, %s parse warnings)"
            % (
                len(stats["missing_hooks"]),
                len(stats["orphan_hooks"]),
                len(parse_warnings),
            ),
            file=sys.stderr,
        )
    if parse_warnings or stats["missing_hooks"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
