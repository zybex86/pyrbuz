# File: kivy_version/src/game.py
# Main game logic for the Kivy version of Suika Game using fruit images.
# This version ensures the play area is always centered, regardless of window size.

import os
import random
import time
import pymunk
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.image import Image
from kivy.clock import Clock
from kivy.graphics import Color, Rectangle, Line
from kivy.core.window import Window

from config import FRUIT_TYPES, FRUIT_RADII
from particle import Particle  # Import the Particle class from the new module
from physics import add_walls  # Add this import

ASSETS_DIR = os.path.join(os.path.dirname(__file__), "assets")

SELECTABLE_FRUITS = FRUIT_TYPES[:4]
SELECTABLE_RADII = FRUIT_RADII[:4]

# Physics constants
GRAVITY = 2000
DENSITY = 0.001
ELASTICITY = 0.5
FRICTION = 0.8

# Wall and background colors
BACKGROUND_COLOR = (250/255, 240/255, 140/255, 1)
WALL_COLOR = (0.2, 0.3, 0.7, 1)  # Distinct blue

class Game(Widget):
    """
    Main game widget. Manages all particles, user controls, and game updates.
    Ensures the play area is always centered and adapts to window resizing.
    """
    DROP_COOLDOWN = 0.5  # Minimum seconds between drops

    def __init__(self, **kwargs):
        """
        Initialize the game state, background, and schedule updates.
        Optimized for tablets in landscape mode.
        """
        super().__init__(**kwargs)
        # Set initial size to match the window
        self.size = Window.size
        self.particles = []
        self.last_drop_time = 0

        # Physics space
        self.space = pymunk.Space()
        self.space.gravity = (0, -GRAVITY)

        # Draw background color
        with self.canvas.before:
            Color(*BACKGROUND_COLOR)
            self.bg_rect = Rectangle(pos=self.pos, size=self.size)
        self.bind(pos=self._update_bg, size=self._update_bg)

        # Draw visible walls (will be updated in _update_play_area)
        with self.canvas:
            Color(*WALL_COLOR)
            self.wall_thickness = 8
            self.left_wall = Line(points=[], width=self.wall_thickness)
            self.right_wall = Line(points=[], width=self.wall_thickness)
            self.floor_wall = Line(points=[], width=self.wall_thickness)

        # Initialize play area and walls
        self._update_play_area()
        self._add_walls()

        # Add a test particle in the center of the play area (random selectable fruit)
        fruit_name, radius = self._get_random_selectable_fruit()
        self.add_particle((self.play_area_x + self.play_area_width // 2, self.play_area_y + self.play_area_height - 100), fruit_name, radius)

        # Prepare next fruit preview (only from selectable fruits)
        self.next_fruit_name, self.next_fruit_radius = self._get_random_selectable_fruit()
        self.next_fruit_x = self.play_area_x + self.play_area_width // 2
        self.next_fruit_preview = Image(
            source=os.path.join(ASSETS_DIR, f"{self.next_fruit_name}.png"),
            size=(self.next_fruit_radius * 2, self.next_fruit_radius * 2),
            pos=(self.next_fruit_x - self.next_fruit_radius, self.play_area_y + self.play_area_height - 80)
        )
        self.add_widget(self.next_fruit_preview)

        # Listen for window resize events to keep play area centered
        Window.bind(size=self._on_window_resize)

        # Schedule the update method to be called every frame.
        Clock.schedule_interval(self.update, 1.0 / 60.0)

    def _update_play_area(self):
        """
        Calculate and update the play area to always be centered and 80% of the window size.
        """
        self.screen_width, self.screen_height = self.size
        self.play_area_width = int(self.screen_width * 0.8)
        self.play_area_height = int(self.screen_height * 0.8)
        self.play_area_x = (self.screen_width - self.play_area_width) // 2
        self.play_area_y = (self.screen_height - self.play_area_height) // 2

        # Update wall lines
        self.left_wall.points = [
            self.play_area_x, self.play_area_y,
            self.play_area_x, self.play_area_y + self.play_area_height
        ]
        self.right_wall.points = [
            self.play_area_x + self.play_area_width, self.play_area_y,
            self.play_area_x + self.play_area_width, self.play_area_y + self.play_area_height
        ]
        self.floor_wall.points = [
            self.play_area_x, self.play_area_y,
            self.play_area_x + self.play_area_width, self.play_area_y
        ]

    def _add_walls(self):
        """
        Add static floor and side walls to the pymunk space, matching the visible walls.
        """
        # Remove previous walls if any
        for s in self.space.shapes[:]:
            if isinstance(s, pymunk.Segment):
                self.space.remove(s)
        thickness = 10
        static_body = self.space.static_body
        x0, y0 = self.play_area_x, self.play_area_y
        x1, y1 = self.play_area_x + self.play_area_width, self.play_area_y + self.play_area_height
        # Floor
        floor = pymunk.Segment(static_body, (x0, y0), (x1, y0), thickness)
        # Left wall
        left = pymunk.Segment(static_body, (x0, y0), (x0, y1), thickness)
        # Right wall
        right = pymunk.Segment(static_body, (x1, y0), (x1, y1), thickness)
        for wall in (floor, left, right):
            wall.elasticity = 0.8
            wall.friction = 1.0
            self.space.add(wall)
        add_walls(self.space, self.play_area_x, self.play_area_y, self.play_area_width, self.play_area_height)

    def _update_bg(self, *args):
        self.bg_rect.pos = self.pos
        self.bg_rect.size = self.size
        self._update_play_area()
        self._add_walls()
        # Update preview fruit position to stay at the top of the play area
        self.next_fruit_x = self.play_area_x + self.play_area_width // 2
        self.next_fruit_preview.pos = (self.next_fruit_x - self.next_fruit_radius, self.play_area_y + self.play_area_height - 80)

    def _on_window_resize(self, instance, size):
        """
        Handle window resize events to keep the play area centered and update all dependent elements.
        """
        self.size = size
        self._update_bg()

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
        particle = Particle(pos, fruit_name, radius, self.space)
        self.particles.append(particle)
        self.add_widget(particle)

    def update(self, dt):
        """
        Step the physics simulation and update all particles each frame.

        Args:
            dt (float): Time since last update.
        """
        self.space.step(dt)
        for particle in self.particles:
            particle.update()

    def on_touch_move(self, touch):
        """
        Move the preview fruit horizontally with the user's finger/mouse, clamped to play area.
        """
        if self.collide_point(*touch.pos):
            min_x = self.play_area_x + SELECTABLE_RADII[-1]
            max_x = self.play_area_x + self.play_area_width - SELECTABLE_RADII[-1]
            self.next_fruit_x = min(max(touch.x, min_x), max_x)
            self.next_fruit_preview.pos = (self.next_fruit_x - self.next_fruit_radius, self.play_area_y + self.play_area_height - 80)
        return super().on_touch_move(touch)

    def on_touch_down(self, touch):
        """
        Handle user touch/click to drop a fruit at the touched x position.
        Enforces a cooldown between drops.
        Only allows dropping selectable fruits.
        """
        now = time.time()
        if self.collide_point(*touch.pos):
            if now - self.last_drop_time >= self.DROP_COOLDOWN:
                min_x = self.play_area_x + SELECTABLE_RADII[-1]
                max_x = self.play_area_x + self.play_area_width - SELECTABLE_RADII[-1]
                drop_x = min(max(touch.x, min_x), max_x)
                drop_y = self.play_area_y + self.play_area_height - 100  # Drop from near the top of play area
                self.add_particle((drop_x, drop_y), self.next_fruit_name, self.next_fruit_radius)
                self.last_drop_time = now
                # Prepare next fruit (only from selectable)
                self.next_fruit_name, self.next_fruit_radius = self._get_random_selectable_fruit()
                self.next_fruit_preview.source = os.path.join(ASSETS_DIR, f"{self.next_fruit_name}.png")
                self.next_fruit_preview.size = (self.next_fruit_radius * 2, self.next_fruit_radius * 2)
                self.next_fruit_preview.pos = (self.next_fruit_x - self.next_fruit_radius, self.play_area_y + self.play_area_height - 80)
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
