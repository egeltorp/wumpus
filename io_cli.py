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
            "no_arrows": "You have no arrows left!",
            "wumpus_attack": "The Wumpus slobbers on your flesh!",
            "pit_fall": "You tripped into a pit like a bitch...",
            "bat_grab": "A bat grabs your skinny ass and drops you in a random room!",
            "invalid_move": "Not a valid move.",
            "invalid_action": "Not a valid action.",
            "arrow_shot": "The arrow enters a room."
        }

    def show_message(self, key):
        text = self.messages.get(key)
        self.console.print(f"[bold italic yellow]{text}[/bold italic yellow]")

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
        rooms = ", ".join(str(id) for id in room_ids)

        lines.append(f"You are in room [bold magenta]{current_room_id}[/bold magenta].")
        lines.append(f"You have [bold red]{arrows}[/bold red] arrows left.")
        lines.append(f"Nearby rooms: [bold magenta]{rooms}[/bold magenta]")
        status_panel = Panel("\n".join(lines), title="[bold magenta]STATUS[/bold magenta]", border_style="magenta")
        return status_panel

    def ask_action(self):
        input_text = Text.from_markup("Enter your action ([magenta]M[/magenta]/[red]S[/red]): ", style="bold")
        action = self.console.input(input_text).strip().upper()      
        return action

    def ask_move_room(self, room_id) -> int:
        self.console.print(f"You are in room [bold magenta]{room_id}[/bold magenta].")
        input_text = Text("Room to enter: ", style="bold magenta")
        input = int(self.console.input(input_text).strip())
        return input

    def ask_target_room(self) -> int:
        input_text = Text("Which room do you want to shoot into? : ", style="bold red")
        target_room_id = int(self.console.input(input_text).strip().upper())
        return target_room_id

    def show_welcome(self):
        # Title panel
        title = Text("WUMPUS", style="bold red on black", justify="center")
        subtitle = Text("Beneath Hardox... he waits.")
        panel = Panel(
            Align.center(Text.assemble(title, "\n", subtitle)),
            border_style="red",
            padding=(1, 4),
            title="[bold bright_red]* * *[/bold bright_red]"
        )
        self.console.print(panel)

        # Skip intro prompt
        yes = "[green]Y[/green]"
        no = "[red]N[/red]"
        prompt = Text.from_markup(f"Skip intro? [{yes}/{no}]: ", style="bold")
        skip = self.console.input(prompt).strip().upper()
        if skip == "Y":
            return

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
            self.console.print("[bold green]Huzzah! The ol' Wumpus has been executed by a swift arrow! You win![/bold green]")
        elif result == "lose":
            time.sleep(1)
            self.console.print("[bold red]Ouch! You met a grim and quite frankly embarassing fate. Better luck next time bozo![/bold red]")

    def show_panels(self, senses_panel: Panel, status_panel: Panel):
        # Shows actions, senses, and status panels

        # Actions panel
        actions_panel_content = (
            "[bold]What do you want to do?[/bold]\n"
            "[bold magenta][M][/bold magenta] Move\n"
            "[bold red][S][/bold red] Shoot an arrow"
        )
        actions_panel = Panel(actions_panel_content, title="[bold white]Your Action[/bold white]", border_style="white",)

        self.console.print(Columns([actions_panel, status_panel, senses_panel], equal=True))

# DEBUGGING
if __name__ == "__main__":
    pass