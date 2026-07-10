# This file is what turns the "game" FOLDER into an importable PACKAGE.
#
# Because this file exists, Python lets you write things like:
#     from game import dice
#     from game.combat import fight
# from any file that sits next to the "game" folder (like main.py).
#
# It can be empty! Its mere existence is the important part.
# But we can also use it to make imports shorter. The line below means
# other code can do `from game import roll` instead of `from game.dice import roll`.

from game.dice import roll  # noqa: F401  (re-export for convenience)
