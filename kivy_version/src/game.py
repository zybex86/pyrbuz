# File: kivy_version/src/game.py
# Main game logic for the Kivy version of Suika Game.
# This module defines the Particle and Game classes, handling game state and rendering.

from kivy.app import App
from kivy.uix.widget import Widget
from kivy.clock import Clock
from kivy.graphics import Color, Ellipse
import random

class Particle(Widget):
    """
    Represents a single fruit in the game.
    Handles its position, drawing, and alive state.
    """
    def __init__(self, pos, radius, **kwargs):
        """
        Initialize a Particle (fruit) at a given position and radius.

        Args:
            pos (tuple): (x, y) position of the particle.
            radius (float): Radius of the fruit.
        """
        super().__init__(**kwargs)
        self.size = (radius * 2, radius * 2)
        self.pos = pos
        self.radius = radius
        self.alive = True
        # Draw the fruit as a colored ellipse.
        with self.canvas:
            Color(random.random(), random.random(), random.random())
            self.ellipse = Ellipse(pos=self.pos, size=self.size)

    def update(self):
        """
        Update the position of the ellipse if the particle is alive.
        """
        if self.alive:
            self.ellipse.pos = self.pos

    def kill(self):
        """
        Mark the particle as dead and remove its visual representation.
        """
        self.alive = False
        self.canvas.remove(self.ellipse)

class Game(Widget):
    """
    Main game widget. Manages all particles and game updates.
    """
    def __init__(self, **kwargs):
        """
        Initialize the game state and schedule updates.
        """
        super().__init__(**kwargs)
        self.particles = []
        # Schedule the update method to be called every frame.
        Clock.schedule_interval(self.update, 1.0 / 60.0)

    def add_particle(self, pos, radius):
        """
        Add a new particle (fruit) to the game.

        Args:
            pos (tuple): (x, y) position for the new particle.
            radius (float): Radius of the new fruit.
        """
        particle = Particle(pos, radius)
        self.particles.append(particle)
        self.add_widget(particle)

    def update(self, dt):
        """
        Update all particles each frame.

        Args:
            dt (float): Time since last update (unused).
        """
        for particle in self.particles:
            particle.update()

class GameApp(App):
    """
    Kivy App class for running the game standalone.
    """
    def build(self):
        """
        Build and return the main game widget.
        """
        game = Game()
        return game

if __name__ == '__main__':
    # Entry point for running the game directly.
    GameApp().run()