"""
Defines the Particle (fruit) class for the Suika Game.
Encapsulates all logic related to a single fruit, including physics and rendering.
"""

import os
from kivy.uix.widget import Widget
from kivy.uix.image import Image
import pymunk
from config import (
    ASSETS_DIR, FRUIT_TYPES, FRUIT_RADII,
    GRAVITY, DENSITY, ELASTICITY, FRICTION,
    BACKGROUND_COLOR, WALL_COLOR
)

class Particle(Widget):
    """
    Represents a single fruit in the game, with physics and image.
    """
    def __init__(self, pos, fruit_name, radius, space, **kwargs):
        super().__init__(**kwargs)
        self.size = (radius * 2, radius * 2)
        self.radius = radius
        self.fruit_name = fruit_name
        self.alive = True

        # Physics body and shape
        mass = DENSITY * (3.1415 * radius * radius)
        moment = pymunk.moment_for_circle(mass, 0, radius)
        self.body = pymunk.Body(mass, moment)
        self.body.position = pos
        self.shape = pymunk.Circle(self.body, radius)
        self.shape.elasticity = ELASTICITY
        self.shape.friction = FRICTION
        space.add(self.body, self.shape)

        # Fruit image
        image_path = os.path.join(ASSETS_DIR, f"{fruit_name}.png")
        self.image = Image(source=image_path, size=self.size)
        self.add_widget(self.image)

    def update(self):
        """
        Sync the Kivy widget position with the pymunk body.
        """
        if self.alive:
            x, y = self.body.position
            self.pos = (x - self.radius, y - self.radius)
            self.image.pos = self.pos

    def kill(self, space):
        """
        Remove the fruit from the game and physics space.
        """
        self.alive = False
        self.remove_widget(self.image)
        space.remove(self.body, self.shape)