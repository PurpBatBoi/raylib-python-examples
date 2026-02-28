from __future__ import annotations

import pyray as pr

# Version checked: raylib 5.x/pyray API parity (reviewed 2026-02-28).

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 450
CAMERA_PERSPECTIVE = int(getattr(pr, "CAMERA_PERSPECTIVE", 0))


def main() -> None:
    """Run the 3D camera mode example."""
    pr.init_window(
        SCREEN_WIDTH, SCREEN_HEIGHT, "raylib [core] example - 3d camera mode"
    )

    camera = pr.Camera3D(
        pr.Vector3(0.0, 10.0, 10.0),
        pr.Vector3(0.0, 0.0, 0.0),
        pr.Vector3(0.0, 1.0, 0.0),
        45.0,
        CAMERA_PERSPECTIVE,
    )
    cube_position = pr.Vector3(0.0, 0.0, 0.0)

    pr.set_target_fps(60)

    while not pr.window_should_close():
        pr.begin_drawing()
        pr.clear_background(pr.RAYWHITE)

        pr.begin_mode_3d(camera)
        pr.draw_cube(cube_position, 2.0, 2.0, 2.0, pr.RED)
        pr.draw_cube_wires(cube_position, 2.0, 2.0, 2.0, pr.MAROON)
        pr.draw_grid(10, 1.0)
        pr.end_mode_3d()

        pr.draw_text("Welcome to the third dimension!", 10, 40, 20, pr.DARKGRAY)
        pr.draw_fps(10, 10)
        pr.end_drawing()

    pr.close_window()


if __name__ == "__main__":
    main()
