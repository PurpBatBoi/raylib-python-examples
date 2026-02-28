from __future__ import annotations

import pyray as pr

# Version checked: raylib 5.x/pyray API parity (reviewed 2026-02-28).

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 450


def main() -> None:
    """Run the input-mouse-wheel example."""
    pr.init_window(
        SCREEN_WIDTH,
        SCREEN_HEIGHT,
        "raylib [core] example - input mouse wheel",
    )

    box_position_y = SCREEN_HEIGHT // 2 - 40
    scroll_speed = 4

    pr.set_target_fps(60)

    while not pr.window_should_close():
        box_position_y -= int(pr.get_mouse_wheel_move() * scroll_speed)

        pr.begin_drawing()
        pr.clear_background(pr.RAYWHITE)
        pr.draw_rectangle(SCREEN_WIDTH // 2 - 40, box_position_y, 80, 80, pr.MAROON)
        pr.draw_text(
            "Use mouse wheel to move the cube up and down!", 10, 10, 20, pr.GRAY
        )
        pr.draw_text(f"Box position Y: {box_position_y:03d}", 10, 40, 20, pr.LIGHTGRAY)
        pr.end_drawing()

    pr.close_window()


if __name__ == "__main__":
    main()
