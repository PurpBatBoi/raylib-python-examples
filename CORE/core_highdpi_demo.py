from __future__ import annotations

import pyray as pr

# Version checked: raylib 5.x/pyray API parity (reviewed 2026-02-28).

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 450
FLAG_WINDOW_HIGHDPI = int(getattr(pr, "FLAG_WINDOW_HIGHDPI", 8192))
FLAG_WINDOW_RESIZABLE = int(getattr(pr, "FLAG_WINDOW_RESIZABLE", 4))
KEY_N = getattr(pr, "KEY_N", 78)


def draw_text_center(
    text: str, x: int, y: int, font_size: int, color: pr.Color
) -> None:
    """Draw text centered around x,y."""
    size = pr.measure_text_ex(pr.get_font_default(), text, float(font_size), 3.0)
    pos = pr.Vector2(x - size.x / 2.0, y - size.y / 2.0)
    pr.draw_text_ex(pr.get_font_default(), text, pos, float(font_size), 3.0, color)


def main() -> None:
    """Run the high-DPI demo example."""
    pr.set_config_flags(FLAG_WINDOW_HIGHDPI | FLAG_WINDOW_RESIZABLE)
    pr.init_window(SCREEN_WIDTH, SCREEN_HEIGHT, "raylib [core] example - highdpi demo")
    pr.set_window_min_size(450, 450)

    logical_grid_desc_y = 120
    logical_grid_label_y = logical_grid_desc_y + 30
    logical_grid_top = logical_grid_label_y + 30
    logical_grid_bottom = logical_grid_top + 80
    pixel_grid_top = logical_grid_bottom - 20
    pixel_grid_bottom = pixel_grid_top + 80
    pixel_grid_label_y = pixel_grid_bottom + 30
    pixel_grid_desc_y = pixel_grid_label_y + 30
    cell_size = 50

    pr.set_target_fps(60)

    while not pr.window_should_close():
        monitor_count = pr.get_monitor_count()
        if monitor_count > 1 and pr.is_key_pressed(KEY_N):
            pr.set_window_monitor((pr.get_current_monitor() + 1) % monitor_count)

        current_monitor = pr.get_current_monitor()
        dpi_scale = pr.get_window_scale_dpi()
        cell_size_px = (
            float(cell_size) / dpi_scale.x if dpi_scale.x != 0.0 else float(cell_size)
        )

        pr.begin_drawing()
        pr.clear_background(pr.RAYWHITE)

        window_center = pr.get_screen_width() // 2
        draw_text_center(
            f"Dpi Scale: {dpi_scale.x:f}", window_center, 30, 40, pr.DARKGRAY
        )
        draw_text_center(
            f"Monitor: {current_monitor + 1}/{monitor_count} ([N] next monitor)",
            window_center,
            70,
            20,
            pr.LIGHTGRAY,
        )
        draw_text_center(
            f'Window is {pr.get_screen_width()} "logical points" wide',
            window_center,
            logical_grid_desc_y,
            20,
            pr.ORANGE,
        )

        odd = True
        for i in range(cell_size, pr.get_screen_width(), cell_size):
            if odd:
                pr.draw_rectangle(
                    i,
                    logical_grid_top,
                    cell_size,
                    logical_grid_bottom - logical_grid_top,
                    pr.ORANGE,
                )
            draw_text_center(f"{i}", i, logical_grid_label_y, 10, pr.LIGHTGRAY)
            pr.draw_line(i, logical_grid_label_y + 10, i, logical_grid_bottom, pr.GRAY)
            odd = not odd

        odd = True
        min_text_space = 30
        last_text_x = -min_text_space
        for i in range(cell_size, pr.get_render_width(), cell_size):
            x = int(float(i) / dpi_scale.x) if dpi_scale.x != 0.0 else i
            if odd:
                pr.draw_rectangle(
                    x,
                    pixel_grid_top,
                    int(cell_size_px),
                    pixel_grid_bottom - pixel_grid_top,
                    pr.Color(0, 121, 241, 100),
                )
            pr.draw_line(x, pixel_grid_top, x, pixel_grid_label_y - 10, pr.GRAY)
            if (x - last_text_x) >= min_text_space:
                draw_text_center(f"{i}", x, pixel_grid_label_y, 10, pr.LIGHTGRAY)
                last_text_x = x
            odd = not odd

        draw_text_center(
            f'Window is {pr.get_render_width()} "physical pixels" wide',
            window_center,
            pixel_grid_desc_y,
            20,
            pr.BLUE,
        )
        text = "Can you see this?"
        size = pr.measure_text_ex(pr.get_font_default(), text, 20.0, 3.0)
        pos = pr.Vector2(
            pr.get_screen_width() - size.x - 5.0, pr.get_screen_height() - size.y - 5.0
        )
        pr.draw_text_ex(pr.get_font_default(), text, pos, 20.0, 3.0, pr.LIGHTGRAY)
        pr.end_drawing()

    pr.close_window()


if __name__ == "__main__":
    main()
