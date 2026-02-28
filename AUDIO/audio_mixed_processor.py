from __future__ import annotations

import math
from pathlib import Path
from typing import Any

import pyray as pr

# Version checked: raylib 5.x/pyray API parity (reviewed 2026-02-28).

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
HISTORY_SIZE = 400
KEY_LEFT = getattr(pr, "KEY_LEFT", 263)
KEY_RIGHT = getattr(pr, "KEY_RIGHT", 262)
KEY_SPACE = getattr(pr, "KEY_SPACE", 32)

exponent = 1.0
average_volume: list[float] = [0.0] * HISTORY_SIZE


@pr.ffi.callback("void(void *, unsigned int)")
def process_audio(buffer: Any, frames: int) -> None:
    global average_volume

    if frames <= 0:
        return

    samples = pr.ffi.cast("float *", buffer)
    average = 0.0

    for frame in range(frames):
        left_index = frame * 2
        right_index = left_index + 1

        left = float(samples[left_index])
        right = float(samples[right_index])

        left = math.copysign(abs(left) ** exponent, left)
        right = math.copysign(abs(right) ** exponent, right)

        samples[left_index] = left
        samples[right_index] = right

        average += abs(left) / frames
        average += abs(right) / frames

    average_volume[:-1] = average_volume[1:]
    average_volume[-1] = average


def main() -> None:
    global exponent

    pr.init_window(
        SCREEN_WIDTH, SCREEN_HEIGHT, "raylib [audio] example - mixed processor"
    )
    pr.init_audio_device()

    pr.attach_audio_mixed_processor(process_audio)

    resources = Path(__file__).resolve().parent / "resources"
    music = pr.load_music_stream(str(resources / "country.mp3"))
    sound = pr.load_sound(str(resources / "coin.wav"))

    pr.play_music_stream(music)
    pr.set_target_fps(60)

    while not pr.window_should_close():
        pr.update_music_stream(music)

        if pr.is_key_pressed(KEY_LEFT):
            exponent -= 0.05
        if pr.is_key_pressed(KEY_RIGHT):
            exponent += 0.05

        exponent = max(0.5, min(3.0, exponent))

        if pr.is_key_pressed(KEY_SPACE):
            pr.play_sound(sound)

        pr.begin_drawing()
        pr.clear_background(pr.RAYWHITE)

        pr.draw_text("MUSIC SHOULD BE PLAYING!", 255, 150, 20, pr.LIGHTGRAY)
        pr.draw_text(f"EXPONENT = {exponent:.2f}", 215, 180, 20, pr.LIGHTGRAY)

        pr.draw_rectangle(199, 199, 402, 34, pr.LIGHTGRAY)
        for i, value in enumerate(average_volume):
            y = 232 - int(value * 32.0)
            x = 201 + i
            pr.draw_line(x, y, x, 232, pr.MAROON)

        pr.draw_rectangle_lines(199, 199, 402, 34, pr.GRAY)

        pr.draw_text("PRESS SPACE TO PLAY OTHER SOUND", 200, 250, 20, pr.LIGHTGRAY)
        pr.draw_text(
            "USE LEFT AND RIGHT ARROWS TO ALTER DISTORTION",
            140,
            280,
            20,
            pr.LIGHTGRAY,
        )

        pr.end_drawing()

    pr.unload_sound(sound)
    pr.unload_music_stream(music)
    pr.detach_audio_mixed_processor(process_audio)
    pr.close_audio_device()
    pr.close_window()


if __name__ == "__main__":
    main()
