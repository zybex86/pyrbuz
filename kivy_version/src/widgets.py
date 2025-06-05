"""
Custom Kivy widgets for the Suika Game.

This module defines reusable UI components for the game.
"""

from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.image import Image
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.widget import Widget
from kivy.properties import StringProperty

class FruitButton(Button):
    def __init__(self, fruit_name, **kwargs):
        super().__init__(**kwargs)
        self.fruit_name = fruit_name
        self.text = fruit_name.capitalize()
        self.size_hint = (None, None)
        self.size = (100, 100)
        self.bind(on_press=self.on_press)

    def on_press(self):
        print(f"{self.fruit_name} button pressed!")

class FruitLabel(Label):
    def __init__(self, text, **kwargs):
        super().__init__(**kwargs)
        self.text = text
        self.font_size = 24

class FruitImage(Image):
    def __init__(self, source, **kwargs):
        super().__init__(**kwargs)
        self.source = source
        self.size_hint = (None, None)
        self.size = (100, 100)

class FruitBoxLayout(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'vertical'

class ScoreLabel(Widget):
    """
    Widget for displaying the player's score.

    Attributes:
        score_text (str): The text to display as the score.
    """
    score_text = StringProperty("Score: 0")

    def update_score(self, score: int) -> None:
        """
        Update the displayed score.

        Args:
            score (int): The new score value.
        """
        self.score_text = f"Score: {score}"