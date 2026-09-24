# Translating Signs of Life

Use `english/Config/` as the reference and put translated entries in the
matching file under `locales/<code>/Config/`. If a line is not ready, leave it
out so the game keeps English. For submissions to this repository, follow
[`CONTRIBUTING.md`](CONTRIBUTING.md).

These are the English reference files and their translatable fields:

- `UILocalization.json` — HUD and menu labels, including `armor.stat.*` / `armor.bonus.*` bonus templates and `equipment.drainPerSecond` / `equipment.doubleJump`
- `TooltipLocalization.json` — HUD hover tooltips
- `StatusEffectLocalization.json` — status-effect labels
- `DialogLocalization.json` — spoken lines, AGIS, player options
- `helpData.json` — MEG help topics (`Key`; translate `Label` / `Category` / `Text`)
- `journalEntries.json` — AGIS journal (`ID`; translate `Message`)
- `InventoryItemData.json` — item names and descriptions (`ItemID` numeric or `sol.*`; translate `Name` / `Description` / existing `Templates` keys; leave `AutoOrganizeString`)
- `MeleeWeaponData.json` / `RangedWeaponData.json` — weapon names (`ItemID`; translate `Name` / `Description`)
- `ProjectileRegistrationData.json` — projectile display names (leave `SaveName`; translate `Name`)
- `CreatureRegistrationData.json` — creature names / codex (leave `LivingEntityType`; translate `Name` / `Description` / `CodexCategory`)
- `StaticPrefabRegistrationData.json` — prefab catalog (leave `SaveName` / `SaveAliases`; translate `Name` / `DisplayName` / `Description` / tooltip fields)
- `DatapadTextData.json` — datapad lore (leave `ID`; translate `Title` / `Category` / `Text`)
- `ArmorSetData.json` — armor names and descriptions (`ItemType`; translate piece `Name` / `Description` and unique bonus `Description` overrides; leave set `Name` and piece `Set`)
- `RecipeLocalization.json` — explicit recipe `DisplayName`, category and adjusted-result labels; keep `Name`, `Key`, and `DisplaySource` unchanged
- `TileLocalization.json` — block and matching recipe display names keyed by numeric tile `ID`
- `GlyphLocalization.json` — xenoid inscriptions; translate `Text`, keeping `ID` and the exact `English` inscription
- `RuntimeContentLocalization.json` — vanilla fluid, flora, structure, status, projectile, and unique equipment-effect prose keyed by `Kind` and full `sol.*` `ID`

Missing overlay IDs keep English. Empty overlay fields keep English. Unknown
keys are skipped. Container titles use `UILocalization.json` `container.*` rows.

[`english/SOURCE.json`](english/SOURCE.json) records the version of the English
reference, which may be updated as the game changes. The `PREVIEW`, `INPUT`, and
`PROMPT` labels are part of game artwork and cannot be replaced by a locale pack
yet. The current fonts support Cyrillic alongside Latin; other scripts listed
in the README's [font limits](README.md#font-and-script-limits) need additional
font support.

## Required strings and inherited names

Translate a recipe `DisplayName` only when the English recipe row has one.
Rows with `DisplaySource` inherit the localized name of their single
result item, tile, prefab, or structure; you may add an explicit recipe
`DisplayName` to override it. Rows with neither field need no translation at
present. Translate categories and
adjusted-result labels as whole phrases. Recipe `Name`, category `Key`, and
result identifiers are stable identities, never translated. Recipe search uses
only the name shown to the player, so test a translated recipe by its displayed
name rather than its English key.

Translate `TileLocalization.json` `DisplayName` once for the block item and its
matching inherited recipe. A prefab whose English `Name` and `DisplayName`
match needs only `Name`; an explicit locale `DisplayName` can override that
inheritance. Repeated English elsewhere may have different context and remain
separate rows; reuse a reviewed translation rather than deleting keys.

For glyphs, keep the exact `English` inscription because old saves and scan
rewards use it. Translate `Text` alone. For runtime content, keep `Kind` and
full `sol.*` `ID`; translate only supplied text fields, including stable
`effect.*` keys. Missing fields fall back to English. Preserve `{0}` style
format tokens, `[key]` tokens, and lore placeholders such as `@CHECKLIST@`.

## Voice and setting

