from __future__ import annotations

import pyray as pr

# Version checked: raylib 5.x/pyray API parity (reviewed 2026-02-28).

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 450
FLAG_WINDOW_RESIZABLE = int(getattr(pr, "FLAG_WINDOW_RESIZABLE", 4))
FLAG_WINDOW_HIGHDPI = int(getattr(pr, "FLAG_WINDOW_HIGHDPI", 8192))
KEY_SPACE = getattr(pr, "KEY_SPACE", 32)
KEY_F = getattr(pr, "KEY_F", 70)


def main() -> None:
    """Run the high-DPI testbed example."""
    pr.set_config_flags(FLAG_WINDOW_RESIZABLE | FLAG_WINDOW_HIGHDPI)
    pr.init_window(
        SCREEN_WIDTH, SCREEN_HEIGHT, "raylib [core] example - highdpi testbed"
    )

    grid_spacing = 40
    pr.set_target_fps(60)

    while not pr.window_should_close():
        mouse_pos = pr.get_mouse_position()
        current_monitor = pr.get_current_monitor()
        scale_dpi = pr.get_window_scale_dpi()
        window_pos = pr.get_window_position()

        if pr.is_key_pressed(KEY_SPACE):
            pr.toggle_borderless_windowed()
        if pr.is_key_pressed(KEY_F):
            pr.toggle_fullscreen()

        pr.begin_drawing()
        pr.clear_background(pr.RAYWHITE)

        for h in range(pr.get_screen_height() // grid_spacing + 1):
            pr.draw_text(f"{h*grid_spacing:02d}", 4, h * grid_spacing - 4, 10, pr.GRAY)
            pr.draw_line(
                24,
                h * grid_spacing,
                pr.get_screen_width(),
                h * grid_spacing,
                pr.LIGHTGRAY,
            )
        for v in range(pr.get_screen_width() // grid_spacing + 1):
            pr.draw_text(f"{v*grid_spacing:02d}", v * grid_spacing - 10, 4, 10, pr.GRAY)
            pr.draw_line(
                v * grid_spacing,
                20,
                v * grid_spacing,
                pr.get_screen_height(),
                pr.LIGHTGRAY,
            )

        pr.draw_text(
            f"CURRENT MONITOR: {current_monitor + 1}/{pr.get_monitor_count()} ({pr.get_monitor_width(current_monitor)}x{pr.get_monitor_height(current_monitor)})",
            50,
            50,
            20,
            pr.DARKGRAY,
        )
        pr.draw_text(
            f"WINDOW POSITION: {int(window_pos.x)}x{int(window_pos.y)}",
            50,
            90,
            20,
            pr.DARKGRAY,
        )
        pr.draw_text(
            f"SCREEN SIZE: {pr.get_screen_width()}x{pr.get_screen_height()}",
            50,
            130,
            20,
            pr.DARKGRAY,
        )
        pr.draw_text(
            f"RENDER SIZE: {pr.get_render_width()}x{pr.get_render_height()}",
            50,
            170,
            20,
            pr.DARKGRAY,
        )
        pr.draw_text(
            f"SCALE FACTOR: {scale_dpi.x:.2f}x{scale_dpi.y:.2f}", 50, 210, 20, pr.GRAY
        )

        pr.draw_rectangle(0, 0, 30, 60, pr.RED)
        pr.draw_rectangle(
            pr.get_screen_width() - 30, pr.get_screen_height() - 60, 30, 60, pr.BLUE
        )
        pr.draw_circle_v(mouse_pos, 20.0, pr.MAROON)
        pr.draw_rectangle_rec(
            pr.Rectangle(mouse_pos.x - 25.0, mouse_pos.y, 50.0, 2.0), pr.BLACK
        )
        pr.draw_rectangle_rec(
            pr.Rectangle(mouse_pos.x, mouse_pos.y - 25.0, 2.0, 50.0), pr.BLACK
        )
        text_y = (
            int(mouse_pos.y) - 46
            if mouse_pos.y > pr.get_screen_height() - 60
            else int(mouse_pos.y) + 30
        )
        pr.draw_text(
            f"[{pr.get_mouse_x()},{pr.get_mouse_y()}]",
            int(mouse_pos.x) - 44,
            text_y,
            20,
            pr.BLACK,
        )
        pr.end_drawing()

    pr.close_window()


if __name__ == "__main__":
    main()
