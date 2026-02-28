from __future__ import annotations

from dataclasses import dataclass
from math import hypot

import pyray as pr

# Version checked: raylib 5.x/pyray API parity (reviewed 2026-02-28).

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 450

G = 400.0
PLAYER_JUMP_SPD = 350.0
PLAYER_HOR_SPD = 200.0

KEY_LEFT = getattr(pr, "KEY_LEFT", 263)
KEY_RIGHT = getattr(pr, "KEY_RIGHT", 262)
KEY_SPACE = getattr(pr, "KEY_SPACE", 32)
KEY_R = getattr(pr, "KEY_R", 82)
KEY_C = getattr(pr, "KEY_C", 67)


@dataclass
class Player:
    """Represent the controllable character in world space."""

    position: pr.Vector2
    speed: float
    can_jump: bool


@dataclass
class EnvItem:
    """Represent a world rectangle and whether it blocks movement."""

    rect: pr.Rectangle
    blocking: bool
    color: pr.Color


@dataclass
class EvenOutState:
    """Track vertical camera smoothing state for landing behavior."""

    evening_out: bool = False
    even_out_target: float = 0.0


def update_player(player: Player, env_items: list[EnvItem], delta: float) -> None:
    """Advance player movement and resolve simple platform collisions."""
    if pr.is_key_down(KEY_LEFT):
        player.position.x -= PLAYER_HOR_SPD * delta
    if pr.is_key_down(KEY_RIGHT):
        player.position.x += PLAYER_HOR_SPD * delta
    if pr.is_key_down(KEY_SPACE) and player.can_jump:
        player.speed = -PLAYER_JUMP_SPD
        player.can_jump = False

    hit_obstacle = False
    for item in env_items:
        if (
            item.blocking
            and item.rect.x <= player.position.x <= item.rect.x + item.rect.width
            and item.rect.y >= player.position.y
            and item.rect.y <= player.position.y + player.speed * delta
        ):
            hit_obstacle = True
            player.speed = 0.0
            player.position.y = item.rect.y
            break

    if not hit_obstacle:
        player.position.y += player.speed * delta
        player.speed += G * delta
        player.can_jump = False
    else:
        player.can_jump = True


def update_camera_center(
    camera: pr.Camera2D,
    player: Player,
    _env_items: list[EnvItem],
    _delta: float,
    width: int,
    height: int,
) -> None:
    """Lock camera target to player center."""
    camera.offset = pr.Vector2(width / 2.0, height / 2.0)
    camera.target = pr.Vector2(player.position.x, player.position.y)


def update_camera_center_inside_map(
    camera: pr.Camera2D,
    player: Player,
    env_items: list[EnvItem],
    _delta: float,
    width: int,
    height: int,
) -> None:
    """Follow player center while clamping against map bounds."""
    camera.target = pr.Vector2(player.position.x, player.position.y)
    camera.offset = pr.Vector2(width / 2.0, height / 2.0)

    min_x = 1000.0
    min_y = 1000.0
    max_x = -1000.0
    max_y = -1000.0

    for item in env_items:
        min_x = min(item.rect.x, min_x)
        max_x = max(item.rect.x + item.rect.width, max_x)
        min_y = min(item.rect.y, min_y)
        max_y = max(item.rect.y + item.rect.height, max_y)

    max_world = pr.get_world_to_screen_2d(pr.Vector2(max_x, max_y), camera)
    min_world = pr.get_world_to_screen_2d(pr.Vector2(min_x, min_y), camera)

    if max_world.x < width:
        camera.offset.x = width - (max_world.x - width / 2.0)
    if max_world.y < height:
        camera.offset.y = height - (max_world.y - height / 2.0)
    if min_world.x > 0.0:
        camera.offset.x = width / 2.0 - min_world.x
    if min_world.y > 0.0:
        camera.offset.y = height / 2.0 - min_world.y


def update_camera_center_smooth_follow(
    camera: pr.Camera2D,
    player: Player,
    _env_items: list[EnvItem],
    delta: float,
    width: int,
    height: int,
) -> None:
    """Smoothly move camera target toward player."""
    min_speed = 30.0
    min_effect_length = 10.0
    fraction_speed = 0.8

    camera.offset = pr.Vector2(width / 2.0, height / 2.0)
    diff_x = player.position.x - camera.target.x
    diff_y = player.position.y - camera.target.y
    length = hypot(diff_x, diff_y)

    if length > min_effect_length:
        speed = max(fraction_speed * length, min_speed)
        camera.target.x += diff_x * speed * delta / length
        camera.target.y += diff_y * speed * delta / length


def update_camera_even_out_on_landing(
    camera: pr.Camera2D,
    player: Player,
    _env_items: list[EnvItem],
    delta: float,
    width: int,
    height: int,
    state: EvenOutState,
) -> None:
    """Track player horizontally and ease vertical camera after landing."""
    even_out_speed = 700.0

    camera.offset = pr.Vector2(width / 2.0, height / 2.0)
    camera.target.x = player.position.x

    if state.evening_out:
        if state.even_out_target > camera.target.y:
            camera.target.y += even_out_speed * delta
            if camera.target.y > state.even_out_target:
                camera.target.y = state.even_out_target
                state.evening_out = False
        else:
            camera.target.y -= even_out_speed * delta
            if camera.target.y < state.even_out_target:
                camera.target.y = state.even_out_target
                state.evening_out = False
    elif (
        player.can_jump and player.speed == 0.0 and player.position.y != camera.target.y
    ):
        state.evening_out = True
        state.even_out_target = player.position.y


