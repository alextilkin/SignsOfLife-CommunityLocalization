#!/usr/bin/env python3
"""Compare locale overlays against english/ and print coverage."""
from __future__ import annotations

import argparse
from collections import Counter
import json
import re
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
    ("DatapadTextData.json", "ID", ("Title", "Category", "Text"), ()),
)

ARMOR_TABLE = "ArmorSetData.json"
STRUCTURED_TABLES = (
    "RecipeLocalization.json",
    "TileLocalization.json",
    "GlyphLocalization.json",
    "RuntimeContentLocalization.json",
)
FORMAT_TOKEN = re.compile(r"\{\d+(?:,[+-]?\d+)?(?::[^{}]*)?\}")
BRACKET_TOKEN = re.compile(r"\[[A-Za-z0-9_]+\]")
REQUIRED_BRACKET_TOKENS = frozenset((
    "[lightkey]", "[menukey]", "[grablaserkey]", "[minimapkey]", "[mapkey]",
    "[grapplekey]", "[holsterkey]", "[kickkey]", "[reloadkey]", "[jump]",
    "[crouch]", "[up]", "[down]", "[left]", "[right]", "[primary]",
    "[secondary]", "[scrollslot1]", "[scrollslot4]", "[hostname]", "[al]",
    "[ENGINEER]", "[CAPTAIN]", "[JANITOR]", "[XENOBIOLOGIST]", "[HOSTNAME]",
))


def assert_unique(rows, keys, label):
    seen = set()
    for row in rows:
        if not isinstance(row, dict):
            raise ValueError("%s contains a non-object row" % label)
        identity = tuple(None if row.get(key) is None else str(row[key]) for key in keys)
        if any(value is None or value == "" for value in identity):
            raise ValueError("%s has a row without %s" % (label, ", ".join(keys)))
        if identity in seen:
            raise ValueError("%s has duplicate %s: %s" % (label, "/".join(keys), identity))
        seen.add(identity)


def validate_unique_rows(path, data):
    name = path.name
    if name == ARMOR_TABLE:
        if not isinstance(data, dict):
            raise ValueError("%s must be an object" % name)
        assert_unique(data.get("Sets") or [], ("Name",), name + ".Sets")
        # The English armor source also contains non-addressable pieces without
        # ItemType; the game cannot match overlay rows for those pieces.
        assert_unique([row for row in data.get("Pieces") or [] if row.get("ItemType")],
                      ("ItemType",), name + ".Pieces")
    elif name == "RecipeLocalization.json":
        if not isinstance(data, dict):
            raise ValueError("%s must be an object" % name)
        for section, key in (("Recipes", "Name"), ("Categories", "Key"),
                             ("Slots", "Key"), ("AdjustedResults", "Key")):
            assert_unique(data.get(section) or [], (key,), name + "." + section)
    elif name == "RuntimeContentLocalization.json":
        assert_unique(data, ("Kind", "ID"), name)
    elif name in UI_TABLES + (DIALOG_TABLE, "TileLocalization.json", "GlyphLocalization.json"):
        assert_unique(data, ("ID",), name)
    else:
        for table, key, _, _ in PROSE_TABLES:
            if name == table:
                assert_unique(data, (key,), name)
                break


def valid_format_syntax(value):
    index = 0
    while index < len(value):
        if value[index] == "{":
            if value[index:index + 2] == "{{":
                index += 2
                continue
            token = FORMAT_TOKEN.match(value, index)
            if token is None:
                return False
            index = token.end()
        elif value[index] == "}":
            if value[index:index + 2] != "}}":
                return False
            index += 2
        else:
            index += 1
    return True


def tokens_match(english, translated):
    if not valid_format_syntax(translated):
        return False
    if Counter(FORMAT_TOKEN.findall(english)) != Counter(FORMAT_TOKEN.findall(translated)):
        return False
    def required_brackets(value):
        return Counter(token for token in BRACKET_TOKEN.findall(value)
                       if token in REQUIRED_BRACKET_TOKENS or token[1:-1].lower().endswith("key"))
    required = required_brackets(english)
    supplied = required_brackets(translated)
    if any(supplied[token] < count for token, count in required.items()):
        return False
    # The words inside @...@ are translated; the markup delimiters must remain.
    if english.count("@") != translated.count("@"):
        return False
    return True


def check_tokens(errors, label, english, translated):
    if translated and not tokens_match(english, translated):
        errors.append("%s has missing or malformed format/keybind/lore/highlight tokens" % label)


