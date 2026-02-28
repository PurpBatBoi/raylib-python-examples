from __future__ import annotations

import pyray as pr

# Version checked: raylib 5.x/pyray API parity (reviewed 2026-02-28).

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 450

KEY_NULL = getattr(pr, "KEY_NULL", 0)
KEY_ESCAPE = getattr(pr, "KEY_ESCAPE", 256)
KEY_Y = getattr(pr, "KEY_Y", 89)
KEY_N = getattr(pr, "KEY_N", 78)


def main() -> None:
    """Run the window-close confirmation example."""
    pr.init_window(
        SCREEN_WIDTH,
        SCREEN_HEIGHT,
        "raylib [core] example - window should close",
    )

    pr.set_exit_key(KEY_NULL)
    exit_window_requested = False
    exit_window = False

    pr.set_target_fps(60)

    while not exit_window:
        if pr.window_should_close() or pr.is_key_pressed(KEY_ESCAPE):
            exit_window_requested = True

        if exit_window_requested:
            if pr.is_key_pressed(KEY_Y):
                exit_window = True
            elif pr.is_key_pressed(KEY_N):
                exit_window_requested = False

        pr.begin_drawing()
        pr.clear_background(pr.RAYWHITE)

        if exit_window_requested:
            pr.draw_rectangle(0, 100, SCREEN_WIDTH, 200, pr.BLACK)
            pr.draw_text(
                "Are you sure you want to exit program? [Y/N]",
                40,
                180,
                30,
                pr.WHITE,
            )
        else:
            pr.draw_text(
                "Try to close the window to get confirmation message!",
                120,
                200,
                20,
                pr.LIGHTGRAY,
            )

        pr.end_drawing()

    pr.close_window()


if __name__ == "__main__":
    main()
