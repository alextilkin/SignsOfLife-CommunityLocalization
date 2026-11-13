"""Content-free catalogue/address regressions for localization refreshes."""
from __future__ import annotations

import json
import os
from pathlib import Path
import sys
import tempfile
import unittest


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from localization_catalog import Address, TABLES, fields_for_table, load_catalog


class AddressTests(unittest.TestCase):
    def test_round_trip_and_order_are_structured(self):
        first = Address("RuntimeContentLocalization.json", "c", "Name", kind="a:b")
        second = Address("RuntimeContentLocalization.json", "b:c", "Name", kind="a")
        self.assertNotEqual(first, second)
        self.assertEqual(first, Address.from_dict(first.to_dict()))
        self.assertEqual(first.to_dict(), {
            "table": first.table, "id": "c", "field": "Name", "kind": "a:b",
        })
        self.assertEqual(sorted([second, first]), [second, first])
        self.assertNotIn("section", Address("UILocalization.json", "ui.key", "Text").to_dict())

    def test_invalid_addresses_are_rejected(self):
        good = {"table": "UILocalization.json", "id": "ui.key", "field": "Text"}
        for bad in (None, [], {}, {**good, "id": 1}, {**good, "field": " "},
                    {**good, "kind": None}, {**good, "section": " "},
                    {**good, "unknown": "x"}, {**good, "table": "../table.json"}):
            with self.subTest(bad=bad), self.assertRaises(ValueError):
                Address.from_dict(bad)


