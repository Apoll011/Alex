import os
import shutil

class Screen:
    """
    A Class for managing the cmd terminal
    """
    def __init__(self, name: str):
        """
        Initializes the AiRepresentationInScreen instance
        """
        self.name = name

    def header(self):
        """
        Prints a header message
        """
        self.print_header_text(f"Initializing {self.name}")

    def print_header_text(self, text, size = 2):
        s = (size + 1)
        terminal_size = shutil.get_terminal_size().columns
        border_size = (terminal_size - len(text) - 2 - self.name.count(" ")) // s  # 2 is for spaces
        print("\33[91m-" * border_size, f"\33[36m{text}\33[91m", "-" * border_size, "\33[97m")

    def footer(self):
        """
        Prints a footer message
        """
        self.print_header_text(f"End initializing {self.name}")

    @staticmethod
    def clear():
        """
        Clears the screen
        """
        os.system("clear")
