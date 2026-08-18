#!/usr/bin/env python3
"""Compare locale overlays against english/ and print coverage."""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

UI_TABLES = (
    "UILocalization.json",
    "TooltipLocalization.json",
    "StatusEffectLocalization.json",
)
DIALOG_TABLE = "DialogLocalization.json"

# (filename, row key, scalar prose fields, nested string-map fields)
PROSE_TABLES = (
    ("helpData.json", "Key", ("Label", "Category", "Text"), ()),
    ("journalEntries.json", "ID", ("Message",), ()),
    ("InventoryItemData.json", "ItemID", ("Name", "Description"), ("Templates",)),
    ("MeleeWeaponData.json", "ItemID", ("Name", "Description"), ()),
    ("RangedWeaponData.json", "ItemID", ("Name", "Description"), ()),
    ("ProjectileRegistrationData.json", "SaveName", ("Name",), ()),
    (
        "CreatureRegistrationData.json",
        "LivingEntityType",
        ("Name", "Description", "CodexCategory"),
        (),
    ),
    (
        "StaticPrefabRegistrationData.json",
        "StaticPrefabType",
        (
            "Name",
            "DisplayName",
            "Description",
            "CodexCategory",
            "TooltipNameOverride",
        ),
        ("DescriptionsByState", "SpecificTooltips"),
    ),
)


def load_json(path: Path):
    if not path.is_file():
        return None
    return json.loads(path.read_text(encoding="utf-8-sig"))


def ui_index(rows):
    index = {}
    for row in rows or []:
        ident = row.get("ID")
        if ident is None or ident == "":
            continue
        index[str(ident)] = (row.get("Text") or "").strip()
    return index


def dialog_index(rows):
    index = {}
    for row in rows or []:
        ident = row.get("ID")
        if ident is None:
            continue
        index[int(ident)] = {
            "Normal": (row.get("Normal") or "").strip(),
            "Robot": (row.get("Robot") or "").strip(),
        }
    return index


def row_key(row, key_name):
    value = row.get(key_name)
    if value is None or value == "":
        return None
    return str(value)


def prose_fields(row, scalars, maps):
    fields = {}
    for name in scalars:
        value = (row.get(name) or "").strip() if isinstance(row.get(name), str) else ""
        if value:
            fields[name] = value
    for map_name in maps:
        nested = row.get(map_name) or {}
        if not isinstance(nested, dict):
            continue
        for nested_key, nested_value in nested.items():
            if not nested_key:
                continue
            text = (nested_value or "").strip() if isinstance(nested_value, str) else ""
            if text:
                fields[map_name + "." + str(nested_key)] = text
    return fields


def prose_index(rows, key_name, scalars, maps):
    index = {}
    for row in rows or []:
        ident = row_key(row, key_name)
        if ident is None:
            continue
        index[ident] = prose_fields(row, scalars, maps)
    return index


def classify(overlay_value: str, english_value: str) -> str:
    if not overlay_value:
        return "missing"
    if overlay_value == english_value:
        return "same-as-english"
    return "translated"


