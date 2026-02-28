from __future__ import annotations

import math
from dataclasses import dataclass, field

import pyray as pr

# Version checked: raylib 5.x/pyray API parity (reviewed 2026-02-28).

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 450

GRAVITY = 32.0
MAX_SPEED = 20.0
CROUCH_SPEED = 5.0
JUMP_FORCE = 12.0
MAX_ACCEL = 150.0
FRICTION = 0.86
AIR_DRAG = 0.98
CONTROL = 15.0
CROUCH_HEIGHT = 0.0
STAND_HEIGHT = 1.0
BOTTOM_HEIGHT = 0.5
NORMALIZE_INPUT = True
PI = float(getattr(pr, "PI", math.pi))
CAMERA_PERSPECTIVE = int(getattr(pr, "CAMERA_PERSPECTIVE", 0))

KEY_A = getattr(pr, "KEY_A", 65)
KEY_D = getattr(pr, "KEY_D", 68)
KEY_S = getattr(pr, "KEY_S", 83)
KEY_W = getattr(pr, "KEY_W", 87)
KEY_SPACE = getattr(pr, "KEY_SPACE", 32)
KEY_LEFT_CONTROL = getattr(pr, "KEY_LEFT_CONTROL", 341)


@dataclass
class Body:
    """Represent player body physics state."""

    position: pr.Vector3 = field(default_factory=lambda: pr.Vector3(0.0, 0.0, 0.0))
    velocity: pr.Vector3 = field(default_factory=lambda: pr.Vector3(0.0, 0.0, 0.0))
    direction: pr.Vector3 = field(default_factory=lambda: pr.Vector3(0.0, 0.0, 0.0))
    is_grounded: bool = False


@dataclass
class FpsState:
    """Store camera and animation state for FPS movement."""

    sensitivity: pr.Vector2 = field(default_factory=lambda: pr.Vector2(0.001, 0.001))
    look_rotation: pr.Vector2 = field(default_factory=lambda: pr.Vector2(0.0, 0.0))
    head_timer: float = 0.0
    walk_lerp: float = 0.0
    head_lerp: float = STAND_HEIGHT
    lean: pr.Vector2 = field(default_factory=lambda: pr.Vector2(0.0, 0.0))
    player: Body = field(default_factory=Body)


def update_body(
    body: Body,
    rot: float,
    side: int,
    forward: int,
    jump_pressed: bool,
    crouch_hold: bool,
) -> None:
    """Update body movement and simple floor collision."""
    input_direction = pr.Vector2(float(side), float(-forward))

    if NORMALIZE_INPUT and side != 0 and forward != 0:
        input_direction = pr.vector2_normalize(input_direction)

    delta = pr.get_frame_time()

    if not body.is_grounded:
        body.velocity.y -= GRAVITY * delta

    if body.is_grounded and jump_pressed:
        body.velocity.y = JUMP_FORCE
        body.is_grounded = False

    front = pr.Vector3(math.sin(rot), 0.0, math.cos(rot))
    right = pr.Vector3(math.cos(-rot), 0.0, math.sin(-rot))

    desired_direction = pr.Vector3(
        input_direction.x * right.x + input_direction.y * front.x,
        0.0,
        input_direction.x * right.z + input_direction.y * front.z,
    )
    body.direction = pr.vector3_lerp(body.direction, desired_direction, CONTROL * delta)

    decel = FRICTION if body.is_grounded else AIR_DRAG
    horizontal_velocity = pr.Vector3(
        body.velocity.x * decel,
        0.0,
        body.velocity.z * decel,
    )

    if pr.vector3_length(horizontal_velocity) < (MAX_SPEED * 0.01):
        horizontal_velocity = pr.Vector3(0.0, 0.0, 0.0)

    speed = pr.vector3_dot_product(horizontal_velocity, body.direction)

    max_speed = CROUCH_SPEED if crouch_hold else MAX_SPEED
    acceleration = pr.clamp(max_speed - speed, 0.0, MAX_ACCEL * delta)
    horizontal_velocity.x += body.direction.x * acceleration
    horizontal_velocity.z += body.direction.z * acceleration

    body.velocity.x = horizontal_velocity.x
    body.velocity.z = horizontal_velocity.z

    body.position.x += body.velocity.x * delta
    body.position.y += body.velocity.y * delta
    body.position.z += body.velocity.z * delta

    if body.position.y <= 0.0:
        body.position.y = 0.0
        body.velocity.y = 0.0
        body.is_grounded = True


