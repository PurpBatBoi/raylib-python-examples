from __future__ import annotations

from pathlib import Path

import pyray as pr

# Version checked: raylib 5.x/pyray API parity (reviewed 2026-02-28).

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 450
MAX_FRAME_SPEED = 15
MIN_FRAME_SPEED = 1

KEY_RIGHT = getattr(pr, "KEY_RIGHT", 262)
KEY_LEFT = getattr(pr, "KEY_LEFT", 263)


def main() -> None:
    """Run sprite sheet animation speed-control demo."""
    pr.init_window(
        SCREEN_WIDTH, SCREEN_HEIGHT, "raylib [textures] example - sprite animation"
    )

    resources = Path(__file__).resolve().parent / "resources"
    scarfy = pr.load_texture(str(resources / "scarfy.png"))

    position = pr.Vector2(350.0, 280.0)
    frame_rec = pr.Rectangle(0.0, 0.0, scarfy.width / 6.0, float(scarfy.height))
    current_frame = 0
    frames_counter = 0
    frames_speed = 8

    pr.set_target_fps(60)

    while not pr.window_should_close():
        frames_counter += 1

        if frames_counter >= (60 // frames_speed):
            frames_counter = 0
            current_frame += 1
            if current_frame > 5:
                current_frame = 0
            frame_rec.x = current_frame * scarfy.width / 6.0

        if pr.is_key_pressed(KEY_RIGHT):
            frames_speed += 1
        elif pr.is_key_pressed(KEY_LEFT):
            frames_speed -= 1

        frames_speed = max(MIN_FRAME_SPEED, min(MAX_FRAME_SPEED, frames_speed))

        pr.begin_drawing()
        pr.clear_background(pr.RAYWHITE)

        pr.draw_texture(scarfy, 15, 40, pr.WHITE)
        pr.draw_rectangle_lines(15, 40, scarfy.width, scarfy.height, pr.LIME)
        pr.draw_rectangle_lines(
            15 + int(frame_rec.x),
            40 + int(frame_rec.y),
            int(frame_rec.width),
            int(frame_rec.height),
            pr.RED,
        )

        pr.draw_text("FRAME SPEED: ", 165, 210, 10, pr.DARKGRAY)
        pr.draw_text(f"{frames_speed:02d} FPS", 575, 210, 10, pr.DARKGRAY)
        pr.draw_text(
            "PRESS RIGHT/LEFT KEYS to CHANGE SPEED!", 290, 240, 10, pr.DARKGRAY
        )

        for index in range(MAX_FRAME_SPEED):
            if index < frames_speed:
                pr.draw_rectangle(250 + 21 * index, 205, 20, 20, pr.RED)
            pr.draw_rectangle_lines(250 + 21 * index, 205, 20, 20, pr.MAROON)

        pr.draw_texture_rec(scarfy, frame_rec, position, pr.WHITE)
        pr.draw_text(
            "(c) Scarfy sprite by Eiden Marsal",
            SCREEN_WIDTH - 200,
            SCREEN_HEIGHT - 20,
            10,
            pr.GRAY,
        )
        pr.end_drawing()

    pr.unload_texture(scarfy)
    pr.close_window()


if __name__ == "__main__":
    main()
