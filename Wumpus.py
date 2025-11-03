'''
Wumpus.py
--------
Version: B-grade | Rich | One-file | Nov 3rd 2025
* Choose difficulty
* Wumpus chases on HARD
* One file for all code

The full runnable game, with all three modules merged: 
* __main__.py
* io_cli.py
* game.py

Uses the rich module for text formatting
--------
Theodor Holmberg aka @egeltorp 2025
'''

# --- STANDARD LIBRARY ---
import random
import sys
import time
from collections import deque

# --- RICH --- 
from rich.console import Console
from rich.table import Table
from rich.text import Text
from rich import box
from rich.panel import Panel
from rich.columns import Columns
from rich.align import Align

# ==============================================================
#                           M A I N
# ==============================================================
# Entry point for Hunt the Wumpus
# Handles init, difficulty selection, and main loop
# ==============================================================

# PARAMETERS
SEED = random.randrange(1, 1000)

def run_game(ui, game):
    # SETUP
    game.random_seed()
    game.generate_rooms()
    game.connect_rooms()
    game.place_hazards()
    game.place_player()

    # RUN GAME TURNS UNTIL END
    while not game.is_over(ui):
        game.play_turn(ui)
        game.check_game_state(ui)
    
    # SHOW RESULT AFTER GAME ENDED
    if game.check_game_state(ui) == "win":
        ui.show_result("win")
    if game.check_game_state(ui) == "lose":
        ui.show_result("lose")

# Main function initializing the program
def main():
    # Print version number
    print("\nVersion: B-grade | Rich | One-file | Nov 3rd 2025\n")

    # Initialize the TextUI interface
    ui = TextUI()

    # Show Welcome and Intro-text
    ui.show_welcome()

    while True:
        # Choose difficulty, returns a dict with chosen parameters
        params = ui.choose_difficulty()

        # Create a new instance of the WumpusGame
        game = WumpusGame(**params, seed = SEED)

        # Run the full game loop
        run_game(ui, game)

        # Check if the user wants to play again, if YES: restart loop and run again
        answer = ui.console.input("[bold white]Play again? [[green]Y[/green]/[red]N[/red]]: [/bold white]\n").strip().upper()
        if answer != "Y":
            ui.console.print("[bold red]Goodbye![/bold red]\n")
            break

