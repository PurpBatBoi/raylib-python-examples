from __future__ import annotations

import pyray as pr

# Version checked: raylib 5.x/pyray API parity (reviewed 2026-02-28).

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 450
KEY_S = getattr(pr, "KEY_S", 83)


def main() -> None:
    """Run the scissor-test example."""
    pr.init_window(SCREEN_WIDTH, SCREEN_HEIGHT, "raylib [core] example - scissor test")

    scissor_area = pr.Rectangle(0.0, 0.0, 300.0, 300.0)
    scissor_mode = True

    pr.set_target_fps(60)

    while not pr.window_should_close():
        if pr.is_key_pressed(KEY_S):
            scissor_mode = not scissor_mode

        scissor_area.x = pr.get_mouse_x() - scissor_area.width / 2.0
        scissor_area.y = pr.get_mouse_y() - scissor_area.height / 2.0

        pr.begin_drawing()
        pr.clear_background(pr.RAYWHITE)

        if scissor_mode:
            pr.begin_scissor_mode(
                int(scissor_area.x),
                int(scissor_area.y),
                int(scissor_area.width),
                int(scissor_area.height),
            )

        pr.draw_rectangle(0, 0, pr.get_screen_width(), pr.get_screen_height(), pr.RED)
        pr.draw_text(
            "Move the mouse around to reveal this text!", 190, 200, 20, pr.LIGHTGRAY
        )

        if scissor_mode:
            pr.end_scissor_mode()

        pr.draw_rectangle_lines_ex(scissor_area, 1.0, pr.BLACK)
        pr.draw_text("Press S to toggle scissor test", 10, 10, 20, pr.BLACK)
        pr.end_drawing()

    pr.close_window()


if __name__ == "__main__":
    main()
