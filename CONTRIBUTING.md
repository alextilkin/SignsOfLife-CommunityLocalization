# Contributing translations

This repository welcomes translations, corrections, and localization notes for
Signs of Life. You can contribute a single string or a larger set of related
strings.

Read the
[Translation Contributor Terms v1.0](https://github.com/alextilkin/SignsOfLife-CommunityLocalization/blob/terms-v1.0/legal/TRANSLATION_TERMS_v1.0.md)
before you open a pull request. You must be at least 18 years old.

## Before you submit

Your submission must be your own human-authored writing. Do not use machine
translation or generative AI to draft, translate, post-edit, or rewrite it.
Ordinary spelling and grammar checkers are fine. Do not copy translations from
other games, unofficial patches, websites, subtitles, or other sources unless
you have the rights to submit them and disclose the source.

When you open a pull request, [CLA Assistant](https://cla-assistant.io) will ask
you to accept the Terms through GitHub. Every person who wrote text in the pull
request must accept them; do not submit someone else's work under your name.

## How to translate

1. Start with [one entry in an empty locale file](#your-first-entry-in-an-empty-locale-file).
2. Read [`TRANSLATING.md`](TRANSLATING.md) for voice and markup.
3. Edit files under `locales/<code>/Config/`. Leave untranslated rows out so
   the game keeps English. Do not copy the whole `english/` directory into a locale.
4. Open a pull request using the template. Describe your changes and identify
   any third-party sources you used.

## Your first entry in an empty locale file

You can do this entirely on GitHub. Fork the repository, then open
[`english/Config/UILocalization.json`](english/Config/UILocalization.json) in one
browser tab and your language's `locales/<code>/Config/UILocalization.json` in
another. The English file begins with `{"ID":"item.ammo","Text":"Ammo"}`;
an untouched language file may contain only `[]`. In your fork, click the
pencil (**Edit this file**) on the language file. Replace its `[]` with:

```json
[
  {
    "ID": "item.ammo",
    "Text": "<your translation of Ammo>"
  }
]
```

The angle-bracket text is an **instructional placeholder**, not a translation
to submit. Replace it with your own wording. Copy only the entry you are
translating, keep `ID` unchanged, and change only `Text`. Preserve any tokens
such as `{0}` or `[lightkey]` when the source entry contains them. For a second
entry, put a comma **between** the two objects, with no comma after the last:

```json
[
  {
    "ID": "item.ammo",
    "Text": "<your translation of Ammo>"
  },
  {
    "ID": "item.none",
    "Text": "<your translation of None>"
  }
]
```

Replace both placeholders before submitting. Use GitHub's preview to check
the changed file, commit to a new branch in your fork, and open a pull request.
Follow the template and CLA Assistant instructions above. The repository's
checks will validate the JSON; using command-line tools is optional. If you
have Python locally, `python scripts/measure-coverage.py` also checks the
locale against the English snapshot. Do not copy untranslated English entries
in bulk: missing rows already fall back to English in the game.

## What to submit

- One language per pull request, with related changes together when practical.
- Overlay JSON that follows the English reference. Keep IDs, keys, and markup
  tokens unchanged as [`TRANSLATING.md`](TRANSLATING.md) describes.
- A short explanation of any terminology choice that may need context.

## Public credit

The pull request template lets you choose your GitHub username, another public
name, or no public credit. If you leave it blank, we will use your GitHub
username in [`CONTRIBUTORS.md`](CONTRIBUTORS.md) if your work is accepted and
used. You can ask us to correct or remove a listing later. Do not put private
contact details in the public credit field.
