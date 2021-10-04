# -------------------------------------------------------------------
#                              Sea Battle Interface
# -------------------------------------------------------------------

import sys

import sea_battle_definitions
from sea_battle_definitions import size         # board size
from sea_battle_definitions import gamer_code   # gamer code
from sea_battle_definitions import result_code  # shot result code

# -------------------------------------------------------------------

def say_greeting(): print("Привет! Сыграем в морской бой?")


def say_game_start():print("Если надоест, скажи волшебное слово end, и игра закончится")


def say_good_by(): print("До свидания!")


def game_is_over():    
    s = input("Сыграем еще? Скажи yes : ")
    if s == "yes":
        return False    # the game is on again!
    else:
        say_good_by()
        return True
# ---------------------------- draw board ---------------------------


hit_sign = 'X'      # ship cell is hit
ship_sign = '■'     # ship cell
shadow_sign = '.'   # cell is in the ship contour
miss_sign = 'T'     # missed shot


def draw_boards(machine_board, man_board):
    
    def appearance(cell, hidden):                   # cell appearance
        if cell.occupied:                           # if the cell is occupied   
            if cell.hit:                            # if it is hit
                return " " + hit_sign               # hit sign
            else:                                   # if it is not hit
                if hidden:                          # if the board i hidden
                    return "  "                     # nothing
                else:                               # if it is not 
                    return " " + ship_sign          # ship sign
        else:                                       # if the cell is not occupied
            if cell.hit: return " " + miss_sign     # and it is hit, miss sign
            else: 
                if cell.shaded: return " "+ shadow_sign
          
        return "  "                                 # nothing in other cases

    print(" -------------------------------")
    print("   Moи корабли |   Твои корабли |")
    print("   1 2 3 4 5 6 |   1 2 3 4 5 6  |")
    for i in range(size):
        s = " "
        s += str(i+1)
        line = machine_board.field[i]
        for cell in line: s += appearance(cell, machine_board.hidden)
        s += " | "
        s += str(i+1)
        line = man_board.field[i]
        for cell in line: s += appearance(cell, False) 
        s += "  |"
        print(s)
    print(" -------------------------------")

# ------------------------ get coordinates --------------------------


def get_coordinates(board):             # get target coordinaes

    def get_line(s):  # get line, if it is "end" terminate process
        line = input(s)
        if line == "end":
            say_good_by()
            sys.exit(0)
        return line


    def get_num(board, s):  # get number, it should be between 1 and board.size
        while True:
            line = get_line(s)
            try:
                numb = int(line)
                if numb in range(1, size + 1):
                    return numb
                else:
                    print("это плохой номер, попробуй еще раз")
            except:
                print("это не номер, попробуй еще раз")

    print("Стреляй!")
    while True:
        row = get_num(board, "cтрока  : ")      # get row
        col = get_num(board, "столбец : ")      # get column
        row -= 1
        col -= 1
        if not board.field[row][col].hit: 
            print("")
            return (row, col)
        print("ты туда уже стрелял, попробуй еще!")

# ---------------------------- show result --------------------------


def show_target(target): 
    row = target[0] + 1
    col = target[1] + 1
    print(f"Стреляю в {(row, col)}!") 


def show_result(code, result):
    if code == gamer_code["machine"]:
        if result == result_code["miss"]:      print("Ты промахнулся")
        if result == result_code["wounded"]:   print("Ты попал!")
        if result == result_code["killed"]:    print("Ты потопил мой корабль!")
        if result == result_code["defeat"]:    print("Ты победил, поздравляю!")

    if code == gamer_code["man"]:
        if result == result_code["miss"]:      print("Я промахнулся")
        if result == result_code["wounded"]:   print("Я попал!")
        if result == result_code["killed"]:    print("Я потопил твой корабль!")
        if result == result_code["defeat"]:    print("Ура! Я победил")

# -------------------------------------------------------------------


