from __future__ import annotations

from pathlib import Path

import pyray as pr

# Version checked: raylib 5.x/pyray API parity (reviewed 2026-02-28).

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 450
BLEND_MULTIPLIED = getattr(pr, "BLEND_MULTIPLIED", 2)
BLEND_CUSTOM_SEPARATE = getattr(pr, "BLEND_CUSTOM_SEPARATE", 7)
RL_ZERO = getattr(pr, "RL_ZERO", 0)
RL_ONE = getattr(pr, "RL_ONE", 1)
RL_FUNC_ADD = getattr(pr, "RL_FUNC_ADD", 32774)


def main() -> None:
    """Run magnifying glass view with circular alpha mask."""
    pr.init_window(
        SCREEN_WIDTH, SCREEN_HEIGHT, "raylib [textures] example - magnifying glass"
    )

    resources = Path(__file__).resolve().parent / "resources"
    bunny = pr.load_texture(str(resources / "raybunny.png"))
    parrots = pr.load_texture(str(resources / "parrots.png"))

    circle = pr.gen_image_color(256, 256, pr.BLANK)
    pr.image_draw_circle(circle, 128, 128, 128, pr.WHITE)
    mask = pr.load_texture_from_image(circle)
    pr.unload_image(circle)

    magnified_world = pr.load_render_texture(256, 256)
    camera = pr.Camera2D(pr.Vector2(128.0, 128.0), pr.Vector2(0.0, 0.0), 0.0, 2.0)

    pr.set_target_fps(60)

    while not pr.window_should_close():
        m_pos = pr.get_mouse_position()
        camera.target = m_pos

        pr.begin_drawing()
        pr.clear_background(pr.RAYWHITE)

        pr.draw_texture(parrots, 144, 33, pr.WHITE)
        pr.draw_text(
            "Use the magnifying glass to find hidden bunnies!", 154, 6, 20, pr.BLACK
        )

        pr.begin_texture_mode(magnified_world)
        pr.clear_background(pr.RAYWHITE)
        pr.begin_mode_2d(camera)
        pr.draw_texture(parrots, 144, 33, pr.WHITE)
        pr.draw_text(
            "Use the magnifying glass to find hidden bunnies!", 154, 6, 20, pr.BLACK
        )

        pr.begin_blend_mode(BLEND_MULTIPLIED)
        pr.draw_texture(bunny, 250, 350, pr.WHITE)
        pr.draw_texture(bunny, 500, 100, pr.WHITE)
        pr.draw_texture(bunny, 420, 300, pr.WHITE)
        pr.draw_texture(bunny, 650, 10, pr.WHITE)
        pr.end_blend_mode()
        pr.end_mode_2d()

        pr.begin_blend_mode(BLEND_CUSTOM_SEPARATE)
        pr.rl_set_blend_factors_separate(
            RL_ZERO, RL_ONE, RL_ONE, RL_ZERO, RL_FUNC_ADD, RL_FUNC_ADD
        )
        pr.draw_texture(mask, 0, 0, pr.WHITE)
        pr.end_blend_mode()
        pr.end_texture_mode()

        pr.draw_texture_rec(
            magnified_world.texture,
            pr.Rectangle(0.0, 0.0, 256.0, -256.0),
            pr.Vector2(m_pos.x - 128.0, m_pos.y - 128.0),
            pr.WHITE,
        )

        pr.draw_ring(m_pos, 126.0, 130.0, 0.0, 360.0, 64, pr.BLACK)
        rx = m_pos.x / 800.0
        ry = m_pos.y / 800.0
        pr.draw_circle(
            int((m_pos.x - 64.0 * rx) - 32.0),
            int((m_pos.y - 64.0 * ry) - 32.0),
            4.0,
            pr.color_alpha(pr.WHITE, 0.5),
        )

        pr.end_drawing()

    pr.unload_texture(parrots)
    pr.unload_texture(bunny)
    pr.unload_texture(mask)
    pr.unload_render_texture(magnified_world)
    pr.close_window()


if __name__ == "__main__":
    main()