# ==============================================================
#                        T E X T   U I
# ==============================================================
# Handles console input/output using rich
# Provides menus, messages, status panels, player interaction
# ==============================================================
# Class for TextUI interfaces, input/output
class TextUI:
    def __init__(self):
        self.console = Console()
        
        self.messages = {
            "no_arrows": "You have no arrows left!\n",
            "arrow_miss": "Your arrow missed.\n",
            "wumpus_attack": "[bold red]The Wumpus SLOBBERS on your FLESH![/bold red]\n",
            "wumpus_move": "[italic red]The Wumpus stomps closer![/italic red]\n",
            "wumpus_hit": "The Wumpus has been struck!\n",
            "pit_fall": "[bold blue]You tripped into a bottomless pit like a buffoon...[/bold blue]\n",
            "invalid_direction": "[bold red]Not a valid direction.[/bold red]\n",
            "invalid_action": "[bold red]Not a valid action.[/bold red]\n",
            "suicide": "[bold red]You killed yourself with the arrow.[/bold red]\n"
        }
    
    # User chooses difficulty with input letter [E/N/H]
    def choose_difficulty(self) -> dict:
        # Easy difficulty, easier than standard parameters
        e_dict = {"num_rooms": 15, "pit_rate": 0.1, "bat_rate": 0.2, "starting_arrows": 6, "wumpus_chases": False}
        easy_text = Text.from_markup("Rooms: 15\nPits: 10%\nBats: 20%\nArrows: 6\nWumpus lurks...", justify="center")
        easy_panel = Panel(easy_text, title="[bold green]EASY [E][/bold green]", border_style="green", padding=(1,2))

        # Normal difficulty, standard Assignment parameters
        n_dict = {"num_rooms": 20, "pit_rate": 0.2, "bat_rate": 0.3, "starting_arrows": 5, "wumpus_chases": False}
        normal_text = Text.from_markup("Rooms: 20\nPits: 20%\nBats: 30%\nArrows: 5\nWumpus lurks...", justify="center")
        normal_panel = Panel(normal_text, title="[bold yellow]NORMAL [N][/bold yellow]", border_style="yellow", padding=(1,2))

        # Hard difficulty, very difficult, more rooms, less arrows
        h_dict = {"num_rooms": 30, "pit_rate": 0.25, "bat_rate": 0.35, "starting_arrows": 3, "wumpus_chases": True}
        hard_text = Text.from_markup("Rooms: 30\nPits: 25%\nBats: 35%\nArrows: 3\nWumpus will chase you!", justify="center")
        hard_panel = Panel(hard_text, title="[bold red]HARDOX [H][/bold red]", border_style="red", padding=(1,2))

        # Arrange difficulty panels in a nice 3 column row of panels
        columns = Columns([easy_panel, normal_panel, hard_panel], expand=True)

        # Display columns in one panel
        main_panel = Panel(columns, title="[bold white]DIFFICULTIES[/bold white]", box=box.SIMPLE_HEAD, border_style="white", padding=(1,1))
        self.console.print(main_panel)

        # Ask for difficulty choice
        E = "[bold green]E[/bold green]"
        N = "[bold yellow]N[/bold yellow]"
        H = "[bold red]H[/bold red]"
        while True:
            choice_text = Text.from_markup(f"Choose a difficulty [{E}/{N}/{H}]: ", style="bold white")
            choice = self.console.input(choice_text).strip().upper()
            if choice == "E":
                self.clear_prompt("prompt")
                self.console.print("You chose [bold green]EASY[/bold green]\n")
                return e_dict
            if choice == "N":
                self.clear_prompt("prompt")
                self.console.print("You chose [bold yellow]NORMAL[/bold yellow]\n")
                return n_dict
            if choice == "H":
                self.clear_prompt("prompt")
                self.console.print("You chose [bold red]HARD[/bold red]\n")
                return h_dict
            else:
                self.clear_prompt("prompt")
                self.console.print("[italic red]Not a valid difficulty![/italic red]\n")

    # General method for displaying a text message
    def show_message(self, key: str):
        text = self.messages.get(key)
        text_formatted = Text.from_markup(text)
        self.console.print(f"{text}")

    # Displays "senses" based on sense_environment() in WumpusGame
    def display_senses(self, sense_dict: dict) -> Panel:
        lines = []
        if sense_dict["pit"]:
            lines.append("You feel a [bold blue]cold breeze.[/bold blue]")
        if sense_dict["bats"]:
            lines.append("You hear the [italic]flapping of wings...[/italic]")
        if sense_dict["wumpus"]:
            lines.append("You smell a [bold red]foul stench[/bold red], reminding you of Hardox!")

        if lines == []:
            lines.append("Nothing special...")
        if lines:
            panel = Panel("\n".join(lines), title="[bold yellow]SENSES[/bold yellow]", border_style="yellow")
            return panel
    
    # Displays status of player: current room, no. of arrows, nearby rooms
    def display_status(self, current_room_id: int, arrows: int, nearby_rooms: list) -> Panel:
        lines = []
        room_ids = [r.room_id for r in nearby_rooms]
        rooms_formatted = "  ".join(f"{r:>2}" for r in room_ids)
        directions = "   N   E   S   W" # spaces for formatting under room_ids

        lines.append(f"[bold white]You are in room [magenta]{current_room_id}[/magenta].[/bold white]")
        lines.append(f"You have [bold red]{arrows} arrows[/bold red] left.")
        lines.append(f"Nearby rooms: [bold magenta]{rooms_formatted}[/bold magenta]")
        lines.append(f"Directions: [bold magenta]{directions}[/bold magenta]")

        status_panel = Panel("\n".join(lines), title="[bold magenta]STATUS[/bold magenta]", border_style="magenta")
        return status_panel

    # Asks user for desired action [M]ove or [S]hoot, returns str
    def ask_action(self) -> str:
        input_text = Text.from_markup("> Move or Shoot ([magenta]M[/magenta]/[red]S[/red]): ", style="bold white")
        action = self.console.input(input_text).strip().upper()
        self.clear_prompt("prompt")    
        return action

    # Asks user for desired direction for movement, returns str
    def ask_move_direction(self, room_id: int) -> str:
        self.console.print(f"You are currently in room [bold magenta]{room_id}[/bold magenta].")
        directions = f"[bold magenta][N/E/S/W][/bold magenta]"
        input_text = Text.from_markup(f"> {directions} Direction: ", style="bold white")
        input = str(self.console.input(input_text).upper().strip())
        return input
    
    # Shows a "moving transition" in the terminal based on movement type
    def show_move_transition(self, new_room_id: int, move_or_bat: str):
        # If it's a bat transport: print bat grab message
        if move_or_bat == "bat":
            self.console.print("A [red]bat[/red] grabs you!", end="", style="bold italic white")
            print()

        # Print dots for "movement"
        for _ in range(3):
            time.sleep(0.3)
            print(".", end="")
            print()
        time.sleep(0.3)
        self.console.print(f"You are now in room [bold magenta]{new_room_id}[/bold magenta]\n", style="bold white")
        time.sleep(0.5)

    # Asks user for a desired direction for shooting/steering arrow, returns str
    def ask_shoot_direction(self, iteration: int) -> str:
        directions = f"[bold red][N/E/S/W][/bold red]"
        room_order = {0: "* First shot", 1: "* Curve the shot!", 2: "* Curve it again!"}
        self.console.print(f"{room_order[iteration]}")
        input_text = Text.from_markup(f"> {directions} Direction: ", style="bold white")
        input = str(self.console.input(input_text).upper().strip())
        return input
    
    # Display text for arrow movement
    def shooting_text(self, room_number: int):
        arrow = "[bold red]arrow[/bold red]"
        if room_number == 1:
            self.console.print(f"The {arrow} enters the first room.\n")
        if room_number == 2:
            self.console.print(f"The {arrow} enters the second room.\n")
        if room_number == 3:
            self.console.print(f"The {arrow} enters the third room.\n")
    
    # Shows welcome title and intro text (if desired by user)
    def show_welcome(self):
        # Title panel
        title = Text("WUMPUS", style="bold red on black", justify="center")
        subtitle = Text("*** Beneath Hardox... he looms. ***", style="white on black")
        panel = Panel(
            Align.center(Text.assemble(title, "\n", subtitle)),
            box = box.ASCII,
            border_style="red",
            padding=(1, 4),
            title="[bold bright_red]* * *[/bold bright_red]"
        )
        self.console.print(panel)

        # "Skip intro" prompt
        yes = "[bold green]Y[/bold green]"
        no = "[bold red]N[/bold red]"
        prompt = Text.from_markup(f"> SKIP INTRO? [{yes}/{no}]: ", style="bold white")
        while True:
            skip = self.console.input(prompt).strip().upper()
            if skip == "Y":
                self.clear_prompt("prompt")
                return
            if skip == "N":
                break
            else:
                self.console.print(Text.from_markup(f"[bold red]X[/bold red] Input must be {yes} or {no}\n", style="white"))

        # Intro text lines
        lines = [
            "> You find yourself in the culverts beneath Hardox, where the gluttonous Wumpus resides.",
            "> To avoid being eaten you have to shoot Wumpus with your bow and arrow.",
            "> The culverts are all connected to a number of rooms via cramped tunnels.",
            "> You can move North, East, South, or West from one room to another.",
            "> Here lurks a number of dangers however:",
            "- Some rooms contain BOTTOMLESS PITS, and falling into one means certain death.",
            "- Others contain BATS, which will fly you to a random room of their choosing.",
            "> In one of the rooms... lurks the mighty Wumpus.",
            "> If encountered, he will instantly gobble you up and you WILL die.",
            "> Luckily, via the SENSES DISPLAY you can feel the cold breeze of a pit nearby, or the flapping of wings...",
            "> ...or the stench of Wumpus.",
            "> Via the STATUS BAR you can see: ",
            "- The room you are currently in",
            "- Nearby rooms.",
            "- How many arrows you have left.",
            "X To win the game you have to shoot and kill Wumpus.",
            "X When you shoot an arrow it will move through THREE rooms.",
            "X You can direct the arrow's direction in each room it enters.",
            "X Be careful however! The tunnels wind in unexpected ways...",
            "X You might shoot yourself! Bozo.",
            "X You have FIVE arrows.",
            "> Qapla' and good luck!"
        ]

        # "Animates" each letter during the intro
        for line in lines:
            for char in line:
                print(char, end="")
                sys.stdout.flush()
                time.sleep(0.03)
            print()
            time.sleep(0.5)

    # Displays the result of the game after game is over
    def show_result(self, result: str):
        # Show win result
        if result == "win":
            time.sleep(1)
            print(".")
            time.sleep(1)
            print(".")
            time.sleep(1)
            print(".")
            win_text = Text.from_markup("[bold green]Huzzah! The ol' Wumpus has been executed by a swift arrow! You win![/bold green]")
            self.console.print(Panel(win_text, expand=False, border_style="green"))
        
        # Show loss result
        elif result == "lose":
            time.sleep(1)
            self.console.print("[bold red]Ouch! You met a grim and quite frankly embarassing fate. Better luck next time bozo![/bold red]")

    # Takes senses_panel and status_panel with actions_panel and arranges them into three columns 
    def show_panels(self, senses_panel: Panel, status_panel: Panel):
        # Actions panel
        actions_panel_content = (
            "[bold white]What do you want to do?[/bold white]\n"
            "\n"
            "[bold magenta][M][/bold magenta] Move\n"
            "[bold red][S][/bold red] Shoot an arrow"
        )
        actions_panel = Panel(actions_panel_content, expand=False, title="[bold white]ACTION[/bold white]", border_style="white",)

        # Print all three panels in three columns
        self.console.print(Columns([actions_panel, status_panel, senses_panel], equal=True))

    # General method for clearing a user prompt question, makes terminal cleaner
    def clear_prompt(self, to_clear: str):
        if to_clear == "prompt":
            sys.stdout.write("\033[F")
            sys.stdout.write("\033[K")
            sys.stdout.flush()

