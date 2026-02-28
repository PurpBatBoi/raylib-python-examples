from __future__ import annotations

from pathlib import Path

import pyray as pr

# Version checked: raylib 5.x/pyray API parity (reviewed 2026-02-28).

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 450
NUM_FRAMES = 3
MOUSE_BUTTON_LEFT = getattr(pr, "MOUSE_BUTTON_LEFT", 0)


def main() -> None:
    """Run sprite-button state and click-sound example."""
    pr.init_window(
        SCREEN_WIDTH, SCREEN_HEIGHT, "raylib [textures] example - sprite button"
    )
    pr.init_audio_device()

    resources = Path(__file__).resolve().parent / "resources"
    fx_button = pr.load_sound(str(resources / "buttonfx.wav"))
    button = pr.load_texture(str(resources / "button.png"))

    frame_height = button.height / float(NUM_FRAMES)
    source_rec = pr.Rectangle(0.0, 0.0, float(button.width), frame_height)
    btn_bounds = pr.Rectangle(
        SCREEN_WIDTH / 2.0 - button.width / 2.0,
        SCREEN_HEIGHT / 2.0 - button.height / NUM_FRAMES / 2.0,
        float(button.width),
        frame_height,
    )

    btn_state = 0
    btn_action = False

    pr.set_target_fps(60)

    while not pr.window_should_close():
        mouse_point = pr.get_mouse_position()
        btn_action = False

        if pr.check_collision_point_rec(mouse_point, btn_bounds):
            if pr.is_mouse_button_down(MOUSE_BUTTON_LEFT):
                btn_state = 2
            else:
                btn_state = 1

            if pr.is_mouse_button_released(MOUSE_BUTTON_LEFT):
                btn_action = True
        else:
            btn_state = 0

        if btn_action:
            pr.play_sound(fx_button)

        source_rec.y = btn_state * frame_height

        pr.begin_drawing()
        pr.clear_background(pr.RAYWHITE)
        pr.draw_texture_rec(
            button, source_rec, pr.Vector2(btn_bounds.x, btn_bounds.y), pr.WHITE
        )
        pr.end_drawing()

    pr.unload_texture(button)
    pr.unload_sound(fx_button)
    pr.close_audio_device()
    pr.close_window()


if __name__ == "__main__":
    main()
