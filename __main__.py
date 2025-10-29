# __main__.py
# Theodor Holmberg 2025

from io_cli import TextUI
from game import WumpusGame

# PARAMETERS
NUM_ROOMS = 16
PIT_RATE = 0.2
BAT_RATE = 0.3
ARROWS = 5
SEED = 1701

def run_game(ui: TextUI):
    game = WumpusGame(num_rooms = NUM_ROOMS,
                       pit_rate = PIT_RATE, 
                       bat_rate = BAT_RATE, 
                       arrows = ARROWS,
                       seed = SEED)
    
    # SETUP
    game.generate_rooms()
    game.connect_rooms()
    game.place_hazards()
    game.place_player()

    # INTRO
    # intro text

    # CORE LOOP
    while not game.is_over():
        # display status
        # get action
        # do action
        # something like that
        pass

    # WIN
    # ui.display_win()

def main():
    ui = TextUI()
    run_game(ui)

if __name__ == "__main__":
    main()