'''
__main__.py
--------
Wumpus Game Main Module
--------
Theodor Holmberg aka @egeltorp 2025
'''

from io_cli import TextUI
from game import WumpusGame
import random

# PARAMETERS for game session
NUM_ROOMS = 20      # no. of rooms
# PIT_RATE = 0.2    # % of rooms with PITS
# BAT_RATE = 0.3    # % of rooms with BATS
# ARROWS = 5          # starting no. of ARROWS

# seed for random module
SEED = random.randrange(1, 100)

def run_game(ui, game: WumpusGame):
    # SETUP
    game.random_seed()
    game.generate_rooms()
    game.connect_rooms()
    game.place_hazards()
    game.place_player()

    # WELCOME and INTRO
    ui.show_welcome()

    # RUN GAME TURNS UNTIL END
    while not game.is_over():
        game.play_turn(ui)
        game.check_game_state()
    
    # SHOW RESULT AFTER GAME ENDED
    if game.check_game_state() == "win":
        ui.show_result("win")
    if game.check_game_state() == "lose":
        ui.show_result("lose")

def main():
    # Initialize the TextUI interface
    ui = TextUI()

    # Choose difficulty, returns a dict with chosen parameters
    params = ui.choose_difficulty()

    # Create a new instance of the WumpusGame
    game = WumpusGame(
                    **params,
                    rooms = [], 
                    safe_rooms = [],
                    seed = SEED)
    while True:
        # Run the full game loop
        run_game(ui, game)

        # Check if the user wants to play again, if YES: restart loop and run again
        answer = ui.console.input("[bold white]Play again? [[green]Y[/green]/[red]N[/red]]: [/bold white]\n").strip().upper()
        if answer != "Y":
            ui.console.print("[bold red]Goodbye![/bold red]\n")
            break

if __name__ == "__main__":
    main()