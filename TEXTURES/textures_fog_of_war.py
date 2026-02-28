from __future__ import annotations

from pathlib import Path

import pyray as pr

# Version checked: raylib 5.x/pyray API parity (reviewed 2026-02-28).

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 450
MAP_TILE_SIZE = 32
PLAYER_SIZE = 16
PLAYER_TILE_VISIBILITY = 2
TEXTURE_FILTER_BILINEAR = getattr(pr, "TEXTURE_FILTER_BILINEAR", 1)
TEXTURE_WRAP_CLAMP = getattr(pr, "TEXTURE_WRAP_CLAMP", 1)
KEY_RIGHT = getattr(pr, "KEY_RIGHT", 262)
KEY_LEFT = getattr(pr, "KEY_LEFT", 263)
KEY_DOWN = getattr(pr, "KEY_DOWN", 264)
KEY_UP = getattr(pr, "KEY_UP", 265)


def main() -> None:
    """Run tile-based fog-of-war rendering demo."""
    pr.init_window(
        SCREEN_WIDTH, SCREEN_HEIGHT, "raylib [textures] example - fog of war"
    )

    tiles_x = 25
    tiles_y = 15
    tile_ids = [pr.get_random_value(0, 1) for _ in range(tiles_x * tiles_y)]
    tile_fog = [0 for _ in range(tiles_x * tiles_y)]

    player_position = pr.Vector2(180.0, 130.0)
    player_tile_x = 0
    player_tile_y = 0

    fog_of_war = pr.load_render_texture(tiles_x, tiles_y)
    pr.set_texture_filter(fog_of_war.texture, TEXTURE_FILTER_BILINEAR)
    pr.set_texture_wrap(fog_of_war.texture, TEXTURE_WRAP_CLAMP)

    pr.set_target_fps(60)

    while not pr.window_should_close():
        if pr.is_key_down(KEY_RIGHT):
            player_position.x += 5.0
        if pr.is_key_down(KEY_LEFT):
            player_position.x -= 5.0
        if pr.is_key_down(KEY_DOWN):
            player_position.y += 5.0
        if pr.is_key_down(KEY_UP):
            player_position.y -= 5.0

        max_x = tiles_x * MAP_TILE_SIZE - PLAYER_SIZE
        max_y = tiles_y * MAP_TILE_SIZE - PLAYER_SIZE
        player_position.x = min(max(player_position.x, 0.0), float(max_x))
        player_position.y = min(max(player_position.y, 0.0), float(max_y))

        for index, value in enumerate(tile_fog):
            if value == 1:
                tile_fog[index] = 2

        player_tile_x = int((player_position.x + MAP_TILE_SIZE / 2.0) / MAP_TILE_SIZE)
        player_tile_y = int((player_position.y + MAP_TILE_SIZE / 2.0) / MAP_TILE_SIZE)

        for y in range(
            player_tile_y - PLAYER_TILE_VISIBILITY,
            player_tile_y + PLAYER_TILE_VISIBILITY,
        ):
            for x in range(
                player_tile_x - PLAYER_TILE_VISIBILITY,
                player_tile_x + PLAYER_TILE_VISIBILITY,
            ):
                if 0 <= x < tiles_x and 0 <= y < tiles_y:
                    tile_fog[y * tiles_x + x] = 1

        pr.begin_texture_mode(fog_of_war)
        pr.clear_background(pr.BLANK)
        for y in range(tiles_y):
            for x in range(tiles_x):
                fog = tile_fog[y * tiles_x + x]
                if fog == 0:
                    pr.draw_rectangle(x, y, 1, 1, pr.BLACK)
                elif fog == 2:
                    pr.draw_rectangle(x, y, 1, 1, pr.fade(pr.BLACK, 0.8))
        pr.end_texture_mode()

        pr.begin_drawing()
        pr.clear_background(pr.RAYWHITE)

        for y in range(tiles_y):
            for x in range(tiles_x):
                tile_color = (
                    pr.BLUE if tile_ids[y * tiles_x + x] == 0 else pr.fade(pr.BLUE, 0.9)
                )
                pr.draw_rectangle(
                    x * MAP_TILE_SIZE,
                    y * MAP_TILE_SIZE,
                    MAP_TILE_SIZE,
                    MAP_TILE_SIZE,
                    tile_color,
                )
                pr.draw_rectangle_lines(
                    x * MAP_TILE_SIZE,
                    y * MAP_TILE_SIZE,
                    MAP_TILE_SIZE,
                    MAP_TILE_SIZE,
                    pr.fade(pr.DARKBLUE, 0.5),
                )

        pr.draw_rectangle_v(
            player_position, pr.Vector2(PLAYER_SIZE, PLAYER_SIZE), pr.RED
        )

        pr.draw_texture_pro(
            fog_of_war.texture,
            pr.Rectangle(
                0.0,
                0.0,
                float(fog_of_war.texture.width),
                float(-fog_of_war.texture.height),
            ),
            pr.Rectangle(
                0.0, 0.0, float(tiles_x * MAP_TILE_SIZE), float(tiles_y * MAP_TILE_SIZE)
            ),
            pr.Vector2(0.0, 0.0),
            0.0,
            pr.WHITE,
        )

        pr.draw_text(
            f"Current tile: [{player_tile_x},{player_tile_y}]", 10, 10, 20, pr.RAYWHITE
        )
        pr.draw_text("ARROW KEYS to move", 10, SCREEN_HEIGHT - 25, 20, pr.RAYWHITE)
        pr.end_drawing()

    pr.unload_render_texture(fog_of_war)
    pr.close_window()


if __name__ == "__main__":
    main()
