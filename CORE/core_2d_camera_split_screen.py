from __future__ import annotations

import pyray as pr

# Version checked: raylib 5.x/pyray API parity (reviewed 2026-02-28).

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 440
PLAYER_SIZE = 40

KEY_W = getattr(pr, "KEY_W", 87)
KEY_A = getattr(pr, "KEY_A", 65)
KEY_S = getattr(pr, "KEY_S", 83)
KEY_D = getattr(pr, "KEY_D", 68)
KEY_UP = getattr(pr, "KEY_UP", 265)
KEY_DOWN = getattr(pr, "KEY_DOWN", 264)
KEY_LEFT = getattr(pr, "KEY_LEFT", 263)
KEY_RIGHT = getattr(pr, "KEY_RIGHT", 262)


def draw_world(player1: pr.Rectangle, player2: pr.Rectangle) -> None:
    """Draw shared scene for each camera."""
    for i in range(SCREEN_WIDTH // PLAYER_SIZE + 1):
        pr.draw_line_v(
            pr.Vector2(float(PLAYER_SIZE * i), 0.0),
            pr.Vector2(float(PLAYER_SIZE * i), float(SCREEN_HEIGHT)),
            pr.LIGHTGRAY,
        )
    for i in range(SCREEN_HEIGHT // PLAYER_SIZE + 1):
        pr.draw_line_v(
            pr.Vector2(0.0, float(PLAYER_SIZE * i)),
            pr.Vector2(float(SCREEN_WIDTH), float(PLAYER_SIZE * i)),
            pr.LIGHTGRAY,
        )
    for i in range(SCREEN_WIDTH // PLAYER_SIZE):
        for j in range(SCREEN_HEIGHT // PLAYER_SIZE):
            pr.draw_text(
                f"[{i},{j}]",
                10 + PLAYER_SIZE * i,
                15 + PLAYER_SIZE * j,
                10,
                pr.LIGHTGRAY,
            )
    pr.draw_rectangle_rec(player1, pr.RED)
    pr.draw_rectangle_rec(player2, pr.BLUE)


def main() -> None:
    """Run the 2D split-screen camera example."""
    pr.init_window(
        SCREEN_WIDTH,
        SCREEN_HEIGHT,
        "raylib [core] example - 2d camera split screen",
    )

    player1 = pr.Rectangle(200.0, 200.0, PLAYER_SIZE, PLAYER_SIZE)
    player2 = pr.Rectangle(250.0, 200.0, PLAYER_SIZE, PLAYER_SIZE)

    camera1 = pr.Camera2D(
        pr.Vector2(200.0, 200.0), pr.Vector2(player1.x, player1.y), 0.0, 1.0
    )
    camera2 = pr.Camera2D(
        pr.Vector2(200.0, 200.0), pr.Vector2(player2.x, player2.y), 0.0, 1.0
    )

    screen_camera1 = pr.load_render_texture(SCREEN_WIDTH // 2, SCREEN_HEIGHT)
    screen_camera2 = pr.load_render_texture(SCREEN_WIDTH // 2, SCREEN_HEIGHT)
    split_screen_rect = pr.Rectangle(
        0.0,
        0.0,
        float(screen_camera1.texture.width),
        float(-screen_camera1.texture.height),
    )

    pr.set_target_fps(60)

    while not pr.window_should_close():
        if pr.is_key_down(KEY_S):
            player1.y += 3.0
        elif pr.is_key_down(KEY_W):
            player1.y -= 3.0
        if pr.is_key_down(KEY_D):
            player1.x += 3.0
        elif pr.is_key_down(KEY_A):
            player1.x -= 3.0

        if pr.is_key_down(KEY_UP):
            player2.y -= 3.0
        elif pr.is_key_down(KEY_DOWN):
            player2.y += 3.0
        if pr.is_key_down(KEY_RIGHT):
            player2.x += 3.0
        elif pr.is_key_down(KEY_LEFT):
            player2.x -= 3.0

        camera1.target = pr.Vector2(player1.x, player1.y)
        camera2.target = pr.Vector2(player2.x, player2.y)

        pr.begin_texture_mode(screen_camera1)
        pr.clear_background(pr.RAYWHITE)
        pr.begin_mode_2d(camera1)
        draw_world(player1, player2)
        pr.end_mode_2d()
        pr.draw_rectangle(
            0, 0, pr.get_screen_width() // 2, 30, pr.fade(pr.RAYWHITE, 0.6)
        )
        pr.draw_text("PLAYER1: W/S/A/D to move", 10, 10, 10, pr.MAROON)
        pr.end_texture_mode()

        pr.begin_texture_mode(screen_camera2)
        pr.clear_background(pr.RAYWHITE)
        pr.begin_mode_2d(camera2)
        draw_world(player1, player2)
        pr.end_mode_2d()
        pr.draw_rectangle(
            0, 0, pr.get_screen_width() // 2, 30, pr.fade(pr.RAYWHITE, 0.6)
        )
        pr.draw_text("PLAYER2: UP/DOWN/LEFT/RIGHT to move", 10, 10, 10, pr.DARKBLUE)
        pr.end_texture_mode()

        pr.begin_drawing()
        pr.clear_background(pr.BLACK)
        pr.draw_texture_rec(
            screen_camera1.texture, split_screen_rect, pr.Vector2(0.0, 0.0), pr.WHITE
        )
        pr.draw_texture_rec(
            screen_camera2.texture,
            split_screen_rect,
            pr.Vector2(SCREEN_WIDTH / 2.0, 0.0),
            pr.WHITE,
        )
        pr.draw_rectangle(
            pr.get_screen_width() // 2 - 2, 0, 4, pr.get_screen_height(), pr.LIGHTGRAY
        )
        pr.end_drawing()

    pr.unload_render_texture(screen_camera1)
    pr.unload_render_texture(screen_camera2)
    pr.close_window()


if __name__ == "__main__":
    main()
