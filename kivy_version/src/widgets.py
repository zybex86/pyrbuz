"""
Custom Kivy widgets for the Suika Game.

This module defines reusable UI components such as FruitButton, FruitLabel,
FruitImage, NextFruitPreview, ScoreLabel, and layout helpers.
"""

import os
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.image import Image
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import StringProperty, NumericProperty
from kivy.animation import Animation
from config import ASSETS_DIR

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

class NextFruitPreview(Image):
    """
    Widget for displaying the next fruit preview above the play area.

    This widget is purely visual and does not participate in game logic or physics.

    Args:
        fruit_name (str): Name of the fruit to preview.
        radius (float): Radius of the fruit.
        play_area_x, play_area_y, play_area_width, play_area_height: Play area geometry for positioning.
    """
    def __init__(self, fruit_name, radius, play_area_x, play_area_y, play_area_width, play_area_height, **kwargs):
        # Set the image source immediately to avoid a blank preview
        source_path = os.path.join(ASSETS_DIR, f"{fruit_name}.png")
        super().__init__(source=source_path, **kwargs)
        self.fruit_name = fruit_name
        self.radius = radius
        self.size = (radius * 2, radius * 2)
        self.allow_stretch = True
        self.keep_ratio = True
        self.update_position(play_area_x, play_area_y, play_area_width, play_area_height)

    def update_preview(self, fruit_name, radius, play_area_x, play_area_y, play_area_width, play_area_height):
        self.fruit_name = fruit_name
        self.radius = radius
        self.source = os.path.join(ASSETS_DIR, f"{fruit_name}.png")
        self.size = (radius * 2, radius * 2)
        self.update_position(play_area_x, play_area_y, play_area_width, play_area_height)

    def update_position(self, play_area_x, play_area_y, play_area_width, play_area_height):
        """
        Place the preview just above the play area, horizontally centered.
        """
        x = play_area_x + play_area_width // 2 - self.radius
        # Place the preview just a few pixels above the play area, not at the window top
        y = play_area_y + play_area_height - self.radius + 10  # 10px above the top edge of play area
        self.pos = (x, y)

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