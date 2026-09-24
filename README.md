# Signs of Life community localization

> **[Start translating in your browser](CONTRIBUTING.md#your-first-entry-in-an-empty-locale-file)** —
> no local Git installation required.

Help other players enjoy *Signs of Life* in your language. A few menu labels, a
dialogue correction, or feedback on a pack can help; you do not need to
translate the whole game.

Use the English files here as a reference and put translated entries in a
language pack. You can start with one line; untranslated entries stay in English
in the game.

The game loads a locale as an ordinary mod pack: copy `locales/<code>/` into
`Documents/My Games/Signs of Life/Mods`, enable it, then **Load Now** or
restart. Enable only one locale pack at a time; the last loaded overlay wins.

## Contributing translations

Submissions to this repository must be your own human-authored work. Please do
not submit text copied from another source or produced with machine translation
or generative AI. Contributors must be at least 18 and agree to the
[Translation Contributor Terms](https://github.com/alextilkin/SignsOfLife-CommunityLocalization/blob/terms-v1.0/legal/TRANSLATION_TERMS_v1.0.md).

Start with the [first-entry browser tutorial](CONTRIBUTING.md#your-first-entry-in-an-empty-locale-file).
The [contribution guide](CONTRIBUTING.md) explains submissions and public credit.

## Repository rights

The English reference remains © Sweet Dog Studios LLC. Read
[`LICENSE.md`](LICENSE.md) for the terms covering unofficial packs.
Submission rules are in [`CONTRIBUTING.md`](CONTRIBUTING.md).

## Available language templates and translation progress

These folders are templates, not claims of official language support. The
percentage measures text coverage against the dated English snapshot; it does
not measure translation quality, in-game review, or release readiness. Names
and words correctly left the same as English may count as untranslated.

<!-- coverage-table:start -->

A field counts toward text coverage when it is non-empty and not a copy of English. Empty overlays stay English in-game. 7712 fields in this snapshot.

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
| [`legal/TRANSLATION_TERMS_v1.0.md`](legal/TRANSLATION_TERMS_v1.0.md) | Terms for submitting translations |
| [`LICENSE.md`](LICENSE.md) | Rights for the English reference and unofficial packs |
| [`CONTRIBUTING.md`](CONTRIBUTING.md) | How to submit a translation |

## English reference and locale files

[`english/Config/`](english/Config/) contains the source text for the supported
overlay files. Its version is recorded in [`english/SOURCE.json`](english/SOURCE.json).
The wording may still change as the English text is reviewed. Use the matching
file under `locales/<code>/Config/` for your language, and include only entries
you have translated. See [`TRANSLATING.md`](TRANSLATING.md) for the fields to
translate and the identifiers and tokens to preserve.
