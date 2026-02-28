from __future__ import annotations

from pathlib import Path

import pyray as pr

# Version checked: raylib 5.x/pyray API parity (reviewed 2026-02-28).

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 450


def main() -> None:
    """Run background parallax scrolling demo."""
    pr.init_window(
        SCREEN_WIDTH,
        SCREEN_HEIGHT,
        "raylib [textures] example - background scrolling",
    )

    resources = Path(__file__).resolve().parent / "resources"
    background = pr.load_texture(str(resources / "cyberpunk_street_background.png"))
    midground = pr.load_texture(str(resources / "cyberpunk_street_midground.png"))
    foreground = pr.load_texture(str(resources / "cyberpunk_street_foreground.png"))

    scrolling_back = 0.0
    scrolling_mid = 0.0
    scrolling_fore = 0.0

    pr.set_target_fps(60)

    while not pr.window_should_close():
        scrolling_back -= 0.1
        scrolling_mid -= 0.5
        scrolling_fore -= 1.0

        if scrolling_back <= -background.width * 2:
            scrolling_back = 0.0
        if scrolling_mid <= -midground.width * 2:
            scrolling_mid = 0.0
        if scrolling_fore <= -foreground.width * 2:
            scrolling_fore = 0.0

        pr.begin_drawing()
        pr.clear_background(pr.get_color(0x052C46FF))

        pr.draw_texture_ex(
            background, pr.Vector2(scrolling_back, 20.0), 0.0, 2.0, pr.WHITE
        )
        pr.draw_texture_ex(
            background,
            pr.Vector2(background.width * 2.0 + scrolling_back, 20.0),
            0.0,
            2.0,
            pr.WHITE,
        )

        pr.draw_texture_ex(
            midground, pr.Vector2(scrolling_mid, 20.0), 0.0, 2.0, pr.WHITE
        )
        pr.draw_texture_ex(
            midground,
            pr.Vector2(midground.width * 2.0 + scrolling_mid, 20.0),
            0.0,
            2.0,
            pr.WHITE,
        )

        pr.draw_texture_ex(
            foreground, pr.Vector2(scrolling_fore, 70.0), 0.0, 2.0, pr.WHITE
        )
        pr.draw_texture_ex(
            foreground,
            pr.Vector2(foreground.width * 2.0 + scrolling_fore, 70.0),
            0.0,
            2.0,
            pr.WHITE,
        )

        pr.draw_text("BACKGROUND SCROLLING & PARALLAX", 10, 10, 20, pr.RED)
        pr.draw_text(
            "(c) Cyberpunk Street Environment by Luis Zuno (@ansimuz)",
            SCREEN_WIDTH - 330,
            SCREEN_HEIGHT - 20,
            10,
            pr.RAYWHITE,
        )
        pr.end_drawing()

    pr.unload_texture(background)
    pr.unload_texture(midground)
    pr.unload_texture(foreground)
    pr.close_window()


if __name__ == "__main__":
    main()
