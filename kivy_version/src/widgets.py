"""
Custom Kivy widgets for the Suika Game.

This module defines reusable UI components for the game.
"""

from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.image import Image
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.widget import Widget
from kivy.properties import StringProperty, NumericProperty
from kivy.animation import Animation

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

class ScoreLabel(Label):
    """
    Widget for displaying the player's score with animation support.

    Attributes:
        score_text (str): The text to display as the score.
        anim_scale (float): The scale factor for score animation.
    """
    score_text = StringProperty("Score: 0")
    anim_scale = NumericProperty(1.0)

    def update_score(self, score: int) -> None:
        """
        Update the displayed score and animate the label.

        Args:
            score (int): The new score value.
        """
        self.score_text = f"Score: {score}"
        # Animate the label to scale up and then back to normal for feedback
        Animation.cancel_all(self, 'anim_scale')
        anim = Animation(anim_scale=1.3, duration=0.1) + Animation(anim_scale=1.0, duration=0.2)
        anim.start(self)