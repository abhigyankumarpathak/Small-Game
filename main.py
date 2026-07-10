"""
main.py  —  The game you actually RUN.

Run it from a terminal, from inside the "Small Game" folder:
    python3 main.py

This file is the "conductor". It doesn't do much math itself — instead it
IMPORTS the modules from our `game` package and tells them what to do.
Read the imports below: every one is a file inside the game/ folder.
"""

# Import our own modules from the "game" package (the game/ folder).
from game import screen                       # game/screen.py
from game import heroes                       # game/heroes.py
from game.heroes import HEROES, MONSTERS      # the data inside heroes.py
from game.combat import fight                 # the fight() function in game/combat.py


def choose_hero():
    """Ask the player which hero they want, and return a fresh fighter."""
    screen.banner("Choose your hero")

    names = list(HEROES.keys())
    for number, name in enumerate(names, start=1):
        stats = HEROES[name]
        print(f"  {number}. {name:<7} [{stats['type']:<8}] HP:{stats['hp']}  ATK:{stats['attack']}  CRIT:{stats['crit']}%")

    # Keep asking until we get a valid choice.
    while True:
        answer = input("\nType a number: ").strip()
        if answer.isdigit() and 1 <= int(answer) <= len(names):
            chosen_name = names[int(answer) - 1]
            return heroes.new_fighter(chosen_name, HEROES[chosen_name])
        print("  Please type one of the numbers shown.")


def main():
    """The whole game from start to finish."""
    screen.banner("MONSTER DUNGEON")
    screen.slow_print("Fight your way through the dungeon. Beat all monsters to win!\n")

    hero = choose_hero()

    # Fight each monster in order. If the hero loses even once, the game is over.
    for monster_data in MONSTERS:
        monster = heroes.new_fighter(monster_data["name"], monster_data)
        won = fight(hero, monster)

        if not won:
            screen.banner("GAME OVER")
            return  # leave main(), which ends the program

        # Small reward for winning: heal up a bit before the next fight.
        healed = min(hero["max_hp"], hero["hp"] + 15)
        print(f"You rest and recover to {healed} HP.\n")
        hero["hp"] = healed

    screen.banner("YOU CLEARED THE DUNGEON!  YOU WIN!")


# This special line means: "only run main() when this file is run directly."
# If some other file ever imports main.py, main() will NOT auto-run.
# It's a very common Python pattern — you'll see it everywhere.
if __name__ == "__main__":
    main()
