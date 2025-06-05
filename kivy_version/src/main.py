"""
Entry point for the Kivy Suika Game application.

This module initializes and runs the Kivy app, keeping the entry point
separate from the main game logic for better maintainability.
"""

from kivy.app import App
from game import Game

class GameApp(App):
    """
    Main Kivy App class responsible for launching the game.
    """
    def build(self):
        """
        Build and return the main game widget.
        """
        return Game()

if __name__ == "__main__":
    GameApp().run()