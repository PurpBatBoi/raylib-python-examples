from __future__ import annotations

from pathlib import Path

import pyray as pr

# Version checked: raylib 5.x/pyray API parity (reviewed 2026-02-28).

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 450


def main() -> None:
    """Run the source-rectangle and destination-rectangle texture demo."""
    pr.init_window(
        SCREEN_WIDTH, SCREEN_HEIGHT, "raylib [textures] example - srcrec dstrec"
    )

    resources = Path(__file__).resolve().parent / "resources"
    scarfy = pr.load_texture(str(resources / "scarfy.png"))

    frame_width = scarfy.width // 6
    frame_height = scarfy.height

    source_rec = pr.Rectangle(0.0, 0.0, float(frame_width), float(frame_height))
    dest_rec = pr.Rectangle(
        SCREEN_WIDTH / 2.0,
        SCREEN_HEIGHT / 2.0,
        frame_width * 2.0,
        frame_height * 2.0,
    )
    origin = pr.Vector2(float(frame_width), float(frame_height))
    rotation = 0

    pr.set_target_fps(60)

    while not pr.window_should_close():
        rotation += 1

        pr.begin_drawing()
        pr.clear_background(pr.RAYWHITE)

        pr.draw_texture_pro(
            scarfy, source_rec, dest_rec, origin, float(rotation), pr.WHITE
        )

        pr.draw_line(int(dest_rec.x), 0, int(dest_rec.x), SCREEN_HEIGHT, pr.GRAY)
        pr.draw_line(0, int(dest_rec.y), SCREEN_WIDTH, int(dest_rec.y), pr.GRAY)
        pr.draw_text(
            "(c) Scarfy sprite by Eiden Marsal", SCREEN_WIDTH - 200, 430, 10, pr.GRAY
        )

        pr.end_drawing()

    pr.unload_texture(scarfy)
    pr.close_window()


if __name__ == "__main__":
    main()
