from __future__ import annotations

from enum import IntEnum

import pyray as pr

# Version checked: raylib 5.x/pyray API parity (reviewed 2026-02-28).

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 450
MOUSE_BUTTON_LEFT = getattr(pr, "MOUSE_BUTTON_LEFT", 0)


class PadButton(IntEnum):
    """Virtual D-pad button ids."""

    NONE = -1
    UP = 0
    LEFT = 1
    RIGHT = 2
    DOWN = 3


def main() -> None:
    """Run the input virtual controls example."""
    pr.init_window(
        SCREEN_WIDTH,
        SCREEN_HEIGHT,
        "raylib [core] example - input virtual controls",
    )

    pad_position = pr.Vector2(100.0, 350.0)
    button_radius = 30.0
    button_positions = [
        pr.Vector2(pad_position.x, pad_position.y - button_radius * 1.5),
        pr.Vector2(pad_position.x - button_radius * 1.5, pad_position.y),
        pr.Vector2(pad_position.x + button_radius * 1.5, pad_position.y),
        pr.Vector2(pad_position.x, pad_position.y + button_radius * 1.5),
    ]

    arrow_tris = [
        (
            pr.Vector2(button_positions[0].x, button_positions[0].y - 12),
            pr.Vector2(button_positions[0].x - 9, button_positions[0].y + 9),
            pr.Vector2(button_positions[0].x + 9, button_positions[0].y + 9),
        ),
        (
            pr.Vector2(button_positions[1].x + 9, button_positions[1].y - 9),
            pr.Vector2(button_positions[1].x - 12, button_positions[1].y),
            pr.Vector2(button_positions[1].x + 9, button_positions[1].y + 9),
        ),
        (
            pr.Vector2(button_positions[2].x + 12, button_positions[2].y),
            pr.Vector2(button_positions[2].x - 9, button_positions[2].y - 9),
            pr.Vector2(button_positions[2].x - 9, button_positions[2].y + 9),
        ),
        (
            pr.Vector2(button_positions[3].x - 9, button_positions[3].y - 9),
            pr.Vector2(button_positions[3].x, button_positions[3].y + 12),
            pr.Vector2(button_positions[3].x + 9, button_positions[3].y - 9),
        ),
    ]
    label_colors = [pr.YELLOW, pr.BLUE, pr.RED, pr.GREEN]

    pressed_button = PadButton.NONE
    player_position = pr.Vector2(SCREEN_WIDTH / 2.0, SCREEN_HEIGHT / 2.0)
    player_speed = 75.0

    pr.set_target_fps(60)

    while not pr.window_should_close():
        if pr.get_touch_point_count() > 0:
            input_position = pr.get_touch_position(0)
        else:
            input_position = pr.get_mouse_position()

        pressed_button = PadButton.NONE
        active_input = pr.get_touch_point_count() > 0 or pr.is_mouse_button_down(
            MOUSE_BUTTON_LEFT
        )
        if active_input:
            for i in range(4):
                dist_x = abs(button_positions[i].x - input_position.x)
                dist_y = abs(button_positions[i].y - input_position.y)
                if dist_x + dist_y < button_radius:
                    pressed_button = PadButton(i)
                    break

        match pressed_button:
            case PadButton.UP:
                player_position.y -= player_speed * pr.get_frame_time()
            case PadButton.LEFT:
                player_position.x -= player_speed * pr.get_frame_time()
            case PadButton.RIGHT:
                player_position.x += player_speed * pr.get_frame_time()
            case PadButton.DOWN:
                player_position.y += player_speed * pr.get_frame_time()

        pr.begin_drawing()
        pr.clear_background(pr.RAYWHITE)
        pr.draw_circle_v(player_position, 50.0, pr.MAROON)
        for i in range(4):
            pr.draw_circle_v(
                button_positions[i],
                button_radius,
                pr.DARKGRAY if pressed_button == PadButton(i) else pr.BLACK,
            )
            tri = arrow_tris[i]
            pr.draw_triangle(tri[0], tri[1], tri[2], label_colors[i])
        pr.draw_text("move the player with D-Pad buttons", 10, 10, 20, pr.DARKGRAY)
        pr.end_drawing()

    pr.close_window()


if __name__ == "__main__":
    main()
