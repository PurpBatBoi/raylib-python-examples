from __future__ import annotations

import pyray as pr

# Version checked: raylib 5.x/pyray API parity (reviewed 2026-02-28).

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 450


def update_draw_frame() -> None:
    """Update and draw one frame."""
    pr.begin_drawing()
    pr.clear_background(pr.RAYWHITE)
    pr.draw_text("Welcome to raylib web structure!", 220, 200, 20, pr.SKYBLUE)
    pr.end_drawing()


def main() -> None:
    """Run the web-structure example."""
    pr.init_window(SCREEN_WIDTH, SCREEN_HEIGHT, "raylib [core] example - window web")
    pr.set_target_fps(60)

    while not pr.window_should_close():
        update_draw_frame()

    pr.close_window()


if __name__ == "__main__":
    main()
