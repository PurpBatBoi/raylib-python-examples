from __future__ import annotations

import pyray as pr

# Version checked: raylib 5.x/pyray API parity (reviewed 2026-02-28).

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 450
CAMERA_PERSPECTIVE = int(getattr(pr, "CAMERA_PERSPECTIVE", 0))
CAMERA_FREE = int(getattr(pr, "CAMERA_FREE", 1))
KEY_Z = getattr(pr, "KEY_Z", 90)


def main() -> None:
    """Run the free 3D camera example."""
    pr.init_window(
        SCREEN_WIDTH, SCREEN_HEIGHT, "raylib [core] example - 3d camera free"
    )

    camera = pr.Camera3D(
        pr.Vector3(10.0, 10.0, 10.0),
        pr.Vector3(0.0, 0.0, 0.0),
        pr.Vector3(0.0, 1.0, 0.0),
        45.0,
        CAMERA_PERSPECTIVE,
    )
    cube_position = pr.Vector3(0.0, 0.0, 0.0)

    pr.disable_cursor()
    pr.set_target_fps(60)

    while not pr.window_should_close():
        pr.update_camera(camera, CAMERA_FREE)
        if pr.is_key_pressed(KEY_Z):
            camera.target = pr.Vector3(0.0, 0.0, 0.0)

        pr.begin_drawing()
        pr.clear_background(pr.RAYWHITE)

        pr.begin_mode_3d(camera)
        pr.draw_cube(cube_position, 2.0, 2.0, 2.0, pr.RED)
        pr.draw_cube_wires(cube_position, 2.0, 2.0, 2.0, pr.MAROON)
        pr.draw_grid(10, 1.0)
        pr.end_mode_3d()

        pr.draw_rectangle(10, 10, 320, 93, pr.fade(pr.SKYBLUE, 0.5))
        pr.draw_rectangle_lines(10, 10, 320, 93, pr.BLUE)
        pr.draw_text("Free camera default controls:", 20, 20, 10, pr.BLACK)
        pr.draw_text("- Mouse Wheel to Zoom in-out", 40, 40, 10, pr.DARKGRAY)
        pr.draw_text("- Mouse Wheel Pressed to Pan", 40, 60, 10, pr.DARKGRAY)
        pr.draw_text("- Z to zoom to (0, 0, 0)", 40, 80, 10, pr.DARKGRAY)
        pr.end_drawing()

    pr.close_window()


if __name__ == "__main__":
    main()
