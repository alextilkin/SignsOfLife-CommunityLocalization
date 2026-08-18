# Maintaining this repository

Studio notes. Not for translators.

When the game’s overlay tables change, copy the JSON files listed in
`english/SOURCE.json` from `Signs of Life/Content/Config/` into
`english/Config/` and update `english/SOURCE.json` with the game commit. Then
drop overlay rows whose IDs no longer exist.

Regenerate the language table with:

```text
python scripts/measure-coverage.py --write coverage.md --readme README.md
```
