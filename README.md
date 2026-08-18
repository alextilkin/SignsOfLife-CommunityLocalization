# Signs of Life community localization

English overlay tables and locale packs for *Signs of Life*. The game loads a
locale as an ordinary mod pack: copy `locales/<code>/` into
`Documents/My Games/Signs of Life/Mods`, enable it, then **Load Now** or
restart. Enable only one locale pack at a time; the last loaded overlay wins.

Do not submit AI generated text. License terms are in
[`LICENSE.md`](LICENSE.md). By opening a pull request you agree to them
([`CONTRIBUTING.md`](CONTRIBUTING.md)).

## Languages Currently Supported

<!-- coverage-table:start -->

A field counts as translated when it is non-empty and not a copy of English. Empty overlays stay English in-game. 4965 fields.

| Language | Pack | Translated |
| --- | --- | ---: |
| Afrikaans | [`af`](locales/af/) | 0.0% |
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
| Slovenčina | [`sk`](locales/sk/) | 0.0% |
| Slovenščina | [`sl`](locales/sl/) | 0.0% |
| Srpski (latinica) | [`sr-Latn`](locales/sr-Latn/) | 0.0% |
| Svenska | [`sv`](locales/sv/) | 0.0% |
| Türkçe | [`tr`](locales/tr/) | 0.0% |

<!-- coverage-table:end -->

## Unsupported Languages

<!-- unsupported-table:start -->

The shipped fonts cannot draw these scripts yet, so there is no pack folder.

| Language | Code | Script |
| --- | --- | --- |
| Русский | `ru` | Cyrillic |
| Українська | `uk` | Cyrillic |
| Български | `bg` | Cyrillic |
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
| [`LICENSE.md`](LICENSE.md) | English stays studio-owned; translators keep their wording, studio may ship it |
| [`CONTRIBUTING.md`](CONTRIBUTING.md) | How to submit, and that a PR accepts the license |

## What the game actually overlays

These pack files replace English prose. Combat stats and frozen lookup keys
are ignored even if present:

- `Config/UILocalization.json`
- `Config/TooltipLocalization.json`
- `Config/StatusEffectLocalization.json`
- `Config/DialogLocalization.json`
- `Config/helpData.json`
- `Config/journalEntries.json`
- `Config/InventoryItemData.json`
- `Config/MeleeWeaponData.json`
- `Config/RangedWeaponData.json`
- `Config/ProjectileRegistrationData.json`
- `Config/CreatureRegistrationData.json`
- `Config/StaticPrefabRegistrationData.json`
- `Config/DatapadTextData.json`

Empty arrays mean “nothing translated yet.” Leave untranslated rows out rather
than copying English. Armor names and container gump titles are not overlayable
yet.
