"""Read the game's overlayable English prose using stable field addresses.

This module only reads inputs. Identity and gameplay fields never become
translation tasks, and the original spelling/whitespace of prose is retained.
"""
from __future__ import annotations

from dataclasses import dataclass
import json
from pathlib import Path
import re
import stat
from typing import Any, Mapping


UI_TABLES = (
    "UILocalization.json", "TooltipLocalization.json", "StatusEffectLocalization.json",
)
PROSE_TABLES = {
    "helpData.json": ("Key", ("Label", "Category", "Text")),
    "journalEntries.json": ("ID", ("Message",)),
    "InventoryItemData.json": ("ItemID", ("Name", "Description")),
    "MeleeWeaponData.json": ("ItemID", ("Name", "Description")),
    "RangedWeaponData.json": ("ItemID", ("Name", "Description")),
    "ProjectileRegistrationData.json": ("SaveName", ("Name",)),
    "CreatureRegistrationData.json": ("LivingEntityType", ("Name", "Description", "CodexCategory")),
    "StaticPrefabRegistrationData.json": (
        "StaticPrefabType",
        ("Name", "DisplayName", "Description", "CodexCategory", "TooltipNameOverride"),
    ),
    "DatapadTextData.json": ("ID", ("Title", "Category", "Text")),
}
TABLES = UI_TABLES + ("DialogLocalization.json",) + tuple(PROSE_TABLES) + (
    "ArmorSetData.json", "RecipeLocalization.json", "TileLocalization.json",
    "GlyphLocalization.json", "RuntimeContentLocalization.json",
)
_NUMERIC_TABLES = {
    "DialogLocalization.json", "journalEntries.json", "DatapadTextData.json",
    "TileLocalization.json",
}
_ITEM_TABLES = {"InventoryItemData.json", "MeleeWeaponData.json", "RangedWeaponData.json"}


@dataclass(frozen=True, order=True)
class Address:
    table: str
    id: str
    field: str
    section: str = ""
    kind: str = ""

    def __post_init__(self) -> None:
        for name in ("table", "id", "field", "section", "kind"):
            value = getattr(self, name)
            if not isinstance(value, str):
                raise ValueError(f"Address {name} must be a string")
            if (name in {"table", "id", "field"} or value) and not value.strip():
                raise ValueError(f"Address {name} must not be blank")
        if "/" in self.table or "\\" in self.table or self.table in {".", ".."}:
            raise ValueError("Address table must be a filename")

    def to_dict(self) -> dict[str, str]:
        result = {"table": self.table, "id": self.id, "field": self.field}
        if self.section:
            result["section"] = self.section
        if self.kind:
            result["kind"] = self.kind
        return result

    @classmethod
    def from_dict(cls, value: Mapping[str, Any]) -> Address:
        if not isinstance(value, Mapping):
            raise ValueError("Address must be an object")
        allowed = {"table", "id", "field", "section", "kind"}
        if set(value) - allowed:
            raise ValueError("Address contains unknown fields")
        if not {"table", "id", "field"}.issubset(value):
            raise ValueError("Address requires table, id, and field")
        return cls(**value)


def _rows(value: Any, label: str) -> list[dict[str, Any]]:
    if not isinstance(value, list):
        raise ValueError(f"{label} must be an array")
    for row in value:
        if not isinstance(row, dict):
            raise ValueError(f"{label} contains a non-object row")
    return value


def _optional_rows(value: Any, label: str) -> list[dict[str, Any]]:
    return [] if value is None else _rows(value, label)


def _identity(row: dict[str, Any], key: str, label: str,
              *, numeric: bool = False, item: bool = False) -> str:
    value = row.get(key)
    if isinstance(value, bool) or not isinstance(value, (str, int)):
        raise ValueError(f"{label} needs a string or integer {key}")
    if isinstance(value, int):
        if not (numeric or item):
            raise ValueError(f"{label} {key} must be a string")
        return str(value)
    if not value.strip():
        raise ValueError(f"{label} {key} must not be blank")
    if numeric:
        if not re.fullmatch(r"[+-]?\d+", value.strip()):
            raise ValueError(f"{label} {key} must be an integer identity")
        return str(int(value))
    # Compiled numeric ItemIDs and string ItemIDs have the same runtime identity.
    if item and re.fullmatch(r"[+-]?\d+", value.strip()):
        return str(int(value))
    return value


