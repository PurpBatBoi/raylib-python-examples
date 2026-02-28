from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

import pyray as pr

# Version checked: raylib 5.x/pyray API parity (reviewed 2026-02-28).

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 450
MAX_BUNNIES = 50000
MAX_BATCH_ELEMENTS = 8192
MOUSE_BUTTON_LEFT = getattr(pr, "MOUSE_BUTTON_LEFT", 0)


@dataclass
class Bunny:
    """Per-bunny state for the bunnymark benchmark."""

    position: pr.Vector2
    speed: pr.Vector2
    color: pr.Color


def make_bunny(position: pr.Vector2) -> Bunny:
    """Create one randomized bunny."""
    return Bunny(
        position=pr.Vector2(position.x, position.y),
        speed=pr.Vector2(
            float(pr.get_random_value(-250, 250)) / 60.0,
            float(pr.get_random_value(-250, 250)) / 60.0,
        ),
        color=pr.Color(
            pr.get_random_value(50, 240),
            pr.get_random_value(80, 240),
            pr.get_random_value(100, 240),
            255,
        ),
    )


def main() -> None:
    """Run bunnymark draw-load stress example."""
    pr.init_window(SCREEN_WIDTH, SCREEN_HEIGHT, "raylib [textures] example - bunnymark")

    resources = Path(__file__).resolve().parent / "resources"
    tex_bunny = pr.load_texture(str(resources / "raybunny.png"))
    bunnies: list[Bunny] = []

    pr.set_target_fps(60)

    while not pr.window_should_close():
        if pr.is_mouse_button_down(MOUSE_BUTTON_LEFT):
            mouse = pr.get_mouse_position()
            for _ in range(100):
                if len(bunnies) >= MAX_BUNNIES:
                    break
                bunnies.append(make_bunny(mouse))

        for bunny in bunnies:
            bunny.position.x += bunny.speed.x
            bunny.position.y += bunny.speed.y

            if (
                bunny.position.x + tex_bunny.width / 2.0 > pr.get_screen_width()
                or bunny.position.x + tex_bunny.width / 2.0 < 0
            ):
                bunny.speed.x *= -1.0

            if (
                bunny.position.y + tex_bunny.height / 2.0 > pr.get_screen_height()
                or bunny.position.y + tex_bunny.height / 2.0 - 40.0 < 0
            ):
                bunny.speed.y *= -1.0

        pr.begin_drawing()
        pr.clear_background(pr.RAYWHITE)

        for bunny in bunnies:
            pr.draw_texture(
                tex_bunny, int(bunny.position.x), int(bunny.position.y), bunny.color
            )

        pr.draw_rectangle(0, 0, SCREEN_WIDTH, 40, pr.BLACK)
        pr.draw_text(f"bunnies: {len(bunnies)}", 120, 10, 20, pr.GREEN)
        pr.draw_text(
            f"batched draw calls: {1 + len(bunnies) // MAX_BATCH_ELEMENTS}",
            320,
            10,
            20,
            pr.MAROON,
        )
        pr.draw_fps(10, 10)
        pr.end_drawing()

    pr.unload_texture(tex_bunny)
    pr.close_window()


if __name__ == "__main__":
    main()
