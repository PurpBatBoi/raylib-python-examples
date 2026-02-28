from __future__ import annotations

import pyray as pr

# Version checked: raylib 5.x/pyray API parity (reviewed 2026-02-28).

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 450


def main() -> None:
    """Run the render-texture example."""
    pr.init_window(
        SCREEN_WIDTH,
        SCREEN_HEIGHT,
        "raylib [core] example - render texture",
    )

    render_texture_width = 300
    render_texture_height = 300
    target = pr.load_render_texture(render_texture_width, render_texture_height)

    ball_position = pr.Vector2(render_texture_width / 2.0, render_texture_height / 2.0)
    ball_speed = pr.Vector2(5.0, 4.0)
    ball_radius = 20.0
    rotation = 0.0

    pr.set_target_fps(60)

    while not pr.window_should_close():
        ball_position.x += ball_speed.x
        ball_position.y += ball_speed.y
        if (
            ball_position.x >= (render_texture_width - ball_radius)
            or ball_position.x <= ball_radius
        ):
            ball_speed.x *= -1.0
        if (
            ball_position.y >= (render_texture_height - ball_radius)
            or ball_position.y <= ball_radius
        ):
            ball_speed.y *= -1.0
        rotation += 0.5

        pr.begin_texture_mode(target)
        pr.clear_background(pr.SKYBLUE)
        pr.draw_rectangle(0, 0, 20, 20, pr.RED)
        pr.draw_circle_v(ball_position, ball_radius, pr.MAROON)
        pr.end_texture_mode()

        pr.begin_drawing()
        pr.clear_background(pr.RAYWHITE)
        pr.draw_texture_pro(
            target.texture,
            pr.Rectangle(
                0.0, 0.0, float(target.texture.width), float(-target.texture.height)
            ),
            pr.Rectangle(
                SCREEN_WIDTH / 2.0,
                SCREEN_HEIGHT / 2.0,
                float(target.texture.width),
                float(target.texture.height),
            ),
            pr.Vector2(target.texture.width / 2.0, target.texture.height / 2.0),
            rotation,
            pr.WHITE,
        )
        pr.draw_text(
            "DRAWING BOUNCING BALL INSIDE RENDER TEXTURE!",
            10,
            SCREEN_HEIGHT - 40,
            20,
            pr.BLACK,
        )
        pr.draw_fps(10, 10)
        pr.end_drawing()

    pr.unload_render_texture(target)
    pr.close_window()


if __name__ == "__main__":
    main()
