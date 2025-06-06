"""
Physics setup and wall management for the Suika Game.

Provides functions to add static boundaries (floor and walls)
to the pymunk physics space, ensuring fruits stay within the play area.
"""

import pymunk

def add_walls(space, play_area_x, play_area_y, play_area_width, play_area_height, thickness=10):
    """
    Add static floor and side walls to the pymunk space.

    Args:
        space (pymunk.Space): The physics space to add walls to.
        play_area_x (int): X coordinate of the play area origin.
        play_area_y (int): Y coordinate of the play area origin.
        play_area_width (int): Width of the play area.
        play_area_height (int): Height of the play area.
        thickness (int): Thickness of the wall segments.
    """
    static_body = space.static_body
    x0, y0 = play_area_x, play_area_y
    x1, y1 = play_area_x + play_area_width, play_area_y + play_area_height

    # Define floor and walls as static segments
    floor = pymunk.Segment(static_body, (x0, y0), (x1, y0), thickness)
    left = pymunk.Segment(static_body, (x0, y0), (x0, y1), thickness)
    right = pymunk.Segment(static_body, (x1, y0), (x1, y1), thickness)

    for wall in (floor, left, right):
        wall.elasticity = 0.8
        wall.friction = 1.0
        space.add(wall)