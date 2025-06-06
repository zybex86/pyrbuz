"""
Main game logic and state management for the Kivy Suika Game.

This module defines the Game widget, which manages the play area, physics,
game state, user input, and UI updates.
"""

import os
import random
import time
import pymunk
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.image import Image
from kivy.clock import Clock
from kivy.uix.label import Label
from kivy.graphics import Color, Rectangle, Line
from kivy.core.window import Window

from config import (
    ASSETS_DIR, FRUIT_TYPES, FRUIT_RADII,
    GRAVITY,
    BACKGROUND_COLOR, WALL_COLOR
)
from particle import Particle  # Import the Particle class from the new module
from physics import add_walls  # Add this import
from widgets import NextFruitPreview, ScoreLabel  # Import the ScoreLabel widget

SELECTABLE_FRUITS = FRUIT_TYPES[:4]
SELECTABLE_RADII = FRUIT_RADII[:4]

# Wall and background colors
BACKGROUND_COLOR = (250/255, 240/255, 140/255, 1)
WALL_COLOR = (0.2, 0.3, 0.7, 1)  # Distinct blue

class Game(Widget):
    """
    Main game widget for Suika Game.

    Responsibilities:
        - Manages all fruit particles and their physics.
        - Handles user input for dropping and moving fruits.
        - Updates score, game over state, and UI elements.
        - Ensures the play area is always centered and responsive to window resizing.

    Attributes:
        particles (list): List of all active Particle instances.
        score (int): Current player score.
        game_over (bool): Whether the game is over.
        next_fruit_name (str): Name of the next fruit to drop.
        next_fruit_radius (float): Radius of the next fruit to drop.
        next_fruit_preview (NextFruitPreview): Widget showing the next fruit.
        ...
    """
    GAME_OVER_MARGIN = 40  # Margin from the top of the play area for game over detection
    DROP_COOLDOWN = 0.5  # Minimum seconds between drops

    def __init__(self, **kwargs):
        # --- Initialize all attributes needed by event handlers BEFORE super().__init__ ---
        self.size = Window.size
        self.particles = []
        self.last_drop_time = 0
        self.score = 0
        self.game_over = False
        self.game_over_label = None

        # Now call super().__init__ (this may trigger on_kv_post)
        super().__init__(**kwargs)

        # Physics space
        self.space = pymunk.Space()
        self.space.gravity = (0, -GRAVITY)
        self._register_merge_handler()

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

        # Draw the game over line (dotted) at the top of the play area
        with self.canvas:
            Color(0.8, 0, 0, 0.5)  # Red color for the game over line
            self.game_over_line = Line(
                points=[],
                width=2,
                dash_offset=5,
                dash_length=10
            )

        # Initialize play area and walls
        self._update_play_area()
        self._add_walls()

        # Add a test particle in the center of the play area (random selectable fruit)
        # fruit_name, radius = self._get_random_selectable_fruit()
        # self.add_particle((self.play_area_x + self.play_area_width // 2, self.play_area_y + self.play_area_height - 100), fruit_name, radius)

        # Prepare next fruit preview (only from selectable fruits)
        self.next_fruit_name, self.next_fruit_radius = self._get_random_selectable_fruit()
        self.next_fruit_preview = NextFruitPreview(
            self.next_fruit_name, self.next_fruit_radius,
            self.play_area_x, self.play_area_y, self.play_area_width, self.play_area_height
        )
        self.add_widget(self.next_fruit_preview)

        # Listen for window resize events to keep play area centered
        Window.bind(size=self._on_window_resize)

        # Schedule the update method to be called every frame.
        Clock.schedule_interval(self.update, 1.0 / 60.0)

    def update_score_label(self):
        """
        Update the score label widget with the current score.
        """
        self.ids.score_label.update_score(self.score)

    def _register_merge_handler(self):
        """
        Register a collision handler for merging fruits of the same type.
        """
        handler = self.space.add_default_collision_handler()
        handler.begin = self._on_fruit_collision

    def _on_fruit_collision(self, arbiter, space, data):
        """
        Handle collision between two fruits. Merge if they are the same type.
        Only process if both bodies have a 'user_data' attribute.
        """
        shape_a, shape_b = arbiter.shapes

        # Check if both bodies have 'user_data' (i.e., are fruits)
        particle_a = getattr(shape_a.body, "user_data", None)
        particle_b = getattr(shape_b.body, "user_data", None)

        # Prevent double-processing or merging dead particles
        if not (particle_a and particle_b):
            return True
        if not (hasattr(particle_a, "fruit_name") and hasattr(particle_b, "fruit_name")):
            return True
        if not (getattr(particle_a, "alive", True) and getattr(particle_b, "alive", True)):
            return True

        if particle_a.fruit_name == particle_b.fruit_name:
            try:
                idx = FRUIT_TYPES.index(f"{particle_a.fruit_name}.png")
                next_idx = idx + 1
                # Only merge if there is a next fruit
                if next_idx < len(FRUIT_TYPES):
                    next_fruit = FRUIT_TYPES[next_idx].replace(".png", "")
                    next_radius = FRUIT_RADII[next_idx]
                    # Mark as dead before spawning new fruit to prevent re-entrancy
                    particle_a.alive = False
                    particle_b.alive = False
                    # Merge at average position
                    x = (particle_a.body.position.x + particle_b.body.position.x) / 2
                    y = (particle_a.body.position.y + particle_b.body.position.y) / 2
                    self.add_particle((x, y), next_fruit, next_radius)
                    # Remove merged fruits
                    particle_a.kill(self.space)
                    particle_b.kill(self.space)
                    if particle_a in self.particles:
                        self.particles.remove(particle_a)
                    if particle_b in self.particles:
                        self.particles.remove(particle_b)
                    # Update score: add points based on fruit size (example: 2^(next_idx))
                    self.score += 2 ** next_idx
                    self.update_score_label()
                    return False  # Prevent default collision resolution (they are gone)
                # If there is no next fruit, do not remove or merge
            except ValueError:
                pass

        return True  # Continue normal collision

    def _update_play_area(self):
        """
        Calculate and update the play area to always be centered and 80% of the window size.
        Also update the position of the game over line.
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

        # Place the game over line at a fixed distance from the top (not based on fruit radius)
        # This avoids issues with preview or large fruits triggering game over immediately.
        line_y = self.play_area_y + self.play_area_height - self.GAME_OVER_MARGIN
        self.game_over_line.points = [
            self.play_area_x, line_y,
            self.play_area_x + self.play_area_width, line_y
        ]
        # Make the line dotted (Kivy 2.2+ supports dash_length and dash_offset)
        self.game_over_line.dash_length = 10
        self.game_over_line.dash_offset = 5

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
        self.next_fruit_preview.update_position(
            self.play_area_x, self.play_area_y, self.play_area_width, self.play_area_height
        )

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
        # Store reference for collision logic
        self.particles.append(particle)
        self.add_widget(particle)

    def update(self, dt):
        """
        Step the physics simulation and update all particles each frame.
        Also check for game over condition.
        """
        if self.game_over:
            return  # Stop updating if game is over

        self.space.step(dt)
        for particle in self.particles:
            particle.update()

        # Check for game over: any fruit above the dotted line?
        # Use the fruit's center (body.position.y) + radius to check the top edge of the fruit
        line_y = self.play_area_y + self.play_area_height - self.GAME_OVER_MARGIN
        for particle in self.particles:
            # Only check for game over if the fruit's top is above the line
            if particle.alive and (particle.body.position.y + particle.radius) > line_y:
                self.trigger_game_over()
                break

    def trigger_game_over(self):
        """
        Handle the game over state: show message, disable input, and stop updates.
        """
        self.game_over = True

        # Show a game over label in the center of the play area
        if not self.game_over_label:
            self.game_over_label = Label(
                text="GAME OVER",
                font_size=48,
                color=(1, 0, 0, 1),
                size_hint=(None, None),
                size=(400, 100),
                pos=(self.play_area_x + self.play_area_width // 2 - 200,
                     self.play_area_y + self.play_area_height // 2 - 50)
            )
            self.add_widget(self.game_over_label)

    def restart_game(self):
        """
        Reset the game state to its initial configuration.

        This method removes all fruit particles, resets the score and physics space,
        updates the next fruit preview, and clears the game over state.
        """
        # Remove all fruit particles from the game area and physics space
        for particle in self.particles[:]:
            particle.kill(self.space)
            self.remove_widget(particle)
        self.particles.clear()

        # Reset the score and update the score label
        self.score = 0
        self.update_score_label()

        # Reset the physics space (remove all shapes except static walls)
        for shape in self.space.shapes[:]:
            if not isinstance(shape, pymunk.Segment):
                self.space.remove(shape.body, shape)

        # Add a new starting fruit in the center of the play area
        fruit_name, radius = self._get_random_selectable_fruit()
        self.add_particle(
            (self.play_area_x + self.play_area_width // 2, self.play_area_y + self.play_area_height - 100),
            fruit_name,
            radius
        )

        # Reset the next fruit preview
        self.next_fruit_name, self.next_fruit_radius = self._get_random_selectable_fruit()
        self.next_fruit_preview.update_preview(
            self.next_fruit_name, self.next_fruit_radius,
            self.play_area_x, self.play_area_y, self.play_area_width, self.play_area_height
        )

        # Reset pending drop position to center
        self._pending_drop_x = self.play_area_x + self.play_area_width // 2

        # Reset game over state and remove label if present
        self.game_over = False
        if self.game_over_label:
            self.remove_widget(self.game_over_label)
            self.game_over_label = None

    def on_touch_down(self, touch):
        """
        On touch down, move the preview fruit horizontally to the touched x position,
        but do not drop the fruit yet.
        """
        if self.game_over:
            return super().on_touch_down(touch)

        # Only respond to touches inside the play area (not on UI)
        if not (self.play_area_x <= touch.x <= self.play_area_x + self.play_area_width and
                self.play_area_y <= touch.y <= self.play_area_y + self.play_area_height):
            return super().on_touch_down(touch)

        # Move the preview fruit horizontally, clamp within play area
        preview_x = min(max(touch.x, self.play_area_x + self.next_fruit_radius),
                        self.play_area_x + self.play_area_width - self.next_fruit_radius)
        # Keep the preview at the same y as before
        preview_y = self.play_area_y + self.play_area_height - self.next_fruit_radius + 10
        self.next_fruit_preview.pos = (preview_x - self.next_fruit_radius, preview_y)
        self._pending_drop_x = preview_x  # Store for use in on_touch_up
        return super().on_touch_down(touch)

    def on_touch_move(self, touch):
        """
        Allow dragging the preview fruit horizontally while holding down.
        """
        if self.game_over:
            return False

        if not (self.play_area_x <= touch.x <= self.play_area_x + self.play_area_width and
                self.play_area_y <= touch.y <= self.play_area_y + self.play_area_height):
            return False

        preview_x = min(max(touch.x, self.play_area_x + self.next_fruit_radius),
                        self.play_area_x + self.play_area_width - self.next_fruit_radius)
        preview_y = self.play_area_y + self.play_area_height - self.next_fruit_radius + 10
        self.next_fruit_preview.pos = (preview_x - self.next_fruit_radius, preview_y)
        self._pending_drop_x = preview_x
        return super().on_touch_move(touch)

    def on_touch_up(self, touch):
        """
        On touch up, drop the fruit at the last preview position if allowed.
        """
        if self.game_over:
            return False

        # Enforce drop cooldown
        now = time.time()
        if now - self.last_drop_time < self.DROP_COOLDOWN:
            return False

        # Only drop if the touch ended inside the play area
        if not (self.play_area_x <= touch.x <= self.play_area_x + self.play_area_width and
                self.play_area_y <= touch.y <= self.play_area_y + self.play_area_height):
            return False

        # Use the last preview x position, or default to center if not set
        drop_x = getattr(self, "_pending_drop_x", self.play_area_x + self.play_area_width // 2)
        drop_y = self.play_area_y + self.play_area_height - 80  # 80px below the top

        self.add_particle((drop_x, drop_y), self.next_fruit_name, self.next_fruit_radius)
        self.last_drop_time = now

        # Prepare the next fruit preview (reset to center)
        self.next_fruit_name, self.next_fruit_radius = self._get_random_selectable_fruit()
        self.next_fruit_preview.update_preview(
            self.next_fruit_name, self.next_fruit_radius,
            self.play_area_x, self.play_area_y, self.play_area_width, self.play_area_height
        )
        self._pending_drop_x = self.play_area_x + self.play_area_width // 2  # Reset
        return super().on_touch_up(touch)

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
