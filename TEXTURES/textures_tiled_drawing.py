from __future__ import annotations
from pathlib import Path

import pyray as pr

# Version checked: raylib 5.x/pyray API parity (reviewed 2026-02-28).

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 450
OPT_WIDTH = 220
MARGIN_SIZE = 8
COLOR_SIZE = 16

FLAG_WINDOW_RESIZABLE = getattr(pr, "FLAG_WINDOW_RESIZABLE", 4)
TEXTURE_FILTER_BILINEAR = getattr(pr, "TEXTURE_FILTER_BILINEAR", 1)
MOUSE_BUTTON_LEFT = getattr(pr, "MOUSE_BUTTON_LEFT", 0)
KEY_UP = getattr(pr, "KEY_UP", 265)
KEY_DOWN = getattr(pr, "KEY_DOWN", 264)
KEY_LEFT = getattr(pr, "KEY_LEFT", 263)
KEY_RIGHT = getattr(pr, "KEY_RIGHT", 262)
KEY_SPACE = getattr(pr, "KEY_SPACE", 32)


def draw_texture_tiled(
    texture: pr.Texture,
    source: pr.Rectangle,
    dest: pr.Rectangle,
    origin: pr.Vector2,
    rotation: float,
    scale: float,
    tint: pr.Color,
) -> None:
    """Draw a source rectangle tiled in the destination rectangle."""
    if texture.id <= 0 or scale <= 0.0:
        return
    if source.width == 0.0 or source.height == 0.0:
        return

    tile_width = int(source.width * scale)
    tile_height = int(source.height * scale)

    if dest.width < tile_width and dest.height < tile_height:
        pr.draw_texture_pro(
            texture,
            pr.Rectangle(
                source.x,
                source.y,
                (dest.width / tile_width) * source.width,
                (dest.height / tile_height) * source.height,
            ),
            pr.Rectangle(dest.x, dest.y, dest.width, dest.height),
            origin,
            rotation,
            tint,
        )
    elif dest.width <= tile_width:
        dy = 0
        while dy + tile_height < dest.height:
            pr.draw_texture_pro(
                texture,
                pr.Rectangle(
                    source.x,
                    source.y,
                    (dest.width / tile_width) * source.width,
                    source.height,
                ),
                pr.Rectangle(dest.x, dest.y + dy, dest.width, float(tile_height)),
                origin,
                rotation,
                tint,
            )
            dy += tile_height

        if dy < dest.height:
            pr.draw_texture_pro(
                texture,
                pr.Rectangle(
                    source.x,
                    source.y,
                    (dest.width / tile_width) * source.width,
                    ((dest.height - dy) / tile_height) * source.height,
                ),
                pr.Rectangle(dest.x, dest.y + dy, dest.width, dest.height - dy),
                origin,
                rotation,
                tint,
            )
    elif dest.height <= tile_height:
        dx = 0
        while dx + tile_width < dest.width:
            pr.draw_texture_pro(
                texture,
                pr.Rectangle(
                    source.x,
                    source.y,
                    source.width,
                    (dest.height / tile_height) * source.height,
                ),
                pr.Rectangle(dest.x + dx, dest.y, float(tile_width), dest.height),
                origin,
                rotation,
                tint,
            )
            dx += tile_width

        if dx < dest.width:
            pr.draw_texture_pro(
                texture,
                pr.Rectangle(
                    source.x,
                    source.y,
                    ((dest.width - dx) / tile_width) * source.width,
                    (dest.height / tile_height) * source.height,
                ),
                pr.Rectangle(dest.x + dx, dest.y, dest.width - dx, dest.height),
                origin,
                rotation,
                tint,
            )
    else:
        dx = 0
        while dx + tile_width < dest.width:
            dy = 0
            while dy + tile_height < dest.height:
                pr.draw_texture_pro(
                    texture,
                    source,
                    pr.Rectangle(
                        dest.x + dx, dest.y + dy, float(tile_width), float(tile_height)
                    ),
                    origin,
                    rotation,
                    tint,
                )
                dy += tile_height

            if dy < dest.height:
                pr.draw_texture_pro(
                    texture,
                    pr.Rectangle(
                        source.x,
                        source.y,
                        source.width,
                        ((dest.height - dy) / tile_height) * source.height,
                    ),
                    pr.Rectangle(
                        dest.x + dx, dest.y + dy, float(tile_width), dest.height - dy
                    ),
                    origin,
                    rotation,
                    tint,
                )
            dx += tile_width

        if dx < dest.width:
            dy = 0
            while dy + tile_height < dest.height:
                pr.draw_texture_pro(
                    texture,
                    pr.Rectangle(
                        source.x,
                        source.y,
                        ((dest.width - dx) / tile_width) * source.width,
                        source.height,
                    ),
                    pr.Rectangle(
                        dest.x + dx, dest.y + dy, dest.width - dx, float(tile_height)
                    ),
                    origin,
                    rotation,
                    tint,
                )
                dy += tile_height

            if dy < dest.height:
                pr.draw_texture_pro(
                    texture,
                    pr.Rectangle(
                        source.x,
                        source.y,
                        ((dest.width - dx) / tile_width) * source.width,
                        ((dest.height - dy) / tile_height) * source.height,
                    ),
                    pr.Rectangle(
                        dest.x + dx, dest.y + dy, dest.width - dx, dest.height - dy
                    ),
                    origin,
                    rotation,
                    tint,
                )


