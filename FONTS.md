# Fonts

Signs of Life draws HUD, menus, and spoken AGIS lines with Kimberley.

## Runtime (default)

Settings → Font Glyphs → Runtime loads `Kimberley Bl.ttf` through FontStashSharp
and rasterizes glyphs as needed. The shipped TTF covers:

- Basic Latin and Latin-1 Supplement
- Latin Extended-A (Central European, Baltic, Turkish, Romanian Ș/Ț, Hungarian Ő/Ű)
- Common punctuation, Euro, trademark

It does **not** cover Cyrillic, Greek (beyond a few math letters), CJK, Hangul,
Arabic, Hebrew, Thai, or Vietnamese horned vowels (ơ, ư, and most tone marks
on those). Folders for those scripts are not in this repo because the current
fonts cannot draw them.

## Baked (optional)

Settings → Font Glyphs → Baked uses a BMFont atlas (~226 glyphs). That is
Western European / Windows-1252 plus Ł/ł, Š/š, Ž/ž, Œ/œ, Ÿ, and ı.

Languages marked `runtime` in `languages.json` need letters the baked atlas
does not have. Translators targeting those languages should keep Font Glyphs
on Runtime.

Missing glyphs typically render as blank or tofu. Do not work around that by
stripping diacritics from a translation.
