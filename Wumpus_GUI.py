'''
Wumpus.py
--------
Version: Legacy UI | B-grade | Print | One-file | Nov 4th 2025
* Choose difficulty
* Wumpus chases on HARD
* One file for all code
--------
Theodor Holmberg aka @egeltorp 2025
'''

# --- STANDARD LIBRARY ---
import random
import sys
import time
from collections import deque

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
    print("\nVersion: Legacy | B-grade | Print | One-file | Nov 3rd 2025\n")

    # Initialize the GUI interface
    ui = GUI()

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
        answer = input("> Play again? [Y/N]: \n").strip().upper()
        if answer != "Y":
            print("Goodbye!\n")
            break

# ==============================================================
#                             G U I
# ==============================================================
# Handles player input/output, uses tkinter for UI
# Provides menus, messages, status, player interaction
# ==============================================================
# Class for GUI interfaces, input/output
class GUI:
    def __init__(self):
        self.messages = {
            "no_arrows": "You have no arrows left!\n",
            "arrow_miss": "Your arrow missed.\n",
            "wumpus_attack": "The Wumpus slobbers on your flesh!\n",
            "wumpus_move": "The Wumpus stomps CLOSER!\n",
            "wumpus_hit": "The Wumpus has been STRUCK!\n",
            "pit_fall": "You tripped into a bottomless PIT like a buffoon...\n",
            "invalid_direction": "NOT a valid direction.\n",
            "invalid_action": "NOT a valid action.\n",
            "suicide": "You KILLED YOURSELF with the arrow.\n",
            "pit": "You feel a cold breeze.",
            "bats": "You hear the flapping of wings...",
            "stench": "You smell a FOUL STENCH, reminding you of Hardox!",
            "death": "Ouch! You met a grim and quite frankly embarassing fate. Better luck next time bozo!",
            "easy": "You chose EASY",
            "normal": "You chose NORMAL",
            "hard": "You chose HARD",
        }

    # Displays the difficulty levels in neat columns
    def display_difficulties(self):
        easy = """- EASY -
Rooms: 15
Pits: 10%
Bats: 20%
Arrows: 6
Wumpus lurks...
"""

        normal = """- NORMAL -
Rooms: 20
Pits: 20%
Bats: 35%
Arrows: 5
Wumpus lurks...
"""

        hard = """- HARD -
Rooms: 30
Pits: 25%
Bats: 35%
Arrows: 3
Wumpus will CHASE you!
"""

        # Split each difficulty into lines and pad nicely
        col1 = easy.strip().splitlines()
        col2 = normal.strip().splitlines()
        col3 = hard.strip().splitlines()

        # Calc max no. of lines and pad
        max_lines = max(len(col1), len(col2), len(col3))
        col1 += [""] * (max_lines - len(col1))
        col2 += [""] * (max_lines - len(col2))
        col3 += [""] * (max_lines - len(col3))
        padding = 6

        # Print columns (using no rich module!! Impressive right...?)
        for a, b, c in zip(col1, col2, col3):
            print(f"{a:<20}{' ' * padding}{b:<20}{' ' * padding}{c:<20}")

    # User chooses difficulty with input letter [E/N/H]
    def choose_difficulty(self) -> dict:
        # Display all difficulty levels
        self.display_difficulties()

        # Easy difficulty, easier than standard parameters
        easy_dict = {"num_rooms": 15, "pit_rate": 0.1, "bat_rate": 0.2, "starting_arrows": 6, "wumpus_chases": False}

        # Normal difficulty, standard Assignment parameters
        normal_dict = {"num_rooms": 20, "pit_rate": 0.2, "bat_rate": 0.3, "starting_arrows": 5, "wumpus_chases": False}

        # Hard difficulty, very difficult, more rooms, less arrows
        hard_dict = {"num_rooms": 30, "pit_rate": 0.25, "bat_rate": 0.35, "starting_arrows": 3, "wumpus_chases": True}
        

        # Ask for difficulty choice
        while True:
            choice_text = "\n> Choose a difficulty [E/N/H]: "
            choice = str(input(choice_text).strip().upper())
            if choice == "E":
                self.clear_prompt("prompt")
                self.show_message("easy", "action")
                time.sleep(1)
                return easy_dict
            if choice == "N":
                self.clear_prompt("prompt")
                self.show_message("normal", "action")
                time.sleep(1)
                return normal_dict
            if choice == "H":
                self.clear_prompt("prompt")
                self.show_message("hard", "action")
                time.sleep(1)
                return hard_dict
            else:
                self.clear_prompt("prompt")
                self.show_message("Not a valid difficulty!\n", "invalid")

    # General method for displaying a text message
    def show_message(self, key: str, type: str):
        # Get message to show
        text = self.messages.get(key)

        # Display style based on type
        if type == "prompt":
            print(f"> {text}")
        if type == "action":
            print(f"... {text}")
        if type == "info":
            print(f"--- {text}")
        if type == "warn":
            print(f"*** {text}")
        if type == "event":
            print(f"!!! {text}")
        if type == "invalid":
            print(f"XXX {text}")

    # Displays "senses" based on sense_environment() in WumpusGame
    def display_senses(self, sense_dict: dict):
        print()
        lines = []
        if sense_dict["pit"]:
            self.show_message("pit", "warn")
        if sense_dict["bats"]:
            self.show_message("bats", "warn")
        if sense_dict["wumpus"]:
            self.show_message("stench", "warn")
        print()
    
    # Displays status of player: current room, no. of arrows, nearby rooms
    def display_status(self, current_room_id: int, arrows: int, nearby_rooms: list):
        lines = []
        room_ids = [r.room_id for r in nearby_rooms]
        rooms_formatted = "  ".join(f"{r:>2}" for r in room_ids)

        print(f"--- You are in room {current_room_id}.")
        print(f"--- You have {arrows} arrows left.")
        print(f"--- Nearby rooms: {rooms_formatted}\n")

    # Asks user for desired action [M]ove or [S]hoot, returns str
    def ask_action(self) -> str:
        action = str(input("> Move or Shoot [M/S]: ").strip().upper())
        self.clear_prompt("prompt")    
        return action

    # Asks user for desired direction for movement or aiming arrow, returns str
    def ask_direction(self, room_id: int, move_or_shoot: str) -> str:
        direction_to_index = {"N": 0, "E": 1, "S": 2, "W": 3} # dict for dir -> int
        direction_strings = ["North", "East", "South", "West"]
        choice_text = "> [N/E/S/W] Direction: "

        if move_or_shoot == "move":
            print(f"--- You are currently in room {room_id}.")
            print("> Where do you want to move?")
        if move_or_shoot == "shoot":
            print("--- You can curve the path of the arrow three times.")
            print("> Where do you want to aim?")
        
        while True:
            choice = str(input(choice_text).strip().upper())
            if choice in direction_to_index:
                direction = direction_to_index[choice] # turns N/E/S/W: str into 0/1/2/3: int
                break
            else:
                self.show_message("invalid_direction", "invalid")

        if move_or_shoot == "shoot":
            print(f"... You aim {direction_strings[direction]}")

        return direction
    
    # Display text for arrow movement
    def shooting_text(self, room_number: int):
        if room_number == 1:
            print("... The arrow enters the FIRST room.\n")
        if room_number == 2:
            print("... The arrow enters the SECOND room.\n")
        if room_number == 3:
            print("... The arrow enters the THIRD room.\n")
    
    
    # Shows a "moving transition" in the terminal based on movement type
    def show_move_transition(self, new_room_id: int, move_or_bat: str):
        # If it's a bat transport: print bat grab message
        if move_or_bat == "bat":
            print("A BAT grabs you!\n")

        # Print dots for "movement"
        for _ in range(3):
            time.sleep(0.3)
            print(".", end="")
            print()
        time.sleep(0.3)
        print(f"You are now in room {new_room_id}\n")
        time.sleep(0.5)

    # Shows welcome title and intro text (if desired by user)
    def show_welcome(self):
        # Title text
        title = r"""
+--------------------------------------------------------------+
|                         W U M P U S                          |
|                                                              |
|                 Beneath Hardox... he looms.                  |
+--------------------------------------------------------------+
"""
        print(title)

        # "Skip intro" prompt
        while True:
            skip = input("> SKIP INTRO? [Y/N]: ").strip().upper()
            if skip == "Y":
                self.clear_prompt("prompt")
                return
            if skip == "N":
                break
            else:
                print("*** Input must be [Y] or [N]")

        # Intro text lines
        lines = [
            "> You find yourself in the culverts beneath Hardox, where the gluttonous WUMPUS resides.",
            "> To avoid being eaten you have to shoot WUMPUS with your bow and arrow.",
            "> The culverts are all connected to a number of rooms via cramped tunnels.",
            "> You can move North, East, South, or West from one room to another.",
            "> Here lurks a number of dangers however:",
            "- Some rooms contain BOTTOMLESS PITS, and falling into one means certain death.",
            "- Others contain BATS, which will fly you to a random room of their choosing.",
            "> In one of the rooms... lurks the mighty WUMPUS.",
            "> If encountered, he will instantly gobble you up and you WILL die.",
            "> Luckily, via the SENSES DISPLAY you can feel the cold breeze of a pit nearby, or the flapping of wings...",
            "> ...or the stench of WUMPUS.",
            "> Via the STATUS BAR you can see: ",
            "- The room you are currently in",
            "- Nearby rooms.",
            "- How many arrows you have left.",
            "X To win the game you have to shoot and kill WUMPUS.",
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
            print(">>> Huzzah! The ol' WUMPUS has been executed by a swift arrow! You win!")
        
        # Show loss result
        elif result == "lose":
            time.sleep(1)
            self.show_message("death", "event")

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
    def wumpus_chase(self, ui: GUI):
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
                ui.show_message("wumpus_move", "warn")
                # DEBUG: print(f"Wumpus MOVED to ROOM {self.wumpus_room.room_id}")
            else:
                # If no path exists, just move randomly
                self.wumpus_room = random.choice(self.safe_rooms)
                ui.show_message("wumpus_move", "warn")
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
    
    # Logic for moving the player, using ui.ask_direction for desired direction
    def move_player(self, ui: GUI):
        connected_rooms = self.player.current_room.connected_rooms
        direction = ui.ask_direction(self.player.current_room.room_id, "move") # returns N,E,S,W string
        target_room_obj = connected_rooms[direction]
        self.player.current_room = target_room_obj
        ui.show_move_transition(self.player.current_room.room_id, "move") # show moving animation
        return

    # Checks if player has entered a room with a pit
    def check_pit_kill(self, ui: GUI):
        if self.player.current_room.has_pit:
            ui.show_message("pit_fall", "event")
            self.player.is_alive = False

    # Checks if player has entered a room with bats, transports player
    def check_bats_transport(self, ui) -> bool:
        if self.player.current_room.has_bats:
            possible_rooms = [room for room in self.safe_rooms if room != self.player.current_room]
            self.player.current_room = random.choice(possible_rooms)
            ui.show_move_transition(self.player.current_room.room_id, "bat")
    
    # Checks for player encounter with Wumpus, changes alive-status of Player instance
    def check_wumpus_encounter(self, ui: GUI):
        if self.player.current_room.has_wumpus:
            ui.show_message("wumpus_attack", "event")
            self.player.is_alive = False

    # Logic fo shooting and steering arrows
    def shoot_arrow(self, ui: GUI):
        # Early escape if no more arrows
        if self.player.arrows <= 0:
            ui.show_message("no_arrows", "warn")
            return
        
        # Decrement no. of arrows available
        self.player.arrows -= 1

        # Run this code three times, once for each direction choice / aiming
        for i in range(0, 3):
            current_arrow_room = self.player.current_room
            connected_rooms = self.player.current_room.connected_rooms
            direction = ui.ask_direction(None, "shoot") # returns an index for direction
            current_arrow_room = connected_rooms[direction]
            ui.shooting_text(i + 1)

            # If arrow "hits" Wumpus
            if current_arrow_room.has_wumpus:
                current_arrow_room.has_wumpus = False
                return
            
            # If arrow "hits" player
            if current_arrow_room.room_id == self.player.current_room.room_id:
                ui.show_message("suicide", "event")
                self.player.is_alive = False
                return
        ui.show_message("arrow_miss", "info")

    # Checks game status based on Wumpus existance or Player alive/arrows status
    def check_game_state(self, ui: GUI) -> str:
        # If player is dead or has no arrows left, they lose
        if not self.player.is_alive:
            return "lose"
        elif self.player.arrows <= 0:
            ui.show_message("no_arrows", "info")
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
    def play_turn(self, ui: GUI):
        senses = ui.display_senses(self.sense_environment())
        status = ui.display_status(self.player.current_room.room_id, 
                                     self.player.arrows, 
                                     self.player.current_room.connected_rooms) 

        # Loop for choosing a player action
        while True:
            action = ui.ask_action()
            if action in ("M", "S"):
                break
            else:
                ui.show_message("invalid_action", "invalid")

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