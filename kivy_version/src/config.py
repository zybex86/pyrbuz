"""
Configuration settings for the Suika Game.

This module contains constants and settings used throughout the game.
"""

import os

# Window size (width, height)
WINDOW_SIZE = (570, 770)

# Padding for the play area (left/right, top)
PADDING = (24, 160)

# Fruit types and their corresponding image filenames
FRUIT_TYPES = [
    "apple.png",
    "cherry.png",
    "grapes.png",
    "melon.png",
    "orange.png",
    "peach.png",
    "pear.png",
    "persimmon.png",
    "pineapple.png",
    "strawberry.png",
    "watermelon.png",
]

# Fruit radii (pixels)
FRUIT_RADII = [17, 25, 32, 38, 50, 63, 75, 87, 100, 115, 135]

# Game physics settings
GRAVITY = 2000
DAMPING = 0.8

# Colors (R, G, B)
BACKGROUND_COLOR = (250, 240, 140)
WALL_COLOR = (250, 190, 58)

# Directory for assets (images, sounds, etc.)
ASSETS_DIR = os.path.join(os.path.dirname(__file__), "assets")

# Physics constants
DENSITY = 0.001
ELASTICITY = 0.5
FRICTION = 0.8

class Config:
    def __init__(self):
        self.screen_width = 1280
        self.screen_height = 720
        self.fps = 60
        self.background_color = (250, 240, 140)
        self.fruit_colors = {
            "cherry": (245, 0, 0),
            "strawberry": (250, 100, 100),
            "grapes": (150, 20, 250),
            "orange": (250, 210, 10),
            "persimmon": (250, 150, 0),
            "apple": (245, 0, 0),
            "pear": (250, 250, 100),
            "peach": (255, 180, 180),
            "pineapple": (255, 255, 0),
            "melon": (180, 215, 10),
            "watermelon": (0, 185, 0),
        }
        self.gravity = 600
        self.damping = 0.8
        self.elasticity = 0.1
        self.density = 0.001
        self.friction = 0.4
        self.impulse = 10000
        self.radius = {
            "cherry": 17,
            "strawberry": 21,
            "grapes": 29,
            "orange": 35,
            "persimmon": 45,
            "apple": 56,
            "pear": 65,
            "peach": 78,
            "pineapple": 87,
            "melon": 109,
            "watermelon": 125,
        }