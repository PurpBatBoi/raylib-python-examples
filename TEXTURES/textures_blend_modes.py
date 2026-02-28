from __future__ import annotations

from pathlib import Path

import pyray as pr

# Version checked: raylib 5.x/pyray API parity (reviewed 2026-02-28).

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 450
KEY_SPACE = getattr(pr, "KEY_SPACE", 32)

BLEND_ALPHA = getattr(pr, "BLEND_ALPHA", 0)
BLEND_ADDITIVE = getattr(pr, "BLEND_ADDITIVE", 1)
BLEND_MULTIPLIED = getattr(pr, "BLEND_MULTIPLIED", 2)
BLEND_ADD_COLORS = getattr(pr, "BLEND_ADD_COLORS", 3)


def main() -> None:
    """Run blend mode switching between foreground and background textures."""
    pr.init_window(
        SCREEN_WIDTH, SCREEN_HEIGHT, "raylib [textures] example - blend modes"
    )

    resources = Path(__file__).resolve().parent / "resources"
    bg_image = pr.load_image(str(resources / "cyberpunk_street_background.png"))
    fg_image = pr.load_image(str(resources / "cyberpunk_street_foreground.png"))

    bg_texture = pr.load_texture_from_image(bg_image)
    fg_texture = pr.load_texture_from_image(fg_image)

    pr.unload_image(bg_image)
    pr.unload_image(fg_image)

    blend_modes = [BLEND_ALPHA, BLEND_ADDITIVE, BLEND_MULTIPLIED, BLEND_ADD_COLORS]
    blend_labels = {
        BLEND_ALPHA: "Current: BLEND_ALPHA",
        BLEND_ADDITIVE: "Current: BLEND_ADDITIVE",
        BLEND_MULTIPLIED: "Current: BLEND_MULTIPLIED",
        BLEND_ADD_COLORS: "Current: BLEND_ADD_COLORS",
    }
    blend_index = 0

    pr.set_target_fps(60)

    while not pr.window_should_close():
        if pr.is_key_pressed(KEY_SPACE):
            blend_index = (blend_index + 1) % len(blend_modes)

        blend_mode = blend_modes[blend_index]

        pr.begin_drawing()
        pr.clear_background(pr.RAYWHITE)

        pr.draw_texture(
            bg_texture,
            SCREEN_WIDTH // 2 - bg_texture.width // 2,
            SCREEN_HEIGHT // 2 - bg_texture.height // 2,
            pr.WHITE,
        )

        pr.begin_blend_mode(blend_mode)
        pr.draw_texture(
            fg_texture,
            SCREEN_WIDTH // 2 - fg_texture.width // 2,
            SCREEN_HEIGHT // 2 - fg_texture.height // 2,
            pr.WHITE,
        )
        pr.end_blend_mode()

        pr.draw_text("Press SPACE to change blend modes.", 310, 350, 10, pr.GRAY)
        pr.draw_text(blend_labels[blend_mode], SCREEN_WIDTH // 2 - 60, 370, 10, pr.GRAY)
        pr.draw_text(
            "(c) Cyberpunk Street Environment by Luis Zuno (@ansimuz)",
            SCREEN_WIDTH - 330,
            SCREEN_HEIGHT - 20,
            10,
            pr.GRAY,
        )

        pr.end_drawing()

    pr.unload_texture(fg_texture)
    pr.unload_texture(bg_texture)
    pr.close_window()


if __name__ == "__main__":
    main()
