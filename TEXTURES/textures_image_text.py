from __future__ import annotations

from pathlib import Path

import pyray as pr

# Version checked: raylib 5.x/pyray API parity (reviewed 2026-02-28).

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 450
KEY_SPACE = getattr(pr, "KEY_SPACE", 32)


def main() -> None:
    """Run the image text drawing and font atlas visualization demo."""
    pr.init_window(
        SCREEN_WIDTH, SCREEN_HEIGHT, "raylib [textures] example - image text"
    )

    resources = Path(__file__).resolve().parent / "resources"
    parrots = pr.load_image(str(resources / "parrots.png"))
    font = pr.load_font_ex(str(resources / "KAISG.ttf"), 64, None, 0)

    pr.image_draw_text_ex(
        parrots,
        font,
        "[Parrots font drawing]",
        pr.Vector2(20.0, 20.0),
        float(font.baseSize),
        0.0,
        pr.RED,
    )

    texture = pr.load_texture_from_image(parrots)
    pr.unload_image(parrots)

    position = pr.Vector2(
        SCREEN_WIDTH / 2.0 - texture.width / 2.0,
        SCREEN_HEIGHT / 2.0 - texture.height / 2.0 - 20.0,
    )

    pr.set_target_fps(60)

    while not pr.window_should_close():
        show_font = pr.is_key_down(KEY_SPACE)

        pr.begin_drawing()
        pr.clear_background(pr.RAYWHITE)

        if not show_font:
            pr.draw_texture_v(texture, position, pr.WHITE)
            pr.draw_text_ex(
                font,
                "[Parrots font drawing]",
                pr.Vector2(position.x + 20.0, position.y + 300.0),
                float(font.baseSize),
                0.0,
                pr.WHITE,
            )
        else:
            pr.draw_texture(
                font.texture, SCREEN_WIDTH // 2 - font.texture.width // 2, 50, pr.BLACK
            )

        pr.draw_text("PRESS SPACE to SHOW FONT ATLAS USED", 290, 420, 10, pr.DARKGRAY)
        pr.end_drawing()

    pr.unload_texture(texture)
    pr.unload_font(font)
    pr.close_window()


if __name__ == "__main__":
    main()
