"""
screen.py  —  Helper functions for showing things on the screen.

Keeping all the "printing" code in one module means the rest of the game
can just say `screen.banner("Victory!")` instead of repeating print() tricks
everywhere. This is the whole point of modules: group related helpers together.

    from game import screen
    screen.banner("Hello")
"""

import time


# ---------------------------------------------------------------------------
# DICE DRAWING
# ---------------------------------------------------------------------------
# A dice face is a 3x3 grid of "pip" spots. For each number 1..6 we list which
# spots have a dot on them. Positions are (row, column), each 0, 1, or 2.
_PIPS = {
    1: {(1, 1)},
    2: {(0, 0), (2, 2)},
    3: {(0, 0), (1, 1), (2, 2)},
    4: {(0, 0), (0, 2), (2, 0), (2, 2)},
    5: {(0, 0), (0, 2), (1, 1), (2, 0), (2, 2)},
    6: {(0, 0), (0, 2), (1, 0), (1, 2), (2, 0), (2, 2)},
}


def _die_lines(value):
    """Return a list of text lines that draw a single dice face for `value`."""
    dots = _PIPS[value]
    lines = ["┌───────┐"]
    for row in range(3):
        cells = []
        for col in range(3):
            cells.append("●" if (row, col) in dots else " ")
        lines.append("│ " + " ".join(cells) + " │")
    lines.append("└───────┘")
    return lines


def draw_dice(*values):
    """Print one or more dice faces side by side.

    Example:  draw_dice(4, 2)  draws a 4-die and a 2-die next to each other.
    """
    # Build each die, then stitch them together line-by-line so they sit
    # side by side instead of stacked on top of each other.
    all_dice = [_die_lines(v) for v in values]
    for row in range(5):  # each die is 5 text lines tall
        print("   ".join(die[row] for die in all_dice))


def roll_dice(roll_fn, count=1, sides=6, frames=8, delay=0.06):
    """Animate rolling `count` dice, then return the final value(s).

    `roll_fn` is a function that returns a random number (we pass in
    dice.roll so this module doesn't need to know about randomness).
    Returns a single int when count == 1, otherwise a list of ints.
    """
    faces = [roll_fn(sides) for _ in range(count)]

    # Tumble: show a few random faces, redrawing them in place, so it looks
    # like the dice are actually rolling before they settle.
    for frame in range(frames):
        if frame > 0:
            # Move the cursor back up over the 5 lines we just drew so the
            # next frame overwrites them (that's the "\033[5A" escape code).
            print("\033[5A", end="")
        shown = faces if frame == frames - 1 else [roll_fn(sides) for _ in range(count)]
        draw_dice(*shown)
        time.sleep(delay)

    return faces[0] if count == 1 else faces


def banner(text):
    """Print text inside a nice box, like a title card."""
    line = "=" * (len(text) + 4)
    print(line)
    print("| " + text + " |")
    print(line)


def slow_print(text, delay=0.02):
    """Print text one character at a time so it feels like a game."""
    for letter in text:
        print(letter, end="", flush=True)
        time.sleep(delay)
    print()  # move to the next line at the end


def health_bar(name, current, maximum, width=20):
    """Draw a text health bar, e.g.  Hero  [#######-------]  35/50"""
    current = max(0, current)  # never show a negative bar
    filled = int(width * current / maximum)
    bar = "#" * filled + "-" * (width - filled)
    print(f"{name:<10} [{bar}] {current}/{maximum}")
