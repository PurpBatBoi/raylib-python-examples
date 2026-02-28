from __future__ import annotations

from pathlib import Path

import pyray as pr

# Version checked: raylib 5.x/pyray API parity (reviewed 2026-02-28).

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 450
KEY_LEFT = getattr(pr, "KEY_LEFT", 263)
KEY_RIGHT = getattr(pr, "KEY_RIGHT", 262)
KEY_A = getattr(pr, "KEY_A", 65)
KEY_D = getattr(pr, "KEY_D", 68)


def main() -> None:
    """Run pseudo-3D sprite stacking demo."""
    pr.init_window(
        SCREEN_WIDTH, SCREEN_HEIGHT, "raylib [textures] example - sprite stacking"
    )

    resources = Path(__file__).resolve().parent / "resources"
    booth = pr.load_texture(str(resources / "booth.png"))

    stack_scale = 3.0
    stack_spacing = 2.0
    stack_count = 122
    rotation_speed = 30.0
    rotation = 0.0
    speed_change = 0.25

    pr.set_target_fps(60)

    while not pr.window_should_close():
        stack_spacing += pr.get_mouse_wheel_move() * 0.1
        stack_spacing = pr.clamp(stack_spacing, 0.0, 5.0)

        if pr.is_key_down(KEY_LEFT) or pr.is_key_down(KEY_A):
            rotation_speed -= speed_change
        if pr.is_key_down(KEY_RIGHT) or pr.is_key_down(KEY_D):
            rotation_speed += speed_change

        rotation += rotation_speed * pr.get_frame_time()

        frame_width = float(booth.width)
        frame_height = float(booth.height) / float(stack_count)
        scaled_width = frame_width * stack_scale
        scaled_height = frame_height * stack_scale

        pr.begin_drawing()
        pr.clear_background(pr.RAYWHITE)

        for index in range(stack_count - 1, -1, -1):
            source = pr.Rectangle(
                0.0, float(index) * frame_height, frame_width, frame_height
            )
            dest = pr.Rectangle(
                SCREEN_WIDTH / 2.0,
                SCREEN_HEIGHT / 2.0
                + index * stack_spacing
                - (stack_spacing * stack_count / 2.0),
                scaled_width,
                scaled_height,
            )
            origin = pr.Vector2(scaled_width / 2.0, scaled_height / 2.0)
            pr.draw_texture_pro(booth, source, dest, origin, rotation, pr.WHITE)

        pr.draw_text(
            "A/D to spin\nmouse wheel to change separation (aka 'angle')",
            10,
            10,
            20,
            pr.DARKGRAY,
        )
        pr.draw_text(f"current spacing: {stack_spacing:.01f}", 10, 50, 20, pr.DARKGRAY)
        pr.draw_text(f"current speed: {rotation_speed:.02f}", 10, 70, 20, pr.DARKGRAY)
        pr.draw_text(
            "redbooth model (c) kluchek under cc 4.0", 10, 420, 20, pr.DARKGRAY
        )
        pr.end_drawing()

    pr.unload_texture(booth)
    pr.close_window()


if __name__ == "__main__":
    main()
