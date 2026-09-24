import importlib.util
from pathlib import Path
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
            source, "[test] Usa [jump_key] para {0} @CHECKLIST@."))
        self.assertFalse(coverage.tokens_match(source, "Usa [jump_key] para {0}."))
        self.assertFalse(coverage.tokens_match(source, "Usa [jump_key] para {0."))

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


if __name__ == "__main__":
    unittest.main()
