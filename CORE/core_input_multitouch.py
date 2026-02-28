from __future__ import annotations

import pyray as pr

# Version checked: raylib 5.x/pyray API parity (reviewed 2026-02-28).

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 450
MAX_TOUCH_POINTS = 10


def main() -> None:
    """Run the input multitouch example."""
    pr.init_window(
        SCREEN_WIDTH,
        SCREEN_HEIGHT,
        "raylib [core] example - input multitouch",
    )

    touch_positions = [pr.Vector2(0.0, 0.0) for _ in range(MAX_TOUCH_POINTS)]
    pr.set_target_fps(60)

    while not pr.window_should_close():
        touch_count = min(pr.get_touch_point_count(), MAX_TOUCH_POINTS)
        for i in range(touch_count):
            touch_positions[i] = pr.get_touch_position(i)

        pr.begin_drawing()
        pr.clear_background(pr.RAYWHITE)

        for i in range(touch_count):
            pos = touch_positions[i]
            if pos.x > 0.0 and pos.y > 0.0:
                pr.draw_circle_v(pos, 34.0, pr.ORANGE)
                pr.draw_text(f"{i}", int(pos.x) - 10, int(pos.y) - 70, 40, pr.BLACK)

        pr.draw_text(
            "touch the screen at multiple locations to get multiple balls",
            10,
            10,
            20,
            pr.DARKGRAY,
        )
        pr.end_drawing()

    pr.close_window()


if __name__ == "__main__":
    main()
