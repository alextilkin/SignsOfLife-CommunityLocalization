import importlib.util
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest


SCRIPT = Path(__file__).resolve().parents[1] / "scripts" / "measure-coverage.py"
SPEC = importlib.util.spec_from_file_location("measure_coverage", SCRIPT)
coverage = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(coverage)


class CoverageTests(unittest.TestCase):
    def test_duplicate_ids_are_rejected(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "UILocalization.json"
            path.write_text('[{"ID":"menu.play","Text":"Play"},'
                            '{"ID":"menu.play","Text":"Start"}]', encoding="utf-8")
            with self.assertRaisesRegex(ValueError, "duplicate"):
                coverage.load_json(path)
            tile = Path(directory) / "TileLocalization.json"
            tile.write_text('[{"ID":2,"DisplayName":"Dirt"},'
                            '{"ID":"2","DisplayName":"Soil"}]', encoding="utf-8")
            with self.assertRaisesRegex(ValueError, "duplicate"):
                coverage.load_json(tile)

    def test_required_tokens_survive_translation(self):
        source = "Use [jump_key] to collect {0} @CHECKLIST@."
        self.assertTrue(coverage.tokens_match(
            source, "[test] Usa [jump_key] para {0} @LISTA@."))
        self.assertFalse(coverage.tokens_match(source, "Usa [jump_key] para {0}."))
        self.assertFalse(coverage.tokens_match(source, "Usa [jump_key] para {0."))

    def test_highlighted_and_bracketed_words_can_be_translated(self):
        source = "It [was] near @SOURCE CRYSTALS@, signed [CAPTAIN]."
        self.assertTrue(coverage.tokens_match(
            source, "[Estaba] cerca de @CRISTALES@, firmado [CAPTAIN]."))
        self.assertFalse(coverage.tokens_match(
            source, "[Estaba] cerca de @CRISTALES@, firmado."))
        self.assertFalse(coverage.tokens_match(
            source, "[Estaba] cerca de @CRISTALES, firmado [CAPTAIN]."))

    def test_runtime_substitution_tokens_can_be_reordered(self):
        source = ("SOURCE [uiprimary] [worldsecondary] [itemcycle] [hotbarselect] "
                  "[itemname] [level] [mobname] [charge] [capacity] [percent]")
        self.assertTrue(coverage.tokens_match(
            source, ("LOCALE [percent] [capacity] [charge] [mobname] [level] [itemname] "
                     "[hotbarselect] [itemcycle] [worldsecondary] [uiprimary]")))

    def test_runtime_substitution_tokens_cannot_be_dropped_or_translated(self):
        for token in ("[uiprimary]", "[worldsecondary]", "[itemcycle]", "[hotbarselect]",
                      "[itemname]", "[level]", "[mobname]", "[charge]", "[capacity]", "[percent]"):
            source = "SOURCE " + token
            with self.subTest(token=token):
                self.assertFalse(coverage.tokens_match(source, "LOCALE"))
                self.assertFalse(coverage.tokens_match(source, "LOCALE [changed_token]"))

    def test_inherited_and_debug_recipes_are_not_required(self):
        rows = coverage.structured_index("RecipeLocalization.json", {
            "Recipes": [
                {"Name": "Apple", "DisplaySource": "Item:sol.apple"},
                {"Name": "Debug Recipe"},
                {"Name": "Apple Pie", "DisplayName": "Apple Pie"},
            ],
            "Categories": [{"Key": "Food", "DisplayName": "Food"}],
            "Slots": [],
            "AdjustedResults": [],
        })
        self.assertEqual({}, rows["Recipes:Apple"])
        self.assertEqual({}, rows["Recipes:Debug Recipe"])
        self.assertEqual({"DisplayName": "Apple Pie"}, rows["Recipes:Apple Pie"])
        self.assertEqual({"DisplayName": "Food"}, rows["Categories:Food"])

    def test_runtime_kind_is_part_of_stable_key(self):
        rows = coverage.structured_index("RuntimeContentLocalization.json", [
            {"Kind": "Flora", "ID": "sol.sample", "Name": "Plant"},
            {"Kind": "Structure", "ID": "sol.sample", "Name": "Building"},
        ])
        self.assertEqual("Plant", rows["Flora:sol.sample"]["Name"])
        self.assertEqual("Building", rows["Structure:sol.sample"]["Name"])

    def test_recipe_arrays_match_game_preflight(self):
        complete = {key: [] for key in ("Recipes", "Categories", "Slots", "AdjustedResults")}
        coverage.validate_unique_rows(Path("RecipeLocalization.json"), complete)
        for section in complete:
            for replacement in ("missing", None, {}):
                malformed = dict(complete)
                if replacement == "missing":
                    del malformed[section]
                else:
                    malformed[section] = replacement
                with self.subTest(section=section, replacement=replacement):
                    with self.assertRaisesRegex(ValueError, "needs an array"):
                        coverage.validate_unique_rows(Path("RecipeLocalization.json"), malformed)


class ContributorCheckTests(unittest.TestCase):
    def setUp(self):
        self.directory = tempfile.TemporaryDirectory()
        self.addCleanup(self.directory.cleanup)
        self.repo = Path(self.directory.name)
        english_config = self.repo / "english" / "Config"
        locale_config = self.repo / "locales" / "test" / "Config"
        english_config.mkdir(parents=True)
        locale_config.mkdir(parents=True)
        self.locale_ui = locale_config / "UILocalization.json"
        tables = (coverage.UI_TABLES + (coverage.DIALOG_TABLE, coverage.ARMOR_TABLE) +
                  tuple(table[0] for table in coverage.PROSE_TABLES) + coverage.STRUCTURED_TABLES)
        for name in tables:
            empty = {} if name in (coverage.ARMOR_TABLE, "RecipeLocalization.json") else []
            if name == "RecipeLocalization.json":
                empty = {section: [] for section in ("Recipes", "Categories", "Slots", "AdjustedResults")}
            (english_config / name).write_text(json.dumps(empty), encoding="utf-8")
        (english_config / "UILocalization.json").write_text(json.dumps([
            {"ID": "test.label", "Text": "SOURCE_LABEL"},
            {"ID": "test.tokens", "Text": "SOURCE {0} [lightkey] [CAPTAIN] @HIGHLIGHT@"},
        ]), encoding="utf-8")
        (self.repo / "english" / "SOURCE.json").write_text(json.dumps({
            "snapshotCommit": "test-source",
            "overlayableFiles": ["Config/" + name for name in tables],
        }), encoding="utf-8")
        (self.repo / "languages.json").write_text(json.dumps({
            "languages": [{"code": "test", "endonym": "Test fixture"}],
        }), encoding="utf-8")
        self.readme = self.repo / "README.md"
        self.readme.write_text("STALE_README_COVERAGE\n", encoding="utf-8")
        (self.repo / "coverage.md").write_text("STALE_COVERAGE\n", encoding="utf-8")

    def run_check(self):
        return subprocess.run([
            sys.executable, str(SCRIPT), "--repo", str(self.repo),
            "--write", "coverage.md", "--json-out", "coverage.json",
        ], cwd=self.repo, capture_output=True, text=True, encoding="utf-8")

    def test_browser_entry_passes_without_updating_summary_files(self):
        self.locale_ui.write_text(json.dumps([
            {"ID": "test.label", "Text": "LOCALE_TEST_LABEL"},
        ]), encoding="utf-8")
        result = self.run_check()
        self.assertEqual(0, result.returncode, result.stderr)
        measured = json.loads((self.repo / "coverage.json").read_text(encoding="utf-8"))
        self.assertEqual(1, measured["locales"][0]["translated"])
        self.assertEqual(2, measured["locales"][0]["total"])
        self.assertIn("| `test` | 1 | 2 | 50.0% |", result.stdout)
        self.assertEqual("STALE_README_COVERAGE\n", self.readme.read_text(encoding="utf-8"))

    def test_malformed_json_fails_the_contributor_check(self):
        self.locale_ui.write_text('[{"ID":"test.label","Text":"TEST",}]', encoding="utf-8")
        result = self.run_check()
        self.assertNotEqual(0, result.returncode)
        self.assertIn("test:", result.stderr)

    def test_missing_required_tokens_fail_the_contributor_check(self):
        complete = "LOCALE_TEST {0} [lightkey] [CAPTAIN] @HIGHLIGHT@"
        for token in ("{0}", "[lightkey]", "[CAPTAIN]", "@HIGHLIGHT@"):
            with self.subTest(token=token):
                self.locale_ui.write_text(json.dumps([
                    {"ID": "test.tokens", "Text": complete.replace(token, "")},
                ]), encoding="utf-8")
                result = self.run_check()
                self.assertNotEqual(0, result.returncode)
                self.assertIn("tokens", result.stderr)


if __name__ == "__main__":
    unittest.main()
