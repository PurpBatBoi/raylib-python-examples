from __future__ import annotations

from pathlib import Path

import pyray as pr

# Version checked: raylib 5.x/pyray API parity (reviewed 2026-02-28).

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 450


def main() -> None:
    """Run the image-to-texture loading example."""
    pr.init_window(
        SCREEN_WIDTH, SCREEN_HEIGHT, "raylib [textures] example - image loading"
    )

    resources = Path(__file__).resolve().parent / "resources"
    image = pr.load_image(str(resources / "raylib_logo.png"))
    texture = pr.load_texture_from_image(image)
    pr.unload_image(image)

    pr.set_target_fps(60)

    while not pr.window_should_close():
        pr.begin_drawing()
        pr.clear_background(pr.RAYWHITE)

        pr.draw_texture(
            texture,
            SCREEN_WIDTH // 2 - texture.width // 2,
            SCREEN_HEIGHT // 2 - texture.height // 2,
            pr.WHITE,
        )
        pr.draw_text("this IS a texture loaded from an image!", 300, 370, 10, pr.GRAY)

        pr.end_drawing()

    pr.unload_texture(texture)
    pr.close_window()


if __name__ == "__main__":
    main()
