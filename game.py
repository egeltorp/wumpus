"""
game.py
--------
Contains all pure game logic for Wumpus.
Handles room generation, hazards, movement, and shooting.
Does not perform any input/output — game.py refers to io_cli.py for UI.
--------
Theodor Holmberg aka @egeltorp 2025
"""

import random
from collections import deque

class Room:
    def __init__(self, room_id: int):
        self.room_id = room_id
        self.connected_rooms = []
        self.has_pit = False
        self.has_bats = False
        self.has_wumpus = False

class Player:
    def __init__(self, starting_room: Room, starting_arrows: int):
        self.current_room = starting_room
        self.arrows = starting_arrows
        self.is_alive = True

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

    def random_seed(self):
        random.seed(self.seed)

    def generate_rooms(self):
        self.rooms = [Room(i) for i in range(self.num_rooms)]

    def connect_rooms(self):
        number_of_connections = 4
        safety_limit = 500

        # Run this code for each room in self.rooms
        for room in self.rooms:
            attempts = 0

            # While the room has less than the required connections 
            # and attempts is less than safety limit
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

    def wumpus_chase(self, ui):
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

    def find_path(self, start, goal):
        queue = deque([[start]])
        visited = {start}

        while queue:
            path = queue.popleft()
            room = path[-1]
            if room == goal:
                return path
            for neighbor in room.connected_rooms:
                if neighbor not in visited:
                    visited.add(neighbor)
                    queue.append(path + [neighbor])

        return []

    def place_player(self):
        # Place player in a random empty room
        spawn_room = random.choice(self.safe_rooms)

        # Creates a Player instance in WumpusGame class
        self.player = Player(spawn_room, self.starting_arrows)

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
    
    def move_player(self, ui) -> bool:
        direction_to_index = {"N": 0, "E": 1, "S": 2, "W": 3}
        connected_rooms = self.player.current_room.connected_rooms

        while True:
            direction = ui.ask_move_direction(self.player.current_room.room_id) # returns N,E,S,W string
            if direction in direction_to_index:
                target_room_obj = connected_rooms[direction_to_index[direction]]
                self.player.current_room = target_room_obj
                ui.show_move_transition(self.player.current_room.room_id, "move") # show moving animation
                return True
            else:
                ui.show_message("invalid_direction")

    def check_pit_kill(self, ui):
        if self.player.current_room.has_pit:
            ui.show_message("pit_fall")
            self.player.is_alive = False

    def check_bats_transport(self, ui) -> bool:
        if self.player.current_room.has_bats:
            possible_rooms = [room for room in self.safe_rooms if room != self.player.current_room]
            self.player.current_room = random.choice(possible_rooms)
            ui.show_move_transition(self.player.current_room.room_id, "bat")
        return False
    
    def check_wumpus_encounter(self, ui) -> bool:
        if self.player.current_room.has_wumpus:
            ui.show_message("wumpus_attack")
            self.player.is_alive = False

    def shoot_arrow(self, ui):
        if self.player.arrows <= 0:
            ui.show_message("no_arrows")
            return False
        
        self.player.arrows -= 1
        direction_to_index = {"N": 0, "E": 1, "S": 2, "W": 3}
        
        for i in range(0, 3):
            current_arrow_room = self.player.current_room
            while True:
                connected_rooms = self.player.current_room.connected_rooms
                direction = ui.ask_shoot_direction() # returns N,E,S,W string
                if direction in direction_to_index:
                    current_arrow_room = connected_rooms[direction_to_index[direction]]
                    break
                else:
                    ui.show_message("invalid_direction")
            ui.shooting_text(i + 1)
            if current_arrow_room.has_wumpus:
                current_arrow_room.has_wumpus = False
                return
            if current_arrow_room.room_id == self.player.current_room.room_id:
                ui.show_message("suicide")
                self.player.is_alive = False
                return
        ui.show_message("arrow_miss")

    def check_game_state(self) -> str:
        # if player is dead, they lose
        if not self.player.is_alive:
            return "lose"
        elif self.player.arrows <= 0:
            return "lose"
        
        # if Wumpus is dead, player wins
        if not any(room.has_wumpus for room in self.rooms):
            return "win"
        
        # otherwise, game continues
        return "running"
    
    def is_over(self) -> bool:
        state = self.check_game_state()
        if state == "lose":
            return True
        elif state == "win":
            return True
        elif state == "running":
            return False

    def play_turn(self, ui):
        # ui.console.clear()
        senses = ui.calculate_senses(self.sense_environment())
        status = ui.calculate_status(self.player.current_room.room_id, 
                                     self.player.arrows, 
                                     self.player.current_room.connected_rooms) 
        ui.show_panels(senses, status)

        while True:
            action = ui.ask_action()
            if action in ("M", "S"):
                break
            else:
                ui.show_message("invalid_action")

        if action == "M":
            self.move_player(ui)
            self.check_pit_kill(ui)
            self.check_bats_transport(ui)

            # Move Wumpus and check for encounter
            self.wumpus_chase(ui)
            self.check_wumpus_encounter(ui)

        elif action == "S":
            self.shoot_arrow(ui)
        else:
            ui.show_message("invalid_action")
