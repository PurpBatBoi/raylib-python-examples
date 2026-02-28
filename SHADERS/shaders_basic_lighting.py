from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

import glm
import pyray as pr

# Version checked: raylib 5.x/pyray API parity (reviewed 2026-02-28).

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 450
GLSL_VERSION = 330
MAX_LIGHTS = 4
LIGHT_POINT = 1

FLAG_MSAA_4X_HINT = getattr(pr, "FLAG_MSAA_4X_HINT", 32)
CAMERA_PERSPECTIVE = getattr(pr, "CAMERA_PERSPECTIVE", 0)
CAMERA_ORBITAL = getattr(pr, "CAMERA_ORBITAL", 2)
SHADER_LOC_VECTOR_VIEW = getattr(pr, "SHADER_LOC_VECTOR_VIEW", 11)
SHADER_UNIFORM_VEC3 = getattr(pr, "SHADER_UNIFORM_VEC3", 2)
SHADER_UNIFORM_VEC4 = getattr(pr, "SHADER_UNIFORM_VEC4", 3)
SHADER_UNIFORM_INT = getattr(pr, "SHADER_UNIFORM_INT", 4)

KEY_Y = getattr(pr, "KEY_Y", 89)
KEY_R = getattr(pr, "KEY_R", 82)
KEY_G = getattr(pr, "KEY_G", 71)
KEY_B = getattr(pr, "KEY_B", 66)


@dataclass
class Light:
    """Point-light state and its cached shader uniform locations."""

    light_type: int
    enabled: bool
    position: glm.vec3
    target: glm.vec3
    color: pr.Color
    enabled_loc: int
    type_loc: int
    position_loc: int
    target_loc: int
    color_loc: int


def glm_to_pr_vec3(value: glm.vec3) -> pr.Vector3:
    """Convert glm vec3 values to pyray Vector3."""
    return pr.Vector3(float(value.x), float(value.y), float(value.z))


def create_light(
    index: int,
    light_type: int,
    position: glm.vec3,
    target: glm.vec3,
    color: pr.Color,
    shader: pr.Shader,
) -> Light:
    """Create a light and cache all related uniform locations."""
    light = Light(
        light_type=light_type,
        enabled=True,
        position=position,
        target=target,
        color=color,
        enabled_loc=pr.get_shader_location(shader, f"lights[{index}].enabled"),
        type_loc=pr.get_shader_location(shader, f"lights[{index}].type"),
        position_loc=pr.get_shader_location(shader, f"lights[{index}].position"),
        target_loc=pr.get_shader_location(shader, f"lights[{index}].target"),
        color_loc=pr.get_shader_location(shader, f"lights[{index}].color"),
    )
    update_light_values(shader, light)
    return light


def update_light_values(shader: pr.Shader, light: Light) -> None:
    """Upload a light's values to shader uniforms."""
    enabled_uniform = pr.ffi.new("int *", int(light.enabled))
    type_uniform = pr.ffi.new("int *", light.light_type)
    position_uniform = pr.ffi.new(
        "float[3]",
        [float(light.position.x), float(light.position.y), float(light.position.z)],
    )
    target_uniform = pr.ffi.new(
        "float[3]",
        [float(light.target.x), float(light.target.y), float(light.target.z)],
    )

    normalized = pr.color_normalize(light.color)
    color_uniform = pr.ffi.new(
        "float[4]", [normalized.x, normalized.y, normalized.z, normalized.w]
    )

    pr.set_shader_value(shader, light.enabled_loc, enabled_uniform, SHADER_UNIFORM_INT)
    pr.set_shader_value(shader, light.type_loc, type_uniform, SHADER_UNIFORM_INT)
    pr.set_shader_value(
        shader, light.position_loc, position_uniform, SHADER_UNIFORM_VEC3
    )
    pr.set_shader_value(shader, light.target_loc, target_uniform, SHADER_UNIFORM_VEC3)
    pr.set_shader_value(shader, light.color_loc, color_uniform, SHADER_UNIFORM_VEC4)