def _text(row: dict[str, Any], field: str, label: str) -> str | None:
    value = row.get(field)
    if value is None:
        return None
    if not isinstance(value, str):
        raise ValueError(f"{label}.{field} must be a string or null")
    return value if value.strip() else None


def fields_for_table(table: str, data: Any) -> dict[Address, str]:
    """Return only nonblank authored prose, keyed by stable identities.

    Armor pieces without ItemType are valid legacy authoring rows, but cannot
    be targeted by a locale overlay and are therefore excluded.
    """
    if table not in TABLES:
        raise ValueError(f"Unsupported localization table: {table}")
    result: dict[Address, str] = {}

    def add(ident: str, field: str, text: str | None,
            section: str = "", kind: str = "") -> None:
        if text is None:
            return
        address = Address(table, ident, field, section, kind)
        if address in result:
            raise ValueError(f"Duplicate localization field: {address.to_dict()}")
        result[address] = text

    def scalars(row: dict[str, Any], ident: str, names: tuple[str, ...],
                section: str = "", kind: str = "") -> None:
        for field in names:
            add(ident, field, _text(row, field, f"{table} {ident}"), section, kind)

    def keyed_rows(value: Any, key: str, section: str = "",
                   numeric: bool = False, item: bool = False):
        seen = set()
        label = table + (f".{section}" if section else "")
        for row in _rows(value, label):
            ident = _identity(row, key, label, numeric=numeric, item=item)
            if ident in seen:
                raise ValueError(f"Duplicate {label} identity: {ident}")
            seen.add(ident)
            yield ident, row

    if table in UI_TABLES:
        for ident, row in keyed_rows(data, "ID"):
            scalars(row, ident, ("Text",))
    elif table == "DialogLocalization.json":
        for ident, row in keyed_rows(data, "ID", numeric=True):
            scalars(row, ident, ("Normal", "Robot", "Gangster", "Cowboy"))
    elif table in PROSE_TABLES:
        key, names = PROSE_TABLES[table]
        for ident, row in keyed_rows(data, key, numeric=table in _NUMERIC_TABLES,
                                     item=table in _ITEM_TABLES):
            scalars(row, ident, names)
            maps = ("Templates",) if table == "InventoryItemData.json" else (
                ("DescriptionsByState", "SpecificTooltips")
                if table == "StaticPrefabRegistrationData.json" else ()
            )
            for name in maps:
                nested = row.get(name, {})
                if nested is None:
                    continue
                if not isinstance(nested, dict):
                    raise ValueError(f"{table} {ident}.{name} must be an object")
                for nested_key in nested:
                    if not isinstance(nested_key, str) or not nested_key.strip():
                        raise ValueError(f"{table} {ident}.{name} needs nonblank string keys")
                    add(ident, f"{name}.{nested_key}", _text(nested, nested_key, name))
            if table == "InventoryItemData.json" and "DescriptionVariants" in row:
                variants = _optional_rows(row["DescriptionVariants"], f"{table} {ident}.DescriptionVariants")
                for variant_id, variant in keyed_rows(variants, "ID", "DescriptionVariants"):
                    for name in ("Name", "Text"):
                        add(ident, f"DescriptionVariants.{variant_id}.{name}",
                            _text(variant, name, f"{table} {ident} variant {variant_id}"))
    elif table == "ArmorSetData.json":
        if not isinstance(data, dict):
            raise ValueError(f"{table} must be an object")
        for section, key in (("Pieces", "ItemType"), ("Sets", "Name")):
            rows = _rows(data.get(section, []), f"{table}.{section}")
            if section == "Pieces":
                rows = [row for row in rows if row.get("ItemType") is not None]
            for ident, row in keyed_rows(rows, key, section):
                if section == "Pieces":
                    scalars(row, ident, ("Name", "Description"), section)
                seen_bonus = set()
                for bonus in _optional_rows(row.get("Bonuses"), f"{table} {ident}.Bonuses"):
                    text = _text(bonus, "Description", f"{table} {ident}.Bonuses")
                    if text is None:
                        continue
                    effect = _identity(bonus, "Effect", f"{table} {ident}.Bonuses")
                    count = bonus.get("NumPieces")
                    if count is not None and (isinstance(count, bool) or not isinstance(count, int)):
                        raise ValueError(f"{table} {ident} bonus NumPieces must be an integer")
                    bonus_id = json.dumps([effect, count], ensure_ascii=False, separators=(",", ":"))
                    if bonus_id in seen_bonus:
                        raise ValueError(f"Duplicate {table} {ident} bonus identity: {bonus_id}")
                    seen_bonus.add(bonus_id)
                    add(ident, f"Bonuses.{bonus_id}.Description", text, section)
    elif table == "RecipeLocalization.json":
        if not isinstance(data, dict):
            raise ValueError(f"{table} must be an object")
        for section, key in (("Recipes", "Name"), ("Categories", "Key"),
                             ("Slots", "Key"), ("AdjustedResults", "Key")):
            for ident, row in keyed_rows(data.get(section, []), key, section):
                scalars(row, ident, ("DisplayName",), section)
    elif table in {"TileLocalization.json", "GlyphLocalization.json"}:
        for ident, row in keyed_rows(data, "ID", numeric=table == "TileLocalization.json"):
            scalars(row, ident, ("Text",) if table == "GlyphLocalization.json" else ("DisplayName",))
    elif table == "RuntimeContentLocalization.json":
        seen = set()
        for row in _rows(data, table):
            ident = _identity(row, "ID", table)
            kind = _identity(row, "Kind", table)
            identity = (kind, ident)
            if identity in seen:
                raise ValueError(f"Duplicate {table} identity: {identity}")
            seen.add(identity)
            for field, value in row.items():
                if field not in {"Kind", "ID"} and isinstance(value, str) and value.strip():
                    add(ident, field, value, kind=kind)
    return dict(sorted(result.items()))


