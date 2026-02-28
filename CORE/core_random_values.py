from __future__ import annotations

import pyray as pr

# Version checked: raylib 5.x/pyray API parity (reviewed 2026-02-28).

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 450


def main() -> None:
    """Run the random-values example."""
    pr.init_window(SCREEN_WIDTH, SCREEN_HEIGHT, "raylib [core] example - random values")

    rand_value = pr.get_random_value(-8, 5)
    frames_counter = 0
    pr.set_target_fps(60)

    while not pr.window_should_close():
        frames_counter += 1
        if ((frames_counter // 120) % 2) == 1:
            rand_value = pr.get_random_value(-8, 5)
            frames_counter = 0

        pr.begin_drawing()
        pr.clear_background(pr.RAYWHITE)
        pr.draw_text(
            "Every 2 seconds a new random value is generated:",
            130,
            100,
            20,
            pr.MAROON,
        )
        pr.draw_text(f"{rand_value}", 360, 180, 80, pr.LIGHTGRAY)
        pr.end_drawing()

    pr.close_window()


if __name__ == "__main__":
    main()
