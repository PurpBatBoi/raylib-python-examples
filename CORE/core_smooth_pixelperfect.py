from __future__ import annotations

import math

import pyray as pr

# Version checked: raylib 5.x/pyray API parity (reviewed 2026-02-28).

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 450
VIRTUAL_SCREEN_WIDTH = 160
VIRTUAL_SCREEN_HEIGHT = 90


def main() -> None:
    """Run the smooth pixel-perfect camera demonstration."""
    virtual_ratio = SCREEN_WIDTH / VIRTUAL_SCREEN_WIDTH

    pr.init_window(
        SCREEN_WIDTH,
        SCREEN_HEIGHT,
        "raylib [core] example - smooth pixelperfect",
    )

    world_space_camera = pr.Camera2D(
        pr.Vector2(0.0, 0.0),
        pr.Vector2(0.0, 0.0),
        0.0,
        1.0,
    )
    screen_space_camera = pr.Camera2D(
        pr.Vector2(0.0, 0.0),
        pr.Vector2(0.0, 0.0),
        0.0,
        1.0,
    )

    target = pr.load_render_texture(VIRTUAL_SCREEN_WIDTH, VIRTUAL_SCREEN_HEIGHT)

    rec01 = pr.Rectangle(70.0, 35.0, 20.0, 20.0)
    rec02 = pr.Rectangle(90.0, 55.0, 30.0, 10.0)
    rec03 = pr.Rectangle(80.0, 65.0, 15.0, 25.0)

    source_rec = pr.Rectangle(
        0.0,
        0.0,
        float(target.texture.width),
        -float(target.texture.height),
    )
    dest_rec = pr.Rectangle(
        -virtual_ratio,
        -virtual_ratio,
        SCREEN_WIDTH + (virtual_ratio * 2.0),
        SCREEN_HEIGHT + (virtual_ratio * 2.0),
    )

    origin = pr.Vector2(0.0, 0.0)
    rotation = 0.0

    pr.set_target_fps(60)

    while not pr.window_should_close():
        rotation += 60.0 * pr.get_frame_time()

        camera_x = math.sin(pr.get_time()) * 50.0 - 10.0
        camera_y = math.cos(pr.get_time()) * 30.0

        screen_space_camera.target = pr.Vector2(camera_x, camera_y)

        world_space_camera.target.x = math.trunc(screen_space_camera.target.x)
        screen_space_camera.target.x -= world_space_camera.target.x
        screen_space_camera.target.x *= virtual_ratio

        world_space_camera.target.y = math.trunc(screen_space_camera.target.y)
        screen_space_camera.target.y -= world_space_camera.target.y
        screen_space_camera.target.y *= virtual_ratio

        pr.begin_texture_mode(target)
        pr.clear_background(pr.RAYWHITE)

        pr.begin_mode_2d(world_space_camera)
        pr.draw_rectangle_pro(rec01, origin, rotation, pr.BLACK)
        pr.draw_rectangle_pro(rec02, origin, -rotation, pr.RED)
        pr.draw_rectangle_pro(rec03, origin, rotation + 45.0, pr.BLUE)
        pr.end_mode_2d()

        pr.end_texture_mode()

        pr.begin_drawing()
        pr.clear_background(pr.RED)

        pr.begin_mode_2d(screen_space_camera)
        pr.draw_texture_pro(target.texture, source_rec, dest_rec, origin, 0.0, pr.WHITE)
        pr.end_mode_2d()

        pr.draw_text(
            f"Screen resolution: {SCREEN_WIDTH}x{SCREEN_HEIGHT}",
            10,
            10,
            20,
            pr.DARKBLUE,
        )
        pr.draw_text(
            f"World resolution: {VIRTUAL_SCREEN_WIDTH}x{VIRTUAL_SCREEN_HEIGHT}",
            10,
            40,
            20,
            pr.DARKGREEN,
        )
        pr.draw_fps(pr.get_screen_width() - 95, 10)

        pr.end_drawing()

    pr.unload_render_texture(target)
    pr.close_window()


if __name__ == "__main__":
    main()