def _unique_object(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in pairs:
        if key in result:
            raise ValueError(f"Duplicate JSON field: {key}")
        result[key] = value
    return result


def _reject_links(path: Path) -> None:
    for part in (path, *path.parents):
        try:
            info = part.lstat()
        except FileNotFoundError:
            continue
        if stat.S_ISLNK(info.st_mode) or getattr(info, "st_file_attributes", 0) & 0x400:
            raise ValueError(f"Linked localization input is not allowed: {part}")


def _config_directory(config_dir: Path) -> tuple[Path, Path]:
    config_dir = Path(config_dir).absolute()
    _reject_links(config_dir)
    if not config_dir.is_dir():
        raise ValueError(f"Localization config directory does not exist: {config_dir}")
    return config_dir, config_dir.resolve(strict=True)


_MISSING = object()


def _read_table(config_dir: Path, resolved_root: Path, table: str) -> Any:
    path = config_dir / table
    _reject_links(path)
    if not path.exists():
        return _MISSING
    if not path.is_file():
        raise ValueError(f"Localization table is not a file: {path}")
    resolved = path.resolve(strict=True)
    if not resolved.is_relative_to(resolved_root):
        raise ValueError(f"Localization table escapes config directory: {path}")
    try:
        return json.loads(path.read_text(encoding="utf-8-sig"), object_pairs_hook=_unique_object)
    except (ValueError, UnicodeError) as error:
        raise ValueError(f"{path}: {error}") from error


def _align_armor_overlay(data: Any, reference: Any) -> dict[str, Any]:
    """Resolve locale bonus prose exactly as PackLocalizationOverlay does.

    Sets with NumPieces target the first matching English bonus; all other
    bonuses target their original overlay position. Locale Effect/NumPieces
    metadata is not authoritative. Only identity metadata is borrowed.
    """
    table = "ArmorSetData.json"
    if not isinstance(data, dict):
        raise ValueError(f"{table} must be an object")
    if reference is _MISSING:
        reference = {}
    # Validate source identities before borrowing any of them.
    fields_for_table(table, reference)
    aligned = dict(data)
    for section, key in (("Pieces", "ItemType"), ("Sets", "Name")):
        source_rows = _rows(reference.get(section, []), f"{table}.{section}")
        by_id = {}
        for row in source_rows:
            if section == "Pieces" and row.get("ItemType") is None:
                continue
            ident = _identity(row, key, f"{table}.{section}")
            by_id[ident] = row
        rows = []
        for row in _rows(data.get(section, []), f"{table}.{section}"):
            if section == "Pieces" and row.get("ItemType") is None:
                # Match the existing treatment of non-addressable legacy rows.
                rows.append(dict(row))
                continue
            ident = _identity(row, key, f"{table}.{section}")
            if section == "Pieces":
                ident = ident.strip()  # Enum.TryParse(row.ItemType.Trim()).
            normalized = dict(row)
            normalized[key] = ident
            normalized["Bonuses"] = []
            overlay_bonuses = row.get("Bonuses")
            if overlay_bonuses is None:
                overlay_bonuses = []
            if not isinstance(overlay_bonuses, list):
                raise ValueError(f"{table} {ident}.Bonuses must be an array")
            source_row = by_id.get(ident)
            source_bonuses = _optional_rows(source_row.get("Bonuses"), f"{table} {ident}.Bonuses") if source_row else []
            if section == "Pieces":
                # The game does not add source piece bonuses without Effect.
                source_bonuses = [bonus for bonus in source_bonuses
                                  if isinstance(bonus.get("Effect"), str) and bonus["Effect"]]
            for index, bonus in enumerate(overlay_bonuses):
                if bonus is None:
                    continue  # Null slots still count toward positional matching.
                if not isinstance(bonus, dict):
                    raise ValueError(f"{table} {ident}.Bonuses contains a non-object row")
                text = _text(bonus, "Description", f"{table} {ident}.Bonuses[{index}]")
                if text is None:
                    continue  # Empty overrides are ignored by the game.
                if source_row is None:
                    raise ValueError(f"Unknown {table}.{section} row for bonus prose: {ident}")
                matched = None
                if section == "Sets" and bonus.get("NumPieces") is not None:
                    count = bonus["NumPieces"]
                    if isinstance(count, bool) or not isinstance(count, int):
                        raise ValueError(f"{table} {ident} bonus NumPieces must be an integer")
                    matched = next((candidate for candidate in source_bonuses
                                    if (candidate.get("NumPieces") if candidate.get("NumPieces") is not None else 0) == count), None)
                    if matched is None:
                        raise ValueError(f"Unknown {table}.Sets {ident} bonus NumPieces: {count}")
                elif index < len(source_bonuses):
                    matched = source_bonuses[index]
                if matched is None:
                    raise ValueError(f"Unknown {table}.{section} {ident} bonus index: {index}")
                normalized_bonus = dict(bonus)
                normalized_bonus["Effect"] = _identity(matched, "Effect", f"{table} {ident}.Bonuses")
                if matched.get("NumPieces") is None:
                    normalized_bonus.pop("NumPieces", None)
                else:
                    normalized_bonus["NumPieces"] = matched["NumPieces"]
                normalized["Bonuses"].append(normalized_bonus)
            rows.append(normalized)
        aligned[section] = rows
    return aligned


def load_catalog(config_dir: Path, reference_dir: Path | None = None) -> dict[Address, str]:
    """Read known tables without links; resolve locale armor against English.

    Supply reference_dir only for a locale catalogue. It supplies stable armor
    bonus identities, never missing locale text or other English prose.
    """
    config_dir, resolved_root = _config_directory(config_dir)
    reference_armor = _MISSING
    if reference_dir is not None:
        reference_dir, resolved_reference = _config_directory(reference_dir)
        reference_armor = _read_table(reference_dir, resolved_reference, "ArmorSetData.json")
    result: dict[Address, str] = {}
    for table in TABLES:
        data = _read_table(config_dir, resolved_root, table)
        if data is _MISSING:
            continue
        try:
            if reference_dir is not None and table == "ArmorSetData.json":
                data = _align_armor_overlay(data, reference_armor)
            result.update(fields_for_table(table, data))
        except (ValueError, UnicodeError) as error:
            raise ValueError(f"{config_dir / table}: {error}") from error
    return dict(sorted(result.items()))