def update_camera_fps(camera: pr.Camera3D, state: FpsState) -> None:
    """Update FPS camera orientation, bobbing, and target."""
    up = pr.Vector3(0.0, 1.0, 0.0)
    target_offset = pr.Vector3(0.0, 0.0, -1.0)

    yaw = pr.vector3_rotate_by_axis_angle(target_offset, up, state.look_rotation.x)

    max_angle_up = pr.vector3_angle(up, yaw) - 0.001
    if -state.look_rotation.y > max_angle_up:
        state.look_rotation.y = -max_angle_up

    max_angle_down = pr.vector3_angle(pr.vector3_negate(up), yaw)
    max_angle_down = max_angle_down * -1.0 + 0.001
    if -state.look_rotation.y < max_angle_down:
        state.look_rotation.y = -max_angle_down

    right = pr.vector3_normalize(pr.vector3_cross_product(yaw, up))

    pitch_angle = -state.look_rotation.y - state.lean.y
    pitch_angle = pr.clamp(pitch_angle, -PI / 2 + 0.0001, PI / 2 - 0.0001)
    pitch = pr.vector3_rotate_by_axis_angle(yaw, right, pitch_angle)

    head_sin = math.sin(state.head_timer * PI)
    head_cos = math.cos(state.head_timer * PI)
    step_rotation = 0.01
    camera.up = pr.vector3_rotate_by_axis_angle(
        up, pitch, head_sin * step_rotation + state.lean.x
    )

    bob_side = 0.1
    bob_up = 0.15
    bobbing = pr.vector3_scale(right, head_sin * bob_side)
    bobbing.y = abs(head_cos * bob_up)

    camera.position = pr.vector3_add(
        camera.position, pr.vector3_scale(bobbing, state.walk_lerp)
    )
    camera.target = pr.vector3_add(camera.position, pitch)


def draw_level() -> None:
    """Draw tiled floor, towers, and sun geometry."""
    floor_extent = 25
    tile_size = 5.0
    tile_color_1 = pr.Color(150, 200, 200, 255)

    for y in range(-floor_extent, floor_extent):
        for x in range(-floor_extent, floor_extent):
            position = pr.Vector3(float(x) * tile_size, 0.0, float(y) * tile_size)
            size = pr.Vector2(tile_size, tile_size)
            if (y & 1) and (x & 1):
                pr.draw_plane(position, size, tile_color_1)
            elif not (y & 1) and not (x & 1):
                pr.draw_plane(position, size, pr.LIGHTGRAY)

    tower_size = pr.Vector3(16.0, 32.0, 16.0)
    tower_color = pr.Color(150, 200, 200, 255)

    tower_pos = pr.Vector3(16.0, 16.0, 16.0)
    pr.draw_cube_v(tower_pos, tower_size, tower_color)
    pr.draw_cube_wires_v(tower_pos, tower_size, pr.DARKBLUE)

    tower_pos.x *= -1.0
    pr.draw_cube_v(tower_pos, tower_size, tower_color)
    pr.draw_cube_wires_v(tower_pos, tower_size, pr.DARKBLUE)

    tower_pos.z *= -1.0
    pr.draw_cube_v(tower_pos, tower_size, tower_color)
    pr.draw_cube_wires_v(tower_pos, tower_size, pr.DARKBLUE)

    tower_pos.x *= -1.0
    pr.draw_cube_v(tower_pos, tower_size, tower_color)
    pr.draw_cube_wires_v(tower_pos, tower_size, pr.DARKBLUE)

    pr.draw_sphere(pr.Vector3(300.0, 300.0, 0.0), 100.0, pr.Color(255, 0, 0, 255))


