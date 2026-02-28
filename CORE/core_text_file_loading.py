from __future__ import annotations

from pathlib import Path

import pyray as pr

# Version checked: raylib 5.x/pyray API parity (reviewed 2026-02-28).

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 450


def wrap_line_for_width(line: str, font_size: int, wrap_width: int) -> str:
    """Insert newline wraps so each visual segment stays under wrap width."""
    if not line:
        return ""

    chars = list(line)
    j = 0
    last_space = 0
    last_wrap_start = 0

    while j <= len(chars):
        current = chars[j] if j < len(chars) else "\0"
        if current in (" ", "\0"):
            before = current
            segment = "".join(chars[last_wrap_start:j])
            if pr.measure_text(segment, font_size) > wrap_width:
                chars[last_space] = "\n"
                last_wrap_start = last_space + 1
            if before != "\0" and j < len(chars):
                chars[j] = " "
            last_space = j
        j += 1

    return "".join(chars)


def main() -> None:
    """Run the text file loading and scrolling example."""
    pr.init_window(
        SCREEN_WIDTH,
        SCREEN_HEIGHT,
        "raylib [core] example - text file loading",
    )

    camera = pr.Camera2D(pr.Vector2(0.0, 0.0), pr.Vector2(0.0, 0.0), 0.0, 1.0)
    file_name = "resources/text_file.txt"
    resource_path = Path(__file__).resolve().parent / file_name
    text = resource_path.read_text(encoding="utf-8")

    font_size = 20
    text_top = 25 + font_size
    wrap_width = SCREEN_WIDTH - 20

    lines = [
        wrap_line_for_width(line, font_size, wrap_width) for line in text.splitlines()
    ]
    if not lines:
        lines = [""]

    text_height = 0
    for line in lines:
        measured = line if line else " "
        size = pr.measure_text_ex(
            pr.get_font_default(), measured, float(font_size), 2.0
        )
        text_height += int(size.y) + 10

    scroll_bar = pr.Rectangle(
        SCREEN_WIDTH - 5.0,
        0.0,
        5.0,
        SCREEN_HEIGHT * 100.0 / max(1, text_height - SCREEN_HEIGHT),
    )

    pr.set_target_fps(60)

    while not pr.window_should_close():
        scroll = pr.get_mouse_wheel_move()
        camera.target.y -= scroll * font_size * 1.5
        if camera.target.y < 0.0:
            camera.target.y = 0.0
        max_scroll = text_height - SCREEN_HEIGHT + text_top
        if camera.target.y > max_scroll:
            camera.target.y = float(max_scroll)

        if text_height - SCREEN_HEIGHT != 0:
            lerp_t = (camera.target.y - text_top) / (text_height - SCREEN_HEIGHT)
            scroll_bar.y = pr.lerp(
                float(text_top), float(SCREEN_HEIGHT) - scroll_bar.height, lerp_t
            )

        pr.begin_drawing()
        pr.clear_background(pr.RAYWHITE)
        pr.begin_mode_2d(camera)
        cursor_y = text_top
        for line in lines:
            measured = line if line else " "
            size = pr.measure_text_ex(
                pr.get_font_default(), measured, float(font_size), 2.0
            )
            pr.draw_text(line, 10, cursor_y, font_size, pr.RED)
            cursor_y += int(size.y) + 10
        pr.end_mode_2d()

        pr.draw_rectangle(0, 0, SCREEN_WIDTH, text_top - 10, pr.BEIGE)
        pr.draw_text(f"File: {file_name}", 10, 10, font_size, pr.MAROON)
        pr.draw_rectangle_rec(scroll_bar, pr.MAROON)
        pr.end_drawing()

    pr.close_window()


if __name__ == "__main__":
    main()
