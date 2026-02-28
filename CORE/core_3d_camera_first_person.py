from __future__ import annotations

import pyray as pr

# Version checked: raylib 5.x/pyray API parity (reviewed 2026-02-28).

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 450
MAX_COLUMNS = 20

CAMERA_PERSPECTIVE = int(getattr(pr, "CAMERA_PERSPECTIVE", 0))
CAMERA_ORTHOGRAPHIC = int(getattr(pr, "CAMERA_ORTHOGRAPHIC", 1))
CAMERA_FREE = int(getattr(pr, "CAMERA_FREE", 1))
CAMERA_FIRST_PERSON = int(getattr(pr, "CAMERA_FIRST_PERSON", 3))
CAMERA_THIRD_PERSON = int(getattr(pr, "CAMERA_THIRD_PERSON", 4))
CAMERA_ORBITAL = int(getattr(pr, "CAMERA_ORBITAL", 2))

KEY_ONE = getattr(pr, "KEY_ONE", 49)
KEY_TWO = getattr(pr, "KEY_TWO", 50)
KEY_THREE = getattr(pr, "KEY_THREE", 51)
KEY_FOUR = getattr(pr, "KEY_FOUR", 52)
KEY_P = getattr(pr, "KEY_P", 80)


def main() -> None:
    """Run the 3D camera first-person example."""
    pr.init_window(
        SCREEN_WIDTH,
        SCREEN_HEIGHT,
        "raylib [core] example - 3d camera first person",
    )

    camera = pr.Camera3D(
        pr.Vector3(0.0, 2.0, 4.0),
        pr.Vector3(0.0, 2.0, 0.0),
        pr.Vector3(0.0, 1.0, 0.0),
        60.0,
        CAMERA_PERSPECTIVE,
    )
    camera_mode = CAMERA_FIRST_PERSON

    heights = []
    positions = []
    colors = []
    for _ in range(MAX_COLUMNS):
        h = float(pr.get_random_value(1, 12))
        heights.append(h)
        positions.append(
            pr.Vector3(
                float(pr.get_random_value(-15, 15)),
                h / 2.0,
                float(pr.get_random_value(-15, 15)),
            )
        )
        colors.append(
            pr.Color(pr.get_random_value(20, 255), pr.get_random_value(10, 55), 30, 255)
        )

    pr.disable_cursor()
    pr.set_target_fps(60)

    while not pr.window_should_close():
        if pr.is_key_pressed(KEY_ONE):
            camera_mode = CAMERA_FREE
            camera.up = pr.Vector3(0.0, 1.0, 0.0)
        if pr.is_key_pressed(KEY_TWO):
            camera_mode = CAMERA_FIRST_PERSON
            camera.up = pr.Vector3(0.0, 1.0, 0.0)
        if pr.is_key_pressed(KEY_THREE):
            camera_mode = CAMERA_THIRD_PERSON
            camera.up = pr.Vector3(0.0, 1.0, 0.0)
        if pr.is_key_pressed(KEY_FOUR):
            camera_mode = CAMERA_ORBITAL
            camera.up = pr.Vector3(0.0, 1.0, 0.0)

        if pr.is_key_pressed(KEY_P):
            if camera.projection == CAMERA_PERSPECTIVE:
                camera_mode = CAMERA_THIRD_PERSON
                camera.position = pr.Vector3(0.0, 25.0, -25.0)
                camera.target = pr.Vector3(0.0, 2.0, 0.0)
                camera.up = pr.Vector3(0.0, 1.0, 0.0)
                camera.projection = CAMERA_ORTHOGRAPHIC
                camera.fovy = 20.0
            else:
                camera_mode = CAMERA_THIRD_PERSON
                camera.position = pr.Vector3(0.0, 2.0, 10.0)
                camera.target = pr.Vector3(0.0, 2.0, 0.0)
                camera.up = pr.Vector3(0.0, 1.0, 0.0)
                camera.projection = CAMERA_PERSPECTIVE
                camera.fovy = 60.0

        pr.update_camera(camera, camera_mode)

        pr.begin_drawing()
        pr.clear_background(pr.RAYWHITE)
        pr.begin_mode_3d(camera)
        pr.draw_plane(pr.Vector3(0.0, 0.0, 0.0), pr.Vector2(32.0, 32.0), pr.LIGHTGRAY)
        pr.draw_cube(pr.Vector3(-16.0, 2.5, 0.0), 1.0, 5.0, 32.0, pr.BLUE)
        pr.draw_cube(pr.Vector3(16.0, 2.5, 0.0), 1.0, 5.0, 32.0, pr.LIME)
        pr.draw_cube(pr.Vector3(0.0, 2.5, 16.0), 32.0, 5.0, 1.0, pr.GOLD)
        for i in range(MAX_COLUMNS):
            pr.draw_cube(positions[i], 2.0, heights[i], 2.0, colors[i])
            pr.draw_cube_wires(positions[i], 2.0, heights[i], 2.0, pr.MAROON)
        if camera_mode == CAMERA_THIRD_PERSON:
            pr.draw_cube(camera.target, 0.5, 0.5, 0.5, pr.PURPLE)
            pr.draw_cube_wires(camera.target, 0.5, 0.5, 0.5, pr.DARKPURPLE)
        pr.end_mode_3d()

        pr.draw_rectangle(5, 5, 330, 100, pr.fade(pr.SKYBLUE, 0.5))
        pr.draw_rectangle_lines(5, 5, 330, 100, pr.BLUE)
        pr.draw_text("Camera controls:", 15, 15, 10, pr.BLACK)
        pr.draw_text("- Move keys: W, A, S, D, Space, Left-Ctrl", 15, 30, 10, pr.BLACK)
        pr.draw_text("- Look around: arrow keys or mouse", 15, 45, 10, pr.BLACK)
        pr.draw_text("- Camera mode keys: 1, 2, 3, 4", 15, 60, 10, pr.BLACK)
        pr.draw_text(
            "- Zoom keys: num-plus, num-minus or mouse scroll", 15, 75, 10, pr.BLACK
        )
        pr.draw_text("- Camera projection key: P", 15, 90, 10, pr.BLACK)

        mode_text = {
            CAMERA_FREE: "FREE",
            CAMERA_FIRST_PERSON: "FIRST_PERSON",
            CAMERA_THIRD_PERSON: "THIRD_PERSON",
            CAMERA_ORBITAL: "ORBITAL",
        }.get(camera_mode, "CUSTOM")
        proj_text = (
            "PERSPECTIVE" if camera.projection == CAMERA_PERSPECTIVE else "ORTHOGRAPHIC"
        )

        pr.draw_rectangle(600, 5, 195, 100, pr.fade(pr.SKYBLUE, 0.5))
        pr.draw_rectangle_lines(600, 5, 195, 100, pr.BLUE)
        pr.draw_text("Camera status:", 610, 15, 10, pr.BLACK)
        pr.draw_text(f"- Mode: {mode_text}", 610, 30, 10, pr.BLACK)
        pr.draw_text(f"- Projection: {proj_text}", 610, 45, 10, pr.BLACK)
        pr.draw_text(
            f"- Position: ({camera.position.x:06.3f}, {camera.position.y:06.3f}, {camera.position.z:06.3f})",
            610,
            60,
            10,
            pr.BLACK,
        )
        pr.draw_text(
            f"- Target: ({camera.target.x:06.3f}, {camera.target.y:06.3f}, {camera.target.z:06.3f})",
            610,
            75,
            10,
            pr.BLACK,
        )
        pr.draw_text(
            f"- Up: ({camera.up.x:06.3f}, {camera.up.y:06.3f}, {camera.up.z:06.3f})",
            610,
            90,
            10,
            pr.BLACK,
        )
        pr.end_drawing()

    pr.close_window()


if __name__ == "__main__":
    main()
