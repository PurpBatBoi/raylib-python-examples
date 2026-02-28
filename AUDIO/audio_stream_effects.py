from __future__ import annotations

from pathlib import Path
from typing import Any

import pyray as pr

# Version checked: raylib 5.x/pyray API parity (reviewed 2026-02-28).

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
KEY_SPACE = getattr(pr, "KEY_SPACE", 32)
KEY_P = getattr(pr, "KEY_P", 80)
KEY_F = getattr(pr, "KEY_F", 70)
KEY_D = getattr(pr, "KEY_D", 68)

# 1 second delay buffer (device sampleRate * channels)
delay_buffer_size = 48000 * 2
delay_buffer = pr.ffi.new("float[]", delay_buffer_size)
delay_read_index = 2
delay_write_index = 0

low = [0.0, 0.0]
cutoff = 70.0 / 44100.0
k = cutoff / (cutoff + 0.1591549431)


@pr.ffi.callback("void(void *, unsigned int)")
def audio_process_effect_lpf(buffer: Any, frames: int) -> None:
    buffer_data = pr.ffi.cast("float *", buffer)

    for i in range(0, frames * 2, 2):
        left = float(buffer_data[i])
        right = float(buffer_data[i + 1])

        low[0] += k * (left - low[0])
        low[1] += k * (right - low[1])

        buffer_data[i] = low[0]
        buffer_data[i + 1] = low[1]


@pr.ffi.callback("void(void *, unsigned int)")
def audio_process_effect_delay(buffer: Any, frames: int) -> None:
    global delay_read_index, delay_write_index

    buffer_data = pr.ffi.cast("float *", buffer)

    for i in range(0, frames * 2, 2):
        left_delay = float(delay_buffer[delay_read_index])
        delay_read_index += 1
        right_delay = float(delay_buffer[delay_read_index])
        delay_read_index += 1

        if delay_read_index == delay_buffer_size:
            delay_read_index = 0

        buffer_data[i] = 0.5 * float(buffer_data[i]) + 0.5 * left_delay
        buffer_data[i + 1] = 0.5 * float(buffer_data[i + 1]) + 0.5 * right_delay

        delay_buffer[delay_write_index] = float(buffer_data[i])
        delay_write_index += 1
        delay_buffer[delay_write_index] = float(buffer_data[i + 1])
        delay_write_index += 1

        if delay_write_index == delay_buffer_size:
            delay_write_index = 0


def main() -> None:
    pr.init_window(
        SCREEN_WIDTH, SCREEN_HEIGHT, "raylib [audio] example - stream effects"
    )
    pr.init_audio_device()

    resources = Path(__file__).resolve().parent / "resources"
    music = pr.load_music_stream(str(resources / "country.mp3"))

    pr.play_music_stream(music)

    time_played = 0.0
    pause = False

    enable_effect_lpf = False
    enable_effect_delay = False

    pr.set_target_fps(60)

    while not pr.window_should_close():
        pr.update_music_stream(music)

        if pr.is_key_pressed(KEY_SPACE):
            pr.stop_music_stream(music)
            pr.play_music_stream(music)

        if pr.is_key_pressed(KEY_P):
            pause = not pause
            if pause:
                pr.pause_music_stream(music)
            else:
                pr.resume_music_stream(music)

        if pr.is_key_pressed(KEY_F):
            enable_effect_lpf = not enable_effect_lpf
            if enable_effect_lpf:
                pr.attach_audio_stream_processor(music.stream, audio_process_effect_lpf)
            else:
                pr.detach_audio_stream_processor(music.stream, audio_process_effect_lpf)

        if pr.is_key_pressed(KEY_D):
            enable_effect_delay = not enable_effect_delay
            if enable_effect_delay:
                pr.attach_audio_stream_processor(
                    music.stream, audio_process_effect_delay
                )
            else:
                pr.detach_audio_stream_processor(
                    music.stream, audio_process_effect_delay
                )

        music_length = pr.get_music_time_length(music)
        if music_length > 0.0:
            time_played = min(1.0, pr.get_music_time_played(music) / music_length)
        else:
            time_played = 0.0

        pr.begin_drawing()
        pr.clear_background(pr.RAYWHITE)

        pr.draw_text("MUSIC SHOULD BE PLAYING!", 245, 200, 20, pr.LIGHTGRAY)

        pr.draw_rectangle(200, 240, 400, 12, pr.LIGHTGRAY)
        pr.draw_rectangle(200, 240, int(time_played * 400.0), 12, pr.MAROON)
        pr.draw_rectangle_lines(200, 240, 400, 12, pr.GRAY)

        pr.draw_text("PRESS SPACE TO RESTART MUSIC", 215, 307, 20, pr.LIGHTGRAY)
        pr.draw_text("PRESS P TO PAUSE/RESUME MUSIC", 208, 347, 20, pr.LIGHTGRAY)

        lpf_state = "ON" if enable_effect_lpf else "OFF"
        delay_state = "ON" if enable_effect_delay else "OFF"
        pr.draw_text(
            f"PRESS F TO TOGGLE LPF EFFECT: {lpf_state}", 200, 427, 20, pr.GRAY
        )
        pr.draw_text(
            f"PRESS D TO TOGGLE DELAY EFFECT: {delay_state}", 180, 467, 20, pr.GRAY
        )

        pr.end_drawing()

    if enable_effect_lpf:
        pr.detach_audio_stream_processor(music.stream, audio_process_effect_lpf)
    if enable_effect_delay:
        pr.detach_audio_stream_processor(music.stream, audio_process_effect_delay)

    pr.unload_music_stream(music)
    pr.close_audio_device()
    pr.close_window()


if __name__ == "__main__":
    main()
