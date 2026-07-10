"""
heroes.py  —  The "data" of our game: heroes you can play and monsters you fight.

A module doesn't have to be only functions. It can also just hold DATA
(lists and dictionaries) that other files import and use. Think of this
file as a tiny database.

    from game.heroes import HEROES, MONSTERS
"""

from game import moves  # each fighter's move list + its element type

# A dictionary of playable heroes.
# Each hero is itself a dictionary of stats. "type" is its element, which
# decides what it's weak or strong against (see game/moves.py TYPE_CHART).
HEROES = {
    "Knight": {"hp": 55, "attack": 12, "crit": 15, "type": "steel"},   # crit = % chance of a big hit
    "Mage":   {"hp": 40, "attack": 16, "crit": 25, "type": "arcane"},
    "Rogue":  {"hp": 45, "attack": 14, "crit": 35, "type": "poison"},
}

# The monsters you will battle, in the order they appear.
MONSTERS = [
    {"name": "Goblin",   "hp": 30, "attack": 8,  "crit": 10, "type": "poison"},
    {"name": "Skeleton", "hp": 40, "attack": 10, "crit": 15, "type": "undead"},
    {"name": "Orc",      "hp": 55, "attack": 13, "crit": 20, "type": "physical"},
    {"name": "Dragon",   "hp": 80, "attack": 18, "crit": 30, "type": "fire"},
]


def new_fighter(name, stats):
    """Build a fresh 'fighter' dictionary from a name and a stats dictionary.

    We copy the stats so that fighting doesn't permanently change the
    original data in HEROES / MONSTERS above. `max_hp` remembers the
    starting health so we can draw the health bar.
    """
    return {
        "name": name,
        "hp": stats["hp"],
        "max_hp": stats["hp"],
        "attack": stats["attack"],
        "crit": stats["crit"],
        "type": stats.get("type", "physical"),  # element used for type match-ups
        "moves": moves.get_moves(name),          # this fighter's list of moves
        "defending": False,                      # True for one turn after guarding
        "poison": 0,                             # turns of poison damage remaining
    }
