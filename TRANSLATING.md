# Translating Signs of Life

Voice, glossary, and markup. English snapshots live in `english/Config/`.
Put translations in `locales/<code>/Config/`. Do not submit AI generated
text. If a line is not ready, omit it so the game keeps English.
A pull request accepts [`LICENSE.md`](LICENSE.md).

This repository can overlay these compiled JSON tables:

- `UILocalization.json` — HUD and menu chrome, including `armor.stat.*` / `armor.bonus.*` mechanical armor bonus templates
- `TooltipLocalization.json` — HUD hover tooltips
- `StatusEffectLocalization.json` — status-effect labels
- `DialogLocalization.json` — spoken lines, AGIS, player options
- `helpData.json` — MEG help topics (`Key`; translate `Label` / `Category` / `Text`)
- `journalEntries.json` — AGIS journal (`ID`; translate `Message`)
- `InventoryItemData.json` — compiled item names (`ItemID`; translate `Name` / `Description` / existing `Templates` keys; leave `AutoOrganizeString`)
- `MeleeWeaponData.json` / `RangedWeaponData.json` — weapon names (`ItemID`; translate `Name` / `Description`)
- `ProjectileRegistrationData.json` — projectile display names (leave `SaveName`; translate `Name`)
- `CreatureRegistrationData.json` — creature names / codex (leave `LivingEntityType`; translate `Name` / `Description` / `CodexCategory`)
- `StaticPrefabRegistrationData.json` — prefab catalog (leave `SaveName` / `SaveAliases`; translate `Name` / `DisplayName` / `Description` / tooltip fields)
- `DatapadTextData.json` — datapad lore (leave `ID`; translate `Title` / `Category` / `Text`)
- `ArmorSetData.json` — compiled armor (`ItemType`; translate piece `Name` / `Description` and unique bonus `Description` overrides; leave set `Name` and piece `Set`)

Missing overlay IDs keep English. Empty overlay fields keep English. Unknown
keys are skipped. Container gump titles are **not** overlayable yet.

The sections below still mention game-repo paths (`Content/Config/...`). For
the overlay tables in this repository, use `english/Config/` instead.

# Translation guide

The shipping game is English-only unless a locale overlay pack is loaded.
Spoken lines, help, journal, HUD chrome, compiled items, melee/ranged names,
projectiles, creatures, static-prefab catalog English, datapad lore, and
compiled armor names live in tables that a pack can overlay from `Config/`.
Container gump titles, glyph quotes, and leftover C# HUD crumbs are not
overlayable yet.
Treat every player-facing English sentence as in-scope unless this guide says
to leave it alone.

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

