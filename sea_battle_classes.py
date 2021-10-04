# -------------------------------------------------------------------
#                              Sea Battle
#
#                             Game Classes
# -------------------------------------------------------------------

import sys
import random

# import definitions

import sea_battle_definitions
from sea_battle_definitions import size
from sea_battle_definitions import gamer_code       # gamer code
from sea_battle_definitions import result_code      # result code

# import interface

from sea_battle_interface import say_greeting       # greeting
from sea_battle_interface import say_game_start     # game is started
from sea_battle_interface import say_good_by        # good by
from sea_battle_interface import game_is_over       # is the game to be continued?
from sea_battle_interface import draw_boards        # draw boards
from sea_battle_interface import get_coordinates    # get_coordinates

from sea_battle_interface import show_target        # show machine code    
from sea_battle_interface import show_result        # show shot result    


# import definitions

import sea_battle_definitions
from sea_battle_definitions import size
from sea_battle_definitions import gamer_code       # gamer code
from sea_battle_definitions import result_code      # result code

# -------------------------------------------------------------------

def in_field(c, size):
    if c[0] < 0 or c[0] > size - 1: return False
    if c[1] < 0 or c[1] > size - 1: return False
    return True
# -------------------------------------------------------------------
#                              Class Cell
# -------------------------------------------------------------------


class Cell():                       # cell

    def __init__(self):             # constructor
        self.hit = False            # not hit now
        self.shaded = False         # nor shaded now
        self.occupied = False       # free cell

# -------------------------------------------------------------------
#                                Class Ship
#--------------------------------------------------------------------

horizontal = 0                      # ship position
vertical = 1


class ShipCreationError(Exception): # ship creation error
    def __init__(self): pass


class Ship():                               # ship

    def good_location(self, f):             # check location
        for c in self.body + self.contour:  # body and contour should be free
            row = c[0]
            col = c[1]
            if f[row][col].occupied: return False
        return True

    def locate(self, i, j):                 # build a frame for a ship

        self.body = []                      # build the body
        for n in range(self.ndecks):
            if self.direction == horizontal:
                self.body.append((i, j + n))
            if self.direction == vertical:
                self.body.append((i + n, j))

        self.contour = []                   # build the contour
        for n in range(self.ndecks):
            if self.direction == horizontal:
                c1 = (i - 1, j + n)
                c2 = (i + 1, j + n)
            if self.direction == vertical:
                c1 = (i + n, j - 1)
                c2 = (i + n, j + 1)
            if in_field(c1, size): self.contour.append(c1)
            if in_field(c2, size): self.contour.append(c2)

        for n in range(3):
            if self.direction == horizontal:
                c1 = (i - 1 + n, j - 1)
                c2 = (i - 1 + n, j + self.ndecks)
            if self.direction == vertical:
                c1 = (i - 1, j - 1 + n)
                c2 = (i + self.ndecks, j - 1 + n)
            if in_field(c1, size): self.contour.append(c1)
            if in_field(c2, size): self.contour.append(c2)

    def __init__(self, f, nd):  # Ship constructor

        self.ndecks = nd        # number of decks
        self.lives = nd
        self.body = []          # ship body
        self.contour = []       # ship contour

        variants = []  # list of placement variants

        self.direction = horizontal  # try horizontal position
        for i in range(size):
            for j in range(6 - self.ndecks):
                self.locate(i, j)
                if self.good_location(f):
                    variants.append((self.direction, i, j))

        self.direction = vertical  # try vertical position
        for j in range(size):
            for i in range(size - self.ndecks):
                self.locate(i, j)
                if self.good_location(f):
                    variants.append((self.direction, i, j))

        if len(variants) == 0: raise ShipCreationError()

        chosen = random.choice(variants)  # choose some variant
        self.direction = chosen[0]
        row = chosen[1]
        col = chosen[2]

        self.locate(row, col)   # build the ship

        for c in self.body:     # place the ship in the field
            row = c[0]
            col = c[1]
            cell = f[row][col]
            cell.occupied = True

# -------------------------------------------------------------------
#                             Class Board
# -------------------------------------------------------------------

