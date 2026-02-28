from __future__ import annotations

import pyray as pr

# Version checked: raylib 5.x/pyray API parity (reviewed 2026-02-28).

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 450

FLAG_WINDOW_RESIZABLE = int(getattr(pr, "FLAG_WINDOW_RESIZABLE", 4))
FLAG_VSYNC_HINT = int(getattr(pr, "FLAG_VSYNC_HINT", 64))
TEXTURE_FILTER_BILINEAR = int(getattr(pr, "TEXTURE_FILTER_BILINEAR", 1))
KEY_SPACE = getattr(pr, "KEY_SPACE", 32)


def main() -> None:
    """Run the letterbox render scaling example."""
    pr.set_config_flags(FLAG_WINDOW_RESIZABLE | FLAG_VSYNC_HINT)
    pr.init_window(
        SCREEN_WIDTH,
        SCREEN_HEIGHT,
        "raylib [core] example - window letterbox",
    )
    pr.set_window_min_size(320, 240)

    game_screen_width = 640
    game_screen_height = 480

    target = pr.load_render_texture(game_screen_width, game_screen_height)
    pr.set_texture_filter(target.texture, TEXTURE_FILTER_BILINEAR)

    colors = [
        pr.Color(
            pr.get_random_value(100, 250),
            pr.get_random_value(50, 150),
            pr.get_random_value(10, 100),
            255,
        )
        for _ in range(10)
    ]

    pr.set_target_fps(60)

    while not pr.window_should_close():
        scale = min(
            pr.get_screen_width() / game_screen_width,
            pr.get_screen_height() / game_screen_height,
        )

        if pr.is_key_pressed(KEY_SPACE):
            colors = [
                pr.Color(
                    pr.get_random_value(100, 250),
                    pr.get_random_value(50, 150),
                    pr.get_random_value(10, 100),
                    255,
                )
                for _ in range(10)
            ]

        mouse = pr.get_mouse_position()
        virtual_mouse = pr.Vector2(
            (mouse.x - (pr.get_screen_width() - game_screen_width * scale) * 0.5)
            / scale,
            (mouse.y - (pr.get_screen_height() - game_screen_height * scale) * 0.5)
            / scale,
        )
        virtual_mouse = pr.vector2_clamp(
            virtual_mouse,
            pr.Vector2(0.0, 0.0),
            pr.Vector2(float(game_screen_width), float(game_screen_height)),
        )

        pr.begin_texture_mode(target)
        pr.clear_background(pr.RAYWHITE)
        for i in range(10):
            pr.draw_rectangle(
                0,
                (game_screen_height // 10) * i,
                game_screen_width,
                game_screen_height // 10,
                colors[i],
            )
        pr.draw_text(
            "If executed inside a window,\nyou can resize the window,\nand see the screen scaling!",
            10,
            25,
            20,
            pr.WHITE,
        )
        pr.draw_text(
            f"Default Mouse: [{int(mouse.x)} , {int(mouse.y)}]", 350, 25, 20, pr.GREEN
        )
        pr.draw_text(
            f"Virtual Mouse: [{int(virtual_mouse.x)} , {int(virtual_mouse.y)}]",
            350,
            55,
            20,
            pr.YELLOW,
        )
        pr.end_texture_mode()

        pr.begin_drawing()
        pr.clear_background(pr.BLACK)
        pr.draw_texture_pro(
            target.texture,
            pr.Rectangle(
                0.0, 0.0, float(target.texture.width), float(-target.texture.height)
            ),
            pr.Rectangle(
                (pr.get_screen_width() - float(game_screen_width) * scale) * 0.5,
                (pr.get_screen_height() - float(game_screen_height) * scale) * 0.5,
                float(game_screen_width) * scale,
                float(game_screen_height) * scale,
            ),
            pr.Vector2(0.0, 0.0),
            0.0,
            pr.WHITE,
        )
        pr.end_drawing()

    pr.unload_render_texture(target)
    pr.close_window()


if __name__ == "__main__":
    main()
