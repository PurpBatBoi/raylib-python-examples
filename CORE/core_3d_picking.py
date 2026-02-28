from __future__ import annotations

import pyray as pr

# Version checked: raylib 5.x/pyray API parity (reviewed 2026-02-28).

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 450
CAMERA_PERSPECTIVE = int(getattr(pr, "CAMERA_PERSPECTIVE", 0))
CAMERA_FIRST_PERSON = int(getattr(pr, "CAMERA_FIRST_PERSON", 3))
MOUSE_BUTTON_LEFT = getattr(pr, "MOUSE_BUTTON_LEFT", 0)
MOUSE_BUTTON_RIGHT = getattr(pr, "MOUSE_BUTTON_RIGHT", 1)


def main() -> None:
    """Run the 3D picking example."""
    pr.init_window(SCREEN_WIDTH, SCREEN_HEIGHT, "raylib [core] example - 3d picking")

    camera = pr.Camera3D(
        pr.Vector3(10.0, 10.0, 10.0),
        pr.Vector3(0.0, 0.0, 0.0),
        pr.Vector3(0.0, 1.0, 0.0),
        45.0,
        CAMERA_PERSPECTIVE,
    )

    cube_position = pr.Vector3(0.0, 1.0, 0.0)
    cube_size = pr.Vector3(2.0, 2.0, 2.0)

    ray = pr.Ray(pr.Vector3(0.0, 0.0, 0.0), pr.Vector3(0.0, 0.0, 0.0))
    collision = pr.RayCollision(
        False, 0.0, pr.Vector3(0.0, 0.0, 0.0), pr.Vector3(0.0, 0.0, 0.0)
    )

    pr.set_target_fps(60)

    while not pr.window_should_close():
        if pr.is_cursor_hidden():
            pr.update_camera(camera, CAMERA_FIRST_PERSON)

        if pr.is_mouse_button_pressed(MOUSE_BUTTON_RIGHT):
            if pr.is_cursor_hidden():
                pr.enable_cursor()
            else:
                pr.disable_cursor()

        if pr.is_mouse_button_pressed(MOUSE_BUTTON_LEFT):
            if not collision.hit:
                ray = pr.get_screen_to_world_ray(pr.get_mouse_position(), camera)
                box = pr.BoundingBox(
                    pr.Vector3(
                        cube_position.x - cube_size.x / 2.0,
                        cube_position.y - cube_size.y / 2.0,
                        cube_position.z - cube_size.z / 2.0,
                    ),
                    pr.Vector3(
                        cube_position.x + cube_size.x / 2.0,
                        cube_position.y + cube_size.y / 2.0,
                        cube_position.z + cube_size.z / 2.0,
                    ),
                )
                collision = pr.get_ray_collision_box(ray, box)
            else:
                collision.hit = False

        pr.begin_drawing()
        pr.clear_background(pr.RAYWHITE)
        pr.begin_mode_3d(camera)

        if collision.hit:
            pr.draw_cube(cube_position, cube_size.x, cube_size.y, cube_size.z, pr.RED)
            pr.draw_cube_wires(
                cube_position, cube_size.x, cube_size.y, cube_size.z, pr.MAROON
            )
            pr.draw_cube_wires(
                cube_position,
                cube_size.x + 0.2,
                cube_size.y + 0.2,
                cube_size.z + 0.2,
                pr.GREEN,
            )
        else:
            pr.draw_cube(cube_position, cube_size.x, cube_size.y, cube_size.z, pr.GRAY)
            pr.draw_cube_wires(
                cube_position, cube_size.x, cube_size.y, cube_size.z, pr.DARKGRAY
            )

        pr.draw_ray(ray, pr.MAROON)
        pr.draw_grid(10, 1.0)
        pr.end_mode_3d()

        pr.draw_text(
            "Try clicking on the box with your mouse!", 240, 10, 20, pr.DARKGRAY
        )
        if collision.hit:
            selected = "BOX SELECTED"
            pr.draw_text(
                selected,
                (SCREEN_WIDTH - pr.measure_text(selected, 30)) // 2,
                int(SCREEN_HEIGHT * 0.1),
                30,
                pr.GREEN,
            )
        pr.draw_text(
            "Right click mouse to toggle camera controls", 10, 430, 10, pr.GRAY
        )
        pr.draw_fps(10, 10)
        pr.end_drawing()

    pr.close_window()


if __name__ == "__main__":
    main()
