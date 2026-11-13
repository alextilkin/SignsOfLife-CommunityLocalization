# Updating a translation after an English refresh

Start with `changes.md`, then find your language in `translation-review.md`.
The reports identify fields by table, stable ID, and field name. Recipe and armor addresses also include a
section; runtime-content addresses include a kind. Array order is not identity.

Check the target game version in this repository's README before testing your
pack. Updating the English reference does not update an installed translation
pack.

## Read the change report

| Status | What to do |
| --- | --- |
| Added | Translate the new field when you want to cover it. |
| Changed | Compare the previous and current English and review your translation, even if its tokens still validate. |
| Replaced | Review the declared destination ID/field. Reuse appropriate wording, preserve the destination's tokens, and keep any existing destination translation until you have reviewed both. |
| Unused | Remove the obsolete locale entry or field. It has no replacement. |
| Removed | A field disappeared without a declared disposition. Check with a maintainer before assuming it was unused. |

The JSON reports include the full English before/after text, replacement
addresses, and preserved obsolete translations. Reports do not move, delete, or
overwrite your translated text. Do not blindly rename IDs: merged instructions
may need different wording or placeholders. Remove an empty row only after all
of its translated fields have been moved or intentionally retired.

`translation-review.json` lists outstanding reviews for each language. Missing
translation counts cover the full catalogue; its `missing` address list covers
only fields affected by the latest refresh. Coverage remains a separate text
count and does not certify that wording is current or reviewed.

## When duplicate text is consolidated

Several former fields may now point to one shared label, description, or
template. Follow each **Replaced** entry to its destination and review that
field's current English and tokens. An inherited field uses its shared source;
restoring the deleted duplicate is not a new translation task. For example,
generic creature descriptions now use `UILocalization.json` /
`agis.unknownDescription` / `Text` when no authored description overrides it.

Shared binding confirmations use `bind.confirmKey`, with `{0}` for the action
and `{1}` for the control name. Preserve both placeholders when reviewing a
translation from an older, device-specific instruction. Similar English does
not guarantee that an old translation fits the destination's context.

An **Unused** field has no destination. Keep any wording you need while
reviewing, then remove the obsolete translated field. A field still marked
**Removed** needs a maintainer's classification before you treat it as unused.
Reports preserve obsolete translations for reference and never perform this
cleanup automatically. A lower English field count can reflect consolidation or
retirement; coverage alone does not tell you whether your remaining translations
need review.

## Find earlier updates and current PR status

The root `changes.md` covers the latest English snapshot transition. For an
earlier transition, use the report permalink in that refresh's PR or inspect
the file's Git history. If you skipped snapshots, follow each intervening
report; pending language reviews carry forward until explicitly acknowledged.

The checked-in `translation-review.md` is generated with the English refresh.
For status after translation edits, open the PR's **Checks**, select
**Translation review**, and follow its run details to the summary and
`translation-review` artifact. You can also find the workflow under **Actions**.
The summary shows review counts; the artifact contains the full Markdown and
JSON reports. Artifact downloads require GitHub sign-in and expire, so the
repository reports and updating guide remain the starting point.

## Acknowledge reviewed wording

A needs-review flag stays pending through later refreshes until someone
explicitly acknowledges the current English and translation. Editing the
translation alone does not clear it. If the existing translation is still
correct, it can be acknowledged without rewriting it.

For a browser-only contribution, open `translation-review.json`, find the field
under your language's `needsReview` list, and copy its complete `acknowledgment`
object into the `reviewed` array in `locales/<code>/review-state.json`. Replace
the existing record with the same table/ID/field/section/kind instead of adding
a duplicate. If you edited the translation, use the fresh acknowledgment from
the **Translation review** job's JSON artifact on your PR; it includes that
translation's current fingerprint. Source and translation fingerprints prevent
an old acknowledgment from silently accepting a later edit.

With Python 3.12 or newer, you can generate the latest status locally:

```text
python scripts/localization-change-report.py status --repo .
```

After reviewing one field, copy its `sourceHash` from the JSON report:

```text
python scripts/localization-change-report.py review --repo . --locale fr --table UILocalization.json --id load.tip.holdReload --field Text --source-hash <sourceHash>
```

For a recipe or armor field, also pass its exact `--section`. For runtime
content, pass its `--kind`. Use the exact field name in the report, including
template, description-variant, or bonus identity when present.

Commit the locale edits and review-state changes in your translation PR. The
Translation review job publishes a fresh summary and JSON artifact without
pushing to your branch. Review flags are informational; the existing JSON,
identifier, token, and contributor checks still apply. Generated root reports
are refreshed by maintainers with the next English snapshot; translators do not
need to commit regenerated reports to submit a translation.
