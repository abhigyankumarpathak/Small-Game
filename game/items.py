"""
items.py  —  The things you carry in your bag.

Another data-plus-helpers module, just like moves.py. ITEMS below is the
"catalogue" (what each item does), and a fighter's BAG is a small dictionary
that remembers how many of each item they still have.

    from game import items
    hero["bag"] = items.new_bag()
    items.use(hero, monster, "Potion")

Using an item costs you your turn — the monster still gets to attack — so
picking the right moment matters.
"""

from game import dice     # game/dice.py   — randomness
from game import screen   # game/screen.py — printing helpers


# ---------------------------------------------------------------------------
# THE ITEM CATALOGUE
# ---------------------------------------------------------------------------
# Each item has a short description (shown in the bag menu) and a "kind" that
# tells use() below what code to run. Change the numbers here to re-balance.
ITEMS = {
    "Potion":   {"kind": "heal",   "power": 25, "desc": "restore 25 HP"},
    "Elixir":   {"kind": "refill", "desc": "refill the PP of every move"},
    "Antidote": {"kind": "cure",   "desc": "cure poison"},
    "Bomb":     {"kind": "damage", "power": 20, "type": "fire",
                 "desc": "throw for 20+ fire damage, never misses"},
}

# What you start the dungeon with. The bag is a dictionary of name -> count.
STARTING_BAG = {"Potion": 3, "Elixir": 1, "Antidote": 2, "Bomb": 2}


def new_bag():
    """Return a fresh copy of the starting bag (so the master copy is safe)."""
    return dict(STARTING_BAG)


def carried(bag):
    """Return the names of items the fighter still has at least one of."""
    return [name for name, count in bag.items() if count > 0]


def show_bag(bag):
    """Print the bag as a numbered menu."""
    print("\n  Your bag:")
    names = carried(bag)
    if not names:
        print("    (empty)")
        return names

    for number, name in enumerate(names, start=1):
        item = ITEMS[name]
        print(f"    {number}. {name:<9} x{bag[name]}   {item['desc']}")
    return names


def use(user, target, name):
    """Use one `name` from `user`'s bag on the battlefield.

    Returns True if the item was actually spent (which uses up your turn),
    or False if it would have been wasted — then you get to choose again.
    """
    item = ITEMS[name]
    kind = item["kind"]

    # --- Checks that stop you wasting an item ---
    if kind == "heal" and user["hp"] >= user["max_hp"]:
        print("  You're already at full health.")
        return False

    if kind == "cure" and user["poison"] <= 0:
        print("  You aren't poisoned.")
        return False

    if kind == "refill" and all(m["pp"] >= m["max_pp"] for m in user["moves"]):
        print("  All your moves are already at full PP.")
        return False

    # --- The item is really being used, so spend it ---
    user["bag"][name] -= 1
    screen.slow_print(f"\n  {user['name']} used the {name}!")

    if kind == "heal":
        user["hp"] = min(user["max_hp"], user["hp"] + item["power"])
        print(f"  Recovered {item['power']} HP! (now {user['hp']}/{user['max_hp']})")

    elif kind == "cure":
        user["poison"] = 0
        print("  The poison is gone!")

    elif kind == "refill":
        for move in user["moves"]:
            move["pp"] = move["max_pp"]
        print("  Every move is back to full PP!")

    elif kind == "damage":
        roll = screen.roll_dice(dice.roll)
        damage = item["power"] + roll
        target["hp"] -= damage
        print(f"  The {name} hits {target['name']} for {damage} damage! "
              f"({item['type']} · power {item['power']} + rolled {roll})")

    return True
