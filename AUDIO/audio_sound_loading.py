from __future__ import annotations

from pathlib import Path

import pyray as pr

# Version checked: raylib 5.x/pyray API parity (reviewed 2026-02-28).

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
KEY_SPACE = getattr(pr, "KEY_SPACE", 32)
KEY_ENTER = getattr(pr, "KEY_ENTER", 257)


def main() -> None:
    pr.init_window(
        SCREEN_WIDTH, SCREEN_HEIGHT, "raylib [audio] example - sound loading"
    )
    pr.init_audio_device()

    resources = Path(__file__).resolve().parent / "resources"
    fx_wav = pr.load_sound(str(resources / "sound.wav"))
    fx_ogg = pr.load_sound(str(resources / "target.ogg"))

    pr.set_target_fps(60)

    while not pr.window_should_close():
        if pr.is_key_pressed(KEY_SPACE):
            pr.play_sound(fx_wav)
        if pr.is_key_pressed(KEY_ENTER):
            pr.play_sound(fx_ogg)

        pr.begin_drawing()
        pr.clear_background(pr.RAYWHITE)

        pr.draw_text("Press SPACE to PLAY the WAV sound!", 200, 240, 20, pr.LIGHTGRAY)
        pr.draw_text("Press ENTER to PLAY the OGG sound!", 200, 293, 20, pr.LIGHTGRAY)

        pr.end_drawing()

    pr.unload_sound(fx_wav)
    pr.unload_sound(fx_ogg)
    pr.close_audio_device()
    pr.close_window()


if __name__ == "__main__":
    main()
