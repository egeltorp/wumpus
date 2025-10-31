# Spec av P-uppgift

# Namn: Theodor Holmberg
# Personnummer: 20030422-3274
# P-uppgift nr: 154
# Titel: Wumpus

# **************************** Organisering ************************

# Mitt program är uppdelat i tre filer:

# io_cli.py - Innehåller all kod för användargränsnittet
# använder rich modulen för att det ska se bra ut i terminalen

# game.py - Innehåller all spel-logik (rumsgenerering, faror, förflyttning, skjuta pilar).
# Ingen in-/utmatning sker i game.py, all sådan hanteras i __main__.py via io_cli.py

# __main__.py - Huvudprogrammet som kopplar ihop allt.

# Planen här är att dela upp koden i tre separata moduler för att hålla
# fördelningen av ansvar för olika delar i programmet
# tydlig och göra koden mer hanterbar.
#
# Detta kommer göra det mycket lättare att sen göra en GUI version av spelet
# via io_gui.py som kan ersätta io_cli.py utan att behöva ändra någonting
# i game.py
#
# Detta går garanterat att göra enklare men jag tycker det verkar väldigt kul
# och lärorikt att dela upp det såhär.


# **************************** Användargränsnitt ************************
"""
io_cli.py
---------
Textbaserat användargränssnitt för Wumpus-spelet.
Använder 'rich' för snygg terminalutskrift med färger.
---------
Theodor Holmberg aka @egeltorp, 2025
"""

from rich.console import Console
from rich.table import Table
from rich.text import Text
from rich.prompt import Prompt
from rich.panel import Panel
from rich.columns import Columns


class TextUI:
	"""Klass för att hantera all terminal-UI i spelet."""

	def __init__(self):
		"""Skapar konsolen och laddar textmeddelanden."""
		self.console = Console()
		self.messages = {}

	# grundläggande meddelanden
	def show_message(self, key: str):
		"""Visar ett textmeddelande utifrån en key från messages dict."""
		pass

	def display_status(self):
		"""Visar spelarens aktuella status (t.ex. rum, pilar)."""
		pass

	# sinnen och händelser
	def calculate_senses(self, sense_dict: dict) -> Panel:
		"""
		Skapar och returnerar en rich panel baserat på spelarens upplevda sinnen.
		Detta för att göra det mer clean när man väl spelar spelet.
		"""
		pass

	# spelarens val
	def ask_action(self) -> str:
		"""Frågar spelaren om vad den vill göra (förflytta eller skjuta)."""
		pass

	def ask_move_room(self) -> int:
		"""Frågar vilket rum spelaren vill gå till."""
		pass

	def ask_target_room(self) -> int:
		"""Frågar vilket rum spelaren vill skjuta en pil mot."""
		pass

	# start/slut skärmar
	def show_welcome(self):
		"""Visar välkomstskärm."""
		pass

	def show_end_screen(self, result: str):
		"""Visar slutskärmen baserat på outcome (vinst/förlust)."""
		pass

	# layout av rich panels
	def show_panels(self):
		"""
		Visar flera Rich-paneler sida vid sida 
		(t.ex. handlingar och sinnen, ksk också rum i närheten).
		"""
		pass

# ***************************** Algoritm/Huvudprogrammet *********************************

# Har inte klurat ut den exakta algoritmen för själva spelet när man väl kör en turn
# i __main__.py men det blir enklare när fler delar av programmet är färdiga.

# något som det här blir det ungefär:
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
                       starting_arrows = ARROWS,
                       rooms = [], 
                       safe_rooms = [],
                       seed = SEED)
    
    # SETUP
    game.random_seed()
    game.generate_rooms()
    game.connect_rooms()
    game.place_hazards()
    game.place_player()
	
    # INTRO
    ui.show_welcome()

    # CORE LOOP
	# while not game.is_over():
        # game.sense_environment()
        # ui.show_panels()
        # ui.ask_action()
        # do action
        # something like that
        # pass

    # WIN
    # ui.display_win()

def main():
    ui = TextUI()
    run_game(ui)

if __name__ == "__main__":
    main()

# ************************** Programskelett game.py ******************************
import random

     #*************** Klasser och dess metoder******************
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

    def random_seed(self):
        # sätter en random seed för hur rummen skapas
        # kan sättas och få samma config varje gång

    def generate_rooms(self):
        # skapar rummen

    def connect_rooms(self):
        # sätter ihop rummen från båda hållen
        # så man kan gå fram o tillbaka

    def place_hazards(self):
        # placerar ut faror i rummen baerat på pit_rate och bat_rate
        # och wumpus placeras också

    def place_player(self):
        # spwawnar spelaren i ett säkert rum

    def sense_environment(self) -> dict:
        # skapar en dict med sinnena som finns
        # i närheten av spelarens rum
    
    def move_player(self, ui) -> bool:
        # förflyttar spelaren om det går

    def shoot_arrow(self, ui):
        # skjuter en pil genom tre rum

    def check_pit_kill(self, ui):
        # döda spelaren om den går i en pit

    def check_bats_transport(self, ui) -> bool:
        # teleportera spelaren med bats om den landar i ett sånt rum
    
    def check_wumpus_encounter(self, ui) -> bool:
        # kolla om spelaren stöter på wumpus och döda spelaren i såna fall

    def check_game_state(self):
        # kolla om spelaren är död eller om wumpus är död

    def play_turn(self, ui):
        # spelarens fulla tur i spelet
		# anropar io_cli för input output och text
		# anropar game.py metoder för spelets logik