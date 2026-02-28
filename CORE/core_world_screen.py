from __future__ import annotations

import pyray as pr

# Version checked: raylib 5.x/pyray API parity (reviewed 2026-02-28).

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 450
CAMERA_PERSPECTIVE = int(getattr(pr, "CAMERA_PERSPECTIVE", 0))
CAMERA_THIRD_PERSON = int(getattr(pr, "CAMERA_THIRD_PERSON", 4))


def main() -> None:
    """Run the world-to-screen coordinate example."""
    pr.init_window(SCREEN_WIDTH, SCREEN_HEIGHT, "raylib [core] example - world screen")

    camera = pr.Camera3D(
        pr.Vector3(10.0, 10.0, 10.0),
        pr.Vector3(0.0, 0.0, 0.0),
        pr.Vector3(0.0, 1.0, 0.0),
        45.0,
        CAMERA_PERSPECTIVE,
    )
    cube_position = pr.Vector3(0.0, 0.0, 0.0)
    cube_screen_position = pr.Vector2(0.0, 0.0)

    pr.disable_cursor()
    pr.set_target_fps(60)

    while not pr.window_should_close():
        pr.update_camera(camera, CAMERA_THIRD_PERSON)
        cube_screen_position = pr.get_world_to_screen(
            pr.Vector3(cube_position.x, cube_position.y + 2.5, cube_position.z),
            camera,
        )

        pr.begin_drawing()
        pr.clear_background(pr.RAYWHITE)

        pr.begin_mode_3d(camera)
        pr.draw_cube(cube_position, 2.0, 2.0, 2.0, pr.RED)
        pr.draw_cube_wires(cube_position, 2.0, 2.0, 2.0, pr.MAROON)
        pr.draw_grid(10, 1.0)
        pr.end_mode_3d()

        enemy_text = "Enemy: 100/100"
        text_x = int(cube_screen_position.x) - pr.measure_text(enemy_text, 20) // 2
        pr.draw_text(enemy_text, text_x, int(cube_screen_position.y), 20, pr.BLACK)
        pr.draw_text(
            f"Cube position in screen space coordinates: [{int(cube_screen_position.x)}, {int(cube_screen_position.y)}]",
            10,
            10,
            20,
            pr.LIME,
        )
        pr.draw_text("Text 2d should be always on top of the cube", 10, 40, 20, pr.GRAY)
        pr.end_drawing()

    pr.close_window()


if __name__ == "__main__":
    main()
