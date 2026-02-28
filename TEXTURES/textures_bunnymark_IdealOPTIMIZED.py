from __future__ import annotations

from pathlib import Path

import pyray as pr

# Version checked: raylib 5.x/pyray API parity (reviewed 2026-02-28).

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 450
MAX_BUNNIES = 50000
MAX_BATCH_ELEMENTS = 8192
MOUSE_BUTTON_LEFT = getattr(pr, "MOUSE_BUTTON_LEFT", 0)


def main() -> None:
    """Run bunnymark draw-load stress example."""
    pr.init_window(SCREEN_WIDTH, SCREEN_HEIGHT, "raylib [textures] example - bunnymark")

    resources = Path(__file__).resolve().parent / "resources"
    tex_bunny = pr.load_texture(str(resources / "raybunny.png"))

    # Structure-of-arrays: far less Python object/attribute overhead in the hot loop.
    pos_x: list[float] = []
    pos_y: list[float] = []
    speed_x: list[float] = []
    speed_y: list[float] = []
    color: list[pr.Color] = []

    # Cache frequently-used callables/constants locally to reduce lookup overhead.
    get_random_value = pr.get_random_value
    draw_texture = pr.draw_texture
    to_int = int
    bunny_half_w = tex_bunny.width * 0.5
    bunny_half_h = tex_bunny.height * 0.5
    screen_w = float(SCREEN_WIDTH)
    screen_h = float(SCREEN_HEIGHT)

    pr.set_target_fps(60)

    while not pr.window_should_close():
        if pr.is_mouse_button_down(MOUSE_BUTTON_LEFT):
            mouse = pr.get_mouse_position()
            spawn_count = min(100, MAX_BUNNIES - len(pos_x))
            for _ in range(spawn_count):
                pos_x.append(mouse.x)
                pos_y.append(mouse.y)
                speed_x.append(float(get_random_value(-250, 250)) / 60.0)
                speed_y.append(float(get_random_value(-250, 250)) / 60.0)
                color.append(
                    pr.Color(
                        get_random_value(50, 240),
                        get_random_value(80, 240),
                        get_random_value(100, 240),
                        255,
                    )
                )

        bunny_count = len(pos_x)
        for i in range(bunny_count):
            x = pos_x[i] + speed_x[i]
            y = pos_y[i] + speed_y[i]

            if x + bunny_half_w > screen_w or x + bunny_half_w < 0.0:
                speed_x[i] *= -1.0
            if y + bunny_half_h > screen_h or y + bunny_half_h - 40.0 < 0.0:
                speed_y[i] *= -1.0

            pos_x[i] = x
            pos_y[i] = y

        pr.begin_drawing()
        pr.clear_background(pr.RAYWHITE)

        for i in range(bunny_count):
            draw_texture(tex_bunny, to_int(pos_x[i]), to_int(pos_y[i]), color[i])

        pr.draw_rectangle(0, 0, SCREEN_WIDTH, 40, pr.BLACK)
        pr.draw_text(f"bunnies: {bunny_count}", 120, 10, 20, pr.GREEN)
        pr.draw_text(
            f"batched draw calls: {1 + bunny_count // MAX_BATCH_ELEMENTS}",
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
