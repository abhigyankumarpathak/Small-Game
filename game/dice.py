"""
dice.py  —  Your very own tiny "random numbers" library.

This is a MODULE: just a .py file full of functions you can import.
Everything here is about randomness, so it all lives together in one place.

Other files import these functions like this:
    from game.dice import roll, chance
"""

import random  # a module from Python's standard library (someone else's library!)


def roll(sides=6):
    """Roll a dice with the given number of sides. Returns 1..sides.

    >>> roll(6)   # gives a number from 1 to 6
    """
    return random.randint(1, sides)


def roll_between(low, high):
    """Return a random whole number from low to high (both included)."""
    return random.randint(low, high)


def chance(percent):
    """Return True `percent`% of the time.

    Example: chance(25) is True about 1 out of every 4 calls.
    Great for "did the attack land a critical hit?" style questions.
    """
    return random.randint(1, 100) <= percent


def pick(items):
    """Pick one random item out of a list."""
    return random.choice(items)
