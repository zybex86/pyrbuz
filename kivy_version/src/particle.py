"""
Defines the Particle (fruit) class for the Suika Game.

Encapsulates all logic related to a single fruit, including physics, rendering,
and interaction with the game space.
"""

import os
from kivy.uix.widget import Widget
from kivy.uix.image import Image
import pymunk
from config import (
    ASSETS_DIR,
    DENSITY, ELASTICITY, FRICTION,
)

class Particle(Widget):
    """
    Represents a single fruit in the game, with physics and image.

    Attributes:
        body (pymunk.Body): The physics body for the fruit.
        shape (pymunk.Shape): The physics shape for the fruit.
        image (Image): The Kivy image widget for rendering.
        fruit_name (str): Name of the fruit.
        radius (float): Radius of the fruit.
        alive (bool): Whether the fruit is active in the game.
    """
    def __init__(self, pos, fruit_name, radius, space, **kwargs):
        super().__init__(**kwargs)
        self.size = (radius * 2, radius * 2)
        self.radius = radius
        self.fruit_name = fruit_name
        self.alive = True

        # Calculate mass using density and area (πr²)
        mass = DENSITY * (3.1415 * radius * radius)
        moment = pymunk.moment_for_circle(mass, 0, radius)
        self.body = pymunk.Body(mass, moment)
        self.body.position = pos
        self.body.user_data = self  # <-- Add this line!

        # Create the shape and set elasticity and friction
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