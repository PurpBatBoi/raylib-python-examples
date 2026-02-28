from __future__ import annotations

from enum import IntEnum
from pathlib import Path

import pyray as pr

# Version checked: raylib 5.x/pyray API parity (reviewed 2026-02-28).

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 450
NUM_PROCESSES = 9

MOUSE_BUTTON_LEFT = getattr(pr, "MOUSE_BUTTON_LEFT", 0)
KEY_DOWN = getattr(pr, "KEY_DOWN", 264)
KEY_UP = getattr(pr, "KEY_UP", 265)
PIXELFORMAT_UNCOMPRESSED_R8G8B8A8 = getattr(pr, "PIXELFORMAT_UNCOMPRESSED_R8G8B8A8", 7)


class ImageProcess(IntEnum):
    """Image processing modes."""

    NONE = 0
    COLOR_GRAYSCALE = 1
    COLOR_TINT = 2
    COLOR_INVERT = 3
    COLOR_CONTRAST = 4
    COLOR_BRIGHTNESS = 5
    GAUSSIAN_BLUR = 6
    FLIP_VERTICAL = 7
    FLIP_HORIZONTAL = 8


PROCESS_TEXT = [
    "NO PROCESSING",
    "COLOR GRAYSCALE",
    "COLOR TINT",
    "COLOR INVERT",
    "COLOR CONTRAST",
    "COLOR BRIGHTNESS",
    "GAUSSIAN BLUR",
    "FLIP VERTICAL",
    "FLIP HORIZONTAL",
]


def apply_process(image: pr.Image, process: int) -> None:
    """Apply the selected processing mode to an image in-place."""
    match ImageProcess(process):
        case ImageProcess.COLOR_GRAYSCALE:
            pr.image_color_grayscale(image)
        case ImageProcess.COLOR_TINT:
            pr.image_color_tint(image, pr.GREEN)
        case ImageProcess.COLOR_INVERT:
            pr.image_color_invert(image)
        case ImageProcess.COLOR_CONTRAST:
            pr.image_color_contrast(image, -40.0)
        case ImageProcess.COLOR_BRIGHTNESS:
            pr.image_color_brightness(image, -80)
        case ImageProcess.GAUSSIAN_BLUR:
            pr.image_blur_gaussian(image, 10)
        case ImageProcess.FLIP_VERTICAL:
            pr.image_flip_vertical(image)
        case ImageProcess.FLIP_HORIZONTAL:
            pr.image_flip_horizontal(image)
        case _:
            return


def main() -> None:
    """Run interactive image processing and texture update demo."""
    pr.init_window(
        SCREEN_WIDTH, SCREEN_HEIGHT, "raylib [textures] example - image processing"
    )

    resources = Path(__file__).resolve().parent / "resources"
    image_origin = pr.load_image(str(resources / "parrots.png"))
    pr.image_format(image_origin, PIXELFORMAT_UNCOMPRESSED_R8G8B8A8)
    texture = pr.load_texture_from_image(image_origin)

    image_copy = pr.image_copy(image_origin)
    current_process = int(ImageProcess.NONE)
    texture_reload = False

    toggle_recs = [
        pr.Rectangle(40.0, float(50 + 32 * index), 150.0, 30.0)
        for index in range(NUM_PROCESSES)
    ]
    mouse_hover_rec = -1

    pr.set_target_fps(60)

    while not pr.window_should_close():
        mouse_hover_rec = -1
        for index, rec in enumerate(toggle_recs):
            if pr.check_collision_point_rec(pr.get_mouse_position(), rec):
                mouse_hover_rec = index
                if pr.is_mouse_button_released(MOUSE_BUTTON_LEFT):
                    current_process = index
                    texture_reload = True
                break

        if pr.is_key_pressed(KEY_DOWN):
            current_process = (current_process + 1) % NUM_PROCESSES
            texture_reload = True
        elif pr.is_key_pressed(KEY_UP):
            current_process = (current_process - 1) % NUM_PROCESSES
            texture_reload = True

        if texture_reload:
            pr.unload_image(image_copy)
            image_copy = pr.image_copy(image_origin)
            apply_process(image_copy, current_process)

            pixels = pr.load_image_colors(image_copy)
            pr.update_texture(texture, pixels)
            pr.unload_image_colors(pixels)
            texture_reload = False

        pr.begin_drawing()
        pr.clear_background(pr.RAYWHITE)

        pr.draw_text("IMAGE PROCESSING:", 40, 30, 10, pr.DARKGRAY)

        for index, rec in enumerate(toggle_recs):
            selected = index in (current_process, mouse_hover_rec)
            pr.draw_rectangle_rec(rec, pr.SKYBLUE if selected else pr.LIGHTGRAY)
            pr.draw_rectangle_lines(
                int(rec.x),
                int(rec.y),
                int(rec.width),
                int(rec.height),
                pr.BLUE if selected else pr.GRAY,
            )
            label = PROCESS_TEXT[index]
            label_x = int(
                rec.x + rec.width / 2.0 - float(pr.measure_text(label, 10)) / 2.0
            )
            pr.draw_text(
                label,
                label_x,
                int(rec.y) + 11,
                10,
                pr.DARKBLUE if selected else pr.DARKGRAY,
            )

        draw_x = SCREEN_WIDTH - texture.width - 60
        draw_y = SCREEN_HEIGHT // 2 - texture.height // 2
        pr.draw_texture(texture, draw_x, draw_y, pr.WHITE)
        pr.draw_rectangle_lines(draw_x, draw_y, texture.width, texture.height, pr.BLACK)

        pr.end_drawing()

    pr.unload_texture(texture)
    pr.unload_image(image_origin)
    pr.unload_image(image_copy)
    pr.close_window()


if __name__ == "__main__":
    main()
