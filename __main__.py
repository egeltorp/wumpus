'''
__main__.py
--------
Wumpus Game Main Module
--------
Theodor Holmberg aka @egeltorp 2025
'''

from io_cli import TextUI
from game import WumpusGame

# PARAMETERS
NUM_ROOMS = 16
PIT_RATE = 0.2
BAT_RATE = 0.3
ARROWS = 5
SEED = 1701

def run_game_cli(ui: TextUI, game: WumpusGame):
    # SETUP
    game.random_seed()
    game.generate_rooms()
    game.connect_rooms()
    game.place_hazards()
    game.place_player()

    ui.show_welcome()

    while not game.is_over():
        print("Starting turn")
        game.play_turn(ui)
        game.check_game_state()
    
    if game.check_game_state() == "win":
        ui.show_result("win")
    if game.check_game_state() == "lose":
        ui.show_result("lose")

def main():
    ui = TextUI()
    game = WumpusGame(num_rooms = NUM_ROOMS,
                    pit_rate = PIT_RATE, 
                    bat_rate = BAT_RATE, 
                    starting_arrows = ARROWS,
                    rooms = [], 
                    safe_rooms = [],
                    seed = SEED)
    run_game_cli(ui, game)

if __name__ == "__main__":
    main()