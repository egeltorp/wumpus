'''
io_cli.py
--------
Module for text-based user interface for the Wumpus game.
Utilizes the 'rich' library for fresh looking terminal output.
--------
Theodor Holmberg aka @egeltorp 2025
'''
import sys
import time

from rich.console import Console
from rich.table import Table
from rich.text import Text
from rich import box
from rich.panel import Panel
from rich.columns import Columns
from rich.align import Align

class TextUI:
    def __init__(self):
        self.console = Console()
        
        self.messages = {
            "no_arrows": "You have no arrows left!\n",
            "arrow_miss": "Your arrow missed.\n",
            "wumpus_attack": "[bold red]The Wumpus SLOBBERS on your FLESH![/bold red]\n",
            "wumpus_move": "[italic red]The Wumpus stomps closer![/italic red]\n",
            "wumpus_hit": "The Wumpus has been struck!\n",
            "pit_fall": "[bold blue]You tripped into a pit like a bitch...[/bold blue]\n",
            "invalid_direction": "[bold red]Not a valid direction.[/bold red]\n",
            "invalid_action": "[bold red]Not a valid action.[/bold red]\n",
            "suicide": "[bold red]You killed yourself with the arrow.[/bold red]\n"
        }
    
    def choose_difficulty(self):
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
                self.console.print("You chose [bold green]EASY[/bold green]")
                return e_dict
            if choice == "N":
                self.clear_prompt("prompt")
                self.console.print("You chose [bold yellow]NORMAL[/bold yellow]")
                return n_dict
            if choice == "H":
                self.clear_prompt("prompt")
                self.console.print("You chose [bold red]HARD[/bold red]")
                return h_dict
            else:
                self.clear_prompt("prompt")
                self.console.print("[italic red]Not a valid difficulty![/italic red]\n")

    def show_message(self, key):
        text = self.messages.get(key)
        text_formatted = Text.from_markup(text)
        self.console.print(f"{text}")

    def calculate_senses(self, sense_dict: dict) -> Panel:
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
        
    def calculate_status(self, current_room_id: int, arrows: int, nearby_rooms: list) -> Panel:
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

    def ask_action(self):
        input_text = Text.from_markup("> Move or Shoot ([magenta]M[/magenta]/[red]S[/red]): ", style="bold white")
        action = self.console.input(input_text).strip().upper()
        self.clear_prompt("prompt")    
        return action

    def ask_move_direction(self, room_id) -> str:
        self.console.print(f"You are currently in room [bold magenta]{room_id}[/bold magenta].")
        directions = f"[bold magenta][N/E/S/W][/bold magenta]"
        input_text = Text.from_markup(f"> {directions} Direction: ", style="bold white")
        input = str(self.console.input(input_text).upper().strip())
        return input
    
    def show_move_transition(self, new_room_id, move_or_bat: str):
        # if it's a bat transport
        if move_or_bat == "bat":
            self.console.print("A [red]bat[/red] grabs you!", end="", style="bold italic white")
            print()

        # print dots for "movement"
        for _ in range(3):
            time.sleep(0.3)
            print(".", end="")
            print()
        time.sleep(0.3)
        self.console.print(f"You are now in room [bold magenta]{new_room_id}[/bold magenta]\n", style="bold white")
        time.sleep(0.5)

    def ask_shoot_direction(self) -> str:
        directions = f"[bold red][N/E/S/W][/bold red]"
        input_text = Text.from_markup(f"> {directions} Direction: ", style="bold white")
        input = str(self.console.input(input_text).upper().strip())
        return input
    
    def shooting_text(self, room_number: int):
        arrow = "[bold red]arrow[/bold red]"
        if room_number == 1:
            self.console.print(f"The {arrow} enters the first room.")
        if room_number == 2:
            self.console.print(f"The {arrow} enters the seconds room.")
        if room_number == 3:
            self.console.print(f"The {arrow} enters the third room.")
        
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

        # Skip intro prompt
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

        # Intro text
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

        for line in lines:
            for char in line:
                print(char, end="")
                sys.stdout.flush()
                time.sleep(0.03)
            print()
            time.sleep(0.5)

    def show_result(self, result: str):
        # Show win/lose result
        if result == "win":
            time.sleep(1)
            print(".")
            time.sleep(1)
            print(".")
            time.sleep(1)
            print(".")
            win_text = Text.from_markup("[bold green]Huzzah! The ol' Wumpus has been executed by a swift arrow! You win![/bold green]")
            self.console.print(Panel(win_text, expand=False, border_style="green"))
        elif result == "lose":
            time.sleep(1)
            self.console.print("[bold red]Ouch! You met a grim and quite frankly embarassing fate. Better luck next time bozo![/bold red]")

    def show_panels(self, senses_panel: Panel, status_panel: Panel):
        # Shows actions, senses, and status panels

        # Actions panel
        actions_panel_content = (
            "[bold white]What do you want to do?[/bold white]\n"
            "\n"
            "[bold magenta][M][/bold magenta] Move\n"
            "[bold red][S][/bold red] Shoot an arrow"
        )
        actions_panel = Panel(actions_panel_content, expand=False, title="[bold white]ACTION[/bold white]", border_style="white",)

        self.console.print(Columns([actions_panel, status_panel, senses_panel], equal=True))

    def clear_prompt(self, to_clear: str):
        if to_clear == "prompt":
            sys.stdout.write("\033[F")
            sys.stdout.write("\033[K")
            sys.stdout.flush()

# DEBUGGING
if __name__ == "__main__":
    pass