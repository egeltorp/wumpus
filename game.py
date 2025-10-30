"""
game.py
--------
Contains all pure game logic for Wumpus.
Handles room generation, hazards, movement, and combat.
Does not perform any input/output — game.py refers to io_cli.py for UI.
"""

import random

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
    def __init__(self, num_rooms: int = 16, 
                 pit_rate: float = 0.2, 
                 bat_rate: float = 0.3,
                 starting_arrows: int = 5,
                 rooms: list = [],
                 safe_rooms: list = [],
                 seed: int = 1701):
        self.num_rooms = num_rooms
        self.pit_rate = pit_rate
        self.bat_rate = bat_rate
        self.starting_arrows = starting_arrows
        self.rooms = rooms
        self.safe_rooms = safe_rooms
        self.seed = seed

    def random_seed(self, seed: int):
        random.seed(seed)
        self.seed = seed

    def generate_rooms(self):
        self.rooms = [Room(i) for i in range(self.num_rooms)]

    def connect_rooms(self):
        number_of_connections = 4
        safety_limit = 500

        # # # BUGGED, sometimes causes a room to only get 2 connections instead of 4

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
        wumpus_room = random.choice(empty_room)
        wumpus_room.has_wumpus = True

        # Store safe rooms
        self.safe_rooms = [room for room in self.rooms if not room.has_pit and not room.has_bats and not room.has_wumpus]

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
        # Check if valid move
        room_id = ui.ask_move_room(self.player.current_room.connected_rooms)
        if room_id in self.player.current_room.connected_rooms:
            self.player.current_room = room
        else:
            ui.show_message("invalid_move")
            return False

    def shoot_arrow(self, ui):
        if self.player.arrows <= 0:
            ui.show_message("no_arrows")
            return False
        
        for i in range(0, 3):
            target_room = ui.ask_target_room(self.player.current_room.connected_rooms)
            self.player.arrows -= 1
            if target_room.has_wumpus:
                ui.show_message("wumpus_hit")
                return True
            else:
                ui.show_message("arrow_miss")
                return False

    def pit_kill_player(self) -> bool:
        if self.player.current_room.has_pit:
            return True
        return False

    def bats_transport_player(self) -> bool:
        if self.player.current_room.has_bats:
            possible_rooms = [room for room in self.safe_rooms if room != self.player.current_room]
            self.player.current_room = random.choice(possible_rooms)
        return False

    def check_win_lose(self):
        # Determine if the player has won or lost
        pass

    def play_turn(self, ui):
        pass

    def is_running(self):
        pass

# DEBUGGNG
if __name__ == "__main__":
    game = WumpusGame()
    game.random_seed(game.seed)
    print(f"Game initialized with seed: {game.seed}")

    game.generate_rooms()
    print(f"Generated {len(game.rooms)} rooms.")

    game.connect_rooms()
    for room in game.rooms:
        connected_ids = [r.room_id for r in room.connected_rooms]
        print(f"Room {room.room_id} connected to rooms: {connected_ids}")

    game.place_hazards()
    for room in game.rooms:
        if room.has_pit:
            print(f"O Room {room.room_id} has a pit.")
    for room in game.rooms:
        if room.has_bats:
            print(f"X Room {room.room_id} has bats.")
    for room in game.rooms:
        if room.has_wumpus:
            print(f"> Room {room.room_id} has the Wumpus.")

    game.place_player()
    print(f"Player is in room {str(game.player.current_room.room_id)} with {game.starting_arrows} arrows.")