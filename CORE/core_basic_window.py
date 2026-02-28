from __future__ import annotations

import pyray as pr

# Version checked: raylib 5.x/pyray API parity (reviewed 2026-02-28).

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 450


def main() -> None:
    """Run the basic window example."""
    pr.init_window(SCREEN_WIDTH, SCREEN_HEIGHT, "raylib [core] example - basic window")
    pr.set_target_fps(60)

    while not pr.window_should_close():
        pr.begin_drawing()
        pr.clear_background(pr.RAYWHITE)
        pr.draw_text(
            "Congrats! You created your first window!", 190, 200, 20, pr.LIGHTGRAY
        )
        pr.end_drawing()

    pr.close_window()


if __name__ == "__main__":
    main()
