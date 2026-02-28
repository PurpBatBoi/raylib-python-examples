from __future__ import annotations

import math
from dataclasses import dataclass

import pyray as pr

# Version checked: raylib 5.x/pyray API parity (reviewed 2026-02-28).

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 450
MAX_BUILDINGS = 100

KEY_RIGHT = getattr(pr, "KEY_RIGHT", 262)
KEY_LEFT = getattr(pr, "KEY_LEFT", 263)
KEY_A = getattr(pr, "KEY_A", 65)
KEY_S = getattr(pr, "KEY_S", 83)
KEY_R = getattr(pr, "KEY_R", 82)


@dataclass
class Building:
    """Store building geometry and render color."""

    rect: pr.Rectangle
    color: pr.Color


def build_scene() -> list[Building]:
    """Generate the random side-scrolling city backdrop."""
    spacing = 0
    buildings: list[Building] = []

    for _ in range(MAX_BUILDINGS):
        width = float(pr.get_random_value(50, 200))
        height = float(pr.get_random_value(100, 800))
        rect = pr.Rectangle(
            -6000.0 + float(spacing),
            SCREEN_HEIGHT - 130.0 - height,
            width,
            height,
        )
        spacing += int(width)

        color = pr.Color(
            pr.get_random_value(200, 240),
            pr.get_random_value(200, 240),
            pr.get_random_value(200, 250),
            255,
        )
        buildings.append(Building(rect=rect, color=color))

    return buildings


def main() -> None:
    """Run the 2D camera movement, zoom, and rotation demo."""
    pr.init_window(SCREEN_WIDTH, SCREEN_HEIGHT, "raylib [core] example - 2d camera")

    player = pr.Rectangle(400.0, 280.0, 40.0, 40.0)
    buildings = build_scene()

    camera = pr.Camera2D(
        pr.Vector2(SCREEN_WIDTH / 2.0, SCREEN_HEIGHT / 2.0),
        pr.Vector2(player.x + 20.0, player.y + 20.0),
        0.0,
        1.0,
    )

    pr.set_target_fps(60)

    while not pr.window_should_close():
        if pr.is_key_down(KEY_RIGHT):
            player.x += 2.0
        elif pr.is_key_down(KEY_LEFT):
            player.x -= 2.0

        camera.target = pr.Vector2(player.x + 20.0, player.y + 20.0)

        if pr.is_key_down(KEY_A):
            camera.rotation -= 1.0
        elif pr.is_key_down(KEY_S):
            camera.rotation += 1.0

        camera.rotation = max(-40.0, min(40.0, camera.rotation))

        if (wheel := pr.get_mouse_wheel_move()) != 0.0:
            camera.zoom = math.exp(math.log(camera.zoom) + wheel * 0.1)
        camera.zoom = max(0.1, min(3.0, camera.zoom))

        if pr.is_key_pressed(KEY_R):
            camera.zoom = 1.0
            camera.rotation = 0.0

        pr.begin_drawing()
        pr.clear_background(pr.RAYWHITE)

        pr.begin_mode_2d(camera)
        pr.draw_rectangle(-6000, 320, 13000, 8000, pr.DARKGRAY)

        for building in buildings:
            pr.draw_rectangle_rec(building.rect, building.color)

        pr.draw_rectangle_rec(player, pr.RED)

        pr.draw_line(
            int(camera.target.x),
            -SCREEN_HEIGHT * 10,
            int(camera.target.x),
            SCREEN_HEIGHT * 10,
            pr.GREEN,
        )
        pr.draw_line(
            -SCREEN_WIDTH * 10,
            int(camera.target.y),
            SCREEN_WIDTH * 10,
            int(camera.target.y),
            pr.GREEN,
        )
        pr.end_mode_2d()

        pr.draw_text("SCREEN AREA", 640, 10, 20, pr.RED)

        pr.draw_rectangle(0, 0, SCREEN_WIDTH, 5, pr.RED)
        pr.draw_rectangle(0, 5, 5, SCREEN_HEIGHT - 10, pr.RED)
        pr.draw_rectangle(SCREEN_WIDTH - 5, 5, 5, SCREEN_HEIGHT - 10, pr.RED)
        pr.draw_rectangle(0, SCREEN_HEIGHT - 5, SCREEN_WIDTH, 5, pr.RED)

        pr.draw_rectangle(10, 10, 250, 113, pr.fade(pr.SKYBLUE, 0.5))
        pr.draw_rectangle_lines(10, 10, 250, 113, pr.BLUE)

        pr.draw_text("Free 2D camera controls:", 20, 20, 10, pr.BLACK)
        pr.draw_text("- Right/Left to move player", 40, 40, 10, pr.DARKGRAY)
        pr.draw_text("- Mouse Wheel to Zoom in-out", 40, 60, 10, pr.DARKGRAY)
        pr.draw_text("- A / S to Rotate", 40, 80, 10, pr.DARKGRAY)
        pr.draw_text("- R to reset Zoom and Rotation", 40, 100, 10, pr.DARKGRAY)

        pr.end_drawing()

    pr.close_window()


if __name__ == "__main__":
    main()
