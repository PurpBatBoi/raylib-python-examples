from __future__ import annotations

import pyray as pr

# Version checked: raylib 5.x/pyray API parity (reviewed 2026-02-28).

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 450

KEY_F = getattr(pr, "KEY_F", 70)
KEY_R = getattr(pr, "KEY_R", 82)
KEY_D = getattr(pr, "KEY_D", 68)
KEY_H = getattr(pr, "KEY_H", 72)
KEY_N = getattr(pr, "KEY_N", 78)
KEY_M = getattr(pr, "KEY_M", 77)
KEY_U = getattr(pr, "KEY_U", 85)
KEY_T = getattr(pr, "KEY_T", 84)
KEY_A = getattr(pr, "KEY_A", 65)
KEY_V = getattr(pr, "KEY_V", 86)
KEY_B = getattr(pr, "KEY_B", 66)

FLAG_FULLSCREEN_MODE = int(getattr(pr, "FLAG_FULLSCREEN_MODE", 2))
FLAG_WINDOW_RESIZABLE = int(getattr(pr, "FLAG_WINDOW_RESIZABLE", 4))
FLAG_WINDOW_UNDECORATED = int(getattr(pr, "FLAG_WINDOW_UNDECORATED", 8))
FLAG_WINDOW_HIDDEN = int(getattr(pr, "FLAG_WINDOW_HIDDEN", 128))
FLAG_WINDOW_MINIMIZED = int(getattr(pr, "FLAG_WINDOW_MINIMIZED", 512))
FLAG_WINDOW_MAXIMIZED = int(getattr(pr, "FLAG_WINDOW_MAXIMIZED", 1024))
FLAG_WINDOW_UNFOCUSED = int(getattr(pr, "FLAG_WINDOW_UNFOCUSED", 2048))
FLAG_WINDOW_TOPMOST = int(getattr(pr, "FLAG_WINDOW_TOPMOST", 4096))
FLAG_WINDOW_ALWAYS_RUN = int(getattr(pr, "FLAG_WINDOW_ALWAYS_RUN", 256))
FLAG_VSYNC_HINT = int(getattr(pr, "FLAG_VSYNC_HINT", 64))
FLAG_BORDERLESS_WINDOWED_MODE = int(getattr(pr, "FLAG_BORDERLESS_WINDOWED_MODE", 32768))
FLAG_WINDOW_HIGHDPI = int(getattr(pr, "FLAG_WINDOW_HIGHDPI", 8192))
FLAG_WINDOW_TRANSPARENT = int(getattr(pr, "FLAG_WINDOW_TRANSPARENT", 16))
FLAG_MSAA_4X_HINT = int(getattr(pr, "FLAG_MSAA_4X_HINT", 32))


