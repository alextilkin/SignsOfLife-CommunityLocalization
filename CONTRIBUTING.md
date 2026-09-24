# Contributing translations

This repository collects optional community translations, corrections, and
localization notes for Signs of Life. Contributors are independent community
contributors, not employees, contractors, or volunteers working for Sweet Dog
Studios LLC.

The human-authorship requirement below governs submissions to this repository.
Independent translation mods, including machine-assisted packs, follow a
separate path and do not require this repository's contributor agreement unless
their authors also submit work here. See the
[free independent-pack permission](LICENSE.md#free-independent-translation-mods)
and its separate rule for shared community translations.

Read the
[Translation Contributor Terms v1.0](https://github.com/alextilkin/SignsOfLife-CommunityLocalization/blob/terms-v1.0/legal/TRANSLATION_TERMS_v1.0.md)
before you open a pull request. You must be at least 18 years old.

## Agreement

Pull request template checkboxes are conspicuous notice. GitHub does not actually
require them to be checked.

[CLA Assistant](https://cla-assistant.io) is the authoritative record. It
authenticates you through GitHub and records agreement to the Terms. Every
**commit author** on the pull request must sign — not only the person who opened
it. A pull request that carries unsigned co-authors will not be merged.

Do not submit another person’s translation behind your own signature. One
translator per pull request, or each translator must have their own commits and
sign.

## How to translate

1. Start with [one entry in an empty locale file](#your-first-entry-in-an-empty-locale-file).
2. Read [`TRANSLATING.md`](TRANSLATING.md) for voice and markup.
3. Edit files under `locales/<code>/Config/`. Leave untranslated rows out so
   the game keeps English. Do not copy the whole `english/` directory into a locale.
4. Open a pull request using the template. Confirm you did not use machine
   translation or generative AI, and answer the third-party-source question.

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
    "Text": "<your own human translation of Ammo>"
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
    "Text": "<your own human translation of Ammo>"
  },
  {
    "ID": "item.none",
    "Text": "<your own human translation of None>"
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

- One language, and one concern when practical (for example UI chrome, not an
  entire game dump mixed with notes).
- Overlay JSON that follows this repository’s English templates. Leave IDs,
  keys, and markup tokens in English as the translation guide describes.
- Original, human-authored work. Do not paste unofficial translation patches,
  other games, published translations, websites, subtitle files, or similar
  third-party material.
- No machine translation and no generative AI. Do not use DeepL, Google
  Translate, ChatGPT, or similar tools to draft, translate, post-edit, or
  rewrite the Contribution. Ordinary spelling and grammar checkers that do
  not translate or generate the wording are allowed.

## Third-party sources

The pull request template asks whether you used a third-party source. Answer
it. Undisclosed copies are rejected. Machine-translated or AI-generated text
is rejected even if disclosed.

## Public credit

The Studio aims to maintain [`CONTRIBUTORS.md`](CONTRIBUTORS.md) for people whose
accepted translations it uses. The pull request template lets you choose your
GitHub username, another public name, or no public credit. If you leave that
field blank, we will use your GitHub username. You may later ask the maintainers
to correct or remove your listing. Do not submit an email address or private
legal name for the list. This is a best-effort practice, not a guarantee that
credit will appear or remain in every pack or game release.

## What this is not

- Not paid work, employment, or a promise of a game key in exchange for volume.
- Not a schedule, quota, or assigned chapter list.
- Not a guarantee that a Contribution will be used, credited, or kept.

You choose whether, when, and how much to contribute. The Studio may edit,
combine, replace, or decline any Contribution.

Accepted Community Contributions, if used, are expected to ship as community or
Workshop locale packs unless the Studio later formalizes an official language
separately.
