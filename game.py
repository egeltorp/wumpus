import random

class Room:
    def __init__(self, room_id: int):
        self.room_id = room_id
        self.connected_rooms = []
        self.has_wumpus = False
        self.has_pit = False
        self.has_bats = False

class Player:
    def __init__(self, starting_room: Room, arrows: int):
        self.current_room = starting_room
        self.arrows = arrows
        self.is_alive = True

class WumpusGame:
    def __init__(self, num_rooms: int = 16, 
                 pit_rate: float = 0.2, 
                 bat_rate: float = 0.3, 
                 arrows: int = 5, 
                 seed: int = 1701):
        self.num_rooms = num_rooms
        self.pit_rate = pit_rate
        self.bat_rate = bat_rate
        self.arrows = arrows
        self.seed = seed

    def random_seed(self, seed: int):
        random.seed(seed)
        self.seed = seed

    def generate_rooms(self):
        self.rooms = [Room(i) for i in range(self.num_rooms)]

    def connect_rooms(self):
        number_of_connections = 4

        # Run this code for each room in self.rooms
        for room in self.rooms:
            while len(room.connected_rooms) < number_of_connections:
                target_room = random.choice(self.rooms)
                if target_room != room and target_room not in room.connected_rooms:
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

    def place_player(self):
        pass

    def sense_environment(self):
        pass
    
    def move_player(self, room_id: int):
        pass

    def shoot_arrow(self, room_id: int) -> bool:
        pass

    def bats_transport_player(self):
        pass

    def pit_kill_player(self):
        pass

    def check_player_win(self) -> bool:
        # Determine if the player has won
        # game.is_over() should return True if the game has ended
        pass

    def play_turn(self, ui):
        pass

    def is_running(self) -> bool:
        # Determine if the game is still running
        # return NOT self.is_over()
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