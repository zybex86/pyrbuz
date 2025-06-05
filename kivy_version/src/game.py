# File: kivy_version/src/game.py
# Main game logic for the Kivy version of Suika Game using fruit images.

import os
import random
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.image import Image
from kivy.clock import Clock
from kivy.graphics import Color, Rectangle

from config import FRUIT_TYPES, FRUIT_RADII

ASSETS_DIR = os.path.join(os.path.dirname(__file__), "assets")

# Only allow the first 3 smallest fruits to be selectable
SELECTABLE_FRUITS = FRUIT_TYPES[:3]
SELECTABLE_RADII = FRUIT_RADII[:3]

class Particle(Widget):
    """
    Represents a single fruit in the game, displayed as an image.
    """
    def __init__(self, pos, fruit_name, radius, **kwargs):
        """
        Initialize a Particle (fruit) at a given position, with a given fruit type and radius.

        Args:
            pos (tuple): (x, y) position of the particle.
            fruit_name (str): Name of the fruit (e.g., "apple").
            radius (float): Radius of the fruit.
        """
        super().__init__(**kwargs)
        self.size = (radius * 2, radius * 2)
        self.pos = (pos[0] - radius, pos[1] - radius)  # Center the image
        self.radius = radius
        self.fruit_name = fruit_name
        self.alive = True

        # Path to the fruit image
        image_path = os.path.join(ASSETS_DIR, f"{fruit_name}.png")
        # Add the fruit image as a child widget
        self.image = Image(source=image_path, size=self.size, pos=self.pos)
        self.add_widget(self.image)

    def update(self):
        """
        Update the position of the fruit image if the particle is alive.
        """
        if self.alive:
            self.image.pos = self.pos

    def kill(self):
        """
        Mark the particle as dead and remove its visual representation.
        """
        self.alive = False
        self.remove_widget(self.image)

class Game(Widget):
    """
    Main game widget. Manages all particles, user controls, and game updates.
    Implements drop rate limiting and random fruit radii.
    Only the first 3 smallest fruits are selectable.
    """
    DROP_COOLDOWN = 0.5  # Minimum seconds between drops

    def __init__(self, **kwargs):
        """
        Initialize the game state, background, and schedule updates.
        """
        super().__init__(**kwargs)
        # Draw background color
        with self.canvas.before:
            Color(250/255, 240/255, 140/255, 1)
            self.bg_rect = Rectangle(pos=self.pos, size=self.size)
        self.bind(pos=self._update_bg, size=self._update_bg)

        self.particles = []
        self.last_drop_time = 0  # Timestamp of last drop

        # Add a test particle in the center of the screen (random selectable fruit)
        fruit_name, radius = self._get_random_selectable_fruit()
        self.add_particle((285, 385), fruit_name, radius)

        # Prepare next fruit preview (only from selectable fruits)
        self.next_fruit_name, self.next_fruit_radius = self._get_random_selectable_fruit()
        self.next_fruit_x = self.width // 2  # Default drop position
        self.bind(size=self._on_size)

        self.next_fruit_preview = Image(
            source=os.path.join(ASSETS_DIR, f"{self.next_fruit_name}.png"),
            size=(self.next_fruit_radius * 2, self.next_fruit_radius * 2),
            pos=(self.next_fruit_x - self.next_fruit_radius, self.height - 80)
        )
        self.add_widget(self.next_fruit_preview)

        # Schedule the update method to be called every frame.
        Clock.schedule_interval(self.update, 1.0 / 60.0)

    def _update_bg(self, *args):
        self.bg_rect.pos = self.pos
        self.bg_rect.size = self.size

    def _on_size(self, *args):
        # Update default drop position when window size changes
        self.next_fruit_x = self.width // 2
        self.next_fruit_preview.pos = (self.next_fruit_x - self.next_fruit_radius, self.height - 80)

    def _get_random_selectable_fruit(self):
        """
        Select a random fruit name and its corresponding radius from the selectable fruits.
        Returns:
            tuple: (fruit_name, radius)
        """
        idx = random.randint(0, len(SELECTABLE_FRUITS) - 1)
        fruit_name = SELECTABLE_FRUITS[idx].replace('.png', '')
        radius = SELECTABLE_RADII[idx]
        return fruit_name, radius

    def add_particle(self, pos, fruit_name, radius):
        """
        Add a new particle (fruit) to the game.

        Args:
            pos (tuple): (x, y) position for the new particle.
            fruit_name (str): Name of the fruit.
            radius (float): Radius of the new fruit.
        """
        particle = Particle(pos, fruit_name, radius)
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

    def on_touch_move(self, touch):
        """
        Move the preview fruit horizontally with the user's finger/mouse.
        """
        if self.collide_point(*touch.pos):
            self.next_fruit_x = touch.x
            self.next_fruit_preview.pos = (self.next_fruit_x - self.next_fruit_radius, self.height - 80)
        return super().on_touch_move(touch)

    def on_touch_down(self, touch):
        """
        Handle user touch/click to drop a fruit at the touched x position.
        Enforces a cooldown between drops.
        Only allows dropping selectable fruits.
        """
        import time
        now = time.time()
        if self.collide_point(*touch.pos):
            if now - self.last_drop_time >= self.DROP_COOLDOWN:
                drop_x = touch.x
                drop_y = self.height - 100  # Drop from near the top
                self.add_particle((drop_x, drop_y), self.next_fruit_name, self.next_fruit_radius)
                self.last_drop_time = now
                # Prepare next fruit (only from selectable)
                self.next_fruit_name, self.next_fruit_radius = self._get_random_selectable_fruit()
                self.next_fruit_preview.source = os.path.join(ASSETS_DIR, f"{self.next_fruit_name}.png")
                self.next_fruit_preview.size = (self.next_fruit_radius * 2, self.next_fruit_radius * 2)
                self.next_fruit_preview.pos = (self.next_fruit_x - self.next_fruit_radius, self.height - 80)
        return super().on_touch_down(touch)

class GameApp(App):
    """
    Kivy App class for running the game standalone.
    """
    def build(self):
        """
        Build and return the main game widget.
        """
        return Game()

if __name__ == '__main__':
    # Entry point for running the game directly.
    GameApp().run()