def main() -> None:
    """Run tiled texture drawing with pattern/color/scale/rotation controls."""
    pr.set_config_flags(FLAG_WINDOW_RESIZABLE)
    pr.init_window(
        SCREEN_WIDTH, SCREEN_HEIGHT, "raylib [textures] example - tiled drawing"
    )

    resources = Path(__file__).resolve().parent / "resources"
    tex_pattern = pr.load_texture(str(resources / "patterns.png"))
    pr.set_texture_filter(tex_pattern, TEXTURE_FILTER_BILINEAR)

    rec_pattern = [
        pr.Rectangle(3.0, 3.0, 66.0, 66.0),
        pr.Rectangle(75.0, 3.0, 100.0, 100.0),
        pr.Rectangle(3.0, 75.0, 66.0, 66.0),
        pr.Rectangle(7.0, 156.0, 50.0, 50.0),
        pr.Rectangle(85.0, 106.0, 90.0, 45.0),
        pr.Rectangle(75.0, 154.0, 100.0, 60.0),
    ]
    colors = [
        pr.BLACK,
        pr.MAROON,
        pr.ORANGE,
        pr.BLUE,
        pr.PURPLE,
        pr.BEIGE,
        pr.LIME,
        pr.RED,
        pr.DARKGRAY,
        pr.SKYBLUE,
    ]
    color_rec: list[pr.Rectangle] = []

    x = 0
    y = 0
    for index in range(len(colors)):
        color_rec.append(
            pr.Rectangle(
                2.0 + MARGIN_SIZE + x,
                22.0 + 256.0 + MARGIN_SIZE + y,
                COLOR_SIZE * 2.0,
                float(COLOR_SIZE),
            )
        )
        if index == (len(colors) // 2 - 1):
            x = 0
            y += COLOR_SIZE + MARGIN_SIZE
        else:
            x += COLOR_SIZE * 2 + MARGIN_SIZE

    active_pattern = 0
    active_col = 0
    scale = 1.0
    rotation = 0.0

    pr.set_target_fps(60)

    while not pr.window_should_close():
        if pr.is_mouse_button_pressed(MOUSE_BUTTON_LEFT):
            mouse = pr.get_mouse_position()

            for index, pattern in enumerate(rec_pattern):
                clickable = pr.Rectangle(
                    2.0 + MARGIN_SIZE + pattern.x,
                    40.0 + MARGIN_SIZE + pattern.y,
                    pattern.width,
                    pattern.height,
                )
                if pr.check_collision_point_rec(mouse, clickable):
                    active_pattern = index
                    break

            for index, rec in enumerate(color_rec):
                if pr.check_collision_point_rec(mouse, rec):
                    active_col = index
                    break

        if pr.is_key_pressed(KEY_UP):
            scale += 0.25
        if pr.is_key_pressed(KEY_DOWN):
            scale -= 0.25
        scale = min(10.0, scale)
        if scale <= 0.0:
            scale = 0.25

        if pr.is_key_pressed(KEY_LEFT):
            rotation -= 25.0
        if pr.is_key_pressed(KEY_RIGHT):
            rotation += 25.0
        if pr.is_key_pressed(KEY_SPACE):
            rotation = 0.0
            scale = 1.0

        pr.begin_drawing()
        pr.clear_background(pr.RAYWHITE)

        draw_texture_tiled(
            tex_pattern,
            rec_pattern[active_pattern],
            pr.Rectangle(
                float(OPT_WIDTH + MARGIN_SIZE),
                float(MARGIN_SIZE),
                pr.get_screen_width() - OPT_WIDTH - 2.0 * MARGIN_SIZE,
                pr.get_screen_height() - 2.0 * MARGIN_SIZE,
            ),
            pr.Vector2(0.0, 0.0),
            rotation,
            scale,
            colors[active_col],
        )

        pr.draw_rectangle(
            MARGIN_SIZE,
            MARGIN_SIZE,
            OPT_WIDTH - MARGIN_SIZE,
            pr.get_screen_height() - 2 * MARGIN_SIZE,
            pr.color_alpha(pr.LIGHTGRAY, 0.5),
        )

        pr.draw_text("Select Pattern", 2 + MARGIN_SIZE, 30 + MARGIN_SIZE, 10, pr.BLACK)
        pr.draw_texture(tex_pattern, 2 + MARGIN_SIZE, 40 + MARGIN_SIZE, pr.BLACK)
        active = rec_pattern[active_pattern]
        pr.draw_rectangle(
            2 + MARGIN_SIZE + int(active.x),
            40 + MARGIN_SIZE + int(active.y),
            int(active.width),
            int(active.height),
            pr.color_alpha(pr.DARKBLUE, 0.3),
        )

        pr.draw_text(
            "Select Color", 2 + MARGIN_SIZE, 10 + 256 + MARGIN_SIZE, 10, pr.BLACK
        )
        for index, rec in enumerate(color_rec):
            pr.draw_rectangle_rec(rec, colors[index])
            if active_col == index:
                pr.draw_rectangle_lines_ex(rec, 3.0, pr.color_alpha(pr.WHITE, 0.5))

        pr.draw_text(
            "Scale (UP/DOWN to change)",
            2 + MARGIN_SIZE,
            80 + 256 + MARGIN_SIZE,
            10,
            pr.BLACK,
        )
        pr.draw_text(
            f"{scale:.2f}x", 2 + MARGIN_SIZE, 92 + 256 + MARGIN_SIZE, 20, pr.BLACK
        )

        pr.draw_text(
            "Rotation (LEFT/RIGHT to change)",
            2 + MARGIN_SIZE,
            122 + 256 + MARGIN_SIZE,
            10,
            pr.BLACK,
        )
        pr.draw_text(
            f"{rotation:.0f} degrees",
            2 + MARGIN_SIZE,
            134 + 256 + MARGIN_SIZE,
            20,
            pr.BLACK,
        )
        pr.draw_text(
            "Press [SPACE] to reset",
            2 + MARGIN_SIZE,
            164 + 256 + MARGIN_SIZE,
            10,
            pr.DARKBLUE,
        )

        pr.draw_text(
            f"{pr.get_fps()} FPS", 2 + MARGIN_SIZE, 2 + MARGIN_SIZE, 20, pr.BLACK
        )
        pr.end_drawing()

    pr.unload_texture(tex_pattern)
    pr.close_window()


if __name__ == "__main__":
    main()