def main() -> None:
    """Run the basic lighting shader example."""
    pr.set_config_flags(FLAG_MSAA_4X_HINT)
    pr.init_window(
        SCREEN_WIDTH,
        SCREEN_HEIGHT,
        "raylib [shaders] example - basic lighting",
    )

    resources = Path(__file__).resolve().parent / "resources"
    shader_dir = resources / "shaders" / f"glsl{GLSL_VERSION}"

    camera_position = glm.vec3(2.0, 4.0, 6.0)
    camera_target = glm.vec3(0.0, 0.5, 0.0)

    camera = pr.Camera3D(
        glm_to_pr_vec3(camera_position),
        glm_to_pr_vec3(camera_target),
        pr.Vector3(0.0, 1.0, 0.0),
        45.0,
        CAMERA_PERSPECTIVE,
    )

    shader = pr.load_shader(
        str(shader_dir / "lighting.vs"),
        str(shader_dir / "lighting.fs"),
    )
    shader.locs[SHADER_LOC_VECTOR_VIEW] = pr.get_shader_location(shader, "viewPos")

    ambient_loc = pr.get_shader_location(shader, "ambient")
    ambient_uniform = pr.ffi.new("float[4]", [0.1, 0.1, 0.1, 1.0])
    pr.set_shader_value(shader, ambient_loc, ambient_uniform, SHADER_UNIFORM_VEC4)

    lights: list[Light] = [
        create_light(
            0,
            LIGHT_POINT,
            glm.vec3(-2.0, 1.0, -2.0),
            glm.vec3(0.0, 0.0, 0.0),
            pr.YELLOW,
            shader,
        ),
        create_light(
            1,
            LIGHT_POINT,
            glm.vec3(2.0, 1.0, 2.0),
            glm.vec3(0.0, 0.0, 0.0),
            pr.RED,
            shader,
        ),
        create_light(
            2,
            LIGHT_POINT,
            glm.vec3(-2.0, 1.0, 2.0),
            glm.vec3(0.0, 0.0, 0.0),
            pr.GREEN,
            shader,
        ),
        create_light(
            3,
            LIGHT_POINT,
            glm.vec3(2.0, 1.0, -2.0),
            glm.vec3(0.0, 0.0, 0.0),
            pr.BLUE,
            shader,
        ),
    ]

    pr.set_target_fps(60)

    while not pr.window_should_close():
        pr.update_camera(camera, CAMERA_ORBITAL)

        view_pos_uniform = pr.ffi.new(
            "float[3]", [camera.position.x, camera.position.y, camera.position.z]
        )
        pr.set_shader_value(
            shader,
            shader.locs[SHADER_LOC_VECTOR_VIEW],
            view_pos_uniform,
            SHADER_UNIFORM_VEC3,
        )

        if pr.is_key_pressed(KEY_Y):
            lights[0].enabled = not lights[0].enabled
        if pr.is_key_pressed(KEY_R):
            lights[1].enabled = not lights[1].enabled
        if pr.is_key_pressed(KEY_G):
            lights[2].enabled = not lights[2].enabled
        if pr.is_key_pressed(KEY_B):
            lights[3].enabled = not lights[3].enabled

        for index in range(MAX_LIGHTS):
            update_light_values(shader, lights[index])

        pr.begin_drawing()
        pr.clear_background(pr.RAYWHITE)

        pr.begin_mode_3d(camera)
        pr.begin_shader_mode(shader)

        pr.draw_plane(pr.Vector3(0.0, 0.0, 0.0), pr.Vector2(10.0, 10.0), pr.WHITE)
        pr.draw_cube(pr.Vector3(0.0, 0.0, 0.0), 2.0, 4.0, 2.0, pr.WHITE)

        pr.end_shader_mode()

        for light in lights:
            if light.enabled:
                pr.draw_sphere_ex(
                    glm_to_pr_vec3(light.position), 0.2, 8, 8, light.color
                )
            else:
                pr.draw_sphere_wires(
                    glm_to_pr_vec3(light.position),
                    0.2,
                    8,
                    8,
                    pr.fade(light.color, 0.3),
                )

        pr.draw_grid(10, 1.0)
        pr.end_mode_3d()

        pr.draw_fps(10, 10)
        pr.draw_text("Use keys [Y][R][G][B] to toggle lights", 10, 40, 20, pr.DARKGRAY)

        pr.end_drawing()

    pr.unload_shader(shader)
    pr.close_window()


if __name__ == "__main__":
    main()
