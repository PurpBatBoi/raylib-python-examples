from __future__ import annotations

from pathlib import Path

import pyray as pr

# Version checked: raylib 5.x/pyray API parity (reviewed 2026-02-28).

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 450
MAX_FRAME_DELAY = 20
MIN_FRAME_DELAY = 1
KEY_RIGHT = getattr(pr, "KEY_RIGHT", 262)
KEY_LEFT = getattr(pr, "KEY_LEFT", 263)


def main() -> None:
    """Run GIF frame playback by uploading each frame to a texture."""
    pr.init_window(
        SCREEN_WIDTH, SCREEN_HEIGHT, "raylib [textures] example - gif player"
    )

    resources = Path(__file__).resolve().parent / "resources"
    anim_frames = pr.ffi.new("int *", 0)
    scarfy_anim = pr.load_image_anim(str(resources / "scarfy_run.gif"), anim_frames)

    tex_scarfy_anim = pr.load_texture_from_image(scarfy_anim)
    next_frame_data_offset = 0

    current_anim_frame = 0
    frame_delay = 8
    frame_counter = 0

    pr.set_target_fps(60)

    while not pr.window_should_close():
        frame_counter += 1
        if frame_counter >= frame_delay:
            current_anim_frame += 1
            if current_anim_frame >= anim_frames[0]:
                current_anim_frame = 0

            next_frame_data_offset = (
                scarfy_anim.width * scarfy_anim.height * 4 * current_anim_frame
            )
            frame_data = (
                pr.ffi.cast("unsigned char *", scarfy_anim.data)
                + next_frame_data_offset
            )
            pr.update_texture(tex_scarfy_anim, frame_data)
            frame_counter = 0

        if pr.is_key_pressed(KEY_RIGHT):
            frame_delay += 1
        elif pr.is_key_pressed(KEY_LEFT):
            frame_delay -= 1

        frame_delay = max(MIN_FRAME_DELAY, min(MAX_FRAME_DELAY, frame_delay))

        pr.begin_drawing()
        pr.clear_background(pr.RAYWHITE)

        pr.draw_text(
            f"TOTAL GIF FRAMES:  {anim_frames[0]:02d}", 50, 30, 20, pr.LIGHTGRAY
        )
        pr.draw_text(f"CURRENT FRAME: {current_anim_frame:02d}", 50, 60, 20, pr.GRAY)
        pr.draw_text(
            f"CURRENT FRAME IMAGE.DATA OFFSET: {next_frame_data_offset:02d}",
            50,
            90,
            20,
            pr.GRAY,
        )

        pr.draw_text("FRAMES DELAY: ", 100, 305, 10, pr.DARKGRAY)
        pr.draw_text(f"{frame_delay:02d} frames", 620, 305, 10, pr.DARKGRAY)
        pr.draw_text(
            "PRESS RIGHT/LEFT KEYS to CHANGE SPEED!", 290, 350, 10, pr.DARKGRAY
        )

        for index in range(MAX_FRAME_DELAY):
            if index < frame_delay:
                pr.draw_rectangle(190 + 21 * index, 300, 20, 20, pr.RED)
            pr.draw_rectangle_lines(190 + 21 * index, 300, 20, 20, pr.MAROON)

        pr.draw_texture(
            tex_scarfy_anim,
            pr.get_screen_width() // 2 - tex_scarfy_anim.width // 2,
            140,
            pr.WHITE,
        )
        pr.draw_text(
            "(c) Scarfy sprite by Eiden Marsal",
            SCREEN_WIDTH - 200,
            SCREEN_HEIGHT - 20,
            10,
            pr.GRAY,
        )

        pr.end_drawing()

    pr.unload_texture(tex_scarfy_anim)
    pr.unload_image(scarfy_anim)
    pr.close_window()


if __name__ == "__main__":
    main()
