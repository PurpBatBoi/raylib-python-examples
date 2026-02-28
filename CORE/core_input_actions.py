from __future__ import annotations

from dataclasses import dataclass
from enum import IntEnum

import pyray as pr

# Version checked: raylib 5.x/pyray API parity (reviewed 2026-02-28).

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 450
KEY_TAB = getattr(pr, "KEY_TAB", 258)
KEY_W = getattr(pr, "KEY_W", 87)
KEY_A = getattr(pr, "KEY_A", 65)
KEY_S = getattr(pr, "KEY_S", 83)
KEY_D = getattr(pr, "KEY_D", 68)
KEY_UP = getattr(pr, "KEY_UP", 265)
KEY_LEFT = getattr(pr, "KEY_LEFT", 263)
KEY_RIGHT = getattr(pr, "KEY_RIGHT", 262)
KEY_DOWN = getattr(pr, "KEY_DOWN", 264)
KEY_SPACE = getattr(pr, "KEY_SPACE", 32)
GAMEPAD_BUTTON_LEFT_FACE_UP = int(getattr(pr, "GAMEPAD_BUTTON_LEFT_FACE_UP", 1))
GAMEPAD_BUTTON_LEFT_FACE_DOWN = int(getattr(pr, "GAMEPAD_BUTTON_LEFT_FACE_DOWN", 3))
GAMEPAD_BUTTON_LEFT_FACE_LEFT = int(getattr(pr, "GAMEPAD_BUTTON_LEFT_FACE_LEFT", 4))
GAMEPAD_BUTTON_LEFT_FACE_RIGHT = int(getattr(pr, "GAMEPAD_BUTTON_LEFT_FACE_RIGHT", 2))
GAMEPAD_BUTTON_RIGHT_FACE_UP = int(getattr(pr, "GAMEPAD_BUTTON_RIGHT_FACE_UP", 5))
GAMEPAD_BUTTON_RIGHT_FACE_DOWN = int(getattr(pr, "GAMEPAD_BUTTON_RIGHT_FACE_DOWN", 7))
GAMEPAD_BUTTON_RIGHT_FACE_LEFT = int(getattr(pr, "GAMEPAD_BUTTON_RIGHT_FACE_LEFT", 8))
GAMEPAD_BUTTON_RIGHT_FACE_RIGHT = int(getattr(pr, "GAMEPAD_BUTTON_RIGHT_FACE_RIGHT", 6))


class ActionType(IntEnum):
    """Actions to map to keyboard/gamepad controls."""

    NO_ACTION = 0
    UP = 1
    DOWN = 2
    LEFT = 3
    RIGHT = 4
    FIRE = 5
    MAX_ACTION = 6


@dataclass
class ActionInput:
    """Store key and gamepad button binding for one action."""

    key: int = 0
    button: int = 0


def is_action_pressed(
    action: ActionType, inputs: list[ActionInput], gamepad_index: int
) -> bool:
    """Return whether an action was pressed this frame."""
    if action >= ActionType.MAX_ACTION:
        return False
    mapped = inputs[int(action)]
    return pr.is_key_pressed(mapped.key) or pr.is_gamepad_button_pressed(
        gamepad_index, mapped.button
    )


def is_action_released(
    action: ActionType, inputs: list[ActionInput], gamepad_index: int
) -> bool:
    """Return whether an action was released this frame."""
    if action >= ActionType.MAX_ACTION:
        return False
    mapped = inputs[int(action)]
    return pr.is_key_released(mapped.key) or pr.is_gamepad_button_released(
        gamepad_index, mapped.button
    )


def is_action_down(
    action: ActionType, inputs: list[ActionInput], gamepad_index: int
) -> bool:
    """Return whether an action is currently held."""
    if action >= ActionType.MAX_ACTION:
        return False
    mapped = inputs[int(action)]
    return pr.is_key_down(mapped.key) or pr.is_gamepad_button_down(
        gamepad_index, mapped.button
    )


