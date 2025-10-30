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
        pass

    def connect_rooms(self):
        pass

    def place_hazards(self):
        pass

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