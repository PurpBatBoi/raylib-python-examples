from __future__ import annotations

import pyray as pr

# Version checked: raylib 5.x/pyray API parity (reviewed 2026-02-28).

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 450
MAX_COLORS_COUNT = 23
KEY_RIGHT = getattr(pr, "KEY_RIGHT", 262)
KEY_LEFT = getattr(pr, "KEY_LEFT", 263)
KEY_C = getattr(pr, "KEY_C", 67)
KEY_S = getattr(pr, "KEY_S", 83)
MOUSE_BUTTON_LEFT = getattr(pr, "MOUSE_BUTTON_LEFT", 0)
MOUSE_BUTTON_RIGHT = getattr(pr, "MOUSE_BUTTON_RIGHT", 1)
GESTURE_DRAG = getattr(pr, "GESTURE_DRAG", 8)


def main() -> None:
    """Run mouse painting with palette, eraser, and save-to-image."""
    pr.init_window(
        SCREEN_WIDTH, SCREEN_HEIGHT, "raylib [textures] example - mouse painting"
    )

    colors = [
        pr.RAYWHITE,
        pr.YELLOW,
        pr.GOLD,
        pr.ORANGE,
        pr.PINK,
        pr.RED,
        pr.MAROON,
        pr.GREEN,
        pr.LIME,
        pr.DARKGREEN,
        pr.SKYBLUE,
        pr.BLUE,
        pr.DARKBLUE,
        pr.PURPLE,
        pr.VIOLET,
        pr.DARKPURPLE,
        pr.BEIGE,
        pr.BROWN,
        pr.DARKBROWN,
        pr.LIGHTGRAY,
        pr.GRAY,
        pr.DARKGRAY,
        pr.BLACK,
    ]

    color_recs = [
        pr.Rectangle(10.0 + 30.0 * i + 2.0 * i, 10.0, 30.0, 30.0)
        for i in range(MAX_COLORS_COUNT)
    ]

    color_selected = 0
    color_selected_prev = 0
    color_mouse_hover = -1
    brush_size = 20.0
    mouse_was_pressed = False

    btn_save_rec = pr.Rectangle(750.0, 10.0, 40.0, 30.0)
    btn_save_mouse_hover = False
    show_save_message = False
    save_message_counter = 0

    target = pr.load_render_texture(SCREEN_WIDTH, SCREEN_HEIGHT)
    pr.begin_texture_mode(target)
    pr.clear_background(colors[0])
    pr.end_texture_mode()

    pr.set_target_fps(120)

    while not pr.window_should_close():
        mouse_pos = pr.get_mouse_position()

        if pr.is_key_pressed(KEY_RIGHT):
            color_selected += 1
        elif pr.is_key_pressed(KEY_LEFT):
            color_selected -= 1
        color_selected = max(0, min(MAX_COLORS_COUNT - 1, color_selected))

        color_mouse_hover = -1
        for index, rect in enumerate(color_recs):
            if pr.check_collision_point_rec(mouse_pos, rect):
                color_mouse_hover = index
                break

        if color_mouse_hover >= 0 and pr.is_mouse_button_pressed(MOUSE_BUTTON_LEFT):
            color_selected = color_mouse_hover
            color_selected_prev = color_selected

        brush_size += pr.get_mouse_wheel_move() * 5.0
        brush_size = max(2.0, min(50.0, brush_size))

        if pr.is_key_pressed(KEY_C):
            pr.begin_texture_mode(target)
            pr.clear_background(colors[0])
            pr.end_texture_mode()

        if pr.is_mouse_button_down(MOUSE_BUTTON_LEFT) or (
            pr.get_gesture_detected() == GESTURE_DRAG
        ):
            pr.begin_texture_mode(target)
            if mouse_pos.y > 50.0:
                pr.draw_circle(
                    int(mouse_pos.x),
                    int(mouse_pos.y),
                    brush_size,
                    colors[color_selected],
                )
            pr.end_texture_mode()

        if pr.is_mouse_button_down(MOUSE_BUTTON_RIGHT):
            if not mouse_was_pressed:
                color_selected_prev = color_selected
                color_selected = 0
            mouse_was_pressed = True

            pr.begin_texture_mode(target)
            if mouse_pos.y > 50.0:
                pr.draw_circle(
                    int(mouse_pos.x), int(mouse_pos.y), brush_size, colors[0]
                )
            pr.end_texture_mode()
        elif pr.is_mouse_button_released(MOUSE_BUTTON_RIGHT) and mouse_was_pressed:
            color_selected = color_selected_prev
            mouse_was_pressed = False

        btn_save_mouse_hover = pr.check_collision_point_rec(mouse_pos, btn_save_rec)
        if (
            btn_save_mouse_hover and pr.is_mouse_button_released(MOUSE_BUTTON_LEFT)
        ) or pr.is_key_pressed(KEY_S):
            image = pr.load_image_from_texture(target.texture)
            pr.image_flip_vertical(image)
            pr.export_image(image, "my_amazing_texture_painting.png")
            pr.unload_image(image)
            show_save_message = True

        if show_save_message:
            save_message_counter += 1
            if save_message_counter > 240:
                show_save_message = False
                save_message_counter = 0

        pr.begin_drawing()
        pr.clear_background(pr.RAYWHITE)

        pr.draw_texture_rec(
            target.texture,
            pr.Rectangle(
                0.0, 0.0, float(target.texture.width), float(-target.texture.height)
            ),
            pr.Vector2(0.0, 0.0),
            pr.WHITE,
        )

        if mouse_pos.y > 50.0:
            if pr.is_mouse_button_down(MOUSE_BUTTON_RIGHT):
                pr.draw_circle_lines(
                    int(mouse_pos.x), int(mouse_pos.y), brush_size, pr.GRAY
                )
            else:
                pr.draw_circle(
                    pr.get_mouse_x(),
                    pr.get_mouse_y(),
                    brush_size,
                    colors[color_selected],
                )

        pr.draw_rectangle(0, 0, pr.get_screen_width(), 50, pr.RAYWHITE)
        pr.draw_line(0, 50, pr.get_screen_width(), 50, pr.LIGHTGRAY)

        for index, rect in enumerate(color_recs):
            pr.draw_rectangle_rec(rect, colors[index])
        pr.draw_rectangle_lines(10, 10, 30, 30, pr.LIGHTGRAY)

        if color_mouse_hover >= 0:
            pr.draw_rectangle_rec(color_recs[color_mouse_hover], pr.fade(pr.WHITE, 0.6))

        selected = color_recs[color_selected]
        pr.draw_rectangle_lines_ex(
            pr.Rectangle(
                selected.x - 2.0,
                selected.y - 2.0,
                selected.width + 4.0,
                selected.height + 4.0,
            ),
            2.0,
            pr.BLACK,
        )

        pr.draw_rectangle_lines_ex(
            btn_save_rec, 2.0, pr.RED if btn_save_mouse_hover else pr.BLACK
        )
        pr.draw_text("SAVE!", 755, 20, 10, pr.RED if btn_save_mouse_hover else pr.BLACK)

        if show_save_message:
            pr.draw_rectangle(
                0,
                0,
                pr.get_screen_width(),
                pr.get_screen_height(),
                pr.fade(pr.RAYWHITE, 0.8),
            )
            pr.draw_rectangle(0, 150, pr.get_screen_width(), 80, pr.BLACK)
            pr.draw_text("IMAGE SAVED!", 150, 180, 20, pr.RAYWHITE)

        pr.end_drawing()

    pr.unload_render_texture(target)
    pr.close_window()


if __name__ == "__main__":
    main()
