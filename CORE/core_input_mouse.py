from __future__ import annotations

import pyray as pr

# Version checked: raylib 5.x/pyray API parity (reviewed 2026-02-28).

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 450

KEY_H = getattr(pr, "KEY_H", 72)

MOUSE_BUTTON_LEFT = getattr(pr, "MOUSE_BUTTON_LEFT", 0)
MOUSE_BUTTON_RIGHT = getattr(pr, "MOUSE_BUTTON_RIGHT", 1)
MOUSE_BUTTON_MIDDLE = getattr(pr, "MOUSE_BUTTON_MIDDLE", 2)
MOUSE_BUTTON_SIDE = getattr(pr, "MOUSE_BUTTON_SIDE", 3)
MOUSE_BUTTON_EXTRA = getattr(pr, "MOUSE_BUTTON_EXTRA", 4)
MOUSE_BUTTON_FORWARD = getattr(pr, "MOUSE_BUTTON_FORWARD", 5)
MOUSE_BUTTON_BACK = getattr(pr, "MOUSE_BUTTON_BACK", 6)


def main() -> None:
    """Run the input-mouse example."""
    pr.init_window(SCREEN_WIDTH, SCREEN_HEIGHT, "raylib [core] example - input mouse")

    ball_position = pr.Vector2(-100.0, -100.0)
    ball_color = pr.DARKBLUE

    pr.set_target_fps(60)

    while not pr.window_should_close():
        if pr.is_key_pressed(KEY_H):
            if pr.is_cursor_hidden():
                pr.show_cursor()
            else:
                pr.hide_cursor()

        ball_position = pr.get_mouse_position()

        if pr.is_mouse_button_pressed(MOUSE_BUTTON_LEFT):
            ball_color = pr.MAROON
        elif pr.is_mouse_button_pressed(MOUSE_BUTTON_MIDDLE):
            ball_color = pr.LIME
        elif pr.is_mouse_button_pressed(MOUSE_BUTTON_RIGHT):
            ball_color = pr.DARKBLUE
        elif pr.is_mouse_button_pressed(MOUSE_BUTTON_SIDE):
            ball_color = pr.PURPLE
        elif pr.is_mouse_button_pressed(MOUSE_BUTTON_EXTRA):
            ball_color = pr.YELLOW
        elif pr.is_mouse_button_pressed(MOUSE_BUTTON_FORWARD):
            ball_color = pr.ORANGE
        elif pr.is_mouse_button_pressed(MOUSE_BUTTON_BACK):
            ball_color = pr.BEIGE

        pr.begin_drawing()
        pr.clear_background(pr.RAYWHITE)
        pr.draw_circle_v(ball_position, 40.0, ball_color)
        pr.draw_text(
            "move ball with mouse and click mouse button to change color",
            10,
            10,
            20,
            pr.DARKGRAY,
        )
        pr.draw_text("Press 'H' to toggle cursor visibility", 10, 30, 20, pr.DARKGRAY)
        if pr.is_cursor_hidden():
            pr.draw_text("CURSOR HIDDEN", 20, 60, 20, pr.RED)
        else:
            pr.draw_text("CURSOR VISIBLE", 20, 60, 20, pr.LIME)
        pr.end_drawing()

    pr.close_window()


if __name__ == "__main__":
    main()
