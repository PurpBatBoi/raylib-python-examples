from __future__ import annotations

from enum import IntEnum

import pyray as pr

# Version checked: raylib 5.x/pyray API parity (reviewed 2026-02-28).

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 450

KEY_ENTER = getattr(pr, "KEY_ENTER", 257)
GESTURE_TAP = getattr(pr, "GESTURE_TAP", 1)


class GameScreen(IntEnum):
    """State machine screens for the demo."""

    LOGO = 0
    TITLE = 1
    GAMEPLAY = 2
    ENDING = 3


def main() -> None:
    """Run the basic screen manager example."""
    pr.init_window(
        SCREEN_WIDTH,
        SCREEN_HEIGHT,
        "raylib [core] example - basic screen manager",
    )

    current_screen = GameScreen.LOGO
    frames_counter = 0

    pr.set_target_fps(60)

    while not pr.window_should_close():
        match current_screen:
            case GameScreen.LOGO:
                frames_counter += 1
                if frames_counter > 120:
                    current_screen = GameScreen.TITLE
            case GameScreen.TITLE:
                if pr.is_key_pressed(KEY_ENTER) or pr.is_gesture_detected(GESTURE_TAP):
                    current_screen = GameScreen.GAMEPLAY
            case GameScreen.GAMEPLAY:
                if pr.is_key_pressed(KEY_ENTER) or pr.is_gesture_detected(GESTURE_TAP):
                    current_screen = GameScreen.ENDING
            case GameScreen.ENDING:
                if pr.is_key_pressed(KEY_ENTER) or pr.is_gesture_detected(GESTURE_TAP):
                    current_screen = GameScreen.TITLE

        pr.begin_drawing()
        pr.clear_background(pr.RAYWHITE)

        match current_screen:
            case GameScreen.LOGO:
                pr.draw_text("LOGO SCREEN", 20, 20, 40, pr.LIGHTGRAY)
                pr.draw_text("WAIT for 2 SECONDS...", 290, 220, 20, pr.GRAY)
            case GameScreen.TITLE:
                pr.draw_rectangle(0, 0, SCREEN_WIDTH, SCREEN_HEIGHT, pr.GREEN)
                pr.draw_text("TITLE SCREEN", 20, 20, 40, pr.DARKGREEN)
                pr.draw_text(
                    "PRESS ENTER or TAP to JUMP to GAMEPLAY SCREEN",
                    120,
                    220,
                    20,
                    pr.DARKGREEN,
                )
            case GameScreen.GAMEPLAY:
                pr.draw_rectangle(0, 0, SCREEN_WIDTH, SCREEN_HEIGHT, pr.PURPLE)
                pr.draw_text("GAMEPLAY SCREEN", 20, 20, 40, pr.MAROON)
                pr.draw_text(
                    "PRESS ENTER or TAP to JUMP to ENDING SCREEN",
                    130,
                    220,
                    20,
                    pr.MAROON,
                )
            case GameScreen.ENDING:
                pr.draw_rectangle(0, 0, SCREEN_WIDTH, SCREEN_HEIGHT, pr.BLUE)
                pr.draw_text("ENDING SCREEN", 20, 20, 40, pr.DARKBLUE)
                pr.draw_text(
                    "PRESS ENTER or TAP to RETURN to TITLE SCREEN",
                    120,
                    220,
                    20,
                    pr.DARKBLUE,
                )

        pr.end_drawing()

    pr.close_window()


if __name__ == "__main__":
    main()
