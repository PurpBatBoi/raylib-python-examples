from __future__ import annotations

from pathlib import Path

import pyray as pr

# Version checked: raylib 5.x/pyray API parity (reviewed 2026-02-28).

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 450


def main() -> None:
    """Run image channel extraction and tinted composition demo."""
    pr.init_window(
        SCREEN_WIDTH, SCREEN_HEIGHT, "raylib [textures] example - image channel"
    )

    resources = Path(__file__).resolve().parent / "resources"
    fudesumi_image = pr.load_image(str(resources / "fudesumi.png"))

    image_alpha = pr.image_from_channel(fudesumi_image, 3)
    pr.image_alpha_mask(image_alpha, image_alpha)

    image_red = pr.image_from_channel(fudesumi_image, 0)
    pr.image_alpha_mask(image_red, image_alpha)

    image_green = pr.image_from_channel(fudesumi_image, 1)
    pr.image_alpha_mask(image_green, image_alpha)

    image_blue = pr.image_from_channel(fudesumi_image, 2)
    pr.image_alpha_mask(image_blue, image_alpha)

    background_image = pr.gen_image_checked(
        SCREEN_WIDTH,
        SCREEN_HEIGHT,
        SCREEN_WIDTH // 20,
        SCREEN_HEIGHT // 20,
        pr.ORANGE,
        pr.YELLOW,
    )

    fudesumi_texture = pr.load_texture_from_image(fudesumi_image)
    texture_alpha = pr.load_texture_from_image(image_alpha)
    texture_red = pr.load_texture_from_image(image_red)
    texture_green = pr.load_texture_from_image(image_green)
    texture_blue = pr.load_texture_from_image(image_blue)
    background_texture = pr.load_texture_from_image(background_image)

    fudesumi_rec = pr.Rectangle(
        0.0, 0.0, float(fudesumi_image.width), float(fudesumi_image.height)
    )
    fudesumi_pos = pr.Rectangle(
        50.0, 10.0, fudesumi_image.width * 0.8, fudesumi_image.height * 0.8
    )
    red_pos = pr.Rectangle(
        410.0, 10.0, fudesumi_pos.width / 2.0, fudesumi_pos.height / 2.0
    )
    green_pos = pr.Rectangle(
        600.0, 10.0, fudesumi_pos.width / 2.0, fudesumi_pos.height / 2.0
    )
    blue_pos = pr.Rectangle(
        410.0, 230.0, fudesumi_pos.width / 2.0, fudesumi_pos.height / 2.0
    )
    alpha_pos = pr.Rectangle(
        600.0, 230.0, fudesumi_pos.width / 2.0, fudesumi_pos.height / 2.0
    )

    pr.unload_image(fudesumi_image)
    pr.unload_image(image_alpha)
    pr.unload_image(image_red)
    pr.unload_image(image_green)
    pr.unload_image(image_blue)
    pr.unload_image(background_image)

    pr.set_target_fps(60)

    while not pr.window_should_close():
        pr.begin_drawing()
        pr.draw_texture(background_texture, 0, 0, pr.WHITE)
        pr.draw_texture_pro(
            fudesumi_texture,
            fudesumi_rec,
            fudesumi_pos,
            pr.Vector2(0.0, 0.0),
            0.0,
            pr.WHITE,
        )
        pr.draw_texture_pro(
            texture_red, fudesumi_rec, red_pos, pr.Vector2(0.0, 0.0), 0.0, pr.RED
        )
        pr.draw_texture_pro(
            texture_green, fudesumi_rec, green_pos, pr.Vector2(0.0, 0.0), 0.0, pr.GREEN
        )
        pr.draw_texture_pro(
            texture_blue, fudesumi_rec, blue_pos, pr.Vector2(0.0, 0.0), 0.0, pr.BLUE
        )
        pr.draw_texture_pro(
            texture_alpha, fudesumi_rec, alpha_pos, pr.Vector2(0.0, 0.0), 0.0, pr.WHITE
        )
        pr.end_drawing()

    pr.unload_texture(background_texture)
    pr.unload_texture(fudesumi_texture)
    pr.unload_texture(texture_red)
    pr.unload_texture(texture_green)
    pr.unload_texture(texture_blue)
    pr.unload_texture(texture_alpha)
    pr.close_window()


if __name__ == "__main__":
    main()
