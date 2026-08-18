# Signs of Life community localization

English overlay tables and locale packs for *Signs of Life*. The game loads a
locale as an ordinary mod pack: copy `locales/<code>/` into
`Documents/My Games/Signs of Life/Mods`, enable it, then **Load Now** or
restart. Enable only one locale pack at a time; the last loaded overlay wins.

Do not add machine-generated player-facing text.

## Layout

| Path | What it is |
| --- | --- |
| [`english/Config/`](english/Config/) | Shipping English tables (snapshot; see `english/SOURCE.json`) |
| [`locales/<code>/`](locales/) | One loadable pack per language the current fonts can draw |
| [`TRANSLATING.md`](TRANSLATING.md) | Voice, glossary, markup tokens |
| [`FONTS.md`](FONTS.md) | Kimberley TTF vs baked BMFont |
| [`languages.json`](languages.json) | Locale list and font mode |
| [`NOTICE`](NOTICE) | Copyright on the English snapshot |

Cyrillic, CJK, Arabic, Hebrew, Thai, and Vietnamese are omitted: the shipped
fonts cannot draw those scripts. `runtime` languages need Settings → Font
Glyphs → Runtime (the default).

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

## Coverage

```text
python scripts/measure-coverage.py
```

A field counts as translated when the overlay is non-empty and not identical
to English. GitHub Actions prints the same table on every push and pull
request. The last generated snapshot is [`coverage.md`](coverage.md).

## Updating English

When the game’s overlay tables change, copy the JSON files listed in
`english/SOURCE.json` from `Signs of Life/Content/Config/` into
`english/Config/` and update `english/SOURCE.json` with the game commit. Then
drop overlay rows whose IDs no longer exist.
