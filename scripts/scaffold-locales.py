#!/usr/bin/env python3
"""Create empty locale pack folders from languages.json. Does not overwrite translations."""
from __future__ import annotations

import json
from pathlib import Path

TABLES = (
    "UILocalization.json",
    "TooltipLocalization.json",
    "StatusEffectLocalization.json",
    "DialogLocalization.json",
    "helpData.json",
    "journalEntries.json",
    "InventoryItemData.json",
    "MeleeWeaponData.json",
    "RangedWeaponData.json",
    "ProjectileRegistrationData.json",
    "CreatureRegistrationData.json",
    "StaticPrefabRegistrationData.json",
    "DatapadTextData.json",
    "ArmorSetData.json",
)


def unique_mod_name(code: str) -> str:
    return "locale_" + code.lower().replace("-", "_")


def empty_table(name: str) -> str:
    if name == "ArmorSetData.json":
        return '{\n  "Sets": [],\n  "Pieces": []\n}\n'
    return "[]\n"


def main() -> None:
    repo = Path(__file__).resolve().parents[1]
    languages = json.loads((repo / "languages.json").read_text(encoding="utf-8"))["languages"]
    locales = repo / "locales"
    locales.mkdir(exist_ok=True)

    for lang in languages:
        code = lang["code"]
        folder = locales / code
        config = folder / "Config"
        config.mkdir(parents=True, exist_ok=True)
        modinfo_path = folder / "modinfo.json"
        if not modinfo_path.is_file():
            modinfo = {
                "UniqueModName": unique_mod_name(code),
                "DisplayName": lang["endonym"],
                "Description": "Locale overlay pack. Copy this folder to Documents/My Games/Signs of Life/Mods, enable it, then Load Now or restart. Missing strings stay English.",
            }
            modinfo_path.write_text(
                json.dumps(modinfo, indent=2, ensure_ascii=False) + "\n",
                encoding="utf-8",
                newline="\n",
            )
        for name in TABLES:
            path = config / name
            if not path.is_file():
                path.write_text(empty_table(name), encoding="utf-8", newline="\n")


if __name__ == "__main__":
    main()
