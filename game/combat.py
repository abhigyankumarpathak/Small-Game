"""
combat.py  —  The rules of fighting (Pokemon style!).

This is where the OTHER modules come together. Notice the imports at the
top: combat.py uses your dice, screen AND moves libraries. That is the big
idea of this project — small modules that import each other.

    from game.combat import fight

Combat is turn-based. On YOUR turn a menu asks what you want to do: FIGHT
(pick a move), use an ITEM from your bag, check your STATUS, or read the
HELP. Each move has a type, a power, an accuracy, and limited PP. The DICE
and the TYPE CHART decide how well it lands. Then the monster takes its turn.
"""

import os
import sys
import time
from game import dice     # our own random-number library (game/dice.py)
from game import screen   # our own display library      (game/screen.py)
from game import moves    # move data + the type chart    (game/moves.py)
from game import items    # your bag of potions & bombs   (game/items.py)


def is_alive(fighter):
    """A fighter is alive while its hp is above 0."""
    return fighter["hp"] > 0


def deal_damage(defender, amount):
    """Apply `amount` damage to `defender`, respecting any active guard.

    Returns the damage actually dealt (after a block is applied).
    """
    # If the defender guarded last turn, halve the incoming hit
    # (and then use up the shield so it only protects once).
    if defender.get("defending"):
        amount = max(1, amount // 2)
        print(f"  {defender['name']}'s guard softens the blow to {amount}!")
        defender["defending"] = False

    defender["hp"] -= amount
    return amount


def perform_move(user, target, move):
    """Carry out one move by `user` against `target`. Handles everything:
    accuracy, dice, type effectiveness, crits, and special effects.
    """
    move["pp"] -= 1  # using a move spends one of its PP
    screen.slow_print(f"\n  {user['name']} used {move['name']}!")

    effect = move.get("effect")

    # --- Pure support moves that don't need to hit an enemy ---
    if effect == "guard" and move["power"] == 0:
        user["defending"] = True
        screen.slow_print(
            "  It braces for the next attack — incoming damage halved!")
        return

    if effect == "heal":
        roll = screen.roll_dice(dice.roll)
        healed = move["power"] + roll * 2
        user["hp"] = min(user["max_hp"], user["hp"] + healed)
        print(
            f"  Rolled {roll} — {user['name']} recovers {healed} HP! (now {user['hp']}/{user['max_hp']})")
        return

    # --- Everything below is an attack that must first LAND ---
    if not dice.chance(move["acc"]):
        print(f"  ...but it MISSED!")
        return

    roll = screen.roll_dice(dice.roll)                     # show the die
    base = move["power"] + roll

    # Type match-up: is this move strong or weak against the target?
    multiplier, message = moves.effectiveness(move["type"], target["type"])
    damage = int(base * multiplier)

    # Critical hit — some moves (like Backstab) add bonus crit chance.
    crit_chance = user["crit"] + move.get("crit_bonus", 0)
    if dice.chance(crit_chance):
        damage = int(damage * 1.5)
        screen.slow_print("  *** A CRITICAL HIT! ***")

    dealt = deal_damage(target, damage)
    if message:
        screen.slow_print(f"  {message}")
    print(
        f"  {target['name']} takes {dealt} damage!  ({move['type']} · power {move['power']} + rolled {roll})")

    # Guard moves that also do damage (like Shield Bash) raise the shield too.
    if effect == "guard":
        user["defending"] = True
        print(f"  {user['name']} also raises its guard!")

    # Poison moves leave the target taking damage over the next few turns.
    if effect == "poison" and is_alive(target) and target["poison"] <= 0:
        target["poison"] = 3
        print(f"  {target['name']} is badly POISONED!")


def tick_poison(fighter):
    """If `fighter` is poisoned, deal a little damage and count down the timer."""
    if fighter["poison"] > 0 and is_alive(fighter):
        damage = 5
        fighter["hp"] -= damage
        fighter["poison"] -= 1
        print(f"  {fighter['name']} is hurt by poison! (-{damage} HP)")


def choose_move(fighter):
    """Show `fighter`'s move menu and return the move the player picks."""
    print("\n  Choose your move:")
    for number, move in enumerate(fighter["moves"], start=1):
        tag = _describe(move)
        print(
            f"    {number}. {move['name']:<13} {tag:<26} PP {move['pp']}/{move['max_pp']}")

    while True:
        answer = input("  Move number: ").strip()
        if answer.isdigit() and 1 <= int(answer) <= len(fighter["moves"]):
            move = fighter["moves"][int(answer) - 1]
            if move["pp"] <= 0:
                print("  That move is out of PP! Pick another.")
                continue
            return move
        print(f"  Please type a number from 1 to {len(fighter['moves'])}.")


def _describe(move):
    """A short label for the move menu, e.g. 'fire · pow 17 · acc 90%'."""
    effect = move.get("effect")
    if effect == "heal":
        return "heal · restore HP"
    if effect == "guard" and move["power"] == 0:
        return "guard · block next hit"
    label = f"{move['type']} · pow {move['power']} · acc {move['acc']}%"
    if effect == "poison":
        label += " · +psn"
    return label


# ---------------------------------------------------------------------------
# THE TURN MENU
# ---------------------------------------------------------------------------
# Attacking and using an item both END your turn. Looking at your status or
# reading the help does NOT — you get to choose again afterwards. That is why
# take_turn() below sits inside a `while True` loop.

def choose_item(hero, monster):
    """Show the bag and use whatever the player picks.

    Returns True if an item was used (turn over), False to go back to the menu.
    """
    names = items.show_bag(hero["bag"])
    if not names:
        return False

    while True:
        answer = input("  Item number (or 'b' to go back): ").strip().lower()
        if answer == "b":
            return False
        if answer.isdigit() and 1 <= int(answer) <= len(names):
            return items.use(hero, monster, names[int(answer) - 1])
        print(f"  Please type a number from 1 to {len(names)}, or 'b'.")


def reset():
    """Reset the game by clearing the screen and re-launching it from the start.
    """
    # Clear the screen first ("cls" on Windows, "clear" everywhere else).
    os.system("cls" if os.name == "nt" else "clear")
    os.execv(sys.executable, [sys.executable] + sys.argv)


def show_status(hero, monster):
    """Print everything the player might want to know before deciding."""
    print()
    for fighter in (hero, monster):
        screen.health_bar(
            f"{fighter['name']} ({fighter['type']})", fighter["hp"], fighter["max_hp"])
        notes = []
        if fighter["poison"] > 0:
            notes.append(f"poisoned for {fighter['poison']} more turn(s)")
        if fighter["defending"]:
            notes.append("guarding")
        if notes:
            print(f"           ...{', '.join(notes)}")

    print(f"\n  Your crit chance: {hero['crit']}%")
    print("  Your moves:")
    for move in hero["moves"]:
        print(
            f"    - {move['name']:<13} {_describe(move):<26} PP {move['pp']}/{move['max_pp']}")
    items.show_bag(hero["bag"])


def show_help():
    """A short reminder of the rules."""
    print("""
  HOW TO PLAY
    - FIGHT uses one of your moves. Each move spends 1 PP, so you can't
      spam your strongest one forever.
    - Every move has a TYPE. Hitting a monster with a type it's weak to
      does extra damage ("super effective"); a bad match-up does less.
    - ITEM uses something from your bag. It costs you your turn — the
      monster still attacks — so heal before you're nearly dead.
    - GUARD moves halve the next hit you take. POISON chips away at a
      fighter for 3 turns.
    - STATUS and HELP are free: they don't use up your turn.
""")


def take_turn(hero, monster):
    """Ask the player what to do, and keep asking until their turn is spent."""
    while True:
        print("\n  What will you do?")
        print("    1. Fight    — attack with one of your moves")
        print("    2. Item     — use something from your bag")
        print("    3. Status   — check both fighters, your moves and your bag")
        print("    4. Chart    — see the type match-up table")
        print("    5. Help     — how the game works")
        print("    6. Restart  — start a new battle")

        answer = input("  Choose 1-6: ").strip()

        if answer == "1":
            perform_move(hero, monster, choose_move(hero))
            return
        elif answer == "2":
            if choose_item(hero, monster):
                return   # the item was used, so the turn is over
        elif answer == "3":
            show_status(hero, monster)
        elif answer == "4":
            show_table()
        elif answer == "5":
            show_help()
        elif answer == "6":
            user_confirm = input(
                "  Are you sure you want to restart? (y/n) ").strip().lower()
            if user_confirm == "y":
                screen.slow_print("  Restarting battle...")
                time.sleep(1.5)
                reset()
        else:
            print("  Please type 1, 2, 3, 4, 5 or 6.")


def monster_choose_move(monster):
    """The monster 'AI': pick a random move it still has PP for."""
    usable = [m for m in monster["moves"] if m["pp"] > 0]
    return dice.pick(usable) if usable else monster["moves"][0]


def fight(hero, monster):
    """Run a full battle between hero and monster.

    Returns True if the hero wins, False if the hero loses.
    Each round: the player picks a move, the monster picks a move, then any
    poison ticks at the end of the round.
    """
    screen.banner(f"{hero['name']}  VS  {monster['name']}")

    # Fresh start each battle: drop any leftover guard/poison and refill PP.
    for f in (hero, monster):
        f["defending"] = False
        f["poison"] = 0
        moves.refill_pp(f)

    # The bag carries over between fights, so only create one if there isn't one.
    hero.setdefault("bag", items.new_bag())

    while is_alive(hero) and is_alive(monster):
        # Show the current health (and type) of both fighters.
        print()
        screen.health_bar(
            f"{hero['name']} ({hero['type']})", hero["hp"], hero["max_hp"])
        screen.health_bar(
            f"{monster['name']} ({monster['type']})", monster["hp"], monster["max_hp"])

        take_turn(hero, monster)

        if is_alive(monster):
            perform_move(monster, hero, monster_choose_move(monster))

        # End of round: poison hurts anyone still standing.
        tick_poison(hero)
        tick_poison(monster)
        print()

    if is_alive(hero):
        screen.slow_print(f"You defeated the {monster['name']}!")
        return True
    else:
        screen.slow_print(f"The {monster['name']} defeated you...")
        return False


def show_table():
    """Print the type chart so the player can plan good match-ups.

    Rows are the ATTACKING move's type, columns are the DEFENDER's type.
    A cell shows the damage multiplier: x2.0 hits hard, x0.5 is resisted,
    and a dash means normal (x1.0) damage.
    """
    col = 9  # width of every column, so the grid lines up neatly

    print("\n  TYPE CHART  —  attacker (row)  vs  defender (column)")
    print("  x2.0 = super effective · x0.5 = resisted · - = normal\n")

    # Header row: an empty corner cell, then every defender type.
    header = " " * col + "".join(f"{t:<{col}}" for t in moves.TYPES)
    print("  " + header)

    for attacker in moves.TYPES:
        row = f"{attacker:<{col}}"
        for defender in moves.TYPES:
            multiplier, _ = moves.effectiveness(attacker, defender)
            cell = "-" if multiplier == 1.0 else f"x{multiplier}"
            row += f"{cell:<{col}}"
        print("  " + row)
