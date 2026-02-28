from __future__ import annotations

from pathlib import Path

import pyray as pr

# Version checked: raylib 5.x/pyray API parity (reviewed 2026-02-28).

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
KEY_SPACE = 32
KEY_P = 80
KEY_LEFT = 263
KEY_RIGHT = 262
KEY_DOWN = 264
KEY_UP = 265


def main() -> None:
    pr.init_window(SCREEN_WIDTH, SCREEN_HEIGHT, "raylib [audio] example - music stream")
    pr.init_audio_device()

    resources = Path(__file__).resolve().parent / "resources"
    music = pr.load_music_stream(str(resources / "country.mp3"))

    pr.play_music_stream(music)

    time_played = 0.0
    pause = False

    pan = 0.0
    pr.set_music_pan(music, (1.0 - pan) * 0.5)

    volume = 0.8
    pr.set_music_volume(music, volume)

    pr.set_target_fps(30)

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

        if pr.is_key_down(KEY_LEFT):
            pan -= 0.05
            if pan < -1.0:
                pan = -1.0
            pr.set_music_pan(music, (1.0 - pan) * 0.5)
        elif pr.is_key_down(KEY_RIGHT):
            pan += 0.05
            if pan > 1.0:
                pan = 1.0
            pr.set_music_pan(music, (1.0 - pan) * 0.5)

        if pr.is_key_down(KEY_DOWN):
            volume -= 0.05
            if volume < 0.0:
                volume = 0.0
            pr.set_music_volume(music, volume)
        elif pr.is_key_down(KEY_UP):
            volume += 0.05
            if volume > 1.0:
                volume = 1.0
            pr.set_music_volume(music, volume)

        time_played = pr.get_music_time_played(music) / pr.get_music_time_length(music)
        if time_played > 1.0:
            time_played = 1.0

        pr.begin_drawing()
        pr.clear_background(pr.RAYWHITE)

        pr.draw_text("MUSIC SHOULD BE PLAYING!", 255, 200, 20, pr.LIGHTGRAY)

        pr.draw_text("LEFT-RIGHT for PAN CONTROL", 320, 99, 10, pr.DARKBLUE)
        pr.draw_rectangle(300, 133, 200, 12, pr.LIGHTGRAY)
        pr.draw_rectangle_lines(300, 133, 200, 12, pr.GRAY)
        pan_x = int(300 + ((pan + 1.0) / 2.0) * 200 - 5)
        pr.draw_rectangle(pan_x, 123, 10, 28, pr.DARKGRAY)

        pr.draw_rectangle(200, 267, 400, 12, pr.LIGHTGRAY)
        pr.draw_rectangle(200, 267, int(time_played * 400.0), 12, pr.MAROON)
        pr.draw_rectangle_lines(200, 267, 400, 12, pr.GRAY)

        pr.draw_text("PRESS SPACE TO RESTART MUSIC", 215, 334, 20, pr.LIGHTGRAY)
        pr.draw_text("PRESS P TO PAUSE/RESUME MUSIC", 208, 373, 20, pr.LIGHTGRAY)

        pr.draw_text("UP-DOWN for VOLUME CONTROL", 320, 445, 10, pr.DARKGREEN)
        pr.draw_rectangle(300, 480, 200, 12, pr.LIGHTGRAY)
        pr.draw_rectangle_lines(300, 480, 200, 12, pr.GRAY)
        volume_x = int(300 + volume * 200 - 5)
        pr.draw_rectangle(volume_x, 472, 10, 28, pr.DARKGRAY)

        pr.end_drawing()

    pr.unload_music_stream(music)
    pr.close_audio_device()
    pr.close_window()


if __name__ == "__main__":
    main()
