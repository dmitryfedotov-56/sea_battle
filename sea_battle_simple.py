# -------------------------------------------------------------------
#                              Sea Battle
#              
#            The Man-machine game, machine makes random shots
#
# -------------------------------------------------------------------

import sys


import sea_battle_interface
from sea_battle_interface import say_greeting
from sea_battle_interface import game_is_over
from sea_battle_interface import draw_boards

from sea_battle_classes import Game

# -------------------------------------------------------------------


say_greeting()
while True:
    game = Game()
    game.start()
    if game_is_over():sys.exit(0)
