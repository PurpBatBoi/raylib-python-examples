from __future__ import annotations

from pathlib import Path

import pyray as pr

# Version checked: raylib 5.x/pyray API parity (reviewed 2026-02-28).

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 450
NPATCH_NINE_PATCH = getattr(pr, "NPATCH_NINE_PATCH", 0)
NPATCH_THREE_PATCH_HORIZONTAL = getattr(pr, "NPATCH_THREE_PATCH_HORIZONTAL", 2)
NPATCH_THREE_PATCH_VERTICAL = getattr(pr, "NPATCH_THREE_PATCH_VERTICAL", 1)


def main() -> None:
    """Run n-patch and 3-patch texture drawing demo."""
    pr.init_window(
        SCREEN_WIDTH, SCREEN_HEIGHT, "raylib [textures] example - npatch drawing"
    )

    resources = Path(__file__).resolve().parent / "resources"
    n_patch_texture = pr.load_texture(str(resources / "ninepatch_button.png"))

    origin = pr.Vector2(0.0, 0.0)
    dst_rec_1 = pr.Rectangle(480.0, 160.0, 32.0, 32.0)
    dst_rec_2 = pr.Rectangle(160.0, 160.0, 32.0, 32.0)
    dst_rec_h = pr.Rectangle(160.0, 93.0, 32.0, 32.0)
    dst_rec_v = pr.Rectangle(92.0, 160.0, 32.0, 32.0)

    nine_patch_info_1 = pr.NPatchInfo(
        pr.Rectangle(0.0, 0.0, 64.0, 64.0),
        12,
        40,
        12,
        12,
        NPATCH_NINE_PATCH,
    )
    nine_patch_info_2 = pr.NPatchInfo(
        pr.Rectangle(0.0, 128.0, 64.0, 64.0),
        16,
        16,
        16,
        16,
        NPATCH_NINE_PATCH,
    )
    h3_patch_info = pr.NPatchInfo(
        pr.Rectangle(0.0, 64.0, 64.0, 64.0),
        8,
        8,
        8,
        8,
        NPATCH_THREE_PATCH_HORIZONTAL,
    )
    v3_patch_info = pr.NPatchInfo(
        pr.Rectangle(0.0, 192.0, 64.0, 64.0),
        6,
        6,
        6,
        6,
        NPATCH_THREE_PATCH_VERTICAL,
    )

    pr.set_target_fps(60)

    while not pr.window_should_close():
        mouse_position = pr.get_mouse_position()

        dst_rec_1.width = mouse_position.x - dst_rec_1.x
        dst_rec_1.height = mouse_position.y - dst_rec_1.y
        dst_rec_2.width = mouse_position.x - dst_rec_2.x
        dst_rec_2.height = mouse_position.y - dst_rec_2.y
        dst_rec_h.width = mouse_position.x - dst_rec_h.x
        dst_rec_v.height = mouse_position.y - dst_rec_v.y

        dst_rec_1.width = max(1.0, min(300.0, dst_rec_1.width))
        dst_rec_1.height = max(1.0, dst_rec_1.height)
        dst_rec_2.width = max(1.0, min(300.0, dst_rec_2.width))
        dst_rec_2.height = max(1.0, dst_rec_2.height)
        dst_rec_h.width = max(1.0, dst_rec_h.width)
        dst_rec_v.height = max(1.0, dst_rec_v.height)

        pr.begin_drawing()
        pr.clear_background(pr.RAYWHITE)

        pr.draw_texture_n_patch(
            n_patch_texture, nine_patch_info_2, dst_rec_2, origin, 0.0, pr.WHITE
        )
        pr.draw_texture_n_patch(
            n_patch_texture, nine_patch_info_1, dst_rec_1, origin, 0.0, pr.WHITE
        )
        pr.draw_texture_n_patch(
            n_patch_texture, h3_patch_info, dst_rec_h, origin, 0.0, pr.WHITE
        )
        pr.draw_texture_n_patch(
            n_patch_texture, v3_patch_info, dst_rec_v, origin, 0.0, pr.WHITE
        )

        pr.draw_rectangle_lines(5, 88, 74, 266, pr.BLUE)
        pr.draw_texture(n_patch_texture, 10, 93, pr.WHITE)
        pr.draw_text("TEXTURE", 15, 360, 10, pr.DARKGRAY)
        pr.draw_text(
            "Move the mouse to stretch or shrink the n-patches",
            10,
            20,
            20,
            pr.DARKGRAY,
        )

        pr.end_drawing()

    pr.unload_texture(n_patch_texture)
    pr.close_window()


if __name__ == "__main__":
    main()