def set_actions_default(inputs: list[ActionInput]) -> None:
    """Configure default WASD + left-face gamepad mapping."""
    inputs[int(ActionType.UP)] = ActionInput(KEY_W, GAMEPAD_BUTTON_LEFT_FACE_UP)
    inputs[int(ActionType.DOWN)] = ActionInput(KEY_S, GAMEPAD_BUTTON_LEFT_FACE_DOWN)
    inputs[int(ActionType.LEFT)] = ActionInput(KEY_A, GAMEPAD_BUTTON_LEFT_FACE_LEFT)
    inputs[int(ActionType.RIGHT)] = ActionInput(KEY_D, GAMEPAD_BUTTON_LEFT_FACE_RIGHT)
    inputs[int(ActionType.FIRE)] = ActionInput(
        KEY_SPACE, GAMEPAD_BUTTON_RIGHT_FACE_DOWN
    )


def set_actions_cursor(inputs: list[ActionInput]) -> None:
    """Configure arrow-key + right-face gamepad mapping."""
    inputs[int(ActionType.UP)] = ActionInput(KEY_UP, GAMEPAD_BUTTON_RIGHT_FACE_UP)
    inputs[int(ActionType.DOWN)] = ActionInput(KEY_DOWN, GAMEPAD_BUTTON_RIGHT_FACE_DOWN)
    inputs[int(ActionType.LEFT)] = ActionInput(KEY_LEFT, GAMEPAD_BUTTON_RIGHT_FACE_LEFT)
    inputs[int(ActionType.RIGHT)] = ActionInput(
        KEY_RIGHT, GAMEPAD_BUTTON_RIGHT_FACE_RIGHT
    )
    inputs[int(ActionType.FIRE)] = ActionInput(KEY_SPACE, GAMEPAD_BUTTON_LEFT_FACE_DOWN)


def main() -> None:
    """Run the input-actions remapping example."""
    pr.init_window(SCREEN_WIDTH, SCREEN_HEIGHT, "raylib [core] example - input actions")

    action_set = 0
    action_inputs = [ActionInput() for _ in range(int(ActionType.MAX_ACTION))]
    set_actions_default(action_inputs)
    release_action = False

    position = pr.Vector2(400.0, 200.0)
    size = pr.Vector2(40.0, 40.0)

    pr.set_target_fps(60)

    while not pr.window_should_close():
        gamepad_index = 0

        if is_action_down(ActionType.UP, action_inputs, gamepad_index):
            position.y -= 2.0
        if is_action_down(ActionType.DOWN, action_inputs, gamepad_index):
            position.y += 2.0
        if is_action_down(ActionType.LEFT, action_inputs, gamepad_index):
            position.x -= 2.0
        if is_action_down(ActionType.RIGHT, action_inputs, gamepad_index):
            position.x += 2.0
        if is_action_pressed(ActionType.FIRE, action_inputs, gamepad_index):
            position.x = (SCREEN_WIDTH - size.x) / 2.0
            position.y = (SCREEN_HEIGHT - size.y) / 2.0

        release_action = is_action_released(
            ActionType.FIRE, action_inputs, gamepad_index
        )

        if pr.is_key_pressed(KEY_TAB):
            action_set = 1 - action_set
            if action_set == 0:
                set_actions_default(action_inputs)
            else:
                set_actions_cursor(action_inputs)

        pr.begin_drawing()
        pr.clear_background(pr.GRAY)
        pr.draw_rectangle_v(position, size, pr.BLUE if release_action else pr.RED)
        pr.draw_text(
            (
                "Current input set: WASD (default)"
                if action_set == 0
                else "Current input set: Arrow keys"
            ),
            10,
            10,
            20,
            pr.WHITE,
        )
        pr.draw_text("Use TAB key to toggles Actions keyset", 10, 50, 20, pr.GREEN)
        pr.end_drawing()

    pr.close_window()


if __name__ == "__main__":
    main()
