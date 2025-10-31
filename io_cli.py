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

    def display_status(self):
        pass

    def calculate_senses(self, sense_dict: dict) -> Panel:
        lines = []
        if sense_dict["pit"]:
            lines.append("[blue]You feel a cold breeze.[/blue]")
        if sense_dict["bats"]:
            lines.append("[italic #FFA500]You hear the flapping of wings...[/italic #FFA500]")
        if sense_dict["wumpus"]:
            lines.append("[bold red]You smell a foul stench, reminding you of Hardox... post-pub![/bold red]")

        if lines:
            panel = Panel("\n".join(lines), title="[bold yellow]Senses[/bold yellow]", border_style="yellow")
            return panel

    def ask_action(self):
        input_text = Text("Enter your action (M/S): ", style="bold cyan")
        action = self.console.input(input_text).strip().upper()      
        return action

    def ask_move_room(self):
        # Ask which room to move to
        pass

    def ask_target_room(self):
        # Ask which room to shoot into, 3x
        pass

    def show_welcome(self):
        # Show welcome screen
        pass

    def show_result(self, result: str):
        # Show win/lose result
        if result == "win":
            self.console.print("[bold green]Huzzah! The ol' Wumpus has been executed by a swift arrow! You win![/bold green]")
        elif result == "lose":
            self.console.print("[bold red]Ouch! You met a grim and quite frankly embarassing fate. Better luck next time bozo![/bold red]")

    def show_panels(self, senses_panel: Panel):
        # Combine all panels side by side

        # Actions panel
        actions_panel_content = (
            "[bold]What do you want to do?[/bold]\n"
            "[bold white][M][/bold white] Move\n"
            "[bold white][S][/bold white] Shoot an arrow"
        )
        actions_panel = Panel(actions_panel_content, title="[bold cyan]Your Action[/bold cyan]", border_style="cyan",)

        self.console.print(Columns([actions_panel, senses_panel], equal=True))

# DEBUGGING
if __name__ == "__main__":
    t = TextUI()

    sense_dict = {"pit": True, "bats": True, "wumpus": True}
    t.show_panels(t.calculate_senses(sense_dict))
    t.ask_action()