English source has real typos (`alotted`, `draggin`, `accesssible`, `Its`
for `It's`, `patten`). Do not copy those into a new language. Do not “fix”
them in English unless the change is a dedicated copy pass. Joke misspellings
and voice tics are different from accidents; see [Humor traps](#humor-traps).

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
(`[ENGINEER]`, `[CAPTAIN]`, `[JANITOR]`) expand to surnames from
`Content/Config/CSV/commonSurnames.csv` (Johnson, Patel, Tremblay, …). Those
surnames stay in their original spelling; they are diegetic Earth names.

## AGIS voices

Spoken strings live in `Content/Config/DialogLocalization.json`. Each row is
`{ ID, Normal, Robot? }`. The table also accepts unused `Gangster` and
`Cowboy` fields; do not invent those unless a personality chip ships.

Lookup:

- **Normal** is the degraded / “wacky” voice. It is the default on the
  campaign world (`NEW_EARTH` / Osiris), because AGIS.IsWeird is true there.
- **Robot** is the professional voice. Used when AGIS is not weird (sandbox
  and most non-story maps). If Robot is missing, lookup falls back to Normal.
- NPC lines, player options, and xenoid dialogue use **Normal** only.
- `Config.GetAGISDialogString` picks the variant. `Config.GetGameString`
  always returns Normal.

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
| Osiris | Destination planet | Keep. UI also shows this generator as “Osiris”; internals still say “New Earth.” |
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

Several items have a **human guess** and a **xenoid true name**. Gameplay
swaps them as `AlienLanguagePercent` rises (`AlienNameMask` until the
threshold, then `Name`). Both strings must be translated, and they must
remain distinct.

| Before language skill | After (true name) |
| --- | --- |
| Strange Artifact | The accessory’s real name (Unyielding Carapace, Mass Displacer, …) |
| Raw / Coarse / Granular / Refined Strange Material | Raw / Coarse / Granular / Refined Sourcemetal |

`AlienString` on artifacts is xenoid flavor, shown word-by-word as knowledge
grows. Untranslated words become `[?]`. Translate the full English
`AlienString`; the masking code splits on spaces, so do not put meaning into
punctuation-only tokens.

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

1. Scanning glyphs, artifacts, and xenoid text raises `AlienLanguagePercent`
   (0.0–1.0).
2. Below **0.3**, xenoid talk and scanner complaints are unintelligible:
   `[unintelligible]`, `*kreech-vash!*`, `*thul'nari vek!*`. Keep the
   asterisks and invented phonemes; they are not English.
3. Between **0.3** and **0.9**, complaints are broken English: `BEAMS HURT`,
   `STOP BEAM`. Translate into equally broken target-language telegrams, not
   fluent speech.
4. At **0.9+**, xenoids speak fluent, formal target language.
5. Glyph displays and `AlienString` fields reveal source words at random
   weighted by knowledge. Hidden words show as `[?]`. Keep `[?]` exactly;
   the code and UI expect that token.

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

`StringUtils.FilterKeyWords` replaces these with the player’s current key.
Unknown `[brackets]` are stripped to their inner text (and in dialogue they
may be `@HIGHLIGHTED@` and uppercased). That is why lore terms in dialogue
sometimes use square brackets: `[Source Mnemonic]` becomes a highlighted
proper term at runtime.

**Never translate the identifier.** Keep exact spelling:

`[lightkey]`, `[menukey]`, `[grablaserkey]`, `[minimapkey]`, `[mapkey]`,
`[grapplekey]`, `[holsterkey]`, `[kickkey]`, `[reloadkey]`, `[jump]`,
`[crouch]`, `[up]`, `[down]`, `[left]`, `[right]`, `[primary]`,
`[secondary]`, `[scrollslot1]`, `[scrollslot4]`, `[hostname]`, `[al]`

Write the surrounding sentence so a key name in the middle still reads
naturally (`press [lightkey] to …`).

### Datapad lore tokens

Shipped datapad bodies run through `ExpandLoreTokens`. Only these inner
names are replaced. Keep the brackets and English identifiers:

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

- `{0}`, `{1}` in C# format strings (grab laser, grapple descriptions).
- JSON/XML keys, file names, `sol.` item UUIDs, dialogue numeric IDs.
- `[unintelligible]`, `[unintelligible xenoid speech]`, `[?]` as displayed
  alien-language UI, not as keybinds.

## Where the English lives

One concern, one store. Do not add a parallel translation file that nothing
loads. Locale overlay packs reuse the same compiled JSON filenames under
`Config/` (datapads overlay `Config/DatapadTextData.json` even though
English is XML) and fall back to English for missing/empty fields. Unknown
keys are skipped. Combat stats, `SaveName`, `ItemID`, `LivingEntityType`,
`StaticPrefabType`, datapad `ID`, and `AutoOrganizeString` stay English even
if the overlay copies them.

| Kind of text | Store | Notes |
| --- | --- | --- |
| Spoken lines, AGIS, player options | `Content/Config/DialogLocalization.json` | Trees in `DialogueData.xml` reference IDs only. Live AGIS `SayQuiet` / tutorial lines use the same numeric IDs. Leave `[left]` / `[menukey]` tokens in the English; they expand at lookup. Pack overlay: `Config/DialogLocalization.json`. |
| Stein ↔ AGIS bridge pairs | `Content/Config/steinAgisDialogPairs.json` | IDs into the spoken table, no prose. Not overlayable. |
| MEG help topics | `Content/Config/helpData.json` | `Label` + `Text`. Newlines are real. Pack overlay: `Config/helpData.json`. |
| Journal | `Content/Config/journalEntries.json` | AGIS log. Pack overlay: `Config/journalEntries.json`. |
| HUD / menu chrome | `Content/Config/UILocalization.json` | String keys. Menus, settings, load tips, and keybind action labels are here. Armor bonus `+N Stat` templates are `armor.bonus.flat` / `armor.bonus.percent` plus `armor.stat.{StatusEffectType}`. Pack overlay: `Config/UILocalization.json`. |
| HUD hover tooltips | `Content/Config/TooltipLocalization.json` | `tooltip.*` IDs. Live numbers and key names are `{0}` placeholders. Pack overlay: `Config/TooltipLocalization.json`. |
| Status-effect labels | `Content/Config/StatusEffectLocalization.json` | `status.{StatusEffectType}` IDs. Types with no authored label stay off the table. Pack overlay: `Config/StatusEffectLocalization.json`. |
| Datapads | `Content/XML/DatapadTextData.xml` | Leave `id`. Translate `title`, `category`, body. Pack overlay: `Config/DatapadTextData.json` (`ID`, `Title`, `Category`, `Text`). |
| Compiled item names / descriptions | `Content/Config/InventoryItemData.json` | Optional `Name` / `Description` plus `Templates` for instance states (`[itemname]`, `[level]`, `[mobname]`). Furniture and placeable display names live here. Shared status lines in `UILocalization.json`. Melee torches keep `MeleeWeaponData.json`. Pack overlay: `Config/InventoryItemData.json` (do not overlay `AutoOrganizeString`). |
| Compiled projectiles | `Content/Config/ProjectileRegistrationData.json` | Leave `SaveName` in English. Translate `Name`. Inventory ammo names stay in `InventoryItemData.json`. Pack overlay: `Config/ProjectileRegistrationData.json`. |
| Container gump layouts | `Content/XML/ContainerGumpData.xml` | Leave `<id>` in English slug form. Translate `<name>` (gump title fallback). Item names stay in `InventoryItemData.json`. Not overlayable yet. |
| Armor names/descriptions | `Content/Config/ArmorSetData.json` | Leave `ItemType` and set `Name` / piece `Set`. Translate piece `Name` / `Description` and unique bonus `Description` overrides. Mechanical `+N Stat` lines come from `UILocalization.json` (`armor.stat.*` / `armor.bonus.*`). Pack overlay: `Config/ArmorSetData.json`. |
| Melee / ranged names | `MeleeWeaponData.json`, `RangedWeaponData.json` | Leave `ItemID`. Translate `Name` / `Description`. Pack overlays: `Config/MeleeWeaponData.json`, `Config/RangedWeaponData.json`. |
| Creature names / codex | `Content/Config/CreatureRegistrationData.json` | Leave `LivingEntityType`. Translate `Name` / `Description` / `CodexCategory`. Pack overlay: `Config/CreatureRegistrationData.json`. |
| Compiled static-prefab catalog | `Content/Config/StaticPrefabRegistrationData.json` | Leave `SaveName` / `SaveAliases` in English. Translate `Name` / `DisplayName` / `Description` / `CodexCategory` / `TooltipNameOverride` / `DescriptionsByState` / `SpecificTooltips`. Pack overlay: `Config/StaticPrefabRegistrationData.json`. |
| Pack items / flora / structures | `Content/LoadedContent/**/item_*.json` etc. | `Name`, `Description`, `AlienNameMask`, `AlienString`. |
| Glyph wall quotes | `Generators/ProceduralGlyphData.cs` (duplicated in a couple of dungeon generators) | Xenoid proverb voice. |
| Scanner complaints | `Entities/Creatures/XenoidWristScannerReaction.cs` | Three pools by language skill. |
| Crafting chrome, prefab interaction / state strings | Prefab table / `DialogLocalization.json` | Specific tooltips, hover name overrides, and state-dependent analyze text live in `StaticPrefabRegistrationData.json`. Numeric AGIS `SayQuiet` IDs stay here. |
| Press / Steam / website | `website/press/signs-of-life-fact-sheet.txt`, `website/game/` | Marketing, same glossary. |

`DialogueData.xml` must not grow inline `<message>` text. If a new spoken
line is needed, add a DialogLocalization ID and point the XML at it.

The content-database tool can search these tables. It will not see hardcoded
C# strings.

## Humor traps

Leave these intact; they are jokes, not errors.

- **Berenstein / Berenstain.** Both spellings must survive. The world flag
  `_berenstainUniverse` picks one. A “correction” to a single spelling kills
  the gag.
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

For a human or agent starting a language pass:

1. This file.
2. AGIS Normal vs Robot pairs in `english/Config/DialogLocalization.json`
   (IDs 138–144 are a complete voice sample).
3. Xenoid dialog IDs around the Source Mnemonic (about 376–392) in
   `english/Config/DialogLocalization.json`.

## Related

- License: [`LICENSE.md`](LICENSE.md)
- How to submit: [`CONTRIBUTING.md`](CONTRIBUTING.md)
