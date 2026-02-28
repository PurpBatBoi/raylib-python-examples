from __future__ import annotations

import pyray as pr

# Version checked: raylib 5.x/pyray API parity (reviewed 2026-02-28).

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 450
MAX_GESTURE_STRINGS = 20

GESTURE_NAMES = {
    int(getattr(pr, "GESTURE_TAP", 1)): "GESTURE TAP",
    int(getattr(pr, "GESTURE_DOUBLETAP", 2)): "GESTURE DOUBLETAP",
    int(getattr(pr, "GESTURE_HOLD", 4)): "GESTURE HOLD",
    int(getattr(pr, "GESTURE_DRAG", 8)): "GESTURE DRAG",
    int(getattr(pr, "GESTURE_SWIPE_RIGHT", 16)): "GESTURE SWIPE RIGHT",
    int(getattr(pr, "GESTURE_SWIPE_LEFT", 32)): "GESTURE SWIPE LEFT",
    int(getattr(pr, "GESTURE_SWIPE_UP", 64)): "GESTURE SWIPE UP",
    int(getattr(pr, "GESTURE_SWIPE_DOWN", 128)): "GESTURE SWIPE DOWN",
    int(getattr(pr, "GESTURE_PINCH_IN", 256)): "GESTURE PINCH IN",
    int(getattr(pr, "GESTURE_PINCH_OUT", 512)): "GESTURE PINCH OUT",
}
GESTURE_NONE = int(getattr(pr, "GESTURE_NONE", 0))


def main() -> None:
    """Run the input gestures example."""
    pr.init_window(
        SCREEN_WIDTH, SCREEN_HEIGHT, "raylib [core] example - input gestures"
    )

    touch_position = pr.Vector2(0.0, 0.0)
    touch_area = pr.Rectangle(220.0, 10.0, SCREEN_WIDTH - 230.0, SCREEN_HEIGHT - 20.0)

    gestures_count = 0
    gesture_strings = [""] * MAX_GESTURE_STRINGS

    current_gesture = GESTURE_NONE
    last_gesture = GESTURE_NONE

    pr.set_target_fps(60)

    while not pr.window_should_close():
        last_gesture = current_gesture
        current_gesture = pr.get_gesture_detected()
        touch_position = pr.get_touch_position(0)

        if (
            pr.check_collision_point_rec(touch_position, touch_area)
            and current_gesture != GESTURE_NONE
            and current_gesture != last_gesture
        ):
            label = GESTURE_NAMES.get(current_gesture)
            if label:
                gesture_strings[gestures_count] = label
                gestures_count += 1
            if gestures_count >= MAX_GESTURE_STRINGS:
                gesture_strings = [""] * MAX_GESTURE_STRINGS
                gestures_count = 0

        pr.begin_drawing()
        pr.clear_background(pr.RAYWHITE)

        pr.draw_rectangle_rec(touch_area, pr.GRAY)
        pr.draw_rectangle(225, 15, SCREEN_WIDTH - 240, SCREEN_HEIGHT - 30, pr.RAYWHITE)
        pr.draw_text(
            "GESTURES TEST AREA",
            SCREEN_WIDTH - 270,
            SCREEN_HEIGHT - 40,
            20,
            pr.fade(pr.GRAY, 0.5),
        )

        for i in range(gestures_count):
            row_alpha = 0.5 if i % 2 == 0 else 0.3
            pr.draw_rectangle(
                10, 30 + 20 * i, 200, 20, pr.fade(pr.LIGHTGRAY, row_alpha)
            )
            pr.draw_text(
                gesture_strings[i],
                35,
                36 + 20 * i,
                10,
                pr.MAROON if i == gestures_count - 1 else pr.DARKGRAY,
            )

        pr.draw_rectangle_lines(10, 29, 200, SCREEN_HEIGHT - 50, pr.GRAY)
        pr.draw_text("DETECTED GESTURES", 50, 15, 10, pr.GRAY)

        if current_gesture != GESTURE_NONE:
            pr.draw_circle_v(touch_position, 30.0, pr.MAROON)

        pr.end_drawing()

    pr.close_window()


if __name__ == "__main__":
    main()
