"""Regression checks for translator refresh reports and review acknowledgments."""

import hashlib
import importlib.util
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
SCRIPT = ROOT / "scripts" / "localization-change-report.py"
SPEC = importlib.util.spec_from_file_location("localization_change_report", SCRIPT)
report = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = report
SPEC.loader.exec_module(report)


TABLE = "UILocalization.json"


def address(ident, field="Text", table=TABLE):
    return {"table": table, "id": ident, "field": field}


def write_json(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def read_json(path):
    return json.loads(path.read_text(encoding="utf-8-sig"))


def tree_bytes(root):
    return {str(path.relative_to(root)): path.read_bytes()
            for path in root.rglob("*") if path.is_file()}


class LocalizationChangesTests(unittest.TestCase):
    def setUp(self):
        artifacts = ROOT / ".artifacts" / "localization-change-tests"
        artifacts.mkdir(parents=True, exist_ok=True)
        self.temporary = tempfile.TemporaryDirectory(dir=artifacts)
        self.addCleanup(self.temporary.cleanup)
        self.root = Path(self.temporary.name)
        self.previous = self.root / "previous"
        self.repo = self.root / "candidate"
        self.registry = self.root / "replacements.json"
        write_json(self.registry, {"schemaVersion": 1, "replacements": []})

    def make_repo(self, root, english, translations=None, commit="old-source"):
        write_json(root / "english" / "SOURCE.json", {
            "snapshotCommit": commit,
            "targetGameVersion": "test-version",
            "overlayableFiles": ["Config/" + TABLE],
        })
        write_json(root / "english" / "Config" / TABLE,
                   [{"ID": key, "Text": value} for key, value in english.items()])
        write_json(root / "languages.json", {"languages": [{"code": "fr"}]})
        write_json(root / "locales" / "fr" / "Config" / TABLE,
                   [{"ID": key, "Text": value} for key, value in (translations or {}).items()])

    def prepare_change(self, old="Use {0}.", new="Use {0} to select ammo.",
                       translation="[fr] Use {0}."):
        self.make_repo(self.previous, {"tip": old}, {"tip": translation})
        self.make_repo(self.repo, {"tip": new}, {"tip": translation}, commit="new-source")
        return report.refresh(self.previous, self.repo, self.registry)

    def test_readable_changes_show_game_versions_and_dates_without_game_commits(self):
        before = {"snapshotCommit": "private-game-before", "targetGameVersion": "1.0.7", "snapshotDate": "2026-11-11"}
        after = {"snapshotCommit": "private-game-after", "targetGameVersion": "1.0.13", "snapshotDate": "2026-11-13"}
        changes = report.build_changes({}, {}, {}, before, after)
        text = report.render_changes(changes)
        self.assertIn("Previous English reference: Signs of Life 1.0.7 (2026-11-11).", text)
        self.assertIn("Current English reference: Signs of Life 1.0.13 (2026-11-13).", text)
        self.assertNotIn("private-game-before", text)
        self.assertNotIn("private-game-after", text)
        self.assertNotIn("snapshotCommit", changes["fromSnapshot"])
        self.assertNotIn("snapshotCommit", changes["toSnapshot"])

    def test_report_json_excludes_private_source_metadata_on_refresh_and_status(self):
        self.make_repo(self.previous, {"tip": "Before"})
        self.make_repo(self.repo, {"tip": "After"})
        private = {"snapshotCommit": "PRIVATE_REVISION", "snapshotSubject": "PRIVATE_SUBJECT",
                   "reviewStatus": "PRIVATE_PREPARATION", "notes": "PRIVATE_NOTES"}
        for repo in (self.previous, self.repo):
            path = repo / "english" / "SOURCE.json"
            metadata = read_json(path)
            metadata.update(private, snapshotDate="2026-11-13")
            write_json(path, metadata)
        changes = report.refresh(self.previous, self.repo, self.registry)
        status = report.status(self.repo)
        expected = {"targetGameVersion": "test-version", "snapshotDate": "2026-11-13"}
        self.assertEqual(expected, changes["fromSnapshot"])
        self.assertEqual(expected, changes["toSnapshot"])
        self.assertEqual(expected, status["snapshot"])
        for value in private.values():
            self.assertNotIn(value, json.dumps(changes))
            self.assertNotIn(value, json.dumps(status))
        self.assertEqual(private["snapshotCommit"], read_json(self.repo / "english" / "SOURCE.json")["snapshotCommit"])

    def locale_status(self, root=None):
        result = report.status(root or self.repo)
        return next(locale for locale in result["locales"] if locale["locale"] == "fr")

    def write_replacements(self, replacements):
        write_json(self.registry, {"schemaVersion": 1, "replacements": replacements})

    def replacement(self, source, target, reason="Test migration"):
        return {"from": address(source),
                "to": address(target) if target is not None else None,
                "reason": reason}

    def test_fingerprints_use_exact_unicode_source_text(self):
        text = "\u03a9 Use {0}.\nSecond line."
        self.assertEqual(hashlib.sha256(text.encode("utf-8")).hexdigest(),
                         report.fingerprint(text))
        self.assertNotEqual(report.fingerprint(text), report.fingerprint(text + " "))

    def test_changed_english_flags_existing_translation_and_preserves_previous_repo(self):
        self.make_repo(self.previous, {"tip": "Use {0}."}, {"tip": "[fr] Use {0}."})
        self.make_repo(self.repo, {"tip": "Use {0} to select ammo."},
                       {"tip": "[fr] Use {0}."}, commit="new-source")
        previous_bytes = tree_bytes(self.previous)
        changes = report.refresh(self.previous, self.repo, self.registry)

        change = next(row for row in changes["changes"] if row["address"] == address("tip"))
        self.assertEqual("changed", change["status"])
        self.assertTrue(change["needsReview"])
        self.assertEqual("Use {0}.", change["oldEnglish"])
        self.assertEqual("Use {0} to select ammo.", change["newEnglish"])
        self.assertEqual(previous_bytes, tree_bytes(self.previous))
        for filename in ("changes.json", "changes.md", "translation-review.json", "translation-review.md"):
            self.assertTrue((self.repo / filename).is_file(), filename)
        self.assertTrue((self.repo / "locales/fr/review-state.json").is_file())

        locale = self.locale_status()
        self.assertEqual(1, locale["summary"]["needsReview"])
        review = locale["needsReview"][0]
        self.assertEqual(address("tip"), review["address"])
        self.assertEqual("Use {0}.", review["previousEnglish"])
        self.assertEqual("Use {0} to select ammo.", review["english"])
        self.assertEqual("[fr] Use {0}.", review["translation"])
        self.assertEqual(report.fingerprint(review["english"]), review["sourceHash"])
        self.assertEqual(report.fingerprint(review["translation"]), review["translationHash"])
        self.assertTrue(review["acknowledgment"])

    def test_repeated_noop_refresh_does_not_erase_needs_review(self):
        report_changes = self.prepare_change()
        self.assertEqual(1, report_changes["summary"]["changed"])
        next_repo = self.root / "next-candidate"
        shutil.copytree(self.repo, next_repo)
        previous_bytes = tree_bytes(self.repo)

        report.refresh(self.repo, next_repo, self.registry)

        self.assertEqual(previous_bytes, tree_bytes(self.repo))
        locale = self.locale_status(next_repo)
        self.assertEqual(1, locale["summary"]["needsReview"])
        self.assertEqual("Use {0}.", locale["needsReview"][0]["previousEnglish"])

    def test_editing_translation_alone_does_not_acknowledge_new_english(self):
        self.prepare_change()
        write_json(self.repo / "locales/fr/Config" / TABLE,
                   [{"ID": "tip", "Text": "[fr] Revised {0}."}])

        locale = self.locale_status()

        self.assertEqual(1, locale["summary"]["needsReview"])
        self.assertEqual("[fr] Revised {0}.", locale["needsReview"][0]["translation"])

    def test_explicit_acknowledgment_clears_only_the_matching_field(self):
        self.make_repo(self.previous, {"one": "Old one", "two": "Old two"},
                       {"one": "[fr] One", "two": "[fr] Two"})
        self.make_repo(self.repo, {"one": "New one", "two": "New two"},
                       {"one": "[fr] One", "two": "[fr] Two"}, commit="new-source")
        report.refresh(self.previous, self.repo, self.registry)

        report.acknowledge(self.repo, "fr", report.Address.from_dict(address("one")),
                           report.fingerprint("New one"))

        locale = self.locale_status()
        self.assertEqual([address("two")], [row["address"] for row in locale["needsReview"]])
        state = read_json(self.repo / "locales/fr/review-state.json")
        reviewed = next(row for row in state["reviewed"] if row["id"] == "one")
        self.assertEqual("New one", reviewed["english"])
        self.assertEqual(report.fingerprint("New one"), reviewed["sourceHash"])
        self.assertEqual(report.fingerprint("[fr] One"), reviewed["translationHash"])

    def test_acknowledgment_rejects_a_stale_source_hash_without_changing_state(self):
        self.prepare_change()
        state = self.repo / "locales/fr/review-state.json"
        original = state.read_bytes()

        with self.assertRaises(ValueError):
            report.acknowledge(self.repo, "fr", report.Address.from_dict(address("tip")),
                               report.fingerprint("Use {0}."))

        self.assertEqual(original, state.read_bytes())
        self.assertEqual(1, self.locale_status()["summary"]["needsReview"])

    def test_editing_an_acknowledged_translation_requires_another_review(self):
        self.prepare_change()
        report.acknowledge(self.repo, "fr", report.Address.from_dict(address("tip")),
                           report.fingerprint("Use {0} to select ammo."))
        self.assertEqual(0, self.locale_status()["summary"]["needsReview"])
        write_json(self.repo / "locales/fr/Config" / TABLE,
                   [{"ID": "tip", "Text": "[fr] A later edit {0}."}])

        locale = self.locale_status()

        self.assertEqual(1, locale["summary"]["needsReview"])
        self.assertEqual(["translation_changed"], locale["needsReview"][0]["reasons"])

    def test_acknowledgment_rejects_a_missing_translation(self):
        self.make_repo(self.previous, {"tip": "Old"})
        self.make_repo(self.repo, {"tip": "New"}, commit="new-source")
        report.refresh(self.previous, self.repo, self.registry)

        with self.assertRaises(ValueError):
            report.acknowledge(self.repo, "fr", report.Address.from_dict(address("tip")),
                               report.fingerprint("New"))

        self.assertIn(address("tip"), self.locale_status()["missing"])

    def test_replacement_preserves_an_existing_target_translation(self):
        self.make_repo(self.previous, {"legacy": "Old tip", "canonical": "Canonical tip"},
                       {"legacy": "[fr] Legacy", "canonical": "[fr] Preferred"})
        self.make_repo(self.repo, {"canonical": "Canonical tip"},
                       {"legacy": "[fr] Legacy", "canonical": "[fr] Preferred"}, commit="new-source")
        self.write_replacements([self.replacement("legacy", "canonical")])

        changes = report.refresh(self.previous, self.repo, self.registry)

        change = next(row for row in changes["changes"] if row["address"] == address("legacy"))
        self.assertEqual("replaced", change["status"])
        self.assertEqual(address("canonical"), change["replacement"])
        self.assertEqual("Canonical tip", change["replacementEnglish"])
        self.assertEqual(report.fingerprint("Canonical tip"), change["replacementSourceHash"])
        self.assertIn("Canonical tip", (self.repo / "changes.md").read_text(encoding="utf-8"))
        translations = read_json(self.repo / "locales/fr/Config" / TABLE)
        canonical = next(row for row in translations if row["ID"] == "canonical")
        self.assertEqual("[fr] Preferred", canonical["Text"])

    def test_unmapped_removals_are_distinct_from_explicitly_unused_ids(self):
        self.make_repo(self.previous, {"unknown": "Unknown retirement", "unused": "Unused label"},
                       {"unknown": "[fr] Unknown", "unused": "[fr] Unused"})
        self.make_repo(self.repo, {}, {"unknown": "[fr] Unknown", "unused": "[fr] Unused"},
                       commit="new-source")
        self.write_replacements([self.replacement("unused", None, "Unused control")])

        changes = report.refresh(self.previous, self.repo, self.registry)

        statuses = {row["address"]["id"]: row["status"] for row in changes["changes"]}
        self.assertEqual("removed", statuses["unknown"])
        self.assertEqual("unused", statuses["unused"])
        self.assertEqual(2, self.locale_status()["summary"]["retiredTranslations"])

    def test_duplicate_replacement_sources_are_rejected(self):
        self.write_replacements([self.replacement("old", "new"), self.replacement("old", None)])

        with self.assertRaises(ValueError):
            report.load_replacements(self.registry)

    def test_retired_dispositions_survive_a_later_noop_refresh(self):
        self.make_repo(self.previous, {"old": "Old", "unused": "Unused", "target": "Target"},
                       {"old": "[fr] Old", "unused": "[fr] Unused", "target": "[fr] Target"})
        self.make_repo(self.repo, {"target": "Target"},
                       {"old": "[fr] Old", "unused": "[fr] Unused", "target": "[fr] Target"},
                       commit="new-source")
        self.write_replacements([self.replacement("old", "target"),
                                 self.replacement("unused", None, "Unused control")])
        report.refresh(self.previous, self.repo, self.registry)
        next_repo = self.root / "next-candidate"
        shutil.copytree(self.repo, next_repo)

        changes = report.refresh(self.repo, next_repo, self.registry)

        self.assertEqual([], changes["changes"])
        retired = {row["address"]["id"]: row for row in self.locale_status(next_repo)["retiredTranslations"]}
        self.assertEqual("replaced", retired["old"]["status"])
        self.assertEqual(address("target"), retired["old"]["replacement"])
        self.assertEqual("[fr] Target", retired["old"]["existingTargetTranslation"])
        self.assertEqual("unused", retired["unused"]["status"])
        self.assertIsNone(retired["unused"]["replacement"])

    def test_explicit_replacement_chains_resolve_to_the_current_target(self):
        self.write_replacements([self.replacement("old", "middle"),
                                 self.replacement("middle", "current")])
        before = {report.Address.from_dict(address("old")): "Old"}
        after = {report.Address.from_dict(address("current")): "Current"}

        changes = report.build_changes(before, after, report.load_replacements(self.registry))

        old = next(row for row in changes["changes"] if row["address"] == address("old"))
        self.assertEqual("replaced", old["status"])
        self.assertEqual(address("current"), old["replacement"])

    def test_successive_refreshes_update_historical_replacements_to_current_target(self):
        self.make_repo(self.previous, {"old": "Old"}, {"old": "[fr] Original"})
        self.make_repo(self.repo, {"middle": "Middle"},
                       {"old": "[fr] Original", "middle": "[fr] Intermediate"}, commit="middle-source")
        self.write_replacements([self.replacement("old", "middle")])
        report.refresh(self.previous, self.repo, self.registry)
        next_repo = self.root / "next-candidate"
        shutil.copytree(self.repo, next_repo)
        write_json(next_repo / "english/Config" / TABLE, [{"ID": "current", "Text": "Current"}])
        write_json(next_repo / "locales/fr/Config" / TABLE, [
            {"ID": "old", "Text": "[fr] Original"},
            {"ID": "middle", "Text": "[fr] Intermediate"},
            {"ID": "current", "Text": "[fr] Final"},
        ])
        self.write_replacements([self.replacement("old", "middle"),
                                 self.replacement("middle", "current")])

        changes = report.refresh(self.repo, next_repo, self.registry)

        historical = next(row for row in changes["retiredFields"] if row["address"] == address("old"))
        self.assertEqual(address("current"), historical["replacement"])
        retired = {row["address"]["id"]: row for row in self.locale_status(next_repo)["retiredTranslations"]}
        self.assertEqual(address("current"), retired["old"]["replacement"])
        self.assertEqual(address("current"), retired["middle"]["replacement"])
        self.assertEqual("[fr] Final", retired["old"]["existingTargetTranslation"])

    def test_replacement_cycles_are_rejected(self):
        self.write_replacements([self.replacement("one", "two"), self.replacement("two", "one")])

        with self.assertRaises(ValueError):
            report.load_replacements(self.registry)

    def test_replacement_to_a_missing_destination_is_rejected(self):
        self.make_repo(self.previous, {"old": "Old"})
        self.make_repo(self.repo, {}, commit="new-source")
        self.write_replacements([self.replacement("old", "does-not-exist")])

        with self.assertRaises(ValueError):
            report.refresh(self.previous, self.repo, self.registry)

    def test_locale_path_escape_is_rejected(self):
        self.prepare_change()
        outside = self.root / "outside"

        with self.assertRaises(ValueError):
            report.acknowledge(self.repo, "../outside", report.Address.from_dict(address("tip")),
                               report.fingerprint("Use {0} to select ammo."))

        self.assertFalse(outside.exists())

    def test_cli_relative_repository_and_report_directory_stay_under_candidate(self):
        self.prepare_change()
        (self.repo / "UPDATING.md").write_text("Review instructions", encoding="utf-8")

        result = subprocess.run(
            [sys.executable, "-B", str(SCRIPT), "status", "--repo", "candidate", "--output", "review"],
            cwd=self.root, capture_output=True, text=True)

        self.assertEqual(0, result.returncode, result.stderr)
        generated = self.repo / "review" / "translation-review.json"
        self.assertTrue(generated.is_file())
        self.assertTrue((self.repo / "review" / "translation-review.md").is_file())
        self.assertEqual("Review instructions", (self.repo / "review" / "UPDATING.md").read_text(encoding="utf-8"))
        self.assertFalse((self.root / "review").exists())
        self.assertEqual(1, read_json(generated)["locales"][0]["summary"]["needsReview"])

    def test_unknown_manifest_table_is_rejected(self):
        row = self.replacement("old", "new")
        row["from"]["table"] = "UILocalizaton.json"
        self.write_replacements([row])
        with self.assertRaisesRegex(ValueError, "Unknown localization table"):
            report.load_replacements(self.registry)

    def test_malformed_review_record_is_a_validation_error(self):
        self.prepare_change()
        write_json(self.repo / "locales/fr/review-state.json", {"schemaVersion": 1, "reviewed": [None]})
        with self.assertRaisesRegex(ValueError, "Review records must be objects"):
            report.status(self.repo)

    def test_status_output_cannot_escape_the_repository(self):
        self.prepare_change()
        outside = self.root / "outside.json"

        with self.assertRaises(ValueError):
            report.status(self.repo, output=outside)

        self.assertFalse(outside.exists())

    def test_refresh_refuses_a_symlink_report_destination(self):
        self.make_repo(self.previous, {"tip": "Old"}, {"tip": "[fr] Old"})
        self.make_repo(self.repo, {"tip": "New"}, {"tip": "[fr] Old"}, commit="new-source")
        outside = self.root / "outside.json"
        outside.write_text("sentinel", encoding="utf-8")
        link = self.repo / "changes.json"
        try:
            link.symlink_to(outside)
        except OSError as error:
            self.skipTest("Creating symlinks is unavailable: " + str(error))

        with self.assertRaises(ValueError):
            report.refresh(self.previous, self.repo, self.registry)

        self.assertEqual("sentinel", outside.read_text(encoding="utf-8"))

    @unittest.skipUnless(os.name == "nt", "Windows junction check")
    def test_status_refuses_a_junction_report_directory(self):
        self.prepare_change()
        outside = self.root / "outside-reports"
        outside.mkdir()
        sentinel = outside / "sentinel.txt"
        sentinel.write_text("unchanged", encoding="utf-8")
        link = self.repo / "linked-output"
        result = subprocess.run(["cmd", "/c", "mklink", "/J", str(link), str(outside)],
                                capture_output=True, text=True)
        if result.returncode:
            self.skipTest("Junction creation is unavailable: " + result.stderr)
        try:
            with self.assertRaises(ValueError):
                report.status(self.repo, output=link)
            self.assertEqual("unchanged", sentinel.read_text(encoding="utf-8"))
            self.assertFalse((outside / "translation-review.json").exists())
        finally:
            link.rmdir()


if __name__ == "__main__":
    unittest.main()
