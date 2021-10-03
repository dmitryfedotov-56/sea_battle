# -------------------------------------------------------------------
#                              Sea Battle
#              
#            The Man-machine game, machine follows the optimal strategy
#
# -------------------------------------------------------------------

import sys
import random

import sea_battle_definitions
from sea_battle_definitions import size
from sea_battle_definitions import gamer_code       # gamer code
from sea_battle_definitions import result_code      # result code

import sea_battle_interface
from sea_battle_interface import say_greeting
from sea_battle_interface import game_is_over
from sea_battle_interface import show_target
from sea_battle_interface import draw_board



from sea_battle_classes import Game
from sea_battle_classes import Gamer
from sea_battle_classes import Machine
from sea_battle_classes import in_field

# -------------------------------------------------------------------
#                              IntelligentMachine
# -------------------------------------------------------------------

class IntelligentMachine(Machine):                      # IntelligentMachine

    def __init__(self, ownboard, oppboard):
        Machine.__init__(self, ownboard, oppboard)
        self.last = None                                # last shot
        self.hits = []                                  # no hits now
        self.cell_to_try = []                           # no cells to try


    def add_cell_to_try(self, c):                       # add a cell to try
        if not in_field(c, size): return                # it should be in field
        if not c in self.not_tried: return              # it should be not hit
        for ship in self.oppboard.fleet:                # it should be not in the contour
            if ship.lives == 0:                         # of a killed ship
                if c in ship.contour: return
        self.cell_to_try.append(c)                      # add to the list


    def get_ship(self, c):                              # find the ship I hit
        for ship in self.oppboard.fleet:
            if c in ship.body: return ship
  
#    def show_variants(self):
#        s = "варианты : "
#        for c in self.cell_to_try: s += str((c[0]+1,c[1]+1))
#        print(s)  


    def get_target(self):                               # get machine's target
        if self.cell_to_try != []:                      # does it have any variants?
#           self.show_variants()
            target = random.choice(self.cell_to_try)    # choose one of them
            self.cell_to_try.remove(target)
        else:                                           # no variants?
            target = random.choice(self.not_tried)      # choose a random target

        self.not_tried.remove(target)                   # now it is used
        self.last = target                              # remember the target
        show_target(target)                             # show target
        return target


    def shot(self):
        result = Gamer.shot(self)                       # gamer's shot
        draw_board(self.oppboard)                       # show opponent board

        if result == result_code["killed"]:             # is it killed?
            self.hits = []                              # no hits
            self.cell_to_try = []                       # no cells to try
            killed_ship = self.get_ship(self.last)      # this ship was killed
            for c in killed_ship.contour:               # remove from not_tried
                if c in self.not_tried:                 # all the cells 
                    self.not_tried.remove(c)            # of killed ship contour

        if result == result_code["wounded"]:            # is it wounded?
            if self.hits == []:
                self.hits.append(self.last)             # only one hit
                row = self.last[0]
                col = self.last[1]
                self.cell_to_try = []                   # add neighboring cells
                self.add_cell_to_try((row, col - 1))
                self.add_cell_to_try((row - 1, col))
                self.add_cell_to_try((row, col + 1))
                self.add_cell_to_try((row + 1, col))

#               self.show_variants()
                return result  

            if len(self.hits) == 1:                     # two hits
                self.hits.append(self.last)

                if self.hits[0][0] == self.hits[1][0]:  # horizontal position
                    self.cell_to_try = []
                    row = self.hits[0][0]
                    col = self.hits[0][1]
                    self.add_cell_to_try((row, col - 1))
                    col = self.hits[1][1]
                    self.add_cell_to_try((row, col + 1))

                if self.hits[0][1] == self.hits[1][1]:  # vertical position
                    self.cell_to_try = []
                    col = self.hits[0][1]
                    row = self.hits[0][0]
                    self.add_cell_to_try((col, row - 1))
                    row = self.hits[1][0]
                    self.add_cell_to_try((col, row + 1))
                
#               self.show_variants()
                return result  
        
        return result # in any case return result

# -------------------------------------------------------------------
#                            Class IntelligentGame
# -------------------------------------------------------------------

class IntelligentGame(Game):    # intelligent machine game

    def __init__(self):
        Game.__init__(self)
        self.machine = IntelligentMachine(self.machine_board, self.man_board)   

# -------------------------------------------------------------------

say_greeting()
while True:
    game = IntelligentGame()
    game.start()
    if game_is_over():sys.exit(0)