def main() -> None:
    """Run the window-flags interaction example."""
    # Maximizing depends on the window being resizable on desktop backends.
    pr.set_config_flags(FLAG_WINDOW_RESIZABLE)
    pr.init_window(SCREEN_WIDTH, SCREEN_HEIGHT, "raylib [core] example - window flags")

    ball_position = pr.Vector2(
        pr.get_screen_width() / 2.0, pr.get_screen_height() / 2.0
    )
    ball_speed = pr.Vector2(5.0, 4.0)
    ball_radius = 20.0
    frames_counter = 0
    restore_minimized_deadline: float | None = None

    pr.set_target_fps(60)

    while not pr.window_should_close():
        if pr.is_key_pressed(KEY_F):
            pr.toggle_fullscreen()
        if pr.is_key_pressed(KEY_R):
            if pr.is_window_state(FLAG_WINDOW_RESIZABLE):
                pr.clear_window_state(FLAG_WINDOW_RESIZABLE)
            else:
                pr.set_window_state(FLAG_WINDOW_RESIZABLE)
        if pr.is_key_pressed(KEY_D):
            if pr.is_window_state(FLAG_WINDOW_UNDECORATED):
                pr.clear_window_state(FLAG_WINDOW_UNDECORATED)
            else:
                pr.set_window_state(FLAG_WINDOW_UNDECORATED)
        if pr.is_key_pressed(KEY_H):
            if not pr.is_window_state(FLAG_WINDOW_HIDDEN):
                pr.set_window_state(FLAG_WINDOW_HIDDEN)
            frames_counter = 0
        if pr.is_window_state(FLAG_WINDOW_HIDDEN):
            frames_counter += 1
            if frames_counter >= 240:
                pr.clear_window_state(FLAG_WINDOW_HIDDEN)
        if pr.is_key_pressed(KEY_N):
            if not pr.is_window_minimized():
                pr.minimize_window()
                restore_minimized_deadline = pr.get_time() + 3.0
        if restore_minimized_deadline is not None:
            if pr.get_time() >= restore_minimized_deadline:
                pr.restore_window()
                restore_minimized_deadline = None
        if pr.is_key_pressed(KEY_M):
            if pr.is_window_maximized():
                pr.restore_window()
            else:
                pr.maximize_window()
        if pr.is_key_pressed(KEY_U):
            if pr.is_window_state(FLAG_WINDOW_UNFOCUSED):
                pr.clear_window_state(FLAG_WINDOW_UNFOCUSED)
            else:
                pr.set_window_state(FLAG_WINDOW_UNFOCUSED)
        if pr.is_key_pressed(KEY_T):
            if pr.is_window_state(FLAG_WINDOW_TOPMOST):
                pr.clear_window_state(FLAG_WINDOW_TOPMOST)
            else:
                pr.set_window_state(FLAG_WINDOW_TOPMOST)
        if pr.is_key_pressed(KEY_A):
            if pr.is_window_state(FLAG_WINDOW_ALWAYS_RUN):
                pr.clear_window_state(FLAG_WINDOW_ALWAYS_RUN)
            else:
                pr.set_window_state(FLAG_WINDOW_ALWAYS_RUN)
        if pr.is_key_pressed(KEY_V):
            if pr.is_window_state(FLAG_VSYNC_HINT):
                pr.clear_window_state(FLAG_VSYNC_HINT)
            else:
                pr.set_window_state(FLAG_VSYNC_HINT)
        if pr.is_key_pressed(KEY_B):
            pr.toggle_borderless_windowed()

        ball_position.x += ball_speed.x
        ball_position.y += ball_speed.y
        if (
            ball_position.x >= (pr.get_screen_width() - ball_radius)
            or ball_position.x <= ball_radius
        ):
            ball_speed.x *= -1.0
        if (
            ball_position.y >= (pr.get_screen_height() - ball_radius)
            or ball_position.y <= ball_radius
        ):
            ball_speed.y *= -1.0

        pr.begin_drawing()
        if pr.is_window_state(FLAG_WINDOW_TRANSPARENT):
            pr.clear_background(pr.BLANK)
        else:
            pr.clear_background(pr.RAYWHITE)

        pr.draw_circle_v(ball_position, ball_radius, pr.MAROON)
        pr.draw_rectangle_lines_ex(
            pr.Rectangle(
                0.0, 0.0, float(pr.get_screen_width()), float(pr.get_screen_height())
            ),
            4.0,
            pr.RAYWHITE,
        )
        pr.draw_circle_v(pr.get_mouse_position(), 10.0, pr.DARKBLUE)
        pr.draw_fps(10, 10)
        pr.draw_text(
            f"Screen Size: [{pr.get_screen_width()}, {pr.get_screen_height()}]",
            10,
            40,
            10,
            pr.GREEN,
        )

        lines = [
            ("Following flags can be set after window creation:", 60, pr.GRAY),
            (
                (
                    "[F] FLAG_FULLSCREEN_MODE: on"
                    if pr.is_window_state(FLAG_FULLSCREEN_MODE)
                    else "[F] FLAG_FULLSCREEN_MODE: off"
                ),
                80,
                pr.LIME if pr.is_window_state(FLAG_FULLSCREEN_MODE) else pr.MAROON,
            ),
            (
                (
                    "[R] FLAG_WINDOW_RESIZABLE: on"
                    if pr.is_window_state(FLAG_WINDOW_RESIZABLE)
                    else "[R] FLAG_WINDOW_RESIZABLE: off"
                ),
                100,
                pr.LIME if pr.is_window_state(FLAG_WINDOW_RESIZABLE) else pr.MAROON,
            ),
            (
                (
                    "[D] FLAG_WINDOW_UNDECORATED: on"
                    if pr.is_window_state(FLAG_WINDOW_UNDECORATED)
                    else "[D] FLAG_WINDOW_UNDECORATED: off"
                ),
                120,
                pr.LIME if pr.is_window_state(FLAG_WINDOW_UNDECORATED) else pr.MAROON,
            ),
            (
                (
                    "[H] FLAG_WINDOW_HIDDEN: on"
                    if pr.is_window_state(FLAG_WINDOW_HIDDEN)
                    else "[H] FLAG_WINDOW_HIDDEN: off (hides for 3 seconds)"
                ),
                140,
                pr.LIME if pr.is_window_state(FLAG_WINDOW_HIDDEN) else pr.MAROON,
            ),
            (
                (
                    "[N] FLAG_WINDOW_MINIMIZED: on"
                    if pr.is_window_minimized()
                    else "[N] FLAG_WINDOW_MINIMIZED: off (restores after 3 seconds)"
                ),
                160,
                pr.LIME if pr.is_window_minimized() else pr.MAROON,
            ),
            (
                (
                    "[M] FLAG_WINDOW_MAXIMIZED: on"
                    if pr.is_window_maximized()
                    else "[M] FLAG_WINDOW_MAXIMIZED: off"
                ),
                180,
                pr.LIME if pr.is_window_maximized() else pr.MAROON,
            ),
            (
                (
                    "[U] FLAG_WINDOW_UNFOCUSED: on"
                    if pr.is_window_state(FLAG_WINDOW_UNFOCUSED)
                    else "[U] FLAG_WINDOW_UNFOCUSED: off"
                ),
                200,
                pr.LIME if pr.is_window_state(FLAG_WINDOW_UNFOCUSED) else pr.MAROON,
            ),
            (
                (
                    "[T] FLAG_WINDOW_TOPMOST: on"
                    if pr.is_window_state(FLAG_WINDOW_TOPMOST)
                    else "[T] FLAG_WINDOW_TOPMOST: off"
                ),
                220,
                pr.LIME if pr.is_window_state(FLAG_WINDOW_TOPMOST) else pr.MAROON,
            ),
            (
                (
                    "[A] FLAG_WINDOW_ALWAYS_RUN: on"
                    if pr.is_window_state(FLAG_WINDOW_ALWAYS_RUN)
                    else "[A] FLAG_WINDOW_ALWAYS_RUN: off"
                ),
                240,
                pr.LIME if pr.is_window_state(FLAG_WINDOW_ALWAYS_RUN) else pr.MAROON,
            ),
            (
                (
                    "[V] FLAG_VSYNC_HINT: on"
                    if pr.is_window_state(FLAG_VSYNC_HINT)
                    else "[V] FLAG_VSYNC_HINT: off"
                ),
                260,
                pr.LIME if pr.is_window_state(FLAG_VSYNC_HINT) else pr.MAROON,
            ),
            (
                (
                    "[B] FLAG_BORDERLESS_WINDOWED_MODE: on"
                    if pr.is_window_state(FLAG_BORDERLESS_WINDOWED_MODE)
                    else "[B] FLAG_BORDERLESS_WINDOWED_MODE: off"
                ),
                280,
                (
                    pr.LIME
                    if pr.is_window_state(FLAG_BORDERLESS_WINDOWED_MODE)
                    else pr.MAROON
                ),
            ),
            ("Following flags can only be set before window creation:", 320, pr.GRAY),
            (
                (
                    "FLAG_WINDOW_HIGHDPI: on"
                    if pr.is_window_state(FLAG_WINDOW_HIGHDPI)
                    else "FLAG_WINDOW_HIGHDPI: off"
                ),
                340,
                pr.LIME if pr.is_window_state(FLAG_WINDOW_HIGHDPI) else pr.MAROON,
            ),
            (
                (
                    "FLAG_WINDOW_TRANSPARENT: on"
                    if pr.is_window_state(FLAG_WINDOW_TRANSPARENT)
                    else "FLAG_WINDOW_TRANSPARENT: off"
                ),
                360,
                pr.LIME if pr.is_window_state(FLAG_WINDOW_TRANSPARENT) else pr.MAROON,
            ),
            (
                (
                    "FLAG_MSAA_4X_HINT: on"
                    if pr.is_window_state(FLAG_MSAA_4X_HINT)
                    else "FLAG_MSAA_4X_HINT: off"
                ),
                380,
                pr.LIME if pr.is_window_state(FLAG_MSAA_4X_HINT) else pr.MAROON,
            ),
        ]
        for text, y, color in lines:
            pr.draw_text(text, 10, y, 10, color)
        pr.end_drawing()

    pr.close_window()


if __name__ == "__main__":
    main()
