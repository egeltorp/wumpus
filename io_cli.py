'''
io_cli.py
--------
Module for text-based user interface for the Wumpus game.
Utilizes the 'rich' library for fresh looking terminal output.
--------
Theodor Holmberg aka @egeltorp 2025
'''
import random
import sys
import time

from rich.console import Console
from rich.table import Table
from rich.text import Text
from rich.prompt import Prompt
from rich.panel import Panel
from rich.columns import Columns
from rich.align import Align

class TextUI:
    def __init__(self):
        self.console = Console()
        
        self.messages = {
            "no_arrows": "You have no arrows left!\n",
            "arrow_miss": "Your arrow missed.\n",
            "wumpus_attack": "The Wumpus slobbers on your flesh!\n",
            "wumpus_hit": "The Wumpus has been struck!\n",
            "pit_fall": "[bold blue]You tripped into a pit like a bitch...[/bold blue]\n",
            "invalid_direction": "[bold red]Not a valid direction.[/bold red]\n",
            "invalid_action": "[bold red]Not a valid action.[/bold red]\n",
            "suicide": "[bold red]You killed yourself with the arrow.[/bold red]\n"
        }

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