class CatalogTests(unittest.TestCase):
    def test_ui_keeps_exact_text_and_ignores_empty_values(self):
        fields = fields_for_table("UILocalization.json", [
            {"ID": "ui.label", "Text": " Label: \n", "Name": "identity"},
            {"ID": "empty", "Text": " \t"}, {"ID": "null", "Text": None},
        ])
        self.assertEqual(fields, {Address("UILocalization.json", "ui.label", "Text"): " Label: \n"})

    def test_dialogue_variants_keep_numeric_identity_and_explicit_fallback(self):
        fields = fields_for_table("DialogLocalization.json", [
            {"ID": 0, "Normal": "normal", "Robot": "", "Gangster": "gangster", "Cowboy": "cowboy"},
            {"ID": "2", "Normal": "second", "Robot": "professional"},
        ])
        self.assertEqual({a.field for a in fields if a.id == "0"}, {"Normal", "Gangster", "Cowboy"})
        self.assertEqual(fields[Address("DialogLocalization.json", "2", "Robot")], "professional")

    def test_all_prose_tables_keep_only_their_authoring_fields(self):
        cases = [
            ("helpData.json", {"Key": "HELP", "Label": "label", "Category": "category", "Text": "help", "IsDefault": True}, 3),
            ("journalEntries.json", {"ID": 1, "Message": "journal"}, 1),
            ("MeleeWeaponData.json", {"ItemID": 1, "Name": "sword", "Description": "sharp", "Damage": 1}, 2),
            ("RangedWeaponData.json", {"Kind": "Arrow", "ItemID": 1, "Name": "arrow", "Description": "pointy"}, 2),
            ("ProjectileRegistrationData.json", {"SaveName": "round", "Name": "projectile", "Description": "not a field"}, 1),
            ("CreatureRegistrationData.json", {"LivingEntityType": "ANT", "Name": "ant", "Description": "insect", "CodexCategory": "bug", "Health": 1}, 3),
            ("StaticPrefabRegistrationData.json", {"StaticPrefabType": "DOOR", "SaveName": "saved door", "Name": "door", "DisplayName": "display", "Description": "description", "CodexCategory": "category", "TooltipNameOverride": "hover"}, 5),
            ("DatapadTextData.json", {"ID": 1, "Title": "pad", "Category": "category", "Text": "body", "IsExtractedData": True}, 3),
        ]
        for table, row, count in cases:
            with self.subTest(table=table):
                fields = fields_for_table(table, [row])
                self.assertEqual(len(fields), count)
                self.assertFalse(any(a.field in {"ID", "ItemID", "Kind", "SaveName", "Health"} for a in fields))

    def test_inventory_templates_and_variant_names_use_variant_identity(self):
        row = {"ItemID": "sol.test", "Name": "item", "Complexity": 5,
               "Templates": {"filled": "full", "empty": ""},
               "DescriptionVariants": [
                   {"ID": "partial", "MinLanguage": .5, "Name": "partial name", "Text": "partial prose"},
                   {"ID": "full", "Name": "full name", "Text": "full prose"},
               ]}
        fields = fields_for_table("InventoryItemData.json", [row])
        self.assertEqual(fields[Address("InventoryItemData.json", "sol.test", "DescriptionVariants.partial.Name")], "partial name")
        self.assertEqual(fields[Address("InventoryItemData.json", "sol.test", "Templates.filled")], "full")
        self.assertEqual(len(fields), 6)
        row["DescriptionVariants"].reverse()
        self.assertEqual(fields_for_table("InventoryItemData.json", [row]), fields)

    def test_optional_null_variant_and_bonus_arrays_are_empty(self):
        self.assertEqual(fields_for_table("InventoryItemData.json", [
            {"ItemID": 1, "Name": "item", "DescriptionVariants": None},
        ]), {Address("InventoryItemData.json", "1", "Name"): "item"})
        self.assertEqual(fields_for_table("ArmorSetData.json", {
            "Sets": [{"Name": "set", "Bonuses": None}],
            "Pieces": [{"ItemType": "HAT", "Name": "hat", "Bonuses": None}],
        }), {Address("ArmorSetData.json", "HAT", "Name", section="Pieces"): "hat"})

    def test_static_prefab_state_maps_remain_distinct(self):
        fields = fields_for_table("StaticPrefabRegistrationData.json", [{
            "StaticPrefabType": "DOOR", "SaveAliases": ["old door"],
            "DescriptionsByState": {"open": "open", "closed": "closed"},
            "SpecificTooltips": {"open": "use"},
        }])
        self.assertEqual({a.field for a in fields}, {
            "DescriptionsByState.open", "DescriptionsByState.closed", "SpecificTooltips.open",
        })

    def test_armor_bonus_addresses_survive_reordering(self):
        data = {"Pieces": [
            {"Name": "legacy non-addressable", "Description": "not an overlay task"},
            {"ItemType": "HAT", "Name": "hat", "Description": "cloth", "Bonuses": [
                {"Effect": "x:y", "NumPieces": 2, "Description": "first"},
                {"Effect": "x", "NumPieces": 3, "Description": "second"},
                {"Effect": "mechanical", "EffectIntensity": 9},
            ]},
        ], "Sets": [{"Name": "HAT", "Description": "not translatable", "Bonuses": [
            {"Effect": "unique", "NumPieces": 2, "Description": "set prose"},
        ]}]}
        fields = fields_for_table("ArmorSetData.json", data)
        self.assertEqual(len(fields), 5)
        self.assertEqual({a.section for a in fields}, {"Pieces", "Sets"})
        self.assertFalse(any(a.field == "Name" and a.section == "Sets" for a in fields))
        data["Pieces"][1]["Bonuses"].reverse()
        self.assertEqual(fields_for_table("ArmorSetData.json", data), fields)

    def test_duplicate_mechanical_armor_bonuses_are_not_translation_tasks(self):
        self.assertEqual(fields_for_table("ArmorSetData.json", {
            "Pieces": [{"ItemType": "HAT", "Bonuses": [
                {"Effect": "same", "EffectIntensity": 1},
                {"Effect": "same", "EffectIntensity": 2},
            ]}], "Sets": [{"Name": "set", "Bonuses": [
                {"Effect": "same", "NumPieces": 2},
                {"Effect": "same", "NumPieces": 2},
            ]}],
        }), {})

    def test_recipes_translate_only_explicit_display_names(self):
        data = {"Recipes": [
            {"Name": "inherited", "DisplaySource": "Item:sol.item"},
            {"Name": "debug"}, {"Name": "explicit", "DisplayName": "display"},
        ], "Categories": [{"Key": "explicit", "DisplayName": "category"}],
            "Slots": [{"Key": "slot", "Description": "not translated"}],
            "AdjustedResults": [{"Key": "explicit", "DisplayName": "adjusted"}]}
        fields = fields_for_table("RecipeLocalization.json", data)
        self.assertEqual(len(fields), 3)
        self.assertEqual({a.section for a in fields}, {"Recipes", "Categories", "AdjustedResults"})

    def test_tiles_glyphs_and_runtime_keys_are_not_prose(self):
        self.assertEqual(fields_for_table("TileLocalization.json", [{"ID": 2, "DisplayName": "dirt", "Name": "identity"}]),
                         {Address("TileLocalization.json", "2", "DisplayName"): "dirt"})
        self.assertEqual(fields_for_table("GlyphLocalization.json", [{"ID": "glyph", "English": "frozen", "Text": "display"}]),
                         {Address("GlyphLocalization.json", "glyph", "Text"): "display"})
        fields = fields_for_table("RuntimeContentLocalization.json", [
            {"Kind": "a:b", "ID": "c", "Name": "first", "effect.test": "effect", "Number": 3},
            {"Kind": "a", "ID": "b:c", "Name": "second"},
        ])
        self.assertEqual(len(fields), 3)
        self.assertEqual({a.kind for a in fields}, {"a:b", "a"})

    def test_duplicate_identities_and_bonus_keys_are_rejected(self):
        cases = [
            ("UILocalization.json", [{"ID": "same"}, {"ID": "same", "Text": "text"}]),
            ("DialogLocalization.json", [{"ID": 2}, {"ID": "02"}]),
            ("InventoryItemData.json", [{"ItemID": 1}, {"ItemID": "1"}]),
            ("InventoryItemData.json", [{"ItemID": 1, "DescriptionVariants": [{"ID": "same"}, {"ID": "same"}]}]),
            ("RuntimeContentLocalization.json", [{"Kind": "Flora", "ID": "same"}, {"Kind": "Flora", "ID": "same"}]),
            ("RecipeLocalization.json", {"Recipes": [{"Name": "same"}, {"Name": "same"}]}),
            ("ArmorSetData.json", {"Pieces": [{"ItemType": "HAT"}, {"ItemType": "HAT"}]}),
            ("ArmorSetData.json", {"Sets": [{"Name": "set", "Bonuses": [
                {"Effect": "same", "NumPieces": 2, "Description": "a"},
                {"Effect": "same", "NumPieces": 2, "Description": "b"},
            ]}]}),
        ]
        for table, data in cases:
            with self.subTest(table=table, data=data), self.assertRaisesRegex(ValueError, "Duplicate"):
                fields_for_table(table, data)

    def test_malformed_shapes_and_text_are_rejected(self):
        cases = [
            ("UILocalization.json", {}), ("UILocalization.json", [None]),
            ("UILocalization.json", [{"Text": "missing ID"}]),
            ("UILocalization.json", [{"ID": "key", "Text": 1}]),
            ("DialogLocalization.json", [{"ID": True}]),
            ("DialogLocalization.json", [{"ID": "word"}]),
            ("InventoryItemData.json", [{"ItemID": 1, "Templates": []}]),
            ("InventoryItemData.json", [{"ItemID": 1, "DescriptionVariants": {}}]),
            ("InventoryItemData.json", [{"ItemID": 1, "DescriptionVariants": [{"ID": "full", "Name": []}]}]),
            ("ArmorSetData.json", []), ("ArmorSetData.json", {"Pieces": {}}),
            ("ArmorSetData.json", {"Sets": [{"Name": "set", "Bonuses": {}}]}),
            ("ArmorSetData.json", {"Sets": [{"Name": "set", "Bonuses": [{"Description": "no effect"}]}]}),
            ("RecipeLocalization.json", []), ("RecipeLocalization.json", {"Recipes": None}),
            ("RuntimeContentLocalization.json", [{"Kind": "Flora", "Name": "missing ID"}]),
        ]
        for table, data in cases:
            with self.subTest(table=table, data=data), self.assertRaises(ValueError):
                fields_for_table(table, data)

    def test_unknown_tables_are_rejected(self):
        with self.assertRaisesRegex(ValueError, "Unsupported"):
            fields_for_table("playerConfig.json", [])


