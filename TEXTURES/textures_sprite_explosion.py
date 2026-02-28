from __future__ import annotations

from pathlib import Path

import pyray as pr

# Version checked: raylib 5.x/pyray API parity (reviewed 2026-02-28).

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 450
NUM_FRAMES_PER_LINE = 5
NUM_LINES = 5
MOUSE_BUTTON_LEFT = getattr(pr, "MOUSE_BUTTON_LEFT", 0)


def main() -> None:
    """Run click-triggered sprite explosion animation demo."""
    pr.init_window(
        SCREEN_WIDTH, SCREEN_HEIGHT, "raylib [textures] example - sprite explosion"
    )
    pr.init_audio_device()

    resources = Path(__file__).resolve().parent / "resources"
    fx_boom = pr.load_sound(str(resources / "boom.wav"))
    explosion = pr.load_texture(str(resources / "explosion.png"))

    frame_width = explosion.width / float(NUM_FRAMES_PER_LINE)
    frame_height = explosion.height / float(NUM_LINES)

    current_frame = 0
    current_line = 0
    frame_rec = pr.Rectangle(0.0, 0.0, frame_width, frame_height)
    position = pr.Vector2(0.0, 0.0)
    active = False
    frames_counter = 0

    pr.set_target_fps(60)

    while not pr.window_should_close():
        if pr.is_mouse_button_pressed(MOUSE_BUTTON_LEFT) and not active:
            position = pr.get_mouse_position()
            position.x -= frame_width / 2.0
            position.y -= frame_height / 2.0
            active = True
            pr.play_sound(fx_boom)

        if active:
            frames_counter += 1
            if frames_counter > 2:
                current_frame += 1
                if current_frame >= NUM_FRAMES_PER_LINE:
                    current_frame = 0
                    current_line += 1
                    if current_line >= NUM_LINES:
                        current_line = 0
                        active = False
                frames_counter = 0

        frame_rec.x = frame_width * current_frame
        frame_rec.y = frame_height * current_line

        pr.begin_drawing()
        pr.clear_background(pr.RAYWHITE)
        if active:
            pr.draw_texture_rec(explosion, frame_rec, position, pr.WHITE)
        pr.end_drawing()

    pr.unload_texture(explosion)
    pr.unload_sound(fx_boom)
    pr.close_audio_device()
    pr.close_window()


if __name__ == "__main__":
    main()
