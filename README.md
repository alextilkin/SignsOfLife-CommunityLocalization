# Signs of Life community localization

> **[Start translating in your browser](CONTRIBUTING.md#your-first-entry-in-an-empty-locale-file)** —
> no local Git installation required.

Help other players enjoy *Signs of Life* in your language. A few menu labels, a
dialogue correction, or feedback on a pack can help; you do not need to
translate the whole game.

This repository collects human-authored community translations. You can also
make an independent translation mod without submitting it here. The human-only
submission rule below applies to this repository, including its pull requests;
it is not a rule for independent Workshop packs, including machine-assisted
ones. The [free translation-mod permission](LICENSE.md#free-independent-translation-mods)
lets you distribute your own pack for the game without charging for it. It
does not let you redistribute other contributors' translations. Independent
authors should describe their pack honestly, including whether it is
machine-assisted, and follow applicable platform rules.

The game loads a locale as an ordinary mod pack: copy `locales/<code>/` into
`Documents/My Games/Signs of Life/Mods`, enable it, then **Load Now** or
restart. Enable only one locale pack at a time; the last loaded overlay wins.

## Contributing translations

Contributions here are optional, unpaid, and must be your own human-authored
work. This curated path allows accepted text to be considered for commercial
use in the game; acceptance as a community contribution or testing in a
community mod does not make a language officially supported.

Accepted Contributions may be edited, combined with other work, and commercially
distributed as part of Signs of Life. Contributors must be at least 18 years old
and must agree to the
[Translation Contributor Terms](https://github.com/alextilkin/SignsOfLife-CommunityLocalization/blob/terms-v1.0/legal/TRANSLATION_TERMS_v1.0.md)
before a pull request can be accepted.

Please do not submit text copied from unofficial translation patches, other
games, published translations, websites, subtitle files, or other third-party
material. Do not submit machine-translated or generative-AI text, including
DeepL, Google Translate, ChatGPT, or similar tools. Ordinary spelling and
grammar checkers are fine.

Contributions are not paid work. We aim to acknowledge accepted work that we
use in a [public contributor list](CONTRIBUTORS.md), with a no-credit option;
inclusion and credit are not guaranteed. There are no schedules, quotas, or
continuing obligations.

Start with the [first-entry browser tutorial](CONTRIBUTING.md#your-first-entry-in-an-empty-locale-file),
then see [CONTRIBUTING.md](CONTRIBUTING.md) for how to submit a pull request.

## Repository rights

Signs of Life, its English source text, and other Studio-provided materials are
proprietary and are © Sweet Dog Studios LLC. [`LICENSE.md`](LICENSE.md) grants
a narrow exception for free, independent Signs of Life translation packs.

Translation Contributions are governed by the Translation Contributor Terms and
any separately identified license. Only the Studio or maintainers it authorizes
in writing may publish combined packs containing other contributors' work.

## Available language templates and translation progress

These folders are templates, not claims of official language support. The
percentage measures text coverage against the dated English snapshot; it does
not measure translation quality, in-game review, or release readiness. Names
and words correctly left the same as English may count as untranslated.

<!-- coverage-table:start -->

A field counts toward text coverage when it is non-empty and not a copy of English. Empty overlays stay English in-game. 6130 fields in this snapshot.

| Language | Pack | Text coverage |
| --- | --- | ---: |
| Afrikaans | [`af`](locales/af/) | 0.0% |
| Български | [`bg`](locales/bg/) | 0.0% |
| Català | [`ca`](locales/ca/) | 0.0% |
| Čeština | [`cs`](locales/cs/) | 0.0% |
| Dansk | [`da`](locales/da/) | 0.0% |
| Deutsch | [`de`](locales/de/) | 0.0% |
| Español | [`es`](locales/es/) | 0.0% |
| Eesti | [`et`](locales/et/) | 0.0% |
| Euskara | [`eu`](locales/eu/) | 0.0% |
| Suomi | [`fi`](locales/fi/) | 0.0% |
| Français | [`fr`](locales/fr/) | 0.0% |
| Galego | [`gl`](locales/gl/) | 0.0% |
| Hrvatski | [`hr`](locales/hr/) | 0.0% |
| Magyar | [`hu`](locales/hu/) | 0.0% |
| Bahasa Indonesia | [`id`](locales/id/) | 0.0% |
| Íslenska | [`is`](locales/is/) | 0.0% |
| Italiano | [`it`](locales/it/) | 0.0% |
| Lietuvių | [`lt`](locales/lt/) | 0.0% |
| Latviešu | [`lv`](locales/lv/) | 0.0% |
| Norsk bokmål | [`nb`](locales/nb/) | 0.0% |
| Nederlands | [`nl`](locales/nl/) | 0.0% |
| Polski | [`pl`](locales/pl/) | 0.0% |
| Português | [`pt`](locales/pt/) | 0.0% |
| Português (Brasil) | [`pt-BR`](locales/pt-BR/) | 0.0% |
| Română | [`ro`](locales/ro/) | 0.0% |
| Русский | [`ru`](locales/ru/) | 0.0% |
| Slovenčina | [`sk`](locales/sk/) | 0.0% |
| Slovenščina | [`sl`](locales/sl/) | 0.0% |
| Srpski (latinica) | [`sr-Latn`](locales/sr-Latn/) | 0.0% |
| Svenska | [`sv`](locales/sv/) | 0.0% |
| Türkçe | [`tr`](locales/tr/) | 0.0% |
| Українська | [`uk`](locales/uk/) | 0.0% |

<!-- coverage-table:end -->

## Font and script limits

<!-- unsupported-table:start -->

The shipped fonts cannot draw these scripts yet, so there is no pack folder.

| Language | Code | Script |
| --- | --- | --- |
| Ελληνικά | `el` | Greek |
| 日本語 | `ja` | CJK |
| 简体中文 | `zh-Hans` | CJK |
| 繁體中文 | `zh-Hant` | CJK |
| 한국어 | `ko` | Hangul |
| العربية | `ar` | Arabic |
| עברית | `he` | Hebrew |
| ไทย | `th` | Thai |
| Tiếng Việt | `vi` | Vietnamese (horned vowels) |

<!-- unsupported-table:end -->

## Layout

| Path | What it is |
| --- | --- |
| [`english/Config/`](english/Config/) | English tables to translate against |
| [`locales/<code>/`](locales/) | One loadable pack per language |
| [`TRANSLATING.md`](TRANSLATING.md) | Voice, glossary, markup tokens |
| [`legal/TRANSLATION_TERMS_v1.0.md`](legal/TRANSLATION_TERMS_v1.0.md) | Frozen contributor terms (CLA Assistant is the merge record) |
| [`LICENSE.md`](LICENSE.md) | English stays studio-owned; contributions are not MIT/CC |
| [`CONTRIBUTING.md`](CONTRIBUTING.md) | How to submit; checkbox is notice, not the merge gate |

## What this English snapshot contains

These files provide the reference rows currently in this repository. The
snapshot commit and date are recorded in [`english/SOURCE.json`](english/SOURCE.json);
it is not yet a complete inventory of the current game build. A refresh after
the game's English freeze will add the newer recipe, tile, glyph, and runtime
content tables. Combat stats and frozen lookup keys are ignored even if present:

- `Config/UILocalization.json`
- `Config/TooltipLocalization.json`
- `Config/StatusEffectLocalization.json`
- `Config/DialogLocalization.json`
- `Config/helpData.json`
- `Config/journalEntries.json`
- `Config/InventoryItemData.json` — compiled items and vanilla pack `sol.*` cards
- `Config/MeleeWeaponData.json`
- `Config/RangedWeaponData.json`
- `Config/ProjectileRegistrationData.json`
- `Config/CreatureRegistrationData.json`
- `Config/StaticPrefabRegistrationData.json`
- `Config/DatapadTextData.json`
- `Config/ArmorSetData.json`

Empty arrays (and empty armor `Sets` / `Pieces`) mean “nothing translated yet.”
Leave untranslated rows out rather than copying English. This snapshot does
not yet provide separate container gump title rows.