class CatalogFileTests(unittest.TestCase):
    def setUp(self):
        root = ROOT / ".artifacts" / "localization-catalog-tests"
        root.mkdir(parents=True, exist_ok=True)
        self.temporary = tempfile.TemporaryDirectory(dir=root)
        self.root = Path(self.temporary.name)

    def tearDown(self):
        self.temporary.cleanup()

    def armor_catalogs(self, source, overlay):
        english = self.root / "english"
        locale = self.root / "locale"
        english.mkdir(exist_ok=True)
        locale.mkdir(exist_ok=True)
        (english / "ArmorSetData.json").write_text(json.dumps(source), encoding="utf-8")
        (locale / "ArmorSetData.json").write_text(json.dumps(overlay), encoding="utf-8")
        return english, locale

    def test_partial_armor_bonuses_use_source_identity_without_copying_prose(self):
        # Mirrors PackLocalizationOverlayTests.ArmorOverlayReplacesPieceProseAndSetBonusDescription.
        source = {"Sets": [{"Name": "Iron Set", "Bonuses": [
            {"NumPieces": 2, "Effect": "MAX_HEALTH", "Description": "English set bonus"},
        ]}], "Pieces": [{"ItemType": "IRON_GLOVES", "Name": "Iron Gloves", "Description": "English gloves.", "Bonuses": [
            {"NumPieces": 1, "Effect": "THORNS", "Description": "English piece bonus"},
        ]}]}
        overlay = {"Sets": [{"Name": "Iron Set", "Bonuses": [
            {"NumPieces": 2, "Description": "[test] set bonus", "EffectIntensity": 99},
        ]}], "Pieces": [{"ItemType": "IRON_GLOVES", "Name": "[test] Iron Gloves", "Bonuses": [
            {"Description": "[test] piece bonus"},
        ]}, {"ItemType": "MISSING_ARMOR", "Name": "Nope"}]}
        english, locale = self.armor_catalogs(source, overlay)
        original_source = (english / "ArmorSetData.json").read_bytes()
        fields = load_catalog(locale, reference_dir=english)
        self.assertEqual(fields[Address("ArmorSetData.json", "Iron Set", 'Bonuses.["MAX_HEALTH",2].Description', section="Sets")], "[test] set bonus")
        self.assertEqual(fields[Address("ArmorSetData.json", "IRON_GLOVES", 'Bonuses.["THORNS",1].Description', section="Pieces")], "[test] piece bonus")
        self.assertEqual(fields[Address("ArmorSetData.json", "MISSING_ARMOR", "Name", section="Pieces")], "Nope")
        self.assertNotIn(Address("ArmorSetData.json", "IRON_GLOVES", "Description", section="Pieces"), fields)
        self.assertFalse(any(value.startswith("English") for value in fields.values()))
        self.assertEqual((english / "ArmorSetData.json").read_bytes(), original_source)

    def test_set_bonuses_match_first_num_pieces_or_original_overlay_index(self):
        source = {"Sets": [{"Name": "set", "Bonuses": [
            {"NumPieces": 2, "Effect": "first", "Description": "first source"},
            {"NumPieces": 2, "Effect": "second", "Description": "second source"},
            {"NumPieces": 4, "Effect": "third", "Description": "third source"},
        ]}]}
        overlay = {"Sets": [{"Name": "set", "Bonuses": [
            {"NumPieces": 2, "Effect": "second", "Description": "count match"},
            {"Description": "index match"},
            {"NumPieces": 4, "Description": "third match"},
        ]}]}
        english, locale = self.armor_catalogs(source, overlay)
        source_before = load_catalog(english)
        before = load_catalog(locale, reference_dir=english)
        first = Address("ArmorSetData.json", "set", 'Bonuses.["first",2].Description', section="Sets")
        second = Address("ArmorSetData.json", "set", 'Bonuses.["second",2].Description', section="Sets")
        self.assertEqual(before[first], "count match")
        self.assertEqual(before[second], "index match")
        source["Sets"][0]["Bonuses"][:2] = reversed(source["Sets"][0]["Bonuses"][:2])
        self.armor_catalogs(source, overlay)
        after = load_catalog(locale, reference_dir=english)
        self.assertEqual(load_catalog(english), source_before)
        self.assertEqual(after[first], "index match")
        self.assertEqual(after[second], "count match")

    def test_piece_bonuses_always_follow_runtime_position_not_locale_metadata(self):
        source = {"Pieces": [{"ItemType": "HAT", "Bonuses": [
            {"Effect": "first", "Description": "first source"},
            {"Effect": "second", "Description": "second source"},
        ]}]}
        overlay = {"Pieces": [{"ItemType": " HAT ", "Bonuses": [
            {"Effect": "second", "NumPieces": 99, "Description": "first translation"},
            {"Description": "second translation"},
        ]}]}
        english, locale = self.armor_catalogs(source, overlay)
        source_before = load_catalog(english)
        before = load_catalog(locale, reference_dir=english)
        first = Address("ArmorSetData.json", "HAT", 'Bonuses.["first",null].Description', section="Pieces")
        second = Address("ArmorSetData.json", "HAT", 'Bonuses.["second",null].Description', section="Pieces")
        self.assertEqual(before[first], "first translation")
        self.assertEqual(before[second], "second translation")
        source["Pieces"][0]["Bonuses"].reverse()
        self.armor_catalogs(source, overlay)
        after = load_catalog(locale, reference_dir=english)
        self.assertEqual(load_catalog(english), source_before)
        self.assertEqual(after[first], "second translation")
        self.assertEqual(after[second], "first translation")

    def test_blank_armor_overrides_keep_original_indices_and_do_not_copy_source(self):
        source = {"Pieces": [{"ItemType": "HAT", "Bonuses": [
            {"Effect": "first", "Description": "first source"},
            {"Effect": "second", "Description": "second source"},
        ]}]}
        overlay = {"Pieces": [{"ItemType": "HAT", "Bonuses": [None, {"Description": "second translation"}, {}]}]}
        english, locale = self.armor_catalogs(source, overlay)
        fields = load_catalog(locale, reference_dir=english)
        self.assertEqual(fields, {Address("ArmorSetData.json", "HAT", 'Bonuses.["second",null].Description', section="Pieces"): "second translation"})

    def test_unmatched_armor_bonus_overrides_are_rejected(self):
        source = {"Pieces": [{"ItemType": "HAT", "Bonuses": []}],
                  "Sets": [{"Name": "set", "Bonuses": [{"Effect": "effect", "NumPieces": 2, "Description": "source"}]}]}
        overlays = [
            {"Pieces": [{"ItemType": "HAT", "Bonuses": [{"Description": "no index"}]}]},
            {"Pieces": [{"ItemType": "UNKNOWN", "Bonuses": [{"Effect": "effect", "Description": "no row"}]}]},
            {"Sets": [{"Name": "set", "Bonuses": [{"NumPieces": 8, "Description": "no count"}]}]},
        ]
        for overlay in overlays:
            english, locale = self.armor_catalogs(source, overlay)
            with self.subTest(overlay=overlay), self.assertRaisesRegex(ValueError, "Unknown"):
                load_catalog(locale, reference_dir=english)

    def test_set_missing_source_num_pieces_matches_runtime_zero_default(self):
        source = {"Sets": [{"Name": "set", "Bonuses": [{"Effect": "effect", "Description": "source"}]}]}
        overlay = {"Sets": [{"Name": "set", "Bonuses": [{"NumPieces": 0, "Description": "translation"}]}]}
        english, locale = self.armor_catalogs(source, overlay)
        self.assertEqual(load_catalog(locale, reference_dir=english), {
            Address("ArmorSetData.json", "set", 'Bonuses.["effect",null].Description', section="Sets"): "translation",
        })

    def test_missing_tables_are_skipped_and_utf8_bom_is_supported(self):
        path = self.root / "UILocalization.json"
        path.write_text('[{"ID":"key","Text":" Ω label "}]', encoding="utf-8-sig")
        (self.root / "ignored.json").write_text("not JSON", encoding="utf-8")
        self.assertEqual(load_catalog(self.root), {Address(path.name, "key", "Text"): " Ω label "})
        self.assertEqual(len(TABLES), 18)

    def test_duplicate_json_object_fields_are_rejected(self):
        (self.root / "UILocalization.json").write_text(
            '[{"ID":"key","Text":"first","Text":"second"}]', encoding="utf-8")
        with self.assertRaisesRegex(ValueError, "Duplicate JSON field"):
            load_catalog(self.root)

    def test_invalid_json_and_directories_are_rejected(self):
        path = self.root / "UILocalization.json"
        path.write_text("{invalid", encoding="utf-8")
        with self.assertRaisesRegex(ValueError, "UILocalization.json"):
            load_catalog(self.root)
        path.unlink()
        path.mkdir()
        with self.assertRaisesRegex(ValueError, "not a file"):
            load_catalog(self.root)
        with self.assertRaisesRegex(ValueError, "does not exist"):
            load_catalog(self.root / "missing")

    def test_linked_input_tables_and_directories_are_rejected(self):
        external = self.root / "external"
        external.mkdir()
        (external / "UILocalization.json").write_text('[{"ID":"key","Text":"text"}]', encoding="utf-8")
        config = self.root / "config"
        config.mkdir()
        link = config / "UILocalization.json"
        try:
            link.symlink_to(external / "UILocalization.json")
        except (OSError, NotImplementedError) as error:
            self.skipTest(f"Symlink creation is unavailable: {error}")
        with self.assertRaisesRegex(ValueError, "Linked"):
            load_catalog(config)
        link.unlink()
        linked_dir = self.root / "linked"
        linked_dir.symlink_to(external, target_is_directory=True)
        with self.assertRaisesRegex(ValueError, "Linked"):
            load_catalog(linked_dir)
        with self.assertRaisesRegex(ValueError, "Linked"):
            load_catalog(linked_dir / "child")

    @unittest.skipUnless(os.name == "nt", "Windows junction check")
    def test_windows_junction_input_directory_is_rejected(self):
        import subprocess
        target = self.root / "target"
        target.mkdir()
        link = self.root / "junction"
        result = subprocess.run(["cmd", "/c", "mklink", "/J", str(link), str(target)],
                                capture_output=True, text=True)
        if result.returncode:
            self.skipTest(f"Junction creation is unavailable: {result.stderr}")
        try:
            with self.assertRaisesRegex(ValueError, "Linked"):
                load_catalog(link)
        finally:
            link.rmdir()

    def test_current_source_catalogue_uses_all_supported_schemas(self):
        config = ROOT / "english" / "Config"
        fields = load_catalog(config)
        self.assertEqual({address.table for address in fields}, set(TABLES))
        self.assertEqual(fields[Address("InventoryItemData.json", "10086", "DescriptionVariants.partial.Name")], "Xenite Crystal")
        self.assertIn(Address("UILocalization.json", "agis.unknownDescription", "Text"), fields)
        self.assertFalse(any(a.table == "GlyphLocalization.json" and a.field == "English" for a in fields))


if __name__ == "__main__":
    unittest.main()