# ==============================================================
#                         G A M E   L O G I C
# ==============================================================
# Core mechanics for the Wumpus Game
# Manages rooms, hazards, movement, encounters, and turns
# ==============================================================

# Class for each Room object in the game
class Room:
    def __init__(self, room_id: int):
        self.room_id = room_id
        self.connected_rooms = []
        self.has_pit = False
        self.has_bats = False
        self.has_wumpus = False

# Class for the player
class Player:
    def __init__(self, starting_room: Room, starting_arrows: int):
        self.current_room = starting_room
        self.arrows = starting_arrows
        self.is_alive = True

# Class for the WumpusGame object and all game logic methods
class WumpusGame:
    def __init__(self, 
                 num_rooms: int = 16, 
                 pit_rate: float = 0.2, 
                 bat_rate: float = 0.3,
                 starting_arrows: int = 5,
                 wumpus_chases: bool = False,
                 seed: int = 1701):
        self.num_rooms = num_rooms
        self.pit_rate = pit_rate
        self.bat_rate = bat_rate
        self.starting_arrows = starting_arrows
        self.wumpus_chases = wumpus_chases
        self.seed = seed
        self.rooms = []
        self.safe_rooms = []
        self.state = "running"
        self.wumpus_room: Room = None

    # Assigns a seed for the random module for reproducability
    def random_seed(self):
        random.seed(self.seed)

    # Generates a list of rooms based on self.num_rooms
    def generate_rooms(self):
        self.rooms = [Room(i) for i in range(self.num_rooms)]

    # Connects all rooms to each other in both ways
    def connect_rooms(self):
        number_of_connections = 4   # each room needs 4 connections
        safety_limit = 500          # loop safety limit to stop infinite looping

        # Run this code for each room in self.rooms
        for room in self.rooms:
            attempts = 0

            # While the room needs further connections and attempts < safety limit
            while len(room.connected_rooms) < number_of_connections and attempts < safety_limit:
                attempts += 1
                target_room = random.choice(self.rooms)

                # Check if the target room can be connected
                if (
                    target_room != room 
                    and target_room not in room.connected_rooms 
                    and len(target_room.connected_rooms) < number_of_connections
                    ):
                    
                    # Create a two-way connection
                    room.connected_rooms.append(target_room)
                    target_room.connected_rooms.append(room)

    # Places hazards in the appropriate number of rooms
    def place_hazards(self):
        # Determine number of rooms with pits and bats
        number_of_pits = int(self.num_rooms * self.pit_rate)
        number_of_bats = int(self.num_rooms * self.bat_rate)

        # Place pits in pit rooms using preselected rooms
        pit_rooms = random.sample(self.rooms, number_of_pits)
        for room in pit_rooms:
            room.has_pit = True

        # Place bats in bat rooms making sure pit rooms are ignored
        empty_rooms = [room for room in self.rooms if not room.has_pit]
        bat_rooms = random.sample(empty_rooms, number_of_bats)
        for room in bat_rooms:
            room.has_bats = True

        # Place Wumpus in a random empty room
        empty_room = [room for room in self.rooms if not room.has_pit and not room.has_bats]
        self.wumpus_room = random.choice(empty_room)
        self.wumpus_room.has_wumpus = True

        # Store safe rooms
        self.safe_rooms = [room for room in self.rooms if not room.has_pit and not room.has_bats and not room.has_wumpus]

    # Wumpus movement logic, uses helper method for pathfinding and moves Wumpus closer to player
    def wumpus_chase(self, ui: TextUI):
        # If wumpus_chases is true: get closeer to player each turn
        if self.wumpus_chases == True:
            self.wumpus_room.has_wumpus = False # Remove old has_wumpus flag
            start = self.wumpus_room
            goal = self.player.current_room

            # If the Wumpus is already in the same room: return
            if start == goal:
                self.wumpus_room.has_wumpus = True
                return
            
            # Find the shortest path to the player from start --> goal, using helper method
            path = self.find_path(start, goal)

            # Move Wumpus one step closer to player
            if len(path) > 1:
                self.wumpus_room = path[1]
                ui.show_message("wumpus_move")
                # DEBUG: print(f"Wumpus MOVED to ROOM {self.wumpus_room.room_id}")
            else:
                # If no path exists, just move randomly
                self.wumpus_room = random.choice(self.safe_rooms)
                ui.show_message("wumpus_move")
                # DEBUG: print(f"Wumpus MOVED (randomly) to ROOM {self.wumpus_room.room_id}")

            # Set new flag for room with Wumpus
            self.wumpus_room.has_wumpus = True

            # Update list of safe rooms
            self.safe_rooms = [room for room in self.rooms if not room.has_pit and not room.has_bats and not room.has_wumpus]

    # Helper method for pathfinding through the lists, returns a path: list
    def find_path(self, start: Room, goal: Room) -> list:
        # Each element in the queue is a path (list of rooms)
        queue = deque([[start]])
        visited = {start}

        while queue:
            path = queue.popleft()
            room = path[-1]

            # If target room reached --> return path
            if room == goal:
                return path
            
            # Explore all unvisited nearby rooms
            for nearby in room.connected_rooms:
                if nearby not in visited:
                    visited.add(nearby)
                    queue.append(path + [nearby])

    # Places the player in a safe room and creates a Player instance in WumpusGame class
    def place_player(self):
        spawn_room = random.choice(self.safe_rooms)
        self.player = Player(spawn_room, self.starting_arrows)

    # Creates a dictionary based on hazards in Player's nearby rooms
    def sense_environment(self) -> dict:
        # Dictionary for storing sensed hazards
        sense_dict = {"pit": False, "bats": False, "wumpus": False}

        # Checking nearby rooms for hazards
        for nearby_room in self.player.current_room.connected_rooms:
            if nearby_room.has_pit:
                sense_dict["pit"] = True
            if nearby_room.has_bats:
                sense_dict["bats"] = True
            if nearby_room.has_wumpus:
                sense_dict["wumpus"] = True

        return sense_dict
    
    # Logic for moving the player, using ui.ask_move_direction for desired direction
    def move_player(self, ui: TextUI):
        direction_to_index = {"N": 0, "E": 1, "S": 2, "W": 3} # dict for dir -> int
        connected_rooms = self.player.current_room.connected_rooms

        while True:
            direction = ui.ask_move_direction(self.player.current_room.room_id) # returns N,E,S,W string
            if direction in direction_to_index:
                target_room_obj = connected_rooms[direction_to_index[direction]]
                self.player.current_room = target_room_obj
                ui.show_move_transition(self.player.current_room.room_id, "move") # show moving animation
                return
            else:
                ui.show_message("invalid_direction")

    # Checks if player has entered a room with a pit
    def check_pit_kill(self, ui: TextUI):
        if self.player.current_room.has_pit:
            ui.show_message("pit_fall")
            self.player.is_alive = False

    # Checks if player has entered a room with bats, transports player
    def check_bats_transport(self, ui) -> bool:
        if self.player.current_room.has_bats:
            possible_rooms = [room for room in self.safe_rooms if room != self.player.current_room]
            self.player.current_room = random.choice(possible_rooms)
            ui.show_move_transition(self.player.current_room.room_id, "bat")
    
    # Checks for player encounter with Wumpus, changes alive-status of Player instance
    def check_wumpus_encounter(self, ui: TextUI):
        if self.player.current_room.has_wumpus:
            ui.show_message("wumpus_attack")
            self.player.is_alive = False

    # Logic fo shooting and steering arrows
    def shoot_arrow(self, ui: TextUI):
        direction_to_index = {"N": 0, "E": 1, "S": 2, "W": 3} # dict for dir -> int

        # Early escape if no more arrows
        if self.player.arrows <= 0:
            ui.show_message("no_arrows")
            return
        
        # Decrement no. of arrows available
        self.player.arrows -= 1

        # Run this code three times, once for each direction choice / steering
        for i in range(0, 3):
            current_arrow_room = self.player.current_room
            while True:
                connected_rooms = self.player.current_room.connected_rooms
                direction = ui.ask_shoot_direction(i) # returns N,E,S,W string
                if direction in direction_to_index:
                    current_arrow_room = connected_rooms[direction_to_index[direction]]
                    break
                else:
                    ui.show_message("invalid_direction")
            ui.shooting_text(i + 1)

            # If arrow "hits" Wumpus
            if current_arrow_room.has_wumpus:
                current_arrow_room.has_wumpus = False
                return
            
            # If arrow "hits" player
            if current_arrow_room.room_id == self.player.current_room.room_id:
                ui.show_message("suicide")
                self.player.is_alive = False
                return
        ui.show_message("arrow_miss")

    # Checks game status based on Wumpus existance or Player alive/arrows status
    def check_game_state(self, ui: TextUI) -> str:
        # If player is dead or has no arrows left, they lose
        if not self.player.is_alive:
            return "lose"
        elif self.player.arrows <= 0:
            ui.show_message("no_arrows")
            return "lose"
        
        # If Wumpus is dead, player wins
        if not any(room.has_wumpus for room in self.rooms):
            return "win"
        
        # Otherwise, game continues
        return "running"
    
    # Method for ending game in run_game() function
    def is_over(self, ui) -> bool:
        state = self.check_game_state(ui)
        if state == "lose":
            return True
        elif state == "win":
            return True
        elif state == "running":
            return False

    # Main method for playing a full turn of the game
    def play_turn(self, ui: TextUI):
        # ui.console.clear()
        senses = ui.display_senses(self.sense_environment())
        status = ui.display_status(self.player.current_room.room_id, 
                                     self.player.arrows, 
                                     self.player.current_room.connected_rooms) 
        ui.show_panels(senses, status)

        # Loop for choosing a player action
        while True:
            action = ui.ask_action()
            if action in ("M", "S"):
                break
            else:
                ui.show_message("invalid_action")

        # Move or Shoot
        if action == "M":
            self.move_player(ui)
        if action == "S":
            self.shoot_arrow(ui)

        # Move Wumpus and check for deaths
        self.check_pit_kill(ui)
        if self.player.is_alive == False:
            return
        self.check_bats_transport(ui)
        self.wumpus_chase(ui)
        self.check_wumpus_encounter(ui)

# Runs the game if program is run NOT as an imported module
if __name__ == "__main__":
    main()