def measure_locale(english_root: Path, locale_root: Path) -> dict:
    errors = []
    tables = {}
    translated = 0
    total = 0

    for name in UI_TABLES:
        english_rows = ui_index(load_json(english_root / "Config" / name) or [])
        overlay_rows = ui_index(load_json(locale_root / "Config" / name) or [])
        unknown = sorted(set(overlay_rows) - set(english_rows))
        if unknown:
            errors.append("%s unknown IDs: %s" % (name, ", ".join(unknown[:20])))

        counts = {"translated": 0, "missing": 0, "same-as-english": 0}
        for ident, english_value in english_rows.items():
            total += 1
            status = classify(overlay_rows.get(ident, ""), english_value)
            counts[status] += 1
            if status == "translated":
                translated += 1
        tables[name] = {"total": len(english_rows), **counts}

    english_dialog = dialog_index(load_json(english_root / "Config" / DIALOG_TABLE) or [])
    overlay_dialog = dialog_index(load_json(locale_root / "Config" / DIALOG_TABLE) or [])
    unknown_ids = sorted(set(overlay_dialog) - set(english_dialog))
    if unknown_ids:
        errors.append(
            "%s unknown IDs: %s"
            % (DIALOG_TABLE, ", ".join(str(i) for i in unknown_ids[:20]))
        )

    counts = {"translated": 0, "missing": 0, "same-as-english": 0}
    dialog_total = 0
    for ident, english_row in english_dialog.items():
        overlay_row = overlay_dialog.get(ident, {})
        fields = ["Normal"]
        if english_row["Robot"]:
            fields.append("Robot")
        for field in fields:
            dialog_total += 1
            total += 1
            status = classify(overlay_row.get(field, ""), english_row[field])
            counts[status] += 1
            if status == "translated":
                translated += 1
    tables[DIALOG_TABLE] = {"total": dialog_total, **counts}

    for name, key_name, scalars, maps in PROSE_TABLES:
        english_rows = prose_index(
            load_json(english_root / "Config" / name) or [], key_name, scalars, maps
        )
        overlay_rows = prose_index(
            load_json(locale_root / "Config" / name) or [], key_name, scalars, maps
        )
        unknown = sorted(set(overlay_rows) - set(english_rows))
        if unknown:
            errors.append("%s unknown keys: %s" % (name, ", ".join(unknown[:20])))

        counts = {"translated": 0, "missing": 0, "same-as-english": 0}
        table_total = 0
        for ident, english_fields in english_rows.items():
            overlay_fields = overlay_rows.get(ident, {})
            for field, english_value in english_fields.items():
                table_total += 1
                total += 1
                status = classify(overlay_fields.get(field, ""), english_value)
                counts[status] += 1
                if status == "translated":
                    translated += 1
        tables[name] = {"total": table_total, **counts}

    percent = (100.0 * translated / total) if total else 0.0
    return {
        "locale": locale_root.name,
        "translated": translated,
        "total": total,
        "percent": round(percent, 1),
        "tables": tables,
        "errors": errors,
    }


README_TABLE_START = "<!-- coverage-table:start -->"
README_TABLE_END = "<!-- coverage-table:end -->"


def load_languages_file(repo: Path) -> dict:
    return json.loads((repo / "languages.json").read_text(encoding="utf-8"))


def load_languages(repo: Path) -> list:
    return load_languages_file(repo)["languages"]


def in_game_label(font: str) -> str:
    if font == "runtime":
        return "Yes ([Runtime font](FONTS.md))"
    return "Yes"


def render_markdown(results: list, source: dict) -> str:
    lines = [
        "# Coverage",
        "",
        "Counted against `english/` snapshot `%s`." % source.get("snapshotCommit", "?")[:8],
        "A field counts as translated when the overlay is non-empty and not identical to English.",
        "Empty overlay fields keep English in-game and count as missing.",
        "",
        "| Locale | Font | Translated | Total | Percent |",
        "| --- | --- | ---: | ---: | ---: |",
    ]
    for row in results:
        lines.append(
            "| `%s` | %s | %s | %s | %s%% |"
            % (
                row["locale"],
                row.get("font", ""),
                row["translated"],
                row["total"],
                row["percent"],
            )
        )
    lines.append("")
    return "\n".join(lines)


