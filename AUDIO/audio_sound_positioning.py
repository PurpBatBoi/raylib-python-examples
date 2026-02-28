from math import cos, sin
from pathlib import Path
from typing import Any

import pyray as pr

# Version checked: raylib 5.x/pyray API parity (reviewed 2026-02-28).

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
MAX_DIST = 1.0
BASE_GAIN = 0.35
CAMERA_PERSPECTIVE = getattr(pr, "CAMERA_PERSPECTIVE", 0)
CAMERA_FREE = getattr(pr, "CAMERA_FREE", 1)


def set_music_position(
    listener: Any,
    music: Any,
    position: pr.Vector3,
    max_dist: float,
    base_gain: float,
) -> None:
    direction = pr.vector3_subtract(position, listener.position)
    distance = pr.vector3_length(direction)

    attenuation = 1.0 / (1.0 + (distance / max_dist))
    attenuation = pr.clamp(attenuation, 0.0, 1.0)

    normalized_direction = pr.vector3_normalize(direction)
    forward = pr.vector3_normalize(
        pr.vector3_subtract(listener.target, listener.position)
    )
    right = pr.vector3_normalize(pr.vector3_cross_product(listener.up, forward))

    dot_product = pr.vector3_dot_product(forward, normalized_direction)
    if dot_product < 0.0:
        attenuation *= 1.0 + dot_product * 0.5

    pan = 0.5 + 0.5 * pr.vector3_dot_product(normalized_direction, right)

    pr.set_music_volume(music, attenuation * base_gain)
    pr.set_music_pan(music, pan)


def main() -> None:
    pr.init_window(
        SCREEN_WIDTH, SCREEN_HEIGHT, "raylib [audio] example - sound positioning"
    )
    pr.init_audio_device()

    camera = pr.Camera3D(
        pr.Vector3(0.0, 5.0, 5.0),
        pr.Vector3(0.0, 0.0, 0.0),
        pr.Vector3(0.0, 1.0, 0.0),
        60.0,
        int(CAMERA_PERSPECTIVE),
    )

    pr.disable_cursor()

    resources = Path(__file__).resolve().parent / "resources"
    music_path = resources / "country.mp3"

    music = pr.load_music_stream(str(music_path))
    music.looping = True
    pr.play_music_stream(music)

    pr.set_target_fps(60)

    while not pr.window_should_close():
        pr.update_camera(camera, int(CAMERA_FREE))
        pr.update_music_stream(music)

        th = pr.get_time()
        sphere_pos = pr.Vector3(5.0 * cos(th), 0.0, 5.0 * sin(th))

        set_music_position(camera, music, sphere_pos, MAX_DIST, BASE_GAIN)

        pr.begin_drawing()
        pr.clear_background(pr.RAYWHITE)

        pr.begin_mode_3d(camera)
        pr.draw_grid(10, 2.0)
        pr.draw_sphere(sphere_pos, 0.5, pr.RED)
        pr.end_mode_3d()

        # display frame rate in the upper‑left corner
        pr.draw_text(f"FPS: {pr.get_fps()}", 10, 10, 20, pr.BLACK)

        pr.end_drawing()

    pr.unload_music_stream(music)
    pr.close_audio_device()
    pr.close_window()


if __name__ == "__main__":
    main()
