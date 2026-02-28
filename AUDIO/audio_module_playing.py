from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

import pyray as pr

# Version checked: raylib 5.x/pyray API parity (reviewed 2026-02-28).

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
MAX_CIRCLES = 64
FLAG_MSAA_4X_HINT = getattr(pr, "FLAG_MSAA_4X_HINT", 32)
KEY_SPACE = getattr(pr, "KEY_SPACE", 32)
KEY_P = getattr(pr, "KEY_P", 80)
KEY_DOWN = getattr(pr, "KEY_DOWN", 264)
KEY_UP = getattr(pr, "KEY_UP", 265)


@dataclass
class Circle:
    position: pr.Vector2
    radius: float
    alpha: float
    speed: float
    color: pr.Color


def create_circle(colors: list[pr.Color]) -> Circle:
    radius = float(pr.get_random_value(10, 40))
    return Circle(
        position=pr.Vector2(
            float(pr.get_random_value(int(radius), int(SCREEN_WIDTH - radius))),
            float(pr.get_random_value(int(radius), int(SCREEN_HEIGHT - radius))),
        ),
        radius=radius,
        alpha=0.0,
        speed=float(pr.get_random_value(1, 100)) / 2000.0,
        color=colors[pr.get_random_value(0, 13)],
    )


def main() -> None:
    pr.set_config_flags(FLAG_MSAA_4X_HINT)
    pr.init_window(
        SCREEN_WIDTH, SCREEN_HEIGHT, "raylib [audio] example - module playing"
    )
    pr.init_audio_device()

    colors: list[pr.Color] = [
        pr.ORANGE,
        pr.RED,
        pr.GOLD,
        pr.LIME,
        pr.BLUE,
        pr.VIOLET,
        pr.BROWN,
        pr.LIGHTGRAY,
        pr.PINK,
        pr.YELLOW,
        pr.GREEN,
        pr.SKYBLUE,
        pr.PURPLE,
        pr.BEIGE,
    ]

    circles: list[Circle] = [create_circle(colors) for _ in range(MAX_CIRCLES)]

    resources = Path(__file__).resolve().parent / "resources"
    music_path = resources / "mini1111.xm"

    music = pr.load_music_stream(str(music_path))
    music.looping = False
    pitch = 1.0

    pr.play_music_stream(music)

    time_played = 0.0
    pause = False

    pr.set_target_fps(60)

    while not pr.window_should_close():
        pr.update_music_stream(music)

        if pr.is_key_pressed(KEY_SPACE):
            pr.stop_music_stream(music)
            pr.play_music_stream(music)
            pause = False

        if pr.is_key_pressed(KEY_P):
            pause = not pause
            if pause:
                pr.pause_music_stream(music)
            else:
                pr.resume_music_stream(music)

        if pr.is_key_down(KEY_DOWN):
            pitch -= 0.01
        elif pr.is_key_down(KEY_UP):
            pitch += 0.01

        pr.set_music_pitch(music, pitch)

        music_time_length = pr.get_music_time_length(music)
        if music_time_length > 0:
            time_played = (
                pr.get_music_time_played(music)
                / music_time_length
                * (SCREEN_WIDTH - 40)
            )
        else:
            time_played = 0.0

        if not pause:
            for i in range(MAX_CIRCLES - 1, -1, -1):
                circle = circles[i]
                circle.alpha += circle.speed
                circle.radius += circle.speed * 10.0

                if circle.alpha > 1.0:
                    circle.speed *= -1

                if circle.alpha <= 0.0:
                    circles[i] = create_circle(colors)

        pr.begin_drawing()
        pr.clear_background(pr.RAYWHITE)

        for circle in reversed(circles):
            pr.draw_circle_v(
                circle.position,
                circle.radius,
                pr.fade(circle.color, circle.alpha),
            )

        pr.draw_rectangle(
            20, SCREEN_HEIGHT - 20 - 12, SCREEN_WIDTH - 40, 12, pr.LIGHTGRAY
        )
        pr.draw_rectangle(20, SCREEN_HEIGHT - 20 - 12, int(time_played), 12, pr.MAROON)
        pr.draw_rectangle_lines(
            20, SCREEN_HEIGHT - 20 - 12, SCREEN_WIDTH - 40, 12, pr.GRAY
        )

        pr.draw_rectangle(20, 20, 425, 145, pr.WHITE)
        pr.draw_rectangle_lines(20, 20, 425, 145, pr.GRAY)
        pr.draw_text("PRESS SPACE TO RESTART MUSIC", 40, 40, 20, pr.BLACK)
        pr.draw_text("PRESS P TO PAUSE/RESUME", 40, 70, 20, pr.BLACK)
        pr.draw_text("PRESS UP/DOWN TO CHANGE SPEED", 40, 100, 20, pr.BLACK)
        pr.draw_text(f"SPEED: {pitch:f}", 40, 130, 20, pr.MAROON)

        pr.end_drawing()

    pr.unload_music_stream(music)
    pr.close_audio_device()
    pr.close_window()


if __name__ == "__main__":
    main()
