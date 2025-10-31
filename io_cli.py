'''
io_cli.py
--------
Module for text-based user interface for the Wumpus game.
Utilizes the 'rich' library for fresh looking terminal output.
--------
Theodor Holmberg aka @egeltorp 2025
'''
import random

from rich.console import Console
from rich.table import Table
from rich.text import Text
from rich.prompt import Prompt
from rich.panel import Panel
from rich.columns import Columns

class TextUI:
    def __init__(self):
        self.console = Console()
        
        self.messages = {
            "no_arrows": "You have no arrows left!",
            "wumpus_attack": "The Wumpus gorges on your flesh! You have been gobbled to death!",
            "pit_fall": "You tripped like a bitch and fell into a pit! Game over!",
            "bat_grab": "A bat grabs your skinny ass and drops you in a random room!",
            "invalid_move": "Not a valid move.",
            "invalid_action": "Not a valid action.",
            "arrow_shot": "The arrow enters a room."
        }

    def show_message(self, key):
        text = self.messages.get(key)
        self.console.print(f"[bold yellow]{text}[/bold yellow]")

    def calculate_senses(self, sense_dict: dict) -> Panel:
        lines = []
        if sense_dict["pit"]:
            lines.append("You feel a [bold blue]cold breeze.[/bold blue]")
        if sense_dict["bats"]:
            lines.append("You hear the [italic]flapping of wings...[/italic]")
        if sense_dict["wumpus"]:
            lines.append("You smell a [bold red]foul stench[/bold red], reminding you of Hardox!")

        if lines:
            panel = Panel("\n".join(lines), title="[bold yellow]Senses[/bold yellow]", border_style="yellow")
            return panel
        
    def calculate_status(self, current_room_id: int, arrows: int, nearby_rooms: list) -> Panel:
        lines = []
        room_ids = [r.room_id for r in nearby_rooms]
        rooms = ", ".join(str(id) for id in room_ids)

        lines.append(f"You are in room [bold magenta]{current_room_id}[/bold magenta].")
        lines.append(f"You have [bold magenta]{arrows}[/bold magenta] arrows left.")
        lines.append(f"Nearby rooms: [bold magenta]{rooms}[/bold magenta]")
        status_panel = Panel("\n".join(lines), title="[bold magenta]Status[/bold magenta]", border_style="magenta")
        return status_panel

    def ask_action(self):
        input_text = Text("Enter your action (M/S): ", style="bold green")
        action = self.console.input(input_text).strip().upper()      
        return action

    def ask_move_room(self) -> int:
        input_text = Text("Room to enter: ", style="bold green")
        input = int(self.console.input(input_text).strip())
        return input

    def ask_target_room(self) -> int:
        input_text = Text("Which room do you want to shoot into? : ", style="bold red")
        target_room_id = int(self.console.input(input_text).strip().upper())
        return target_room_id

    def show_welcome(self):
        print("Welcome to Wumpus!")

    def show_result(self, result: str):
        # Show win/lose result
        if result == "win":
            self.console.print("[bold green]Huzzah! The ol' Wumpus has been executed by a swift arrow! You win![/bold green]")
        elif result == "lose":
            self.console.print("[bold red]Ouch! You met a grim and quite frankly embarassing fate. Better luck next time bozo![/bold red]")

    def show_panels(self, senses_panel: Panel, status_panel: Panel):
        # Shows actions, senses, and status panels

        # Actions panel
        actions_panel_content = (
            "[bold]What do you want to do?[/bold]\n"
            "[bold white][M][/bold white] Move\n"
            "[bold white][S][/bold white] Shoot an arrow"
        )
        actions_panel = Panel(actions_panel_content, title="[bold cyan]Your Action[/bold cyan]", border_style="cyan",)

        self.console.print(Columns([actions_panel, status_panel, senses_panel], equal=True))

# DEBUGGING
if __name__ == "__main__":
    pass