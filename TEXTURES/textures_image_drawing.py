from __future__ import annotations

from pathlib import Path

import pyray as pr

# Version checked: raylib 5.x/pyray API parity (reviewed 2026-02-28).

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 450


def main() -> None:
    """Run the image composition and drawing example."""
    pr.init_window(
        SCREEN_WIDTH, SCREEN_HEIGHT, "raylib [textures] example - image drawing"
    )

    resources = Path(__file__).resolve().parent / "resources"

    cat = pr.load_image(str(resources / "cat.png"))
    pr.image_crop(cat, pr.Rectangle(100.0, 10.0, 280.0, 380.0))
    pr.image_flip_horizontal(cat)
    pr.image_resize(cat, 150, 200)

    parrots = pr.load_image(str(resources / "parrots.png"))

    pr.image_draw(
        parrots,
        cat,
        pr.Rectangle(0.0, 0.0, float(cat.width), float(cat.height)),
        pr.Rectangle(30.0, 40.0, cat.width * 1.5, cat.height * 1.5),
        pr.WHITE,
    )
    pr.image_crop(
        parrots,
        pr.Rectangle(0.0, 50.0, float(parrots.width), float(parrots.height - 100)),
    )

    pr.image_draw_pixel(parrots, 10, 10, pr.RAYWHITE)
    pr.image_draw_circle_lines(parrots, 10, 10, 5, pr.RAYWHITE)
    pr.image_draw_rectangle(parrots, 5, 20, 10, 10, pr.RAYWHITE)

    pr.unload_image(cat)

    font = pr.load_font(str(resources / "custom_jupiter_crash.png"))
    pr.image_draw_text_ex(
        parrots,
        font,
        "PARROTS & CAT",
        pr.Vector2(300.0, 230.0),
        float(font.baseSize),
        -2.0,
        pr.WHITE,
    )
    pr.unload_font(font)

    texture = pr.load_texture_from_image(parrots)
    pr.unload_image(parrots)

    pr.set_target_fps(60)

    while not pr.window_should_close():
        pr.begin_drawing()
        pr.clear_background(pr.RAYWHITE)

        draw_x = SCREEN_WIDTH // 2 - texture.width // 2
        draw_y = SCREEN_HEIGHT // 2 - texture.height // 2 - 40

        pr.draw_texture(texture, draw_x, draw_y, pr.WHITE)
        pr.draw_rectangle_lines(
            draw_x, draw_y, texture.width, texture.height, pr.DARKGRAY
        )

        pr.draw_text(
            "We are drawing only one texture from various images composed!",
            240,
            350,
            10,
            pr.DARKGRAY,
        )
        pr.draw_text(
            "Source images have been cropped, scaled, flipped and copied one over the other.",
            190,
            370,
            10,
            pr.DARKGRAY,
        )

        pr.end_drawing()

    pr.unload_texture(texture)
    pr.close_window()


if __name__ == "__main__":
    main()
