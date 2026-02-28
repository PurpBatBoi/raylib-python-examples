from __future__ import annotations

import pyray as pr

# Version checked: raylib 5.x/pyray API parity (reviewed 2026-02-28).

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 450
IMAGE_WIDTH = 800
IMAGE_HEIGHT = 800 // 2

DRAW_RULE_START_X = 585
DRAW_RULE_START_Y = 10
DRAW_RULE_SPACING = 15
DRAW_RULE_GROUP_SPACING = 50
DRAW_RULE_SIZE = 14
DRAW_RULE_INNER_SIZE = 10

PRESETS_SIZE_X = 42
PRESETS_SIZE_Y = 22
LINES_UPDATED_PER_FRAME = 4

MOUSE_BUTTON_LEFT = getattr(pr, "MOUSE_BUTTON_LEFT", 0)


def compute_line(image: pr.Image, line: int, rule: int) -> None:
    """Compute one elementary cellular automata line for a rule bitmask."""
    for x in range(1, IMAGE_WIDTH - 1):
        prev_value = (
            (4 if pr.get_image_color(image, x - 1, line - 1).r < 5 else 0)
            + (2 if pr.get_image_color(image, x, line - 1).r < 5 else 0)
            + (1 if pr.get_image_color(image, x + 1, line - 1).r < 5 else 0)
        )
        curr_value = (rule & (1 << prev_value)) != 0
        pr.image_draw_pixel(image, x, line, pr.BLACK if curr_value else pr.RAYWHITE)