def render_readme_table(results: list, source: dict, unsupported: list) -> str:
    ordered = sorted(
        results,
        key=lambda row: (-row["percent"], row["locale"].lower()),
    )
    snapshot = source.get("snapshotCommit", "?")[:8]
    total = ordered[0]["total"] if ordered else 0
    lines = [
        README_TABLE_START,
        "",
        "Counted against English snapshot `%s` (%s overlay fields). A field counts as translated when it is non-empty and not a copy of English. Empty overlays stay English in-game."
        % (snapshot, total),
        "",
        "| Language | Pack | In-game | Translated |",
        "| --- | --- | --- | ---: |",
    ]
    for row in ordered:
        code = row["locale"]
        name = row.get("endonym") or code
        lines.append(
            "| %s | [`%s`](locales/%s/) | %s | %s%% |"
            % (name, code, code, in_game_label(row.get("font", "")), row["percent"])
        )

    lines.extend(
        [
            "",
            "`Yes` means the current Kimberley fonts can draw the language. Packs marked Runtime need Settings → Font Glyphs → **Runtime** (the default). See [`FONTS.md`](FONTS.md).",
            "",
            "These scripts have **no pack** yet: the shipped fonts cannot draw them, so in-game text would be blank.",
            "",
            "| Language | Code | In-game |",
            "| --- | --- | --- |",
        ]
    )
    for item in unsupported or []:
        lines.append(
            "| %s | `%s` | No — %s glyphs missing |"
            % (item.get("name", ""), item.get("code", ""), item.get("script", "required"))
        )
    lines.extend(["", README_TABLE_END])
    return "\n".join(lines)


def replace_readme_table(readme: str, table: str) -> str:
    start = readme.find(README_TABLE_START)
    end = readme.find(README_TABLE_END)
    if start < 0 or end < 0 or end < start:
        raise SystemExit(
            "README.md is missing %s / %s markers."
            % (README_TABLE_START, README_TABLE_END)
        )
    end += len(README_TABLE_END)
    return readme[:start] + table + readme[end:]


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo", type=Path, default=Path(__file__).resolve().parents[1])
    parser.add_argument("--write", type=Path, help="Write coverage.md")
    parser.add_argument("--json-out", type=Path, help="Write coverage.json")
    parser.add_argument(
        "--readme",
        type=Path,
        help="Replace the coverage table between HTML markers in README.md",
    )
    args = parser.parse_args(argv)

    repo = args.repo
    english_root = repo / "english"
    locales_root = repo / "locales"
    source = json.loads((english_root / "SOURCE.json").read_text(encoding="utf-8"))
    languages_file = load_languages_file(repo)
    languages = languages_file["languages"]
    unsupported = languages_file.get("unsupported") or []

    results = []
    failed = False
    listed = {lang["code"] for lang in languages}
    present = {p.name for p in locales_root.iterdir() if p.is_dir()} if locales_root.is_dir() else set()

    missing_dirs = sorted(listed - present)
    extra_dirs = sorted(present - listed)
    if missing_dirs:
        print("Missing locale folders: " + ", ".join(missing_dirs), file=sys.stderr)
        failed = True
    if extra_dirs:
        print("Unexpected locale folders: " + ", ".join(extra_dirs), file=sys.stderr)
        failed = True

    for lang in languages:
        locale_root = locales_root / lang["code"]
        if not locale_root.is_dir():
            continue
        result = measure_locale(english_root, locale_root)
        result["font"] = lang.get("font", "")
        result["endonym"] = lang.get("endonym", "")
        results.append(result)
        if result["errors"]:
            failed = True
            for err in result["errors"]:
                print("%s: %s" % (result["locale"], err), file=sys.stderr)

    markdown = render_markdown(results, source)
    if args.write:
        args.write.write_text(markdown, encoding="utf-8", newline="\n")
    if args.json_out:
        args.json_out.write_text(
            json.dumps({"source": source, "locales": results}, indent=2) + "\n",
            encoding="utf-8",
            newline="\n",
        )
    if args.readme:
        readme_path = args.readme
        updated = replace_readme_table(
            readme_path.read_text(encoding="utf-8"),
            render_readme_table(results, source, unsupported),
        )
        if not updated.endswith("\n"):
            updated += "\n"
        readme_path.write_text(updated, encoding="utf-8", newline="\n")
    sys.stdout.write(markdown)
    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
