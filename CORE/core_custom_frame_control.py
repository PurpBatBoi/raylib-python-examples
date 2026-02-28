from __future__ import annotations

import pyray as pr

# Version checked: raylib 5.x/pyray API parity (reviewed 2026-02-28).

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 450
KEY_SPACE = getattr(pr, "KEY_SPACE", 32)
KEY_UP = getattr(pr, "KEY_UP", 265)
KEY_DOWN = getattr(pr, "KEY_DOWN", 264)


def main() -> None:
    """Run the custom frame control example."""
    pr.init_window(
        SCREEN_WIDTH,
        SCREEN_HEIGHT,
        "raylib [core] example - custom frame control",
    )

    time_counter = 0.0
    position = 0.0
    pause = False
    target_fps = 60
    pr.set_target_fps(target_fps)

    while not pr.window_should_close():
        if pr.is_key_pressed(KEY_SPACE):
            pause = not pause
        if pr.is_key_pressed(KEY_UP):
            target_fps += 20
            pr.set_target_fps(target_fps)
        elif pr.is_key_pressed(KEY_DOWN):
            target_fps -= 20
            if target_fps < 0:
                target_fps = 0
            pr.set_target_fps(target_fps)

        delta_time = pr.get_frame_time()

        if not pause:
            position += 200.0 * delta_time
            if position >= pr.get_screen_width():
                position = 0.0
            time_counter += delta_time

        pr.begin_drawing()
        pr.clear_background(pr.RAYWHITE)
        for i in range(max(1, pr.get_screen_width() // 200)):
            pr.draw_rectangle(200 * i, 0, 1, pr.get_screen_height(), pr.SKYBLUE)
        pr.draw_circle(int(position), pr.get_screen_height() // 2 - 25, 50.0, pr.RED)
        pr.draw_text(
            f"{time_counter*1000.0:03.0f} ms",
            int(position) - 40,
            pr.get_screen_height() // 2 - 100,
            20,
            pr.MAROON,
        )
        pr.draw_text(
            f"PosX: {position:03.0f}",
            int(position) - 50,
            pr.get_screen_height() // 2 + 40,
            20,
            pr.BLACK,
        )
        pr.draw_text(
            "Circle is moving at a constant 200 pixels/sec,\nindependently of the frame rate.",
            10,
            10,
            20,
            pr.DARKGRAY,
        )
        pr.draw_text(
            "PRESS SPACE to PAUSE MOVEMENT",
            10,
            pr.get_screen_height() - 60,
            20,
            pr.GRAY,
        )
        pr.draw_text(
            "PRESS UP | DOWN to CHANGE TARGET FPS",
            10,
            pr.get_screen_height() - 30,
            20,
            pr.GRAY,
        )
        pr.draw_text(
            f"TARGET FPS: {target_fps}", pr.get_screen_width() - 220, 10, 20, pr.LIME
        )
        if delta_time != 0.0:
            pr.draw_text(
                f"CURRENT FPS: {int(1.0/delta_time)}",
                pr.get_screen_width() - 220,
                40,
                20,
                pr.GREEN,
            )
        pr.end_drawing()

    pr.close_window()


if __name__ == "__main__":
    main()
