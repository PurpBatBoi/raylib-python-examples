from __future__ import annotations

import pyray as pr

# Version checked: raylib 5.x/pyray API parity (reviewed 2026-02-28).

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 450
NUM_TEXTURES = 9

MOUSE_BUTTON_LEFT = getattr(pr, "MOUSE_BUTTON_LEFT", 0)
KEY_RIGHT = getattr(pr, "KEY_RIGHT", 262)


def main() -> None:
    """Run procedural image generation and texture cycling."""
    pr.init_window(
        SCREEN_WIDTH, SCREEN_HEIGHT, "raylib [textures] example - image generation"
    )

    images = [
        pr.gen_image_gradient_linear(SCREEN_WIDTH, SCREEN_HEIGHT, 0, pr.RED, pr.BLUE),
        pr.gen_image_gradient_linear(SCREEN_WIDTH, SCREEN_HEIGHT, 90, pr.RED, pr.BLUE),
        pr.gen_image_gradient_linear(SCREEN_WIDTH, SCREEN_HEIGHT, 45, pr.RED, pr.BLUE),
        pr.gen_image_gradient_radial(
            SCREEN_WIDTH, SCREEN_HEIGHT, 0.0, pr.WHITE, pr.BLACK
        ),
        pr.gen_image_gradient_square(
            SCREEN_WIDTH, SCREEN_HEIGHT, 0.0, pr.WHITE, pr.BLACK
        ),
        pr.gen_image_checked(SCREEN_WIDTH, SCREEN_HEIGHT, 32, 32, pr.RED, pr.BLUE),
        pr.gen_image_white_noise(SCREEN_WIDTH, SCREEN_HEIGHT, 0.5),
        pr.gen_image_perlin_noise(SCREEN_WIDTH, SCREEN_HEIGHT, 50, 50, 4.0),
        pr.gen_image_cellular(SCREEN_WIDTH, SCREEN_HEIGHT, 32),
    ]
    textures = [pr.load_texture_from_image(image) for image in images]

    for image in images:
        pr.unload_image(image)

    labels = [
        ("VERTICAL GRADIENT", 560, pr.RAYWHITE),
        ("HORIZONTAL GRADIENT", 540, pr.RAYWHITE),
        ("DIAGONAL GRADIENT", 540, pr.RAYWHITE),
        ("RADIAL GRADIENT", 580, pr.LIGHTGRAY),
        ("SQUARE GRADIENT", 580, pr.LIGHTGRAY),
        ("CHECKED", 680, pr.RAYWHITE),
        ("WHITE NOISE", 640, pr.RED),
        ("PERLIN NOISE", 640, pr.RED),
        ("CELLULAR", 670, pr.RAYWHITE),
    ]

    current_texture = 0
    pr.set_target_fps(60)

    while not pr.window_should_close():
        if pr.is_mouse_button_pressed(MOUSE_BUTTON_LEFT) or pr.is_key_pressed(
            KEY_RIGHT
        ):
            current_texture = (current_texture + 1) % NUM_TEXTURES

        pr.begin_drawing()
        pr.clear_background(pr.RAYWHITE)

        pr.draw_texture(textures[current_texture], 0, 0, pr.WHITE)

        pr.draw_rectangle(30, 400, 325, 30, pr.fade(pr.SKYBLUE, 0.5))
        pr.draw_rectangle_lines(30, 400, 325, 30, pr.fade(pr.WHITE, 0.5))
        pr.draw_text(
            "MOUSE LEFT BUTTON to CYCLE PROCEDURAL TEXTURES", 40, 410, 10, pr.WHITE
        )

        text, text_x, text_color = labels[current_texture]
        pr.draw_text(text, text_x, 10, 20, text_color)

        pr.end_drawing()

    for texture in textures:
        pr.unload_texture(texture)
    pr.close_window()


if __name__ == "__main__":
    main()