def structured_index(name, data):
    rows = {}
    if name == "RecipeLocalization.json":
        for section, key in (("Recipes", "Name"), ("Categories", "Key"),
                             ("Slots", "Key"), ("AdjustedResults", "Key")):
            for row in data.get(section) or []:
                ident = section + ":" + str(row[key])
                rows[ident] = {"DisplayName": row["DisplayName"]} if isinstance(row.get("DisplayName"), str) and row["DisplayName"].strip() else {}
    elif name == "RuntimeContentLocalization.json":
        for row in data:
            ident = str(row["Kind"]) + ":" + str(row["ID"])
            rows[ident] = {key: value for key, value in row.items()
                           if key not in ("Kind", "ID") and isinstance(value, str) and value.strip()}
    else:
        field = "Text" if name == "GlyphLocalization.json" else "DisplayName"
        for row in data:
            value = row.get(field)
            rows[str(row["ID"])] = {field: value} if isinstance(value, str) and value.strip() else {}
    return rows


def armor_index(data):
    """Index overlayable armor prose. Mechanical bonus lines are generated
    in-game; only unique authored Bonuses[].Description overrides count."""
    index = {}
    if not isinstance(data, dict):
        return index
    for row in data.get("Pieces") or []:
        ident = row.get("ItemType")
        if ident is None or ident == "":
            continue
        fields = {}
        for name in ("Name", "Description"):
            value = (row.get(name) or "").strip() if isinstance(row.get(name), str) else ""
            if value:
                fields[name] = value
        for i, bonus in enumerate(row.get("Bonuses") or []):
            if not isinstance(bonus, dict):
                continue
            desc = (bonus.get("Description") or "").strip() if isinstance(bonus.get("Description"), str) else ""
            if desc:
                fields["Bonuses.%s.Description" % i] = desc
        index["piece:" + str(ident)] = fields
    for row in data.get("Sets") or []:
        ident = row.get("Name")
        if ident is None or ident == "":
            continue
        fields = {}
        for i, bonus in enumerate(row.get("Bonuses") or []):
            if not isinstance(bonus, dict):
                continue
            desc = (bonus.get("Description") or "").strip() if isinstance(bonus.get("Description"), str) else ""
            if desc:
                fields["Bonuses.%s.Description" % i] = desc
        if fields:
            index["set:" + ident] = fields
    return index


def load_json(path: Path):
    if not path.is_file():
        return None
    data = json.loads(path.read_text(encoding="utf-8-sig"))
    validate_unique_rows(path, data)
    return data


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
            overlay_value = overlay_rows.get(ident, "")
            check_tokens(errors, "%s %s" % (name, ident), english_value, overlay_value)
            status = classify(overlay_value, english_value)
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
            overlay_value = overlay_row.get(field, "")
            check_tokens(errors, "%s %s.%s" % (DIALOG_TABLE, ident, field),
                         english_row[field], overlay_value)
            status = classify(overlay_value, english_row[field])
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
            unknown_fields = sorted(set(overlay_fields) - set(english_fields))
            if name == "StaticPrefabRegistrationData.json":
                # A matching English DisplayName inherits Name but a pack may
                # still explicitly override the displayed prefab name.
                unknown_fields = [field for field in unknown_fields if field != "DisplayName"]
            for field in unknown_fields:
                errors.append("%s %s has unknown field %s" % (name, ident, field))
            for field, english_value in english_fields.items():
                table_total += 1
                total += 1
                overlay_value = overlay_fields.get(field, "")
                check_tokens(errors, "%s %s.%s" % (name, ident, field),
                             english_value, overlay_value)
                status = classify(overlay_value, english_value)
                counts[status] += 1
                if status == "translated":
                    translated += 1
        tables[name] = {"total": table_total, **counts}

    english_armor = armor_index(load_json(english_root / "Config" / ARMOR_TABLE) or {})
    overlay_armor = armor_index(load_json(locale_root / "Config" / ARMOR_TABLE) or {})
    unknown_armor = sorted(set(overlay_armor) - set(english_armor))
    if unknown_armor:
        errors.append("%s unknown keys: %s" % (ARMOR_TABLE, ", ".join(unknown_armor[:20])))

    counts = {"translated": 0, "missing": 0, "same-as-english": 0}
    armor_total = 0
    for ident, english_fields in english_armor.items():
        overlay_fields = overlay_armor.get(ident, {})
        for field, english_value in english_fields.items():
            armor_total += 1
            total += 1
            overlay_value = overlay_fields.get(field, "")
            check_tokens(errors, "%s %s.%s" % (ARMOR_TABLE, ident, field),
                         english_value, overlay_value)
            status = classify(overlay_value, english_value)
            counts[status] += 1
            if status == "translated":
                translated += 1
    tables[ARMOR_TABLE] = {"total": armor_total, **counts}

    for name in STRUCTURED_TABLES:
        english_rows = structured_index(name, load_json(english_root / "Config" / name) or ({} if name == "RecipeLocalization.json" else []))
        overlay_rows = structured_index(name, load_json(locale_root / "Config" / name) or ({} if name == "RecipeLocalization.json" else []))
        unknown = sorted(set(overlay_rows) - set(english_rows))
        if unknown:
            errors.append("%s unknown keys: %s" % (name, ", ".join(unknown[:20])))
        counts = {"translated": 0, "missing": 0, "same-as-english": 0}
        table_total = 0
        for ident, english_fields in english_rows.items():
            overlay_fields = overlay_rows.get(ident, {})
            unknown_fields = sorted(set(overlay_fields) - set(english_fields))
            # An inherited recipe may supply an optional explicit DisplayName.
            if name == "RecipeLocalization.json" and ident.startswith("Recipes:"):
                unknown_fields = [field for field in unknown_fields if field != "DisplayName"]
            for field in unknown_fields:
                errors.append("%s %s has unknown field %s" % (name, ident, field))
            for field, english_value in english_fields.items():
                table_total += 1
                total += 1
                overlay_value = overlay_fields.get(field, "")
                check_tokens(errors, "%s %s.%s" % (name, ident, field),
                             english_value, overlay_value)
                status = classify(overlay_value, english_value)
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
UNSUPPORTED_TABLE_START = "<!-- unsupported-table:start -->"
UNSUPPORTED_TABLE_END = "<!-- unsupported-table:end -->"


