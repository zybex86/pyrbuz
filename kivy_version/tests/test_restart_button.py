"""
Integration test for the Restart button in the Suika Game.

This test checks that pressing the Restart button triggers the correct method.
"""

from kivy.base import EventLoop
from game import Game

def test_restart_button_triggers_restart(monkeypatch):
    """
    Test that pressing the restart button calls the restart_game method.
    """
    game = Game()
    called = {}

    def fake_restart_game():
        called['restart'] = True

    game.restart_game = fake_restart_game
    EventLoop.ensure_window()
    # Simulate button press via the ScoreLabel's parent (BoxLayout)
    for child in game.ids.score_label.parent.children:
        if hasattr(child, 'text') and child.text == "Restart":
            child.dispatch('on_release')
            break
    assert called.get('restart', False)

# Note: This test assumes the widget tree is built as in your KV file.
