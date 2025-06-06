"""
Entry point for the Kivy Suika Game application.

This module initializes and runs the Kivy app, loading the main UI layout
and setting up the root Game widget.
"""

from kivy.app import App
from game import Game
from kivy.lang import Builder

Builder.load_file("kv/main.kv")

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