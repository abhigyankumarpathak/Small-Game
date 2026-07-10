# Monster Dungeon 🐉

A tiny terminal battle game, built to teach **modules, functions, and importing
your own files** in Python.

## Run it instantly (no install)

[![Run on Replit](https://replit.com/badge/github/abhigyankumarpathak/Small-Game)](https://replit.com/github/abhigyankumarpathak/Small-Game)

Click the badge above. Replit opens the project in your browser and imports the
code — then just press the big green **Run** button and play in the console.
(No install; a free Replit account is all you need.)

## Run locally (no account needed)

Have Python installed? Skip the sign-ups entirely. Grab the code and run it:

```bash
git clone https://github.com/abhigyankumarpathak/Small-Game.git
cd Small-Game
python3 main.py
```

No `git`? On the GitHub page click **`< > Code` → Download ZIP**, unzip it, then
`cd` into the folder and run `python3 main.py`.

## How to play

Open a terminal, go into this folder, and run:

```bash
cd "Small Game"
python3 main.py
```

Pick a hero, then battle each monster **Pokemon-style**. Every round a menu asks
what you want to do:

```
  What will you do?
    1. Fight    — attack with one of your moves
    2. Item     — use something from your bag
    3. Status   — check both fighters, your moves and your bag
    4. Help     — how the game works
```

**Fight** and **Item** use up your turn; **Status** and **Help** are free.

- **Types matter.** A move can be *super effective* or *not very effective*
  depending on the target (e.g. the Mage's **Ice Shard** shreds the fire-type
  Dragon; the Knight's **Holy Strike** wrecks the undead Skeleton).
- **Special effects:** some moves *heal*, some *guard* (halve the next hit), and
  some *poison* the enemy so it keeps losing HP each turn.
- **PP is limited** — you can't spam your strongest move forever.
- **Your bag** starts with 3 Potions, 1 Elixir, 2 Antidotes and 2 Bombs, and
  what's left **carries over** into the next fight. Spend it wisely.

Beat all four monsters to clear the dungeon.

### The three heroes

| Hero   | Type   | Style                              | Signature moves          |
|--------|--------|-----------------------------------|--------------------------|
| Knight | steel  | Tanky, guards and heals           | Holy Strike, Second Wind |
| Mage   | arcane | Glass cannon, hits elements       | Fireball, Arcane Blast   |
| Rogue  | poison | Fast, high crit, damage-over-time | Backstab, Poison Dagger  |

## The folder = the lesson

```
Small Game/
├── main.py            ← the file you RUN. It imports everything else.
└── game/              ← a PACKAGE (a folder of modules you made yourself)
    ├── __init__.py    ← makes "game" importable; can be almost empty
    ├── dice.py        ← your random-number library  (roll, chance, pick...)
    ├── screen.py      ← printing helpers + dice art  (banner, health_bar, draw_dice...)
    ├── heroes.py      ← the DATA: heroes & monsters  (stats + which moves they know)
    ├── moves.py       ← every fighter's moves + the TYPE CHART (super effective!)
    ├── items.py       ← the bag: potions, elixirs, antidotes, bombs
    └── combat.py      ← the fight logic; it IMPORTS dice, screen, moves AND items
```

## The 3 things to understand about imports

1. **A module is just a `.py` file.** `dice.py` is a module. To use its
   functions somewhere else you write `from game.dice import roll`.

2. **A package is a folder with an `__init__.py` file.** That empty-ish file is
   the only reason Python lets you write `from game import screen`. Delete it and
   the imports break — try it!

3. **`from game import dice` vs `import random`** — they work the *same way*.
   The only difference is `random` was written by the Python team, and `dice`
   was written by **you**. Once you can make `dice.py`, you can make any library.

## Try changing things (good beginner exercises)

- Open `game/heroes.py` and add a new hero to the `HEROES` dictionary, then give
  it a move list in `game/moves.py`. It shows up in the menu automatically.
- Invent a brand-new move in `game/moves.py` (say, a `"fire"` move called
  "Flame Slash") and hand it to a hero — no other file needs to change.
- Add a new element to the `TYPE_CHART` in `game/moves.py` and watch the
  "super effective!" messages change.
- In `game/screen.py`, change the `#` in `health_bar` to `█` for a fancier bar.
- Invent a new item in the `ITEMS` dictionary in `game/items.py` (reuse a `kind`
  like `"heal"`), then add it to `STARTING_BAG` so it shows up in your menu.
- Add a 5th monster to the `MONSTERS` list in `heroes.py` (give it a `type` and
  a move list too).

Each of these teaches you that a program is many small files working together
through imports — not one giant file.