def main() -> None:
    """Run cellular automata visualization with editable rule bits."""
    pr.init_window(
        SCREEN_WIDTH, SCREEN_HEIGHT, "raylib [textures] example - cellular automata"
    )

    image = pr.gen_image_color(IMAGE_WIDTH, IMAGE_HEIGHT, pr.RAYWHITE)
    pr.image_draw_pixel(image, IMAGE_WIDTH // 2, 0, pr.BLACK)
    texture = pr.load_texture_from_image(image)

    preset_values = [18, 30, 60, 86, 102, 124, 126, 150, 182, 225]
    rule = 30
    line = 1

    pr.set_target_fps(60)

    while not pr.window_should_close():
        mouse = pr.get_mouse_position()
        mouse_in_cell = -1

        for i in range(8):
            cell_x = DRAW_RULE_START_X - DRAW_RULE_GROUP_SPACING * i + DRAW_RULE_SPACING
            cell_y = DRAW_RULE_START_Y + DRAW_RULE_SPACING
            if (
                cell_x <= mouse.x <= cell_x + DRAW_RULE_SIZE
                and cell_y <= mouse.y <= cell_y + DRAW_RULE_SIZE
            ):
                mouse_in_cell = i
                break

        if mouse_in_cell < 0:
            for i in range(len(preset_values)):
                cell_x = 4 + (PRESETS_SIZE_X + 2) * (i // 2)
                cell_y = 2 + (PRESETS_SIZE_Y + 2) * (i % 2)
                if (
                    cell_x <= mouse.x <= cell_x + PRESETS_SIZE_X
                    and cell_y <= mouse.y <= cell_y + PRESETS_SIZE_Y
                ):
                    mouse_in_cell = i + 8
                    break

        if pr.is_mouse_button_pressed(MOUSE_BUTTON_LEFT) and mouse_in_cell >= 0:
            if mouse_in_cell < 8:
                rule ^= 1 << mouse_in_cell
            else:
                rule = preset_values[mouse_in_cell - 8]

            pr.image_clear_background(image, pr.RAYWHITE)
            pr.image_draw_pixel(image, IMAGE_WIDTH // 2, 0, pr.BLACK)
            line = 1

        if line < IMAGE_HEIGHT:
            for i in range(LINES_UPDATED_PER_FRAME):
                if line + i < IMAGE_HEIGHT:
                    compute_line(image, line + i, rule)
            line += LINES_UPDATED_PER_FRAME
            pr.update_texture(texture, image.data)

        pr.begin_drawing()
        pr.clear_background(pr.RAYWHITE)
        pr.draw_texture(texture, 0, SCREEN_HEIGHT - IMAGE_HEIGHT, pr.WHITE)

        for i, value in enumerate(preset_values):
            pr.draw_text(
                f"{value}",
                8 + (PRESETS_SIZE_X + 2) * (i // 2),
                4 + (PRESETS_SIZE_Y + 2) * (i % 2),
                20,
                pr.GRAY,
            )
            pr.draw_rectangle_lines(
                4 + (PRESETS_SIZE_X + 2) * (i // 2),
                2 + (PRESETS_SIZE_Y + 2) * (i % 2),
                PRESETS_SIZE_X,
                PRESETS_SIZE_Y,
                pr.BLUE,
            )
            if mouse_in_cell == i + 8:
                pr.draw_rectangle_lines_ex(
                    pr.Rectangle(
                        2.0 + (PRESETS_SIZE_X + 2.0) * (i // 2),
                        (PRESETS_SIZE_Y + 2.0) * (i % 2),
                        PRESETS_SIZE_X + 4.0,
                        PRESETS_SIZE_Y + 4.0,
                    ),
                    3.0,
                    pr.RED,
                )

        for i in range(8):
            for j in range(3):
                x = (
                    DRAW_RULE_START_X
                    - DRAW_RULE_GROUP_SPACING * i
                    + DRAW_RULE_SPACING * j
                )
                pr.draw_rectangle_lines(
                    x, DRAW_RULE_START_Y, DRAW_RULE_SIZE, DRAW_RULE_SIZE, pr.GRAY
                )
                if i & (4 >> j):
                    pr.draw_rectangle(
                        DRAW_RULE_START_X
                        + 2
                        - DRAW_RULE_GROUP_SPACING * i
                        + DRAW_RULE_SPACING * j,
                        DRAW_RULE_START_Y + 2,
                        DRAW_RULE_INNER_SIZE,
                        DRAW_RULE_INNER_SIZE,
                        pr.BLACK,
                    )

            pr.draw_rectangle_lines(
                DRAW_RULE_START_X - DRAW_RULE_GROUP_SPACING * i + DRAW_RULE_SPACING,
                DRAW_RULE_START_Y + DRAW_RULE_SPACING,
                DRAW_RULE_SIZE,
                DRAW_RULE_SIZE,
                pr.BLUE,
            )
            if rule & (1 << i):
                pr.draw_rectangle(
                    DRAW_RULE_START_X
                    + 2
                    - DRAW_RULE_GROUP_SPACING * i
                    + DRAW_RULE_SPACING,
                    DRAW_RULE_START_Y + 2 + DRAW_RULE_SPACING,
                    DRAW_RULE_INNER_SIZE,
                    DRAW_RULE_INNER_SIZE,
                    pr.BLACK,
                )

            if mouse_in_cell == i:
                pr.draw_rectangle_lines_ex(
                    pr.Rectangle(
                        DRAW_RULE_START_X
                        - DRAW_RULE_GROUP_SPACING * i
                        + DRAW_RULE_SPACING
                        - 2.0,
                        DRAW_RULE_START_Y + DRAW_RULE_SPACING - 2.0,
                        DRAW_RULE_SIZE + 4.0,
                        DRAW_RULE_SIZE + 4.0,
                    ),
                    3.0,
                    pr.RED,
                )

        pr.draw_text(
            f"RULE: {rule}",
            DRAW_RULE_START_X + DRAW_RULE_SPACING * 4,
            DRAW_RULE_START_Y + 1,
            30,
            pr.GRAY,
        )
        pr.end_drawing()

    pr.unload_image(image)
    pr.unload_texture(texture)
    pr.close_window()


if __name__ == "__main__":
    main()
