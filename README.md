# Signs of Life community localization

English overlay tables and locale packs for *Signs of Life*. The game loads a
locale as an ordinary mod pack: copy `locales/<code>/` into
`Documents/My Games/Signs of Life/Mods`, enable it, then **Load Now** or
restart. Enable only one locale pack at a time; the last loaded overlay wins.

Do not add machine-generated player-facing text. License terms are in
[`LICENSE.md`](LICENSE.md). By opening a pull request you agree to them
([`CONTRIBUTING.md`](CONTRIBUTING.md)).

## Languages

<!-- coverage-table:start -->

Counted against English snapshot `90165c63` (4728 overlay fields). A field counts as translated when it is non-empty and not a copy of English. Empty overlays stay English in-game.

| Language | Pack | In-game | Translated |
| --- | --- | --- | ---: |
| Afrikaans | [`af`](locales/af/) | Yes | 0.0% |
| Català | [`ca`](locales/ca/) | Yes | 0.0% |
| Čeština | [`cs`](locales/cs/) | Yes | 0.0% |
| Dansk | [`da`](locales/da/) | Yes | 0.0% |
| Deutsch | [`de`](locales/de/) | Yes | 0.0% |
| Español | [`es`](locales/es/) | Yes | 0.0% |
| Eesti | [`et`](locales/et/) | Yes | 0.0% |
| Euskara | [`eu`](locales/eu/) | Yes | 0.0% |
| Suomi | [`fi`](locales/fi/) | Yes | 0.0% |
| Français | [`fr`](locales/fr/) | Yes | 0.0% |
| Galego | [`gl`](locales/gl/) | Yes | 0.0% |
| Hrvatski | [`hr`](locales/hr/) | Yes | 0.0% |
| Magyar | [`hu`](locales/hu/) | Yes | 0.0% |
| Bahasa Indonesia | [`id`](locales/id/) | Yes | 0.0% |
| Íslenska | [`is`](locales/is/) | Yes | 0.0% |
| Italiano | [`it`](locales/it/) | Yes | 0.0% |
| Lietuvių | [`lt`](locales/lt/) | Yes | 0.0% |
| Latviešu | [`lv`](locales/lv/) | Yes | 0.0% |
| Norsk bokmål | [`nb`](locales/nb/) | Yes | 0.0% |
| Nederlands | [`nl`](locales/nl/) | Yes | 0.0% |
| Polski | [`pl`](locales/pl/) | Yes | 0.0% |
| Português | [`pt`](locales/pt/) | Yes | 0.0% |
| Português (Brasil) | [`pt-BR`](locales/pt-BR/) | Yes | 0.0% |
| Română | [`ro`](locales/ro/) | Yes | 0.0% |
| Slovenčina | [`sk`](locales/sk/) | Yes | 0.0% |
| Slovenščina | [`sl`](locales/sl/) | Yes | 0.0% |
| Srpski (latinica) | [`sr-Latn`](locales/sr-Latn/) | Yes | 0.0% |
| Svenska | [`sv`](locales/sv/) | Yes | 0.0% |
| Türkçe | [`tr`](locales/tr/) | Yes | 0.0% |

`Yes` means the current fonts can draw the language.

These scripts have **no pack** yet: the shipped fonts cannot draw them, so in-game text would be blank.

| Language | Code | In-game |
| --- | --- | --- |
| Русский | `ru` | No — Cyrillic glyphs missing |
| Українська | `uk` | No — Cyrillic glyphs missing |
| Български | `bg` | No — Cyrillic glyphs missing |
| Ελληνικά | `el` | No — Greek glyphs missing |
| 日本語 | `ja` | No — CJK glyphs missing |
| 简体中文 | `zh-Hans` | No — CJK glyphs missing |
| 繁體中文 | `zh-Hant` | No — CJK glyphs missing |
| 한국어 | `ko` | No — Hangul glyphs missing |
| العربية | `ar` | No — Arabic glyphs missing |
| עברית | `he` | No — Hebrew glyphs missing |
| ไทย | `th` | No — Thai glyphs missing |
| Tiếng Việt | `vi` | No — Vietnamese (horned vowels) glyphs missing |

<!-- coverage-table:end -->

## Layout

| Path | What it is |
| --- | --- |
| [`english/Config/`](english/Config/) | Shipping English tables (snapshot; see `english/SOURCE.json`) |
| [`locales/<code>/`](locales/) | One loadable pack per language the current fonts can draw |
| [`TRANSLATING.md`](TRANSLATING.md) | Voice, glossary, markup tokens |
| [`LICENSE.md`](LICENSE.md) | English stays studio-owned; translators keep their wording, studio may ship it |
| [`CONTRIBUTING.md`](CONTRIBUTING.md) | How to submit, and that a PR accepts the license |
| [`languages.json`](languages.json) | Locale list |
| [`NOTICE`](NOTICE) | Short copyright pointer |

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

Empty arrays mean “nothing translated yet.” Leave untranslated rows out rather
than copying English. XML datapads, armor names, and container gump titles are
not overlayable yet.

## Updating English

When the game’s overlay tables change, copy the JSON files listed in
`english/SOURCE.json` from `Signs of Life/Content/Config/` into
`english/Config/` and update `english/SOURCE.json` with the game commit. Then
drop overlay rows whose IDs no longer exist.

Regenerate the language table with:

```text
python scripts/measure-coverage.py --write coverage.md --readme README.md
```
