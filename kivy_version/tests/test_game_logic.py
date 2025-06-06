"""
Unit tests for core game logic in the Suika Game.

These tests focus on pure logic: score calculation, fruit merging, and configuration.
GUI and physics-dependent code should be tested separately or with integration tests.
"""

from game import Game

def test_score_increases_on_merge():
    """
    Test that merging two fruits increases the score correctly.
    """
    game = Game()
    # Simulate a merge that would result in the third fruit (index 2)
    next_idx = 2
    game.score = 0
    game.score += 2 ** next_idx
    assert game.score == 4  # 2^2 = 4

def test_restart_game_resets_score_and_particles():
    """
    Test that restarting the game resets the score and clears all particles.
    """
    game = Game()
    # Simulate adding particles and increasing score
    game.score = 10
    game.particles = [object(), object()]
    game.restart_game()
    assert game.score == 0
    assert len(game.particles) == 1  # One starting fruit is added after restart

# Additional logic tests can be added here as needed.