The files above cover spoken lines, help, journal, menus, items, recipes,
tiles, glyphs, creatures, datapads, and other vanilla descriptions. Translate
the player-facing fields while preserving the identifiers and tokens described
here.

## What the game is

*Signs of Life* is a 2D sci-fi survival sandbox platformer. The player is
stranded on an alien planet, mines and crafts a toolkit from whatever they
find, and slowly learns that the planet already had a history.

The official short description:

> Signs of Life is a 2D sci-fi survival game about being stranded on an alien
> planet, building a life out of whatever you can find, and uncovering a
> mystery that started long before you arrived.

Genre tags that should stay accurate in store copy and UI: **sci-fi**,
**survival**, **sandbox**, **platformer**, **crafting**, **co-op**, **PvP**.
It is not a city-builder, not a 4X, and not a visual novel with a survival
skin. Combat, building, and story investigation are all first-class.

The title is a pun. Keep it if the target language can carry all three
meanings; otherwise pick the reading that still works as a product name:

1. Biological traces — phosphine, bodies, ruins, living creatures.
2. The player’s own survival — they are the remaining sign of life.
3. A literal mission briefing: Dr. Stein sends the player to look for
   “signs of life” on an asteroid.

Do not rename the game in-body. `Signs of Life` is the product name.

Cyrillic HUD text is supported. Kimberley still draws Latin; Courier covers
Cyrillic at runtime. Leave `AGIS`, `MEG`, and other Latin-capital product
tokens in Latin as the glossary says. Greek, CJK, Hangul, Arabic, Hebrew,
Thai, and Vietnamese glyphs are still missing.

## Tone

The writing is American English, informal, and often slightly broken on
purpose. It mixes:

- Practical survival instruction (how to dig, eat, craft, die, respawn).
- Deadpan sci-fi bureaucracy (cryo shifts, checklists, incident reports).
- Dark comedy (corpses, brain printing, chickens that should not exist).
- Occasional genuine awe when xenoid lore appears.

Default register is conversational, not military-manual. AGIS’s degraded
campaign voice is the house style for most spoken help. Professional AGIS,
Dr. Stein, and xenoid elders are the exceptions.

Humor is dry, not sitcom-quippy. When a line is stupid, it is stupid
in-character: an AI that lost its ship-cloud, a colonist who will not stop
talking about chickens, a datapad titled `Hahn is Garbage`. Preserve that
unevenness. Cleaning every sentence into polished localization English
erases the game.

English source has occasional accidental typos. Translate the intended
meaning without copying them. Joke misspellings and voice tics are different
from accidents; see [Humor traps](#humor-traps).

## Setting (spoilers)

Translators need the plot. Players should meet it in order.

Humanity sends two ships toward a potentially habitable planet **14
light-years** from Earth. The scout ship **Hermes** arrives first. Four years
later the colony ship **U.N. Hephaestus** stops at a nearby asteroid because
sensors found unidentified material and traces of **phosphine**. The player,
cycled out of cryo for a shift, is sent to investigate.

On the asteroid they find alien architecture and insert a crystal into a
device. That wakes something. An alien craft destroys the Hephaestus. The
player reaches the planet **Osiris** in a wrecked landing pod with clothes, a
cracked wrist tool, and **AGIS** running in degraded local backup.

On Osiris:

- The **Pioneer Station** and **Mining Base** are the first human outposts,
  already ruined.
- **Dr. Hahn**, the station xenobiologist, has gone violently chicken-obsessed.
  His story is body horror mixed with farmyard farce. Do not sanitize it.
- Human colonists left **datapads** — personal logs, safety memos, research
  notes. They are the main lore channel for the Hermes crew’s fate.
- The player is fitted with a **MEG tool**, a wrist rig that digs, grabs,
  scans, lights, maps, grapples, and hosts AGIS.
- Death is not the end. Nanomachines capture brain state and a **respawner**
  (bio-printer) reprints the body. Journal and AGIS lines treat this as
  grimly casual.

Deeper in, the player meets the **xenoids**, the native intelligent species.
Their civilization used a power they call **the Source**. Abuse of it caused
**the Calamity**, which destroyed their homeworld. A relic the player carries
is a **Source Mnemonic**: it lets them read **Source Flows** and, in gameplay
terms, slowly learn the xenoid language. Some xenoids want the Mnemonic
delivered into the sun. Others still chase the same ambitions that caused the
Calamity.

Sandbox worlds (including the default **Osiris** / “New Earth” generator)
reuse the same items, creatures, and tools without the scripted colony-ship
opening. AGIS is more professional there. See [AGIS voices](#agis-voices).

## Cast

| Name | Role | Voice |
| --- | --- | --- |
| **The player** | Unnamed colonist, recently thawed. Journal entries address them as “you.” Dialogue options are short and often start with `- "…"`. | Sparse. Player lines are functional, not heroic speeches. |
| **AGIS** | Ship AI living in the MEG tool. After the Hephaestus dies, it runs locally and gets weirder. | Campaign: rambling, lowercase-ish, checklist humor, “uh,” “lets see,” “probably fine.” Sandbox: clipped professional. Details below. |
| **Dr. Stein** | Hephaestus scientist on the Bridge. Sends the player to the asteroid. | Calm, slightly stiff, mission-briefing English. Not comic. |
| **Larry** | Hangar / landing-pod technician. | Practical, informal, helpful. Name stays **Larry**. |
| **Dr. Hahn** | Pioneer Station xenobiologist. Chicken fixation, then atrocity. Already dead when the player arrives. | In datapads: unhinged, repetitive, mean. Other people write about him with rising panic. Keep **Hahn**; do not nickname him. |
| **Captain [CAPTAIN]** | Pioneer Station captain. Surname is rolled per world. | Authoritative, then strained. Datapads argue with him. |
| **Chief Engineer [ENGINEER]** | Station engineer. Surname rolled per world. | Hands-on, sweary, proud of lenses and bombs. |
| **Head Xenobiologist [XENOBIOLOGIST]** | Token does **not** insert the rolled surname. It inserts **Berenstein** or **Berenstain**. That is a Mandela-effect joke. Keep both spellings as a pair. | Scientific, increasingly terrified. |
| **Janitor [JANITOR]** | Rare datapad surname token. Rolled per world. | Working-stiff. |
| **Xenoid speakers** | Native NPCs, glyph walls, artifact flavor. | Formal, slightly biblical, collective “we.” After language skill rises, they become fluent. Before that they are noise. |

Named humans (**Stein**, **Hahn**, **Larry**, **AGIS**) are proper names. Do
not translate them into local equivalents. Crew-role tokens
(`[ENGINEER]`, `[CAPTAIN]`, `[JANITOR]`) become surnames such as
Johnson, Patel, and Tremblay. Keep their original spelling; they are names
from Earth.

## AGIS voices

Spoken lines are in `DialogLocalization.json`. Some AGIS lines have two
versions:

- **Normal** is the degraded, playful voice heard in the story on Osiris.
- **Robot** is the professional voice heard in sandbox worlds. When a row has
  no `Robot` text, the game uses `Normal` for both.
- NPC lines, player options, and xenoid dialogue use `Normal`.

When both variants exist, they must say the **same gameplay facts**
(which key, which station, which item). Only the personality changes:

| Normal (weird) | Robot (professional) |
| --- | --- |
| “Umm lets see, I think I'm supposed to scan you or something hang on let me get out my @CHECKLIST@.” | “I am initiating a scan. Retrieving checklist.” |
| “I'll just write \"probably fine\" really small in that box.” | Status listed as “probably fine” in relevant documentation. |
| “Ok i'm already like super bored of this quiz…” | Direct instruction, no nap. |
| Contractions, fragments, “lol,” “beep boop.” | Complete sentences, passive-leaning, no slang. |

Weird AGIS still has to teach the player. Do not make Normal so chaotic that
the instruction disappears. Do not make Robot warm and jokey; the contrast is
the joke.

Journal entries (`journalEntries.json`) are AGIS in bureaucratic mode even on
the campaign world: “AGIS Assisted Journalling Subsystem,” “your actions have
been reported.” Keep that stiff, slightly threatening HR tone.

## Glossary

### Keep as-is (product / proper / coined)

These are names, not descriptions. Transliterate only if the script requires
it. Do not calque them into “Alien-ite,” “Source-metal” compounds that no
longer look like names.

| Term | What it is | Notes |
| --- | --- | --- |
| Signs of Life | Game title | See pun above. |
| Sweet Dog Studios | Developer | |
| AGIS | Wrist AI | Always Latin capitals. Never “Agis” in UI. Not expanded in English. |
| MEG, MEG tool | Wrist multi-tool | Always Latin capitals. English never expands the acronym. Keep **MEG**; you may translate **tool** (`MEG-Werkzeug`, `herramienta MEG`). |
| HUD | Heads-up display | Standard game term. MEG help sometimes spells it out in Robot voice only. |
| MEG (in MEG archive) | In-game codex / help | Same letters as the tool. Context is “open MEG,” not a second acronym. |
| Codex | Creature / datapad archive inside MEG | Can be localized as the local word for a catalog, but stay consistent. |
| Hephaestus, U.N. Hephaestus | Colony ship | Greek smith-god. Keep the myth name. |
| Hermes | Scout ship | Keep. |
| Osiris | Destination planet | Keep as a proper name. |
| Pioneer Station | First colony outpost | Descriptive; translate the words, keep it a proper place name. |
| Mining Base | Sister outpost | Same. |
| Xenoid | Native intelligent species | Coined. Adjective and noun. Plural **xenoids**. |
| Xenite | Human lab name for Source matter / related constructs | Human coinage (`xeno-` + `-ite`). Keep or transliterate. |
| Xenostone | Related mineral / biome / structures | Human coinage. Keep. |
| Sourcemetal | Xenoid name for the purple metal | One word, capital S. Revealed name; see dual names below. |
| Sourcecrystal / Source crystals | Xenoid name for the energy gems | English source is inconsistent (`Sourcecrystals`, `Source crystals`). Pick one form per language and use it everywhere. |
| Source, the Source | Xenoid fundamental energy | Capitalize as a proper mythic term, not “the source of the river.” |
| Source Mnemonic | Pre-Calamity translation relic | Keep **Mnemonic**; it is the in-world class of artifact. |
| Source Flows | Readable Source energy | Proper term. |
| the Calamity | Xenoid homeworld catastrophe | Proper event name. Not “a calamity.” |
| the Foundations | Xenoid term for underlying reality | Proper. |
| Project Phoenix | Hahn-era research program | Translate **Project** if needed; keep **Phoenix** as the code name. |
| Mass Driver | Hephaestus weapon | Keep as a named ship system. |
| Energite | Crafted exotic resource | Coined. Keep. |
| respawner | Bio-printer that reprints the player | Gameplay term. Translate as a device name, not “checkpoint.” |

### Dual names (load-bearing)

Several items have a **human guess** and a **xenoid true name**. The name
shown to the player changes as they learn the xenoid language. Translate
both names, and keep them distinct.

| Before language skill | After (true name) |
| --- | --- |
| Strange Artifact | The accessory’s real name (Unyielding Carapace, Mass Displacer, …) |
| Raw / Coarse / Granular / Refined Strange Material | Raw / Coarse / Granular / Refined Sourcemetal |

`AlienString` on artifacts is xenoid flavor, revealed one word at a time as
knowledge grows. Hidden words appear as `[?]`. Translate the full English
`AlienString` and separate words with spaces so they reveal naturally.

Human scientists in datapads still say **strange purple metal**, **Xenostone**,
**Xenite**. That is earlier in the story. Do not silently upgrade those logs
to Sourcemetal.

### Gameplay vocabulary

Translate these, but pick one term and reuse it in UI, help, AGIS, and item
text:

| English | Meaning |
| --- | --- |
| MEG tool | Wrist rig. |
| Wrist Light | MEG flashlight. |
| Dig Laser / Extraction Laser | MEG mining beam. Help text uses both. Prefer **Dig Laser** for UI. |
| Grab Laser / Manipulation Laser | Tractor / vacuum for world items. Prefer **Grab Laser** for UI. |
| Wrist Scanner / Scan Laser | Codex + ore scan. Scanner radiation **hurts xenoids**; that is intentional. |
| Grapple Module | Pulls the player to terrain. |
| Key Items | Non-drop pouch. Survives death. |
| Hotbar / scroll slots | 1–8 equip row. |
| Quick slots | Z/X utility slots, not the 1–8 hotbar. |
| Projects / Build in World | Large recipes placed in the world rather than the backpack. |
| Crafting Menu | Recipe UI. |
| Equipment | Worn armor / clothing screen. |
| Bank | Shared storage, not a financial bank. |
| Container | Any inventory box, chest, pouch, corpse pack. |
| Datapad | Handheld lore document. Keep as one word if the language allows. |
| Journal | AGIS action log. |
| Minimap / wrist map | Local map. |
| Beacon | Nav marker on the minimap. |
| Lens, Battery, Capacitor | MEG upgrade slots. Gems (ruby, sapphire, topaz, emerald) upgrade specific functions. |
| Encumberance / weight | Inventory burden. |
| Energy | MEG power, not HP. |
| Health / fullness | Body vitals. Food in the stomach regenerates health. |
| Codex | Scanned creature archive. |
| Mods / Workshop / Staged Mods | Player content. Keep **Steam Workshop** as the store name. |
| Sandbox | Unscripted world, as opposed to the colony-ship story opening. |

### Creature names

Earth animals (**Chicken**, **Sheep**, **Goat**, **Hog**, **Ant**) translate
normally.

Invented critters should stay playful proper names, not descriptions:

**Duglette**, **Kangit**, **Pindlebag**, **Gronday**, **Flancer**, **Geoguy**,
**Monstralorp**, **Crystal Nug**, **Impaler**, **Popper**, **Leaper**,
**Spitter**, **Crawler Medusa**.

Faction / boss names to keep close:

**Buff Mechington**, **Buff Mechington Mk2**, **Mechington Brood** — Hahn’s
chicken-mech horror. The silly name is the point.

**Xenoid Churl**, **Ironback**, **Caster**, **Scout**, **Artillery**,
**Specialist**, **Hound** — military roles after the species name.

**Protoxenoid** *X* — precursor/feral xenoid-related fauna.

**Billy** — a specific named creature in datapads and the bestiary. Keep
**Billy**.

## In-game translation mechanic

The game already contains a language-learning system. Localization must not
collapse it.

1. Scanning glyphs, artifacts, and xenoid text teaches the player the xenoid
   language.
2. Early on, xenoid talk and scanner complaints are unintelligible:
   `[unintelligible]`, `*kreech-vash!*`, `*thul'nari vek!*`. Keep the
   asterisks and invented phonemes; they are not English.
3. As the player learns, complaints become broken speech: `BEAMS HURT`,
   `STOP BEAM`. Translate into equally broken target-language telegrams, not
   fluent speech.
4. Once the language is learned, xenoids speak fluent, formal language.
5. Glyph displays and `AlienString` fields reveal words as knowledge grows.
   Hidden words show as `[?]`. Keep that marker exactly.

English in this system is the **xenoid-to-human** reveal language. After
localization, the reveal language is the player’s language. Do not leave
English words in glyph translations for a non-English client.

## Markup — do not eat these

Player-facing strings contain machine tokens. Translators move words around
them; they do not translate the token names.

### `@HIGHLIGHT@`

Spoken lines wrap UI nouns in `@…@` (MEG TOOL, PIONEER STATION, LARRY). The
game styles those spans. Rules:

- Keep both `@` signs.
- Translate the words inside when they are English UI terms:
  `@WRIST LIGHT@` → `@LUZ DE MUÑECA@`.
- Do not translate names: `@AGIS@`, `@LARRY@`, `@OSIRIS@`.
- Do not nest, and do not add spaces inside the `@` unless the English did.
- Some English spans include punctuation (`@Dr. Hahn.@`). Keep the period
  inside if you keep the highlight on the name.

### `[keybind]` tokens

The game replaces these with the player’s current key. Other bracketed words
may appear as highlighted terms in dialogue, such as `[Source Mnemonic]`.

**Never translate the identifier.** Keep exact spelling:

`[lightkey]`, `[menukey]`, `[grablaserkey]`, `[minimapkey]`, `[mapkey]`,
`[grapplekey]`, `[holsterkey]`, `[kickkey]`, `[reloadkey]`, `[jump]`,
`[crouch]`, `[up]`, `[down]`, `[left]`, `[right]`, `[primary]`,
`[secondary]`, `[scrollslot1]`, `[scrollslot4]`, `[hostname]`, `[al]`

Write the surrounding sentence so a key name in the middle still reads
naturally (`press [lightkey] to …`).

### Datapad lore tokens

The game replaces these tokens in datapads. Keep the brackets and English
identifiers:

| Token | Becomes |
| --- | --- |
| `[ENGINEER]` | Rolled surname |
| `[CAPTAIN]` | Rolled surname |
| `[JANITOR]` | Rolled surname |
| `[XENOBIOLOGIST]` | `Berenstein` or `Berenstain` |
| `[HOSTNAME]` | Host machine name |

Player-authored datapads do **not** expand these; they print the brackets
literally. That is intended.

### Other literals

- `{0}`, `{1}` where the game inserts a value (grab laser, grapple descriptions).
- JSON/XML keys, file names, `sol.` item UUIDs, dialogue numeric IDs.
- `[unintelligible]`, `[unintelligible xenoid speech]`, `[?]` as displayed
  alien-language UI, not as keybinds.

## Pack files and fallback

Keep each translated row in the matching `Config/` file for your language.
The file list above identifies the fields you can translate. Leave IDs, save
names, categories used as keys, and gameplay values unchanged. Missing or empty
translated fields fall back to English; unknown IDs are ignored. You do not
need to edit the game files to contribute a translation here.

## Humor traps

Leave these intact; they are jokes, not errors.

- **Berenstein / Berenstain.** Both spellings must survive. Different worlds
  use different spellings; a “correction” to a single spelling kills the gag.
- **Buff Mechington.** Do not rename to a serious mech designation.
- **“He was a real bad egg.”** Hahn / chicken motif. Keep an egg idiom if
  the language has one; otherwise a chicken insult of similar register.
- **finders keepers lol.** Weird AGIS. Robot variant restates without `lol`.
- **Independence Day** line (dialog ID 16) is calendar flavor, not US civics
  education.
- **“So You've Been Stranded…”** datapads parody in-flight safety cards.
  Keep the magazine-issue framing (`Issue 1`, `Issue 2`).
- Glyph proverbs are sincere, not sarcastic: “The Source provides.”
  “Decay is an extant form of life.” Translate as earnest alien scripture.
- **Unintelligible xenoid**: invented syllables in `*asterisks*`. Do not
  replace with “alien noises” in the target language.

## Practical rules

1. **Match the speaker, not a house style guide.** Weird AGIS, Robot AGIS,
   Stein, datapad colonists, and xenoid elders are different people.
2. **Keep Normal and Robot in lockstep.** Same facts, different mouth.
3. **Preserve dual item names.** Strange Material ≠ Sourcemetal.
4. **Do not translate identifiers.** Keys, IDs, `@AGIS@`, `[lightkey]`,
   `[ENGINEER]`, `[?]`.
5. **You may rearrange grammar** around tokens so the sentence is native.
   Example: `Press [lightkey] to toggle the wrist light.`
6. **Length.** Dialogue boxes and glyph plaques are narrow. Prefer the
   shorter of two accurate options. MEG help and datapads can run long.
7. **Second person.** The game addresses the player as **you**. Keep that
   unless the language requires a formal/informal choice; then pick informal
   for AGIS-weird and datapads, and a slightly more formal you for Robot AGIS
   and Stein.
8. **Gender.** The player character can be male or female. Avoid gendered
   player adjectives. Hahn, Stein, Larry, and the captain/engineer in logs
   are he/him in English.
9. **Numbers and units.** Keep gameplay numbers. Light-years, phosphine, and
   gem names stay scientific.
10. **Mods.** Workshop packs ship their own `Name` / `Description` English.
    Vanilla localization does not rewrite subscribed mods.
11. **When unsure**, look at an adjacent string from the same speaker in the
    same file, then at this glossary. Do not borrow Halo / Terraria / Starbound
    coinages for Source, MEG, or xenoids.

## Suggested reading order

For a translator starting a language pass:

1. This file.
2. AGIS Normal vs Robot pairs in `english/Config/DialogLocalization.json`
   (IDs 138–144 are a complete voice sample).
3. Xenoid dialog IDs around the Source Mnemonic (about 376–392) in
   `english/Config/DialogLocalization.json`.

## Related

- Terms: [`legal/TRANSLATION_TERMS_v1.0.md`](legal/TRANSLATION_TERMS_v1.0.md)
- Repository rights: [`LICENSE.md`](LICENSE.md)
- How to submit: [`CONTRIBUTING.md`](CONTRIBUTING.md)
