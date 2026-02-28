from __future__ import annotations

import math

import pyray as pr

# Version checked: raylib 5.x/pyray API parity (reviewed 2026-02-28).

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 450

KEY_ONE = getattr(pr, "KEY_ONE", 49)
KEY_TWO = getattr(pr, "KEY_TWO", 50)
MOUSE_BUTTON_LEFT = getattr(pr, "MOUSE_BUTTON_LEFT", 0)
MOUSE_BUTTON_RIGHT = getattr(pr, "MOUSE_BUTTON_RIGHT", 1)


def draw_reference_grid(step: int, lines: int) -> None:
    """Draw a centered XY-style reference grid in 2D world space."""
    half = step * lines
    for x in range(-half, half + 1, step):
        color = pr.GRAY if x == 0 else pr.LIGHTGRAY
        pr.draw_line(x, -half, x, half, color)
    for y in range(-half, half + 1, step):
        color = pr.GRAY if y == 0 else pr.LIGHTGRAY
        pr.draw_line(-half, y, half, y, color)


def main() -> None:
    """Run the 2D camera mouse zoom example."""
    pr.init_window(
        SCREEN_WIDTH,
        SCREEN_HEIGHT,
        "raylib [core] example - 2d camera mouse zoom",
    )

    camera = pr.Camera2D(
        pr.Vector2(0.0, 0.0),
        pr.Vector2(0.0, 0.0),
        0.0,
        1.0,
    )
    zoom_mode = 0

    pr.set_target_fps(60)

    while not pr.window_should_close():
        if pr.is_key_pressed(KEY_ONE):
            zoom_mode = 0
        elif pr.is_key_pressed(KEY_TWO):
            zoom_mode = 1

        if pr.is_mouse_button_down(MOUSE_BUTTON_LEFT):
            delta = pr.get_mouse_delta()
            delta = pr.vector2_scale(delta, -1.0 / camera.zoom)
            camera.target = pr.vector2_add(camera.target, delta)

        if zoom_mode == 0:
            wheel = pr.get_mouse_wheel_move()
            if wheel != 0.0:
                mouse_world_pos = pr.get_screen_to_world_2d(
                    pr.get_mouse_position(), camera
                )
                camera.offset = pr.get_mouse_position()
                camera.target = mouse_world_pos
                scale = 0.2 * wheel
                camera.zoom = pr.clamp(
                    math.exp(math.log(camera.zoom) + scale), 0.125, 64.0
                )
        else:
            if pr.is_mouse_button_pressed(MOUSE_BUTTON_RIGHT):
                mouse_world_pos = pr.get_screen_to_world_2d(
                    pr.get_mouse_position(), camera
                )
                camera.offset = pr.get_mouse_position()
                camera.target = mouse_world_pos
            if pr.is_mouse_button_down(MOUSE_BUTTON_RIGHT):
                scale = 0.005 * pr.get_mouse_delta().x
                camera.zoom = pr.clamp(
                    math.exp(math.log(camera.zoom) + scale), 0.125, 64.0
                )

        pr.begin_drawing()
        pr.clear_background(pr.RAYWHITE)

        pr.begin_mode_2d(camera)
        draw_reference_grid(50, 50)
        pr.draw_circle(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2, 50.0, pr.MAROON)
        pr.end_mode_2d()

        mouse = pr.get_mouse_position()
        pr.draw_circle_v(mouse, 4.0, pr.DARKGRAY)
        pr.draw_text(
            f"[{int(mouse.x)}, {int(mouse.y)}]",
            int(mouse.x) - 44,
            int(mouse.y) - 24,
            20,
            pr.BLACK,
        )
        pr.draw_text(
            "[1][2] Select mouse zoom mode (Wheel or Move)", 20, 20, 20, pr.DARKGRAY
        )
        if zoom_mode == 0:
            pr.draw_text(
                "Mouse left button drag to move, mouse wheel to zoom",
                20,
                50,
                20,
                pr.DARKGRAY,
            )
        else:
            pr.draw_text(
                "Mouse left button drag to move, mouse press and move to zoom",
                20,
                50,
                20,
                pr.DARKGRAY,
            )
        pr.end_drawing()

    pr.close_window()


if __name__ == "__main__":
    main()
