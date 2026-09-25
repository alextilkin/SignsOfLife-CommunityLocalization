# Translating Signs of Life

Use the file in [`english/Config/`](english/Config/) as your reference and add
translated rows to the matching file under `locales/<code>/Config/`. You can
start with one row. Missing rows and empty translated fields stay in English.
For submissions to this repository, read [`CONTRIBUTING.md`](CONTRIBUTING.md).

## Find your file

| What you are translating | JSON files | Guide section |
| --- | --- | --- |
| Menus, HUD, help, and status labels | `UILocalization.json`, `TooltipLocalization.json`, `StatusEffectLocalization.json`, `helpData.json` | [Interface and help](#interface-and-help) |
| Spoken lines and player choices | `DialogLocalization.json` | [Dialogue](#dialogue) |
| Journals and datapads | `journalEntries.json`, `DatapadTextData.json` | [Logs and lore](#logs-and-lore) |
| Items, weapons, armor, and projectiles | `InventoryItemData.json`, `MeleeWeaponData.json`, `RangedWeaponData.json`, `ArmorSetData.json`, `ProjectileRegistrationData.json` | [Equipment and items](#equipment-and-items) |
| Recipes and blocks | `RecipeLocalization.json`, `TileLocalization.json` | [Crafting and blocks](#crafting-and-blocks) |
| Creatures, objects, and vanilla content | `CreatureRegistrationData.json`, `StaticPrefabRegistrationData.json`, `RuntimeContentLocalization.json` | [World content](#world-content) |
| Xenoid inscriptions | `GlyphLocalization.json` | [Glyphs and language learning](#glyphs-and-language-learning) |

Keep each row's ID and other lookup fields exactly as they appear in English.
Translate only the text fields named below. Do not copy untranslated English
rows into a locale: the game already supplies the fallback. The version of the
English reference is recorded in [`english/SOURCE.json`](english/SOURCE.json).

## Interface and help

**`UILocalization.json`** contains menus, HUD labels, container titles
(`container.*`), and shared text templates. It also has `armor.stat.*` and
`armor.bonus.*` labels, plus `equipment.drainPerSecond` and
`equipment.doubleJump`. Translate `Text`; keep `ID`. Use the same term for a
tool or screen here and in its help and dialogue.

**`TooltipLocalization.json`** contains hover text. Translate `Text`, keeping
`ID` and any placeholders such as `{0}` where the game inserts a live number
or key name. You may move a placeholder within the sentence to suit your
language.

**`StatusEffectLocalization.json`** contains status labels. Translate `Text`
and keep `ID`. “Energy” means MEG power, not health. “Fullness” describes food
in the stomach, which helps regenerate health.

**`helpData.json`** contains MEG help topics. Keep `Key`; translate `Label`,
`Category`, and `Text`. These are practical instructions, so preserve the
actual action and keybind token even when AGIS makes a joke. Help and datapad
text can be longer than dialogue, but check that headings remain easy to scan.

Common UI terms to keep consistent:

| English | Meaning |
| --- | --- |
| MEG tool | Wrist rig that digs, grabs, scans, lights, maps, and grapples. Keep `MEG` in Latin capitals; translate “tool” if useful. |
| Dig Laser / Extraction Laser | MEG mining beam. Prefer the equivalent of “Dig Laser” for a short UI label. |
| Grab Laser / Manipulation Laser | Pulls world items. Prefer the equivalent of “Grab Laser” for a short UI label. |
| Wrist Scanner / Scan Laser | Scans creatures and ore. Its beam hurts xenoids. |
| Hotbar / scroll slots | The 1–8 equipment row. |
| Quick slots | Z/X utility slots, separate from the hotbar. |
| Projects / Build in World | Large structures built directly in the world rather than produced as inventory items. |
| Codex | Creature and datapad archive in the MEG. |
| Respawner | Device that reprints the player after death. |

## Dialogue

**`DialogLocalization.json`** contains spoken lines, AGIS, xenoid speech, and
player choices. Keep `ID`; translate the supplied `Normal` and, where present,
`Robot` fields. The player usually speaks briefly and directly. Dr. Stein is
calm and formal; Larry is practical and informal.

AGIS has two voices. `Normal` is the degraded, playful voice in the story on
Osiris. `Robot` is the polished, robotic version for when AGIS is running at
full capacity. If a row has no `Robot`, the game uses `Normal` for both.
NPC, player, and xenoid lines use `Normal`. When both AGIS versions exist,
keep the *same gameplay facts* in
both; only the personality changes. Weird AGIS may ramble, use fragments, or
say “lol,” but its instructions must remain clear. Robot AGIS is direct and
unsentimental. IDs 138–144 in the English file show a complete voice sample.

Xenoid speech changes as the player learns their language. Early lines are
unintelligible (`*kreech-vash!*`); intermediate lines are terse (`BEAMS HURT`);
later lines are fluent and formal. Preserve that progression and invented
phonemes. Do not turn a broken-speech line into a fluent one. The Source
Mnemonic lines around IDs 376–392 show the change in context.

Dialogue uses two kinds of markup:

- `@WRIST LIGHT@` marks highlighted words. Keep both `@` signs and translate
  the words inside when they are UI terms. Keep names such as `@AGIS@` and
  `@LARRY@`. Do not nest highlights or add spaces just inside the markers.
- Tokens such as `[lightkey]` become the player's current key. Keep the token
  spelling and place it where the key name reads naturally. Other bracketed
  phrases, such as `[Source Mnemonic]`, may appear as highlighted lore terms.

## Logs and lore

**`journalEntries.json`** uses `ID` as its lookup. Translate `Message`. The
journal is AGIS in bureaucratic mode even when its spoken `Normal` voice is
chaotic: think incident reports and slightly threatening paperwork.

**`DatapadTextData.json`** uses `ID` as its lookup. Translate `Title`,
`Category`, and `Text`. These are personal logs, safety memos, and research
notes. Dr. Hahn becomes obsessive and cruel; other writers become increasingly
alarmed. Preserve each writer's voice and the period in the story when the log
was written. Early human logs call the purple material “strange,” “Xenite,” or
“Xenostone”; do not silently replace those names with the later xenoid name
“Sourcemetal.”

Keep these datapad tokens exactly; the game replaces them in shipped logs:

| Token | Displayed value |
| --- | --- |
| `[ENGINEER]`, `[CAPTAIN]`, `[JANITOR]` | A surname chosen for the world. |
| `[XENOBIOLOGIST]` | Either **Berenstein** or **Berenstain**. Both spellings are part of a joke. |
| `[HOSTNAME]` | The host machine name. |

Names such as **Stein**, **Hahn**, **Larry**, and **AGIS** stay as names.

## Equipment and items

**`InventoryItemData.json`** contains item names and descriptions. Rows use a
numeric `ItemID` or a full `sol.*` ID. Translate `Name`, `Description`, and
existing `Templates` text; keep `ItemID`, `AutoOrganizeString`, and template
keys. Some artifacts switch from a human guess (“Strange Material”) to a true
xenoid name (“Sourcemetal”) as the player learns the language. Translate
the true `Name` supplied here. The earlier guess labels are not present in
the English reference yet. An artifact's `AlienString` reveals words gradually.
Translate the full text and separate words with spaces; the game shows
`[?]` for words still hidden from the player.

**`MeleeWeaponData.json`** and **`RangedWeaponData.json`** use `ItemID`. Translate
`Name` and `Description`; keep the ID. **`ProjectileRegistrationData.json`**
uses `SaveName` as its identity; translate its visible `Name`.

**`ArmorSetData.json`** uses `ItemType` for armor pieces. Translate piece
`Name`, `Description`, and any supplied unique bonus `Description`. Keep
`ItemType`, set `Name`, and piece `Set`. Shared mechanical bonus wording comes
from `UILocalization.json`, so use the same stat terms in both files.

## Crafting and blocks

**`RecipeLocalization.json`** has recipe names, category labels, and
adjusted-result labels. Keep recipe `Name`, category `Key`, result IDs, and
`DisplaySource` unchanged. Translate a recipe `DisplayName` when the English
row supplies one. A `DisplaySource` row normally shows its single result's
localized item, tile, prefab, or structure name; an explicit recipe
`DisplayName` can override that. Rows with neither field need no translation
at present. Translate categories and adjusted-result labels as complete
phrases. Recipe search uses *only the displayed name*, so try searching for
your translation rather than the English `Name` key.

**`TileLocalization.json`** uses numeric tile `ID`. Translate `DisplayName`
once for the block item and its matching inherited recipe. Keep the ID.

## World content

**`CreatureRegistrationData.json`** uses `LivingEntityType`. Translate
`Name`, `Description`, and `CodexCategory`; keep the type. Earth animals such
as Chicken, Sheep, and Goat translate normally. Invented creature names such
as Duglette, Kangit, Pindlebag, and Monstralorp should remain playful names.
Preserve the absurdity of **Buff Mechington**. Xenoid Churl, Scout, Hound,
and similar names describe roles within the xenoid faction.

**`StaticPrefabRegistrationData.json`** uses `SaveName` and `SaveAliases` as
identities. Translate supplied `Name`, `DisplayName`, `Description`,
`CodexCategory`, `TooltipNameOverride`, `DescriptionsByState`, and
`SpecificTooltips` text. If English `Name` and `DisplayName` are identical,
a translated `Name` also supplies the display name unless you explicitly
translate `DisplayName` differently.

**`RuntimeContentLocalization.json`** contains visible vanilla flora,
structure, status, projectile, and unique equipment-effect prose. Keep
`Kind`, the full `sol.*` `ID`, and any `effect.*` text keys; translate
only their supplied text values.

## Glyphs and language learning

**`GlyphLocalization.json`** contains xenoid inscriptions. Translate `Text`;
keep `ID` and the exact `English` inscription, including distinct quote
variants. Old saves and scan rewards use that English inscription. The game
reveals translated words as the player's language knowledge grows, showing
`[?]` for hidden words. Write the translation as normal space-separated words
so it reveals naturally. Glyph proverbs are sincere, almost scriptural, not
sarcastic. Plaques are narrow, so prefer a shorter accurate phrase when you
have a choice.

## Rules shared by all files

- Keep IDs, save names, category keys, `sol.*` identifiers, and gameplay values
  unchanged. Missing or empty translated fields use English; unknown IDs are
  ignored.
- Preserve `{0}`, `{1}`, and other numbered placeholders wherever the game
  inserts a value. Move them within a sentence if grammar requires it.
- Keep keybind tokens exactly as written: `[lightkey]`, `[menukey]`,
  `[grablaserkey]`, `[minimapkey]`, `[mapkey]`, `[grapplekey]`, `[holsterkey]`,
  `[kickkey]`, `[reloadkey]`, `[jump]`, `[crouch]`, `[up]`, `[down]`, `[left]`,
  `[right]`, `[primary]`, `[secondary]`, `[scrollslot1]`, `[scrollslot4]`,
  `[hostname]`, and `[al]`.
- The player can be male or female. Avoid gendered descriptions of the player
  where your language allows it. Keep gameplay numbers and units accurate.
- Translate the intended meaning of accidental English typos. Keep deliberate
  voice quirks, jokes, and invented syllables.

The `PREVIEW`, `INPUT`, and `PROMPT` labels are embedded in game artwork and
cannot yet be changed by a locale pack. Current fonts support Latin and
Cyrillic; see the README's [font and script limits](README.md#font-and-script-limits)
for other scripts.

## Setting and terminology (spoilers)

*Signs of Life* is a survival sandbox about a colonist stranded on **Osiris**.
The scout ship **Hermes** arrives before the colony ship **Hephaestus**.
A discovery on an asteroid leads to the Hephaestus's destruction, leaving the
player with a damaged MEG tool and AGIS in local backup. **Pioneer Station**
and the **Mining Base** are already ruined. Deeper in, the player encounters
the **xenoids**, their energy called **the Source**, and the catastrophe they
call **the Calamity**. A **Source Mnemonic** helps the player learn their
language. Sandbox worlds omit the colony-ship opening; AGIS is more
professional there.

| Term | Translation guidance |
| --- | --- |
| Signs of Life | Keep the product name in body text. The title plays on biological evidence, the player's survival, and Dr. Stein's mission to find “signs of life.” |
| Sweet Dog Studios, AGIS, MEG | Keep as proper names. `AGIS` and `MEG` stay in Latin capitals. |
| Hephaestus, Hermes, Osiris | Keep the ship and planet names. |
| Pioneer Station, Mining Base | Translate the descriptive words consistently as place names. |
| Xenoid, Xenite, Xenostone | Coined names; keep or transliterate rather than turning them into generic descriptions. |
| Sourcemetal, Sourcecrystal, the Source | Later xenoid terms. Keep a consistent form for “Source”; English varies between “Sourcecrystal” and “Source crystals.” |
| Source Mnemonic, Source Flows | Proper xenoid terms. Keep “Mnemonic” as the artifact class. |
| the Calamity, the Foundations | Named concepts in xenoid lore; distinguish them from ordinary uses of those words. |
| Project Phoenix, Mass Driver, Energite | Keep the code name “Phoenix” and the coined “Energite”; treat Mass Driver as a named ship system. |

Dry humor belongs to the speaker: Hahn's chicken obsession, **Buff
Mechington**, AGIS's “finders keepers lol,” and the **Berenstein/Berenstain**
variation are deliberate. A datapad titled “So You've Been Stranded…” parodies
an in-flight safety card. Xenoid proverbs such as “The Source provides” should
remain earnest. When in doubt, read nearby entries by the same speaker rather
than applying one voice to the whole game.

## Related

- [How to submit a translation](CONTRIBUTING.md)
- [Repository rights](LICENSE.md)
- [Translation Contributor Terms](legal/TRANSLATION_TERMS_v1.0.md)
