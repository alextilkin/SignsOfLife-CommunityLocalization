#!/usr/bin/env python3
"""Report English changes and explicit per-language translation review state.

Refresh writes only the prepared candidate. It never edits translated prose or
guesses replacement IDs. Review flags are informational, separate from coverage.
"""
from __future__ import annotations

import argparse
import hashlib
import html
import json
from pathlib import Path
import re
import sys

sys.dont_write_bytecode = True
from localization_catalog import Address, TABLES, load_catalog

SCHEMA_VERSION = 1
LOCALE_CODE = re.compile(r"[A-Za-z][A-Za-z0-9]*(?:-[A-Za-z0-9]+)*\Z")
HASH = re.compile(r"[0-9a-f]{64}\Z")


def fingerprint(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def safe_path(root: Path, *parts: str) -> Path:
    root = Path(root).absolute()
    path = root.joinpath(*parts)
    if root.is_symlink() or root.is_junction() or path.is_symlink():
        raise ValueError("Filesystem links are not supported: " + str(path))
    resolved_root, resolved = root.resolve(), path.resolve()
    if not resolved.is_relative_to(resolved_root):
        raise ValueError("Path escapes repository: " + str(path))
    for parent in (path, *path.parents):
        if parent == root:
            break
        if parent.is_symlink() or parent.is_junction():
            raise ValueError("Filesystem links are not supported: " + str(parent))
    return path


def read_json(path: Path, default=None):
    def unique(pairs):
        result = {}
        for key, value in pairs:
            if key in result:
                raise ValueError("Duplicate JSON field: " + key)
            result[key] = value
        return result
    return json.loads(path.read_text(encoding="utf-8-sig"), object_pairs_hook=unique) if path.exists() else default


def write_json(path: Path, value) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def public_snapshot_metadata(metadata: dict) -> dict:
    return {key: metadata.get(key) for key in
            ("targetGameVersion", "snapshotDate") if metadata.get(key) is not None}


def source_metadata(repo: Path) -> dict:
    return public_snapshot_metadata(read_json(safe_path(repo, "english", "SOURCE.json"), {}))


def english_catalog(repo: Path) -> dict:
    metadata = read_json(safe_path(repo, "english", "SOURCE.json"))
    if not isinstance(metadata, dict) or not isinstance(metadata.get("overlayableFiles"), list):
        raise ValueError("English SOURCE.json must declare overlayableFiles")
    seen = set()
    for relative in metadata["overlayableFiles"]:
        if not isinstance(relative, str) or not relative.startswith("Config/"):
            raise ValueError("Invalid English overlay table path")
        table = relative.removeprefix("Config/")
        if table not in TABLES or table in seen:
            raise ValueError("Unknown or duplicate English overlay table: " + table)
        seen.add(table)
        if not safe_path(repo, "english", "Config", table).is_file():
            raise ValueError("Missing declared English table: " + table)
    return load_catalog(safe_path(repo, "english", "Config"))


def locales(repo: Path) -> list[str]:
    data = read_json(safe_path(repo, "languages.json"))
    if not isinstance(data, dict) or not isinstance(data.get("languages"), list):
        raise ValueError("languages.json must contain a languages array")
    result = []
    for row in data["languages"]:
        code = row.get("code") if isinstance(row, dict) else None
        if not isinstance(code, str) or not LOCALE_CODE.fullmatch(code) or code in result:
            raise ValueError("Invalid or duplicate locale code: " + str(code))
        safe_path(repo, "locales", code)
        result.append(code)
    return sorted(result)


def load_replacements(path: Path) -> dict:
    data = read_json(Path(path))
    if not isinstance(data, dict) or data.get("schemaVersion") != SCHEMA_VERSION or not isinstance(data.get("replacements"), list):
        raise ValueError("Invalid replacement manifest schema")
    result = {}
    for row in data["replacements"]:
        if not isinstance(row, dict) or "from" not in row or "to" not in row:
            raise ValueError("Replacement needs from and to addresses")
        origin = Address.from_dict(row["from"])
        target = None if row["to"] is None else Address.from_dict(row["to"])
        if origin.table not in TABLES or (target is not None and target.table not in TABLES):
            raise ValueError("Unknown localization table in replacement manifest")
        reason = row.get("reason")
        if origin in result or not isinstance(reason, str) or not reason.strip():
            raise ValueError("Duplicate replacement or missing reason: " + str(origin))
        result[origin] = {"to": target, "reason": reason}
    for origin in result:
        seen = set()
        current = origin
        while current in result:
            if current in seen:
                raise ValueError("Replacement cycle: " + str(origin))
            seen.add(current)
            current = result[current]["to"]
    return result


def replacement_for(address: Address, after: dict, registry: dict):
    if address not in registry:
        return None, "No replacement has been declared.", "removed"
    target = registry[address]["to"]
    reason = registry[address]["reason"]
    while target is not None and target not in after and target in registry:
        reason += " " + registry[target]["reason"]
        target = registry[target]["to"]
    if target is not None and target not in after:
        raise ValueError("Replacement destination is missing: " + str(target))
    return target, reason, "unused" if target is None else "replaced"


def build_changes(before: dict, after: dict, registry: dict,
                  before_meta: dict | None = None, after_meta: dict | None = None) -> dict:
    changes = []
    counts = dict.fromkeys(("added", "changed", "replaced", "unused", "removed"), 0)
    for address in sorted(before.keys() | after.keys()):
        old, new = before.get(address), after.get(address)
        if old == new:
            continue
        target, reason = None, ""
        if old is None:
            kind = "added"
        elif new is not None:
            kind = "changed"
        else:
            target, reason, kind = replacement_for(address, after, registry)
        counts[kind] += 1
        changes.append({"address": address.to_dict(), "status": kind,
                        "oldEnglish": old, "newEnglish": new,
                        "needsReview": kind in ("added", "changed", "replaced", "removed"),
                        "replacement": target.to_dict() if target else None,
                        "replacementEnglish": after.get(target),
                        "replacementSourceHash": fingerprint(after[target]) if target else None,
                        "reason": reason})
    return {"schemaVersion": SCHEMA_VERSION,
            "fromSnapshot": public_snapshot_metadata(before_meta or {}),
            "toSnapshot": public_snapshot_metadata(after_meta or {}),
            "summary": counts, "changes": changes}


def state_path(repo: Path, locale: str) -> Path:
    if locale not in locales(repo):
        raise ValueError("Unknown locale: " + locale)
    return safe_path(repo, "locales", locale, "review-state.json")


def load_state(repo: Path, locale: str) -> dict:
    data = read_json(state_path(repo, locale), {"schemaVersion": SCHEMA_VERSION, "reviewed": []})
    if not isinstance(data, dict) or data.get("schemaVersion") != SCHEMA_VERSION or not isinstance(data.get("reviewed"), list):
        raise ValueError("Invalid review state for " + locale)
    result = {}
    for row in data["reviewed"]:
        if not isinstance(row, dict):
            raise ValueError("Review records must be objects for " + locale)
        address = Address.from_dict({key: value for key, value in row.items()
                                     if key in ("table", "id", "field", "section", "kind")})
        english = row.get("english")
        source_hash, translation_hash = row.get("sourceHash"), row.get("translationHash")
        if address in result or not isinstance(english, str) or not isinstance(source_hash, str) or not isinstance(translation_hash, str):
            raise ValueError("Invalid or duplicate review record for " + locale)
        if not HASH.fullmatch(translation_hash) or source_hash != fingerprint(english):
            raise ValueError("Invalid review fingerprint for " + locale)
        result[address] = row
    return result


def save_state(repo: Path, locale: str, records: dict) -> None:
    write_json(state_path(repo, locale), {"schemaVersion": SCHEMA_VERSION,
                                        "reviewed": [records[key] for key in sorted(records)]})


def acknowledgement(address: Address, english: str, translation: str) -> dict:
    return {**address.to_dict(), "english": english, "sourceHash": fingerprint(english),
            "translationHash": fingerprint(translation)}


def label(address: dict) -> str:
    identity = "/".join(str(address[key]) for key in ("section", "kind", "id") if address.get(key))
    return address["table"] + " / " + identity + " / " + address["field"]


def cell(value) -> str:
    return html.escape(str(value or "")).replace("|", "&#124;").replace("`", "&#96;").replace("\r\n", "\n").replace("\n", "<br>")


def details(title: str, pairs: list[tuple[str, str | None]]) -> list[str]:
    lines = ["", "<details><summary>" + cell(title) + "</summary>", ""]
    for heading, value in pairs:
        if value is None:
            continue
        lines += ["**" + heading + "**", "", cell(value), ""]
    return lines + ["</details>", ""]


def snapshot_label(metadata: dict) -> str:
    version, date = metadata.get("targetGameVersion"), metadata.get("snapshotDate")
    label = "Signs of Life " + str(version) if version else "Version not recorded"
    return cell(label + (" (" + str(date) + ")" if date else ""))


def render_changes(report: dict) -> str:
    counts = report["summary"]
    lines = ["# English localization changes", "",
             "Previous English reference: " + snapshot_label(report["fromSnapshot"]) + ".",
             "Current English reference: " + snapshot_label(report["toSnapshot"]) + ".", "",
             "; ".join(str(counts[key]) + " " + key for key in counts) + ".", "",
             "Review your translation whenever the English wording changes.",
             "Follow replacement entries to the current field; the report does not move or overwrite your translations.",
             "Ask a maintainer about entries marked removed. See [per-language review status](translation-review.md)",
             "and [updating instructions](UPDATING.md).", "",
             "| Status | Table / ID / field | Replacement | Needs review |", "| --- | --- | --- | --- |"]
    for row in report["changes"]:
        target = label(row["replacement"]) if row["replacement"] else ("Unused" if row["status"] == "unused" else "—")
        lines.append("| " + " | ".join((row["status"], cell(label(row["address"])), cell(target),
                                        "Yes" if row["needsReview"] else "No")) + " |")
    for row in report["changes"]:
        lines += details(label(row["address"]), [("Previous English", row["oldEnglish"]),
                                                  ("Current English", row["newEnglish"]),
                                                  ("Replacement English", row.get("replacementEnglish")),
                                                  ("Replacement note", row["reason"] or None)])
    return "\n".join(lines) + "\n"


def status(repo: Path, output: Path | None = None) -> dict:
    repo = Path(repo)
    current = english_catalog(repo)
    changes = read_json(safe_path(repo, "changes.json"), {"changes": []})
    affected = set()
    retired = {}
    for row in changes.get("retiredFields", []) + changes["changes"]:
        address = Address.from_dict(row["address"])
        if address in current:
            affected.add(address)
        else:
            retired[address] = row
        if row.get("replacement"):
            affected.add(Address.from_dict(row["replacement"]))
    results = []
    for locale in locales(repo):
        translated = load_catalog(safe_path(repo, "locales", locale, "Config"),
                                  reference_dir=safe_path(repo, "english", "Config"))
        reviewed = load_state(repo, locale)
        pending, missing, obsolete = [], [], []
        missing_count = 0
        for address, english in sorted(current.items()):
            translation = translated.get(address)
            record = reviewed.get(address)
            confirmed = bool(record and record["sourceHash"] == fingerprint(english) and
                             translation is not None and record["translationHash"] == fingerprint(translation))
            if translation is None or (translation == english and record is None):
                missing_count += 1
                if address in affected:
                    missing.append(address.to_dict())
                continue
            if confirmed:
                continue
            reasons = []
            if record is None:
                reasons.append("not_reviewed")
            else:
                if record["sourceHash"] != fingerprint(english):
                    reasons.append("english_changed")
                if record["translationHash"] != fingerprint(translation):
                    reasons.append("translation_changed")
            ack = acknowledgement(address, english, translation)
            pending.append({"address": address.to_dict(), "needsReview": True, "reasons": reasons,
                            "english": english, "previousEnglish": record["english"] if record else None,
                            "translation": translation, "sourceHash": ack["sourceHash"],
                            "translationHash": ack["translationHash"], "acknowledgment": ack})
        for address in sorted(translated.keys() - current.keys()):
            removal = retired.get(address, {})
            target = removal.get("replacement")
            obsolete.append({"address": address.to_dict(), "translation": translated[address],
                             "status": removal.get("status", "removed"), "replacement": target,
                             "existingTargetTranslation": translated.get(Address.from_dict(target)) if target else None,
                             "reason": removal.get("reason", "No replacement has been declared.")})
        results.append({"locale": locale,
                        "summary": {"needsReview": len(pending), "missing": missing_count,
                                    "retiredTranslations": len(obsolete)},
                        "needsReview": pending, "missing": missing, "retiredTranslations": obsolete})
    report = {"schemaVersion": SCHEMA_VERSION, "snapshot": source_metadata(repo), "locales": results}
    if output is None:
        destination = repo.absolute()
    else:
        destination = Path(output)
        if not destination.is_absolute():
            destination = repo / destination
    # Reports and acknowledgments always stay inside the explicitly selected repo.
    destination = safe_path(repo, str(destination.absolute().relative_to(repo.absolute())))
    write_json(safe_path(destination, "translation-review.json"), report)
    safe_path(destination, "translation-review.md").write_text(render_status(report), encoding="utf-8")
    guide = safe_path(repo, "UPDATING.md")
    if destination.resolve() != repo.resolve() and guide.exists():
        safe_path(destination, "UPDATING.md").write_text(guide.read_text(encoding="utf-8-sig"), encoding="utf-8")
    return report


def render_status(report: dict) -> str:
    lines = ["# Translation review status", "",
             "Review the translations listed below to check that they still match the current English.",
             "Entries stay listed until you confirm that you have checked them.",
             "Missing counts cover the whole catalogue; missing-address lists in JSON cover this refresh's affected fields.",
             "See [updating instructions](UPDATING.md) and `translation-review.json` for copyable acknowledgments.", "",
             "| Language | Needs review | Missing translations | Retired entries to clean up |",
             "| --- | ---: | ---: | ---: |"]
    for row in report["locales"]:
        counts = row["summary"]
        lines.append(f"| {row['locale']} | {counts['needsReview']} | {counts['missing']} | {counts['retiredTranslations']} |")
    for row in report["locales"]:
        if not row["needsReview"] and not row["retiredTranslations"]:
            continue
        lines += ["", "## " + row["locale"], ""]
        for field in row["needsReview"]:
            lines += details(label(field["address"]) + " — needs review", [
                ("Last reviewed English", field["previousEnglish"]), ("Current English", field["english"]),
                ("Current translation", field["translation"]), ("English fingerprint", field["sourceHash"])])
        if row["retiredTranslations"]:
            lines += ["| Retired field | Status | Replacement | Preserved translation |", "| --- | --- | --- | --- |"]
            for field in row["retiredTranslations"]:
                target = label(field["replacement"]) if field["replacement"] else "—"
                lines.append("| " + " | ".join((cell(label(field["address"])), field["status"],
                                                cell(target), cell(field["translation"]))) + " |")
    return "\n".join(lines) + "\n"


def refresh(previous_repo: Path, repo: Path, replacements_path: Path) -> dict:
    previous_repo, repo = Path(previous_repo), Path(repo)
    old_root, new_root = previous_repo.resolve(), repo.resolve()
    if old_root == new_root or old_root.is_relative_to(new_root) or new_root.is_relative_to(old_root):
        raise ValueError("Previous and candidate repositories must not overlap")
    before = english_catalog(previous_repo)
    after = english_catalog(repo)
    registry = load_replacements(replacements_path)
    report = build_changes(before, after, registry,
                           source_metadata(previous_repo), source_metadata(repo))
    previous_changes = read_json(safe_path(previous_repo, "changes.json"), {"changes": []})
    retired = {Address.from_dict(row["address"]): row
               for row in previous_changes.get("retiredFields", previous_changes["changes"])
               if row["status"] in ("removed", "replaced", "unused")}
    retired.update({Address.from_dict(row["address"]): row for row in report["changes"]
                    if row["status"] in ("removed", "replaced", "unused")})
    for address, row in retired.items():
        if address in after:
            continue
        if address in registry:
            target, reason, kind = replacement_for(address, after, registry)
            row = {**row, "replacement": target.to_dict() if target else None,
                   "replacementEnglish": after.get(target),
                   "replacementSourceHash": fingerprint(after[target]) if target else None,
                   "status": kind, "needsReview": target is not None, "reason": reason}
            retired[address] = row
        elif row.get("replacement") and Address.from_dict(row["replacement"]) not in after:
            retired[address] = {**row, "status": "removed", "replacement": None,
                                "replacementEnglish": None, "replacementSourceHash": None,
                                "needsReview": True,
                                "reason": "The historical replacement was also removed without a declared destination."}
    report["retiredFields"] = [retired[key] for key in sorted(retired) if key not in after]
    previous_tracking = safe_path(previous_repo, "translation-review.json").exists()
    previous_locales = set(locales(previous_repo))
    # Bootstrap once against old English, not the newly exported snapshot.
    for locale in locales(repo):
        records = load_state(repo, locale)
        if not previous_tracking and not state_path(repo, locale).exists() and locale in previous_locales:
            old_translation = load_catalog(safe_path(previous_repo, "locales", locale, "Config"),
                                           reference_dir=safe_path(previous_repo, "english", "Config"))
            for address in sorted(before.keys() & old_translation.keys()):
                if old_translation[address] != before[address]:
                    records[address] = acknowledgement(address, before[address], old_translation[address])
        save_state(repo, locale, records)
    write_json(safe_path(repo, "changes.json"), report)
    safe_path(repo, "changes.md").write_text(render_changes(report), encoding="utf-8")
    status(repo)
    return report


def acknowledge(repo: Path, locale: str, address: Address, expected_source_hash: str) -> None:
    current = english_catalog(repo)
    translated = load_catalog(safe_path(repo, "locales", locale, "Config"),
                              reference_dir=safe_path(repo, "english", "Config"))
    if address not in current or fingerprint(current[address]) != expected_source_hash:
        raise ValueError("English fingerprint is stale or field is unknown; review current English first")
    if address not in translated:
        raise ValueError("Cannot acknowledge a missing translation")
    records = load_state(repo, locale)
    records[address] = acknowledgement(address, current[address], translated[address])
    save_state(repo, locale, records)


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest="command", required=True)
    prepare = commands.add_parser("refresh", help="Compare previous English and prepare candidate reports")
    prepare.add_argument("--previous-repo", type=Path, required=True)
    prepare.add_argument("--repo", type=Path, required=True)
    prepare.add_argument("--replacements", type=Path, required=True)
    check = commands.add_parser("status", help="Report outstanding review work without changing translations")
    check.add_argument("--repo", type=Path, default=Path("."))
    check.add_argument("--output", type=Path)
    review = commands.add_parser("review", help="Acknowledge one explicitly reviewed translation")
    review.add_argument("--repo", type=Path, default=Path("."))
    review.add_argument("--locale", required=True)
    review.add_argument("--table", required=True)
    review.add_argument("--id", required=True)
    review.add_argument("--field", required=True)
    review.add_argument("--section", default="")
    review.add_argument("--kind", default="")
    review.add_argument("--source-hash", required=True)
    args = parser.parse_args(argv)
    try:
        if args.command == "refresh":
            result = refresh(args.previous_repo, args.repo, args.replacements)
            print("Localization changes: " + json.dumps(result["summary"]))
        elif args.command == "status":
            result = status(args.repo, args.output)
            print("Outstanding translation reviews: " + str(sum(row["summary"]["needsReview"] for row in result["locales"])))
        else:
            address = Address.from_dict({"table": args.table, "id": args.id, "field": args.field,
                                         "section": args.section, "kind": args.kind})
            acknowledge(args.repo, args.locale, address, args.source_hash)
            status(args.repo)
            print("Reviewed " + label(address.to_dict()) + " for " + args.locale)
    except (ValueError, OSError, KeyError, TypeError) as error:
        parser.exit(1, "Localization report failed: " + str(error) + "\n")
    return 0


if __name__ == "__main__":
    sys.exit(main())