def update_camera_player_bounds_push(
    camera: pr.Camera2D,
    player: Player,
    _env_items: list[EnvItem],
    _delta: float,
    width: int,
    height: int,
) -> None:
    """Push camera only when player moves near viewport edges."""
    bbox = pr.Vector2(0.2, 0.2)

    bbox_world_min = pr.get_screen_to_world_2d(
        pr.Vector2((1.0 - bbox.x) * 0.5 * width, (1.0 - bbox.y) * 0.5 * height),
        camera,
    )
    bbox_world_max = pr.get_screen_to_world_2d(
        pr.Vector2((1.0 + bbox.x) * 0.5 * width, (1.0 + bbox.y) * 0.5 * height),
        camera,
    )
    camera.offset = pr.Vector2(
        (1.0 - bbox.x) * 0.5 * width,
        (1.0 - bbox.y) * 0.5 * height,
    )

    if player.position.x < bbox_world_min.x:
        camera.target.x = player.position.x
    if player.position.y < bbox_world_min.y:
        camera.target.y = player.position.y
    if player.position.x > bbox_world_max.x:
        camera.target.x = bbox_world_min.x + (player.position.x - bbox_world_max.x)
    if player.position.y > bbox_world_max.y:
        camera.target.y = bbox_world_min.y + (player.position.y - bbox_world_max.y)


def main() -> None:
    """Run the 2D platformer with switchable camera behaviors."""
    pr.init_window(
        SCREEN_WIDTH,
        SCREEN_HEIGHT,
        "raylib [core] example - 2d camera platformer",
    )

    player = Player(position=pr.Vector2(400.0, 280.0), speed=0.0, can_jump=False)
    env_items = [
        EnvItem(pr.Rectangle(0.0, 0.0, 1000.0, 400.0), False, pr.LIGHTGRAY),
        EnvItem(pr.Rectangle(0.0, 400.0, 1000.0, 200.0), True, pr.GRAY),
        EnvItem(pr.Rectangle(300.0, 200.0, 400.0, 10.0), True, pr.GRAY),
        EnvItem(pr.Rectangle(250.0, 300.0, 100.0, 10.0), True, pr.GRAY),
        EnvItem(pr.Rectangle(650.0, 300.0, 100.0, 10.0), True, pr.GRAY),
    ]

    camera = pr.Camera2D(
        pr.Vector2(SCREEN_WIDTH / 2.0, SCREEN_HEIGHT / 2.0),
        pr.Vector2(player.position.x, player.position.y),
        0.0,
        1.0,
    )

    camera_descriptions = [
        "Follow player center",
        "Follow player center, but clamp to map edges",
        "Follow player center; smoothed",
        "Follow player center horizontally; update player center vertically after landing",
        "Player push camera on getting too close to screen edge",
    ]

    even_out_state = EvenOutState()

    camera_option = 0
    pr.set_target_fps(60)

    while not pr.window_should_close():
        delta_time = pr.get_frame_time()

        update_player(player, env_items, delta_time)

        camera.zoom += pr.get_mouse_wheel_move() * 0.05
        camera.zoom = max(0.25, min(3.0, camera.zoom))

        if pr.is_key_pressed(KEY_R):
            camera.zoom = 1.0
            player.position = pr.Vector2(400.0, 280.0)
            player.speed = 0.0
            player.can_jump = False

        if pr.is_key_pressed(KEY_C):
            camera_option = (camera_option + 1) % len(camera_descriptions)

        match camera_option:
            case 0:
                update_camera_center(
                    camera,
                    player,
                    env_items,
                    delta_time,
                    SCREEN_WIDTH,
                    SCREEN_HEIGHT,
                )
            case 1:
                update_camera_center_inside_map(
                    camera,
                    player,
                    env_items,
                    delta_time,
                    SCREEN_WIDTH,
                    SCREEN_HEIGHT,
                )
            case 2:
                update_camera_center_smooth_follow(
                    camera,
                    player,
                    env_items,
                    delta_time,
                    SCREEN_WIDTH,
                    SCREEN_HEIGHT,
                )
            case 3:
                update_camera_even_out_on_landing(
                    camera,
                    player,
                    env_items,
                    delta_time,
                    SCREEN_WIDTH,
                    SCREEN_HEIGHT,
                    even_out_state,
                )
            case _:
                update_camera_player_bounds_push(
                    camera,
                    player,
                    env_items,
                    delta_time,
                    SCREEN_WIDTH,
                    SCREEN_HEIGHT,
                )

        pr.begin_drawing()
        pr.clear_background(pr.LIGHTGRAY)

        pr.begin_mode_2d(camera)

        for item in env_items:
            pr.draw_rectangle_rec(item.rect, item.color)

        player_rect = pr.Rectangle(
            player.position.x - 20.0,
            player.position.y - 40.0,
            40.0,
            40.0,
        )
        pr.draw_rectangle_rec(player_rect, pr.RED)

        pr.draw_circle_v(player.position, 5.0, pr.GOLD)

        pr.end_mode_2d()

        pr.draw_text("Controls:", 20, 20, 10, pr.BLACK)
        pr.draw_text("- Right/Left to move", 40, 40, 10, pr.DARKGRAY)
        pr.draw_text("- Space to jump", 40, 60, 10, pr.DARKGRAY)
        pr.draw_text("- Mouse Wheel to Zoom in-out", 40, 80, 10, pr.DARKGRAY)
        pr.draw_text("- R to reset position + zoom", 40, 100, 10, pr.DARKGRAY)
        pr.draw_text("- C to change camera mode", 40, 120, 10, pr.DARKGRAY)
        pr.draw_text("Current camera mode:", 20, 140, 10, pr.BLACK)
        pr.draw_text(camera_descriptions[camera_option], 40, 160, 10, pr.DARKGRAY)

        pr.end_drawing()

    pr.close_window()


if __name__ == "__main__":
    main()
