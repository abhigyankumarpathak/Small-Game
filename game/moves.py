"""
moves.py  —  The "moves" every fighter can use, plus the TYPE CHART.

This is the Pokemon-style heart of the game. Each fighter has a short list
of named MOVES (like Fireball or Backstab). Every move has:

    name    — what it's called
    type    — its element: physical, fire, ice, holy, poison, arcane, steel
    power   — how hard it hits (bigger = more damage)
    acc     — accuracy: the % chance it lands at all
    pp      — how many times it can be used before you run out
    effect  — an optional special: "heal", "guard", or "poison"

The TYPE_CHART decides whether a move is "super effective" against the
target's type — the same rock-paper-scissors idea Pokemon uses.

    from game import moves
    my_moves = moves.get_moves("Mage")
"""

# ---------------------------------------------------------------------------
# TYPE CHART
# ---------------------------------------------------------------------------
# TYPE_CHART[move_type][defender_type] = damage multiplier.
# Anything not listed defaults to 1.0 (normal damage). 2.0 = double damage,
# 0.5 = half damage. This is what makes picking the RIGHT move matter.
TYPE_CHART = {
    "holy":     {"undead": 2.0, "poison": 1.5},
    "poison":   {"undead": 0.5, "steel": 0.5, "poison": 0.5, "physical": 1.2},
    "fire":     {"fire": 0.5, "undead": 1.5, "steel": 1.5, "poison": 1.2},
    "ice":      {"fire": 2.0, "physical": 1.0},
    "arcane":   {"steel": 1.5, "physical": 1.5, "arcane": 0.5},
    "physical": {"steel": 0.5, "undead": 0.5},
    "steel":    {"poison": 1.5},
}


# Every element in the game, in a sensible reading order. show_table() in
# combat.py walks this list to print one row and one column per type, so the
# "fighting table" always stays in sync with the chart above.
TYPES = ["physical", "fire", "ice", "arcane", "holy", "poison", "steel", "undead"]


def effectiveness(move_type, defender_type):
    """Return (multiplier, message) for a move type hitting a defender type."""
    multiplier = TYPE_CHART.get(move_type, {}).get(defender_type, 1.0)
    if multiplier >= 1.5:
        message = "It's super effective!"
    elif multiplier <= 0.75:
        message = "It's not very effective..."
    else:
        message = ""
    return multiplier, message


# ---------------------------------------------------------------------------
# THE MOVE LISTS
# ---------------------------------------------------------------------------
# Every hero and monster gets its own set of 2-4 moves. Change these numbers
# to re-balance the game — no other file needs to change.
MOVES = {
    # ---- Heroes ----
    "Knight": [
        {"name": "Sword Slash", "type": "physical", "power": 11, "acc": 95, "pp": 25},
        {"name": "Shield Bash", "type": "steel",    "power": 8,  "acc": 100, "pp": 15, "effect": "guard"},
        {"name": "Holy Strike", "type": "holy",     "power": 16, "acc": 85, "pp": 10},
        {"name": "Second Wind", "type": "holy",     "power": 20, "acc": 100, "pp": 5,  "effect": "heal"},
    ],
    "Mage": [
        {"name": "Fireball",     "type": "fire",   "power": 17, "acc": 90,  "pp": 15},
        {"name": "Ice Shard",    "type": "ice",    "power": 12, "acc": 100, "pp": 20},
        {"name": "Arcane Blast", "type": "arcane", "power": 22, "acc": 80,  "pp": 8},
        {"name": "Mana Barrier", "type": "arcane", "power": 0,  "acc": 100, "pp": 5, "effect": "guard"},
    ],
    "Rogue": [
        {"name": "Quick Slash",  "type": "physical", "power": 10, "acc": 100, "pp": 30},
        {"name": "Poison Dagger", "type": "poison",  "power": 9,  "acc": 95,  "pp": 15, "effect": "poison"},
        {"name": "Backstab",     "type": "physical", "power": 18, "acc": 75,  "pp": 10, "crit_bonus": 30},
        {"name": "Smoke Screen", "type": "poison",   "power": 0,  "acc": 100, "pp": 5,  "effect": "guard"},
    ],

    # ---- Monsters (the AI picks one of these at random each turn) ----
    "Goblin": [
        {"name": "Scratch",    "type": "physical", "power": 8, "acc": 100, "pp": 99},
        {"name": "Venom Bite", "type": "poison",   "power": 7, "acc": 90,  "pp": 99, "effect": "poison"},
    ],
    "Skeleton": [
        {"name": "Bone Club",    "type": "physical", "power": 10, "acc": 95, "pp": 99},
        {"name": "Shadow Grasp", "type": "arcane",   "power": 9,  "acc": 90, "pp": 99},
    ],
    "Orc": [
        {"name": "Cleave", "type": "physical", "power": 12, "acc": 90, "pp": 99},
        {"name": "Smash",  "type": "physical", "power": 17, "acc": 75, "pp": 99},
    ],
    "Dragon": [
        {"name": "Fire Breath", "type": "fire",     "power": 18, "acc": 90,  "pp": 99},
        {"name": "Tail Swipe",  "type": "physical", "power": 12, "acc": 100, "pp": 99},
        {"name": "Inferno",     "type": "fire",     "power": 24, "acc": 70,  "pp": 99},
    ],
}

# A safe fallback so any fighter without a custom list can still act.
_DEFAULT = [{"name": "Struggle", "type": "physical", "power": 8, "acc": 100, "pp": 99}]


def get_moves(name):
    """Return a FRESH copy of `name`'s moves (so each fighter tracks its own PP).

    We also remember each move's starting PP as `max_pp` so a fight can
    refill it later.
    """
    source = MOVES.get(name, _DEFAULT)
    fresh = []
    for move in source:
        copy = dict(move)          # copy so decrementing PP doesn't touch the master list
        copy["max_pp"] = copy["pp"]
        fresh.append(copy)
    return fresh


def refill_pp(fighter):
    """Restore every move's PP back to full (called at the start of each fight)."""
    for move in fighter["moves"]:
        move["pp"] = move["max_pp"]