def main() -> None:
    """Run the FPS 3D camera example."""
    pr.init_window(SCREEN_WIDTH, SCREEN_HEIGHT, "raylib [core] example - 3d camera fps")

    state = FpsState()

    camera = pr.Camera3D(
        pr.Vector3(
            state.player.position.x,
            state.player.position.y + (BOTTOM_HEIGHT + state.head_lerp),
            state.player.position.z,
        ),
        pr.Vector3(0.0, 0.0, -1.0),
        pr.Vector3(0.0, 1.0, 0.0),
        60.0,
        CAMERA_PERSPECTIVE,
    )

    update_camera_fps(camera, state)

    pr.disable_cursor()
    pr.set_target_fps(60)

    while not pr.window_should_close():
        mouse_delta = pr.get_mouse_delta()
        state.look_rotation.x -= mouse_delta.x * state.sensitivity.x
        state.look_rotation.y += mouse_delta.y * state.sensitivity.y

        sideway = int(pr.is_key_down(KEY_D)) - int(pr.is_key_down(KEY_A))
        forward = int(pr.is_key_down(KEY_W)) - int(pr.is_key_down(KEY_S))
        crouching = pr.is_key_down(KEY_LEFT_CONTROL)

        update_body(
            state.player,
            state.look_rotation.x,
            sideway,
            forward,
            pr.is_key_pressed(KEY_SPACE),
            crouching,
        )

        delta = pr.get_frame_time()
        target_head = CROUCH_HEIGHT if crouching else STAND_HEIGHT
        state.head_lerp = pr.lerp(state.head_lerp, target_head, 20.0 * delta)

        camera.position = pr.Vector3(
            state.player.position.x,
            state.player.position.y + (BOTTOM_HEIGHT + state.head_lerp),
            state.player.position.z,
        )

        if state.player.is_grounded and (forward != 0 or sideway != 0):
            state.head_timer += delta * 3.0
            state.walk_lerp = pr.lerp(state.walk_lerp, 1.0, 10.0 * delta)
            camera.fovy = pr.lerp(camera.fovy, 55.0, 5.0 * delta)
        else:
            state.walk_lerp = pr.lerp(state.walk_lerp, 0.0, 10.0 * delta)
            camera.fovy = pr.lerp(camera.fovy, 60.0, 5.0 * delta)

        state.lean.x = pr.lerp(state.lean.x, sideway * 0.02, 10.0 * delta)
        state.lean.y = pr.lerp(state.lean.y, forward * 0.015, 10.0 * delta)

        update_camera_fps(camera, state)

        pr.begin_drawing()
        pr.clear_background(pr.RAYWHITE)

        pr.begin_mode_3d(camera)
        draw_level()
        pr.end_mode_3d()

        pr.draw_rectangle(5, 5, 330, 90, pr.fade(pr.SKYBLUE, 0.5))
        pr.draw_rectangle_lines(5, 5, 330, 90, pr.BLUE)

        velocity_len = pr.vector2_length(
            pr.Vector2(state.player.velocity.x, state.player.velocity.z)
        )

        pr.draw_text("Camera controls:", 15, 15, 10, pr.BLACK)
        pr.draw_text("- Move keys: W, A, S, D, Space, Left-Ctrl", 15, 30, 10, pr.BLACK)
        pr.draw_text("- Look around: arrow keys or mouse", 15, 45, 10, pr.BLACK)
        pr.draw_text(f"- Velocity Len: ({velocity_len:06.3f})", 15, 60, 10, pr.BLACK)
        pr.draw_text(f"FPS: {pr.get_fps()}", 15, 75, 10, pr.BLACK)

        pr.end_drawing()

    pr.close_window()


if __name__ == "__main__":
    main()
