from __future__ import annotations

import math
from typing import Any

import pyray as pr

# Version checked: raylib 5.x/pyray API parity (reviewed 2026-02-28).

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
MAX_SAMPLES = 512
MAX_SAMPLES_PER_UPDATE = 4096
MOUSE_BUTTON_LEFT = getattr(pr, "MOUSE_BUTTON_LEFT", 0)

frequency = 440.0
audio_frequency = 440.0
old_frequency = 1.0
sine_idx = 0.0


@pr.ffi.callback("void(void *, unsigned int)")
def audio_input_callback(buffer: Any, frames: int) -> None:
    global audio_frequency, sine_idx

    audio_frequency = frequency + (audio_frequency - frequency) * 0.95

    increment = audio_frequency / 44100.0
    data = pr.ffi.cast("short *", buffer)

    for i in range(frames):
        data[i] = int(32000.0 * math.sin(2.0 * math.pi * sine_idx))
        sine_idx += increment
        if sine_idx > 1.0:
            sine_idx -= 1.0


def main() -> None:
    global frequency, old_frequency

    pr.init_window(SCREEN_WIDTH, SCREEN_HEIGHT, "raylib [audio] example - raw stream")
    pr.init_audio_device()

    pr.set_audio_stream_buffer_size_default(MAX_SAMPLES_PER_UPDATE)

    stream = pr.load_audio_stream(44100, 16, 1)
    pr.set_audio_stream_callback(stream, audio_input_callback)

    data: list[int] = [0] * MAX_SAMPLES

    pr.play_audio_stream(stream)

    wave_length = 1

    pr.set_target_fps(30)

    while not pr.window_should_close():
        mouse_position = pr.get_mouse_position()

        if pr.is_mouse_button_down(MOUSE_BUTTON_LEFT):
            frequency = 40.0 + mouse_position.y
            pan = mouse_position.x / SCREEN_WIDTH
            pr.set_audio_stream_pan(stream, pan)

        if frequency != old_frequency:
            wave_length = int(22050 / frequency)
            wave_length = max(1, min(MAX_SAMPLES // 2, wave_length))

            for i in range(wave_length * 2):
                data[i] = int(math.sin((2.0 * math.pi * i) / wave_length) * 32000)
            for j in range(wave_length * 2, MAX_SAMPLES):
                data[j] = 0

            old_frequency = frequency

        pr.begin_drawing()
        pr.clear_background(pr.RAYWHITE)

        pr.draw_text(
            f"sine frequency: {int(frequency)}",
            pr.get_screen_width() - 220,
            10,
            20,
            pr.RED,
        )
        pr.draw_text(
            "click mouse button to change frequency or pan", 10, 10, 20, pr.DARKGRAY
        )

        for i in range(SCREEN_WIDTH):
            sample_index = i * MAX_SAMPLES // SCREEN_WIDTH
            y = int(333 + 67 * data[sample_index] / 32000.0)
            pr.draw_pixel(i, y, pr.RED)

        pr.end_drawing()

    pr.unload_audio_stream(stream)
    pr.close_audio_device()
    pr.close_window()


if __name__ == "__main__":
    main()