def load_languages_file(repo: Path) -> dict:
    return json.loads((repo / "languages.json").read_text(encoding="utf-8"))


def load_languages(repo: Path) -> list:
    return load_languages_file(repo)["languages"]


def render_markdown(results: list, source: dict) -> str:
    lines = [
        "# Coverage",
        "",
        "Counted against `english/` snapshot `%s`." % source.get("snapshotCommit", "?")[:8],
        "A field counts toward text coverage when the overlay is non-empty and not identical to English.",
        "Empty overlay fields keep English in-game and count as missing.",
        "",
        "| Locale | Translated fields | Total fields | Text coverage |",
        "| --- | ---: | ---: | ---: |",
    ]
    for row in results:
        lines.append(
            "| `%s` | %s | %s | %s%% |"
            % (
                row["locale"],
                row["translated"],
                row["total"],
                row["percent"],
            )
        )
    lines.append("")
    return "\n".join(lines)


def render_readme_table(results: list, source: dict) -> str:
    ordered = sorted(
        results,
        key=lambda row: (-row["percent"], row["locale"].lower()),
    )
    total = ordered[0]["total"] if ordered else 0
    lines = [
        README_TABLE_START,
        "",
        "A field counts toward text coverage when it is non-empty and not a copy of English. Empty overlays stay English in-game. %s fields in this snapshot."
        % total,
        "",
        "| Language | Pack | Text coverage |",
        "| --- | --- | ---: |",
    ]
    for row in ordered:
        code = row["locale"]
        name = row.get("endonym") or code
        lines.append(
            "| %s | [`%s`](locales/%s/) | %s%% |"
            % (name, code, code, row["percent"])
        )
    lines.extend(["", README_TABLE_END])
    return "\n".join(lines)


def render_unsupported_table(unsupported: list) -> str:
    lines = [
        UNSUPPORTED_TABLE_START,
        "",
        "The shipped fonts cannot draw these scripts yet, so there is no pack folder.",
        "",
        "| Language | Code | Script |",
        "| --- | --- | --- |",
    ]
    for item in unsupported or []:
        lines.append(
            "| %s | `%s` | %s |"
            % (item.get("name", ""), item.get("code", ""), item.get("script", ""))
        )
    lines.extend(["", UNSUPPORTED_TABLE_END])
    return "\n".join(lines)


def replace_marked_section(readme: str, start_marker: str, end_marker: str, table: str) -> str:
    start = readme.find(start_marker)
    end = readme.find(end_marker)
    if start < 0 or end < 0 or end < start:
        raise SystemExit(
            "README.md is missing %s / %s markers." % (start_marker, end_marker)
        )
    end += len(end_marker)
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
    measured = set(UI_TABLES + (DIALOG_TABLE, ARMOR_TABLE) +
                   tuple(table[0] for table in PROSE_TABLES) + STRUCTURED_TABLES)
    declared = {Path(path).name for path in source["overlayableFiles"]}
    if declared != measured:
        raise SystemExit("SOURCE.json tables differ from coverage tables: %s" %
                         ", ".join(sorted(declared.symmetric_difference(measured))))
    missing_english = sorted(name for name in measured
                             if not (english_root / "Config" / name).is_file())
    if missing_english:
        raise SystemExit("Missing English source tables: " + ", ".join(missing_english))
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
        try:
            result = measure_locale(english_root, locale_root)
        except (ValueError, json.JSONDecodeError) as exc:
            print("%s: %s" % (lang["code"], exc), file=sys.stderr)
            failed = True
            continue
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
        updated = readme_path.read_text(encoding="utf-8")
        updated = replace_marked_section(
            updated,
            README_TABLE_START,
            README_TABLE_END,
            render_readme_table(results, source),
        )
        updated = replace_marked_section(
            updated,
            UNSUPPORTED_TABLE_START,
            UNSUPPORTED_TABLE_END,
            render_unsupported_table(unsupported),
        )
        if not updated.endswith("\n"):
            updated += "\n"
        readme_path.write_text(updated, encoding="utf-8", newline="\n")
    sys.stdout.write(markdown)
    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
