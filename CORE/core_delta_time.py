from __future__ import annotations

import pyray as pr

# Version checked: raylib 5.x/pyray API parity (reviewed 2026-02-28).

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 450
KEY_R = getattr(pr, "KEY_R", 82)


def main() -> None:
    """Run the delta-time movement comparison example."""
    pr.init_window(SCREEN_WIDTH, SCREEN_HEIGHT, "raylib [core] example - delta time")

    current_fps = 60
    delta_circle = pr.Vector2(0.0, SCREEN_HEIGHT / 3.0)
    frame_circle = pr.Vector2(0.0, SCREEN_HEIGHT * (2.0 / 3.0))
    speed = 10.0
    circle_radius = 32.0

    pr.set_target_fps(current_fps)

    while not pr.window_should_close():
        mouse_wheel = pr.get_mouse_wheel_move()
        if mouse_wheel != 0.0:
            current_fps += int(mouse_wheel)
            if current_fps < 0:
                current_fps = 0
            pr.set_target_fps(current_fps)

        delta_circle.x += pr.get_frame_time() * 6.0 * speed
        frame_circle.x += 0.1 * speed

        if delta_circle.x > SCREEN_WIDTH:
            delta_circle.x = 0.0
        if frame_circle.x > SCREEN_WIDTH:
            frame_circle.x = 0.0

        if pr.is_key_pressed(KEY_R):
            delta_circle.x = 0.0
            frame_circle.x = 0.0

        pr.begin_drawing()
        pr.clear_background(pr.RAYWHITE)

        pr.draw_circle_v(delta_circle, circle_radius, pr.RED)
        pr.draw_circle_v(frame_circle, circle_radius, pr.BLUE)

        if current_fps <= 0:
            fps_text = f"FPS: unlimited ({pr.get_fps()})"
        else:
            fps_text = f"FPS: {pr.get_fps()} (target: {current_fps})"

        pr.draw_text(fps_text, 10, 10, 20, pr.DARKGRAY)
        pr.draw_text(
            f"Frame time: {pr.get_frame_time():02.02f} ms", 10, 30, 20, pr.DARKGRAY
        )
        pr.draw_text(
            "Use the scroll wheel to change the fps limit, r to reset",
            10,
            50,
            20,
            pr.DARKGRAY,
        )
        pr.draw_text("FUNC: x += GetFrameTime()*speed", 10, 90, 20, pr.RED)
        pr.draw_text("FUNC: x += speed", 10, 240, 20, pr.BLUE)
        pr.end_drawing()

    pr.close_window()


if __name__ == "__main__":
    main()
