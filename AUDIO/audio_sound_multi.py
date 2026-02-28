from __future__ import annotations

from pathlib import Path

import pyray as pr

# Version checked: raylib 5.x/pyray API parity (reviewed 2026-02-28).

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
MAX_SOUNDS = 10
KEY_SPACE = getattr(pr, "KEY_SPACE", 32)


def main() -> None:
    pr.init_window(SCREEN_WIDTH, SCREEN_HEIGHT, "raylib [audio] example - sound multi")
    pr.init_audio_device()

    resources = Path(__file__).resolve().parent / "resources"
    source_sound = pr.load_sound(str(resources / "sound.wav"))

    sound_array = [source_sound]
    for _ in range(1, MAX_SOUNDS):
        sound_array.append(pr.load_sound_alias(source_sound))

    current_sound = 0

    pr.set_target_fps(60)

    while not pr.window_should_close():
        if pr.is_key_pressed(KEY_SPACE):
            pr.play_sound(sound_array[current_sound])
            current_sound += 1
            if current_sound >= MAX_SOUNDS:
                current_sound = 0

        pr.begin_drawing()
        pr.clear_background(pr.RAYWHITE)

        pr.draw_text("Press SPACE to PLAY a WAV sound!", 200, 240, 20, pr.LIGHTGRAY)

        pr.end_drawing()

    for i in range(1, MAX_SOUNDS):
        pr.unload_sound_alias(sound_array[i])
    pr.unload_sound(source_sound)

    pr.close_audio_device()
    pr.close_window()


if __name__ == "__main__":
    main()