class Board():                              # playing board

    def add_ship(self, ship):               # add a new ship
        self.nships += 1
        self.fleet.append(ship)

    def create_fleet(self):                 # new placement

        self.field = []                     # build the playing field
        for i in range(size):
            line = []
            for j in range(size):
                c = Cell()
                line.append(c)
            self.field.append(line)

        self.nships = 0                     # no ships now

        try:
            ship = Ship(self.field, 3)                      # one battleship
            if ship is not None: self.add_ship(ship)

            for n in range(2):                              # two cruisers
                 ship = Ship(self.field, 2)
                 if ship is not None: self.add_ship(ship)

            for n in range(4):                              # four destroyers
                ship = Ship(self.field, 1)
                if ship is not None: self.add_ship(ship)

        except ShipCreationError as e:
            self.fleet = []

    def __init__(self, code):                               # Board constructor

        self.code = code
        if(code == gamer_code["man"]):                      # man's board is not hidden
            self.hidden = False
        if(code == gamer_code["machine"]):                  # machine's board is hidden
            self.hidden = True
 
        self.fleet = []                                     # no fleet now
        while self.fleet == []:                             # create the fleet
            self.create_fleet()

  
    def shot(self, target):                                 # shot
        row = target[0]
        col = target[1]
        self.field[row][col].hit = True                     # the cell is hit
        for ship in self.fleet:                             # check the fleet ships
            for c in ship.body:
                if c == target:                             # the shot hit the ship
                    ship.lives -= 1                         # one less live
                    if not ship.lives == 0:                 # is it wounded?
                        return result_code["wounded"]       # it is wounded
                    else:  # is it killed?
                        self.nships -= 1                    # one less ship
                        if self.nships == 0:                # no more ships?
                            return result_code["defeat"]    # defeat
                        else:                               # not the last ship
                            return result_code["killed"]    # but it is killed

        return result_code["miss"]                          # miss

# -------------------------------------------------------------------
#                                 Class Gamer
# -------------------------------------------------------------------

class Gamer():

    def __init__(self, ownboard, oppboard):

        self.target = None
        self.ownboard = ownboard                    # own board
        self.oppboard = oppboard                    # opponent board


    def get_target(self):   pass                    # get target


    def get_ship(self, c):                          # find the ship I hit
        for ship in self.oppboard.fleet:
            if c in ship.body: return ship

    def shot(self):
        self.target = self.get_target()                 # get target
        result = self.oppboard.shot(self.target)        # shoot at the opponent's board
        if result == result_code["killed"]:             # is it killed?
            killed_ship = self.get_ship(self.target)    # find the killed ship
            for c in killed_ship.contour:               # outline the contour
                row = c[0]
                col = c[1]
                self.oppboard.field[row][col].shaded = True

        show_result(self.code, result)                  # show result
        return result

 # -------------------------------------------------------------------
#                                 Class Man
# -------------------------------------------------------------------

class Man(Gamer):                                   # man as a gamer

    def __init__(self, ownboard, oppboard):         # man is a gamer
        Gamer.__init__(self, ownboard, oppboard)
        self.code = gamer_code["machine"]

    def get_target(self):                           # get man's target
        return get_coordinates(self.oppboard)       # get coordinates

 

# -------------------------------------------------------------------
#                                 Class Machine
# -------------------------------------------------------------------


class Machine(Gamer):                           # machine is a gamer   
    
    def __init__(self, ownboard, oppboard):        
        Gamer.__init__(self, ownboard, oppboard)
        self.code = gamer_code["man"]
  
        self.not_tried = []                     # not tried
        for i in range(size):
            for j in range(size): self.not_tried.append((i, j))

    def get_target(self):                       # get machine's target
        target = random.choice(self.not_tried)  # choose a random target
        self.not_tried.remove(target)           # now it is used
        show_target(target)                     # show target
        return target


    def get_ship(self, c):                      # find the ship I hit
        for ship in self.oppboard.fleet:
            if c in ship.body: return ship


    def shot(self):                             # machine's shot                   
        result = Gamer.shot(self)
        return result

# -------------------------------------------------------------------
#                                 Class Game
# -------------------------------------------------------------------

class Game():                                       # Game

    def __init__(self):
        self.man_board = Board(gamer_code["man"])           # man's board
        self.machine_board = Board(gamer_code["machine"])   # machine board

        self.man = Man(self.man_board, self.machine_board)          # man is a gamer
        self.machine = Machine(self.machine_board, self.man_board)  # machine is a gamer


    def move(self, gamer):
        while True:
            result =gamer.shot()                                # gamer's shot
            if result == result_code["defeat"]:                 # check result
                self.machine_board.hidden = False
                draw_boards(self.machine_board, self.man_board)
                return result
            draw_boards(self.machine_board, self.man_board)
            if result == result_code["miss"]: return result


    def start(self):                                            # start the game
        say_game_start()                                        # game is started    
        draw_boards(self.machine_board, self.man_board)         # draw boards
        while True:
            result = self.move(self.man)                        # man's move
            if result == result_code["defeat"]:return           # check result
            result = self.move(self.machine)                    # machine's move
            if result == result_code["defeat"]:return           # check result           

 # -------------------------------------------------------------------









