from __future__ import annotations

import pyray as pr

# Version checked: raylib 5.x/pyray API parity (reviewed 2026-02-28).

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 450
KEY_W = getattr(pr, "KEY_W", 87)
KEY_S = getattr(pr, "KEY_S", 83)
KEY_UP = getattr(pr, "KEY_UP", 265)
KEY_DOWN = getattr(pr, "KEY_DOWN", 264)
CAMERA_PERSPECTIVE = int(getattr(pr, "CAMERA_PERSPECTIVE", 0))


def draw_world(
    camera_player1: pr.Camera3D, camera_player2: pr.Camera3D, count: int, spacing: float
) -> None:
    """Draw shared 3D scene for both players."""
    pr.draw_plane(pr.Vector3(0.0, 0.0, 0.0), pr.Vector2(50.0, 50.0), pr.BEIGE)
    x = -count * spacing
    while x <= count * spacing:
        z = -count * spacing
        while z <= count * spacing:
            pr.draw_cube(pr.Vector3(x, 1.5, z), 1.0, 1.0, 1.0, pr.LIME)
            pr.draw_cube(pr.Vector3(x, 0.5, z), 0.25, 1.0, 0.25, pr.BROWN)
            z += spacing
        x += spacing
    pr.draw_cube(camera_player1.position, 1.0, 1.0, 1.0, pr.RED)
    pr.draw_cube(camera_player2.position, 1.0, 1.0, 1.0, pr.BLUE)


def main() -> None:
    """Run the 3D split-screen camera example."""
    pr.init_window(
        SCREEN_WIDTH,
        SCREEN_HEIGHT,
        "raylib [core] example - 3d camera split screen",
    )

    camera_player1 = pr.Camera3D(
        pr.Vector3(0.0, 1.0, -3.0),
        pr.Vector3(0.0, 1.0, 0.0),
        pr.Vector3(0.0, 1.0, 0.0),
        45.0,
        CAMERA_PERSPECTIVE,
    )
    screen_player1 = pr.load_render_texture(SCREEN_WIDTH // 2, SCREEN_HEIGHT)

    camera_player2 = pr.Camera3D(
        pr.Vector3(-3.0, 3.0, 0.0),
        pr.Vector3(0.0, 3.0, 0.0),
        pr.Vector3(0.0, 1.0, 0.0),
        45.0,
        CAMERA_PERSPECTIVE,
    )
    screen_player2 = pr.load_render_texture(SCREEN_WIDTH // 2, SCREEN_HEIGHT)

    split_screen_rect = pr.Rectangle(
        0.0,
        0.0,
        float(screen_player1.texture.width),
        float(-screen_player1.texture.height),
    )
    count = 5
    spacing = 4.0
    pr.set_target_fps(60)

    while not pr.window_should_close():
        offset_this_frame = 10.0 * pr.get_frame_time()
        if pr.is_key_down(KEY_W):
            camera_player1.position.z += offset_this_frame
            camera_player1.target.z += offset_this_frame
        elif pr.is_key_down(KEY_S):
            camera_player1.position.z -= offset_this_frame
            camera_player1.target.z -= offset_this_frame

        if pr.is_key_down(KEY_UP):
            camera_player2.position.x += offset_this_frame
            camera_player2.target.x += offset_this_frame
        elif pr.is_key_down(KEY_DOWN):
            camera_player2.position.x -= offset_this_frame
            camera_player2.target.x -= offset_this_frame

        pr.begin_texture_mode(screen_player1)
        pr.clear_background(pr.SKYBLUE)
        pr.begin_mode_3d(camera_player1)
        draw_world(camera_player1, camera_player2, count, spacing)
        pr.end_mode_3d()
        pr.draw_rectangle(
            0, 0, pr.get_screen_width() // 2, 40, pr.fade(pr.RAYWHITE, 0.8)
        )
        pr.draw_text("PLAYER1: W/S to move", 10, 10, 20, pr.MAROON)
        pr.end_texture_mode()

        pr.begin_texture_mode(screen_player2)
        pr.clear_background(pr.SKYBLUE)
        pr.begin_mode_3d(camera_player2)
        draw_world(camera_player1, camera_player2, count, spacing)
        pr.end_mode_3d()
        pr.draw_rectangle(
            0, 0, pr.get_screen_width() // 2, 40, pr.fade(pr.RAYWHITE, 0.8)
        )
        pr.draw_text("PLAYER2: UP/DOWN to move", 10, 10, 20, pr.DARKBLUE)
        pr.end_texture_mode()

        pr.begin_drawing()
        pr.clear_background(pr.BLACK)
        pr.draw_texture_rec(
            screen_player1.texture, split_screen_rect, pr.Vector2(0.0, 0.0), pr.WHITE
        )
        pr.draw_texture_rec(
            screen_player2.texture,
            split_screen_rect,
            pr.Vector2(SCREEN_WIDTH / 2.0, 0.0),
            pr.WHITE,
        )
        pr.draw_rectangle(
            pr.get_screen_width() // 2 - 2, 0, 4, pr.get_screen_height(), pr.LIGHTGRAY
        )
        pr.end_drawing()

    pr.unload_render_texture(screen_player1)
    pr.unload_render_texture(screen_player2)
    pr.close_window()


if __name__ == "__main__":
    main()
