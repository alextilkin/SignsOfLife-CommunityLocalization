import importlib.util
import json
from pathlib import Path
import unittest


SCRIPT = Path(__file__).resolve().parents[1] / "scripts" / "export-pack-item-prose.py"
SPEC = importlib.util.spec_from_file_location("export_pack_item_prose", SCRIPT)
export = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(export)


class PackItemExportTests(unittest.TestCase):
    def test_pack_prose_merge_preserves_variant_text_and_rules(self):
        variants = [
            {"ID": "known", "Name": "SOURCE_NAME", "Text": "SOURCE {0} [reload]", "Priority": 100,
             "MinLanguage": 0.5, "RequiredKnowledgeFlags": ["RULE_ID"]},
            {"ID": "other", "Text": "SOURCE_OTHER", "Priority": 5},
        ]
        source = json.dumps([{
            "ItemID": "sol.test", "Complexity": 2, "AutoOrganizeString": "SOURCE_SORT",
            "Templates": {"held": "SOURCE [mobname]"}, "DescriptionVariants": variants,
        }, {"ItemID": 123, "DescriptionVariants": variants}], indent=4, separators=(",", ":  "))
        prose = {"sol.test": {"Name": "SOURCE_PACK_NAME", "Description": "SOURCE_PACK_DESCRIPTION"}}
        merged, stats = export.merge(source, prose)
        rows = json.loads(merged)
        self.assertEqual(variants, rows[0]["DescriptionVariants"])
        self.assertEqual(variants, rows[1]["DescriptionVariants"])
        self.assertEqual("SOURCE_PACK_NAME", rows[0]["Name"])
        self.assertEqual("SOURCE_PACK_DESCRIPTION", rows[0]["Description"])
        self.assertEqual({"held": "SOURCE [mobname]"}, rows[0]["Templates"])
        self.assertEqual([], stats["missing_hooks"])
        self.assertEqual([], stats["orphan_hooks"])
        self.assertEqual(merged, export.merge(merged, prose)[0])


if __name__ == "__main__":
    unittest.main()
