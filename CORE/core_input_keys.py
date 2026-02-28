from __future__ import annotations

import pyray as pr

# Version checked: raylib 5.x/pyray API parity (reviewed 2026-02-28).

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 450

KEY_RIGHT = getattr(pr, "KEY_RIGHT", 262)
KEY_LEFT = getattr(pr, "KEY_LEFT", 263)
KEY_UP = getattr(pr, "KEY_UP", 265)
KEY_DOWN = getattr(pr, "KEY_DOWN", 264)


def main() -> None:
    """Run the input-keys example."""
    pr.init_window(SCREEN_WIDTH, SCREEN_HEIGHT, "raylib [core] example - input keys")

    ball_position = pr.Vector2(SCREEN_WIDTH / 2.0, SCREEN_HEIGHT / 2.0)
    pr.set_target_fps(60)

    while not pr.window_should_close():
        if pr.is_key_down(KEY_RIGHT):
            ball_position.x += 2.0
        if pr.is_key_down(KEY_LEFT):
            ball_position.x -= 2.0
        if pr.is_key_down(KEY_UP):
            ball_position.y -= 2.0
        if pr.is_key_down(KEY_DOWN):
            ball_position.y += 2.0

        pr.begin_drawing()
        pr.clear_background(pr.RAYWHITE)
        pr.draw_text("move the ball with arrow keys", 10, 10, 20, pr.DARKGRAY)
        pr.draw_circle_v(ball_position, 50.0, pr.MAROON)
        pr.end_drawing()

    pr.close_window()


if __name__ == "__main__":
    main()
