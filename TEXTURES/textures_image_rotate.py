from __future__ import annotations

from pathlib import Path

import pyray as pr

# Version checked: raylib 5.x/pyray API parity (reviewed 2026-02-28).

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 450
NUM_TEXTURES = 3
MOUSE_BUTTON_LEFT = getattr(pr, "MOUSE_BUTTON_LEFT", 0)
KEY_RIGHT = getattr(pr, "KEY_RIGHT", 262)


def main() -> None:
    """Run image rotation conversions and texture cycling demo."""
    pr.init_window(
        SCREEN_WIDTH, SCREEN_HEIGHT, "raylib [textures] example - image rotate"
    )

    resources = Path(__file__).resolve().parent / "resources"
    image_45 = pr.load_image(str(resources / "raylib_logo.png"))
    image_90 = pr.load_image(str(resources / "raylib_logo.png"))
    image_neg_90 = pr.load_image(str(resources / "raylib_logo.png"))

    pr.image_rotate(image_45, 45)
    pr.image_rotate(image_90, 90)
    pr.image_rotate(image_neg_90, -90)

    textures = [
        pr.load_texture_from_image(image_45),
        pr.load_texture_from_image(image_90),
        pr.load_texture_from_image(image_neg_90),
    ]

    pr.unload_image(image_45)
    pr.unload_image(image_90)
    pr.unload_image(image_neg_90)

    current_texture = 0
    pr.set_target_fps(60)

    while not pr.window_should_close():
        if pr.is_mouse_button_pressed(MOUSE_BUTTON_LEFT) or pr.is_key_pressed(
            KEY_RIGHT
        ):
            current_texture = (current_texture + 1) % NUM_TEXTURES

        texture = textures[current_texture]

        pr.begin_drawing()
        pr.clear_background(pr.RAYWHITE)
        pr.draw_texture(
            texture,
            SCREEN_WIDTH // 2 - texture.width // 2,
            SCREEN_HEIGHT // 2 - texture.height // 2,
            pr.WHITE,
        )
        pr.draw_text(
            "Press LEFT MOUSE BUTTON to rotate the image clockwise",
            250,
            420,
            10,
            pr.DARKGRAY,
        )
        pr.end_drawing()

    for texture in textures:
        pr.unload_texture(texture)
    pr.close_window()


if __name__ == "__main__":
    main()
