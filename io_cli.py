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
        }

    def show_message(self, key):
        text = self.messages.get(key)
        self.console.print(f"[bold yellow]{text}[/bold yellow]")

    def show_senses(self, sense_dict: dict):
        lines = []
        if sense_dict["pit"]:
            lines.append("[blue]You feel a cold breeze.[/blue]")
        if sense_dict["bats"]:
            lines.append("[#FFA500]You hear the flapping of wings...[/#FFA500]")
        #if sense_dict["wumpus"]:
            lines.append("[red]You smell a foul stench, reminding you of Hardox... post-pub![/red]")

        if lines:
            self.console.print(Panel("\n".join(lines), title="[bold yellow]Senses[/bold yellow]", border_style="yellow"))

# DEBUGGING
if __name__ == "__main__":
    t = TextUI()
    t.show_message("invalid_move")