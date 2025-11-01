'''
__main__.py
--------
Wumpus Game Main Module
--------
Theodor Holmberg aka @egeltorp 2025
'''

from io_cli import TextUI
# from io_gui import GUI
from game import WumpusGame
import time

# PARAMETERS
NUM_ROOMS = 40  # no. of rooms
PIT_RATE = 0.2  # % of rooms with PITS
BAT_RATE = 0.3  # % of rooms with BATS
ARROWS = 5      # starting no. of ARROWS
SEED = 1701     # seed for random module

def run_game(ui, game: WumpusGame):
    # SETUP
    game.random_seed()
    game.generate_rooms()
    game.connect_rooms()
    game.place_hazards()
    game.place_player()

    ui.show_welcome()

    while not game.is_over():
        game.play_turn(ui)
        game.check_game_state()
    
    if game.check_game_state() == "win":
        ui.show_result("win")
    if game.check_game_state() == "lose":
        ui.show_result("lose")

def main():
    # UI for CLI
    ui = TextUI()

    # UI for GUI
    # ui = GUI()

    game = WumpusGame(num_rooms = NUM_ROOMS,
                    pit_rate = PIT_RATE, 
                    bat_rate = BAT_RATE, 
                    starting_arrows = ARROWS,
                    rooms = [], 
                    safe_rooms = [],
                    seed = SEED)
    run_game(ui, game)

if __name__ == "__main__":
    main()