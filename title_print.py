import os
import shutil

def clear_screen():
	if os.name == "nt":
		os.system("cls")
	else:
		os.system("clear")

def main():
	# Title
	title_lines = [
		r" /$$      /$$ /$$   /$$ /$$      /$$ /$$$$$$$  /$$   /$$  /$$$$$$ ",
		r"| $$  /$ | $$| $$  | $$| $$$    /$$$| $$__  $$| $$  | $$ /$$__  $$",
		r"| $$ /$$$| $$| $$  | $$| $$$$  /$$$$| $$  \ $$| $$  | $$| $$  \__/",
		r"| $$/$$ $$ $$| $$  | $$| $$ $$/$$ $$| $$$$$$$/| $$  | $$|  $$$$$$ ",
		r"| $$$$_  $$$$| $$  | $$| $$  $$$| $$| $$____/ | $$  | $$ \____  $$",
		r"| $$$/ \  $$$| $$  | $$| $$\  $ | $$| $$      | $$  | $$ /$$  \ $$",
		r"| $$/   \  $$|  $$$$$$/| $$ \/  | $$| $$      |  $$$$$$/|  $$$$$$/",
		r"|__/     \__/ \______/ |__/     |__/|__/       \______/  \______/ ",
		r"                                                                   ",
		r"                                                                   ",
		r"                                                                   ",
	]

	# Get terminal size
	size = shutil.get_terminal_size(fallback=(80, 24))
	term_width = size.columns
	term_height = size.lines

	# Center each line horizontally
	centered_lines = []
	for line in title_lines:
		line_len = len(line)
		if line_len >= term_width:
			# If line is longer than terminal, just use it raw
			centered_lines.append(line)
		else:
			padding = (term_width - line_len) // 2
			centered_lines.append(" " * padding + line)

	# Center vertically
	total_lines = len(centered_lines)
	if total_lines >= term_height:
		top_padding = 0
	else:
		top_padding = (term_height - total_lines) // 2

	clear_screen()

	# Print top padding
	for _ in range(top_padding):
		print()

	# Print the title
	for line in centered_lines:
		print(line)

	print()
	print(" " * ((term_width - 32) // 2) + "Press ENTER to start...", end="")
	try:
		input()
	except EOFError:
		pass

if __name__ == "__main__":
	main()
