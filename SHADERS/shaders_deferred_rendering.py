"""raylib [shaders] example - deferred rendering (Python port)."""

from __future__ import annotations

import random
from dataclasses import dataclass
from enum import IntEnum
from pathlib import Path

import glm
import pyray as pr

# Version checked: raylib 5.x/pyray API parity (reviewed 2026-02-28).

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 450
GLSL_VERSION = 330
MAX_CUBES = 30
MAX_LIGHTS = 4
LIGHT_POINT = 1
CUBE_SCALE = 0.25
DEPTH_BUFFER_BIT = 0x00000100

CAMERA_PERSPECTIVE = getattr(pr, "CAMERA_PERSPECTIVE", 0)
CAMERA_ORBITAL = getattr(pr, "CAMERA_ORBITAL", 2)
SHADER_LOC_VECTOR_VIEW = getattr(pr, "SHADER_LOC_VECTOR_VIEW", 11)
SHADER_UNIFORM_VEC3 = getattr(pr, "SHADER_UNIFORM_VEC3", 2)
SHADER_UNIFORM_VEC4 = getattr(pr, "SHADER_UNIFORM_VEC4", 3)
SHADER_UNIFORM_INT = getattr(pr, "SHADER_UNIFORM_INT", 4)
RL_SHADER_UNIFORM_SAMPLER2D = getattr(pr, "RL_SHADER_UNIFORM_SAMPLER2D", 12)
RL_PIXELFORMAT_UNCOMPRESSED_R16G16B16 = getattr(
    pr, "RL_PIXELFORMAT_UNCOMPRESSED_R16G16B16", 12
)
RL_PIXELFORMAT_UNCOMPRESSED_R8G8B8A8 = getattr(pr, "RL_PIXELFORMAT_UNCOMPRESSED_R8G8B8A8", 7)
RL_ATTACHMENT_COLOR_CHANNEL0 = getattr(pr, "RL_ATTACHMENT_COLOR_CHANNEL0", 0)
RL_ATTACHMENT_COLOR_CHANNEL1 = getattr(pr, "RL_ATTACHMENT_COLOR_CHANNEL1", 1)
RL_ATTACHMENT_COLOR_CHANNEL2 = getattr(pr, "RL_ATTACHMENT_COLOR_CHANNEL2", 2)
RL_ATTACHMENT_TEXTURE2D = getattr(pr, "RL_ATTACHMENT_TEXTURE2D", 100)
RL_ATTACHMENT_DEPTH = getattr(pr, "RL_ATTACHMENT_DEPTH", 100)
RL_ATTACHMENT_RENDERBUFFER = getattr(pr, "RL_ATTACHMENT_RENDERBUFFER", 200)
RL_READ_FRAMEBUFFER = getattr(pr, "RL_READ_FRAMEBUFFER", 36008)
RL_DRAW_FRAMEBUFFER = getattr(pr, "RL_DRAW_FRAMEBUFFER", 36009)
KEY_Y = getattr(pr, "KEY_Y", 89)
KEY_R = getattr(pr, "KEY_R", 82)
KEY_G = getattr(pr, "KEY_G", 71)
KEY_B = getattr(pr, "KEY_B", 66)
KEY_ONE = getattr(pr, "KEY_ONE", 49)
KEY_TWO = getattr(pr, "KEY_TWO", 50)
KEY_THREE = getattr(pr, "KEY_THREE", 51)
KEY_FOUR = getattr(pr, "KEY_FOUR", 52)
LOG_WARNING = getattr(pr, "LOG_WARNING", 2)


@dataclass
class GBuffer:
    """GPU handles used by deferred rendering."""

    framebuffer_id: int = 0
    position_texture_id: int = 0
    normal_texture_id: int = 0
    albedo_spec_texture_id: int = 0
    depth_renderbuffer_id: int = 0


@dataclass
class Light:
    """Deferred light state and cached uniform locations."""

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


class DeferredMode(IntEnum):
    """Debug/visualization pass selection."""

    POSITION = 0
    NORMAL = 1
    ALBEDO = 2
    SHADING = 3


def glm_to_pr_vec3(value: glm.vec3) -> pr.Vector3:
    """Convert a glm vec3 to pyray Vector3."""
    return pr.Vector3(float(value.x), float(value.y), float(value.z))


def create_debug_texture(texture_id: int, width: int, height: int, texture_format: int) -> pr.Texture2D:
    """Build a temporary texture view from a raw rlgl texture id."""
    texture = pr.Texture2D()
    texture.id = texture_id
    texture.width = width
    texture.height = height
    texture.mipmaps = 1
    texture.format = texture_format
    return texture


def create_light(
    index: int,
    light_type: int,
    position: glm.vec3,
    target: glm.vec3,
    color: pr.Color,
    shader: pr.Shader,
) -> Light:
    """Create a deferred light and cache its shader uniform locations."""
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
    """Send light data to deferred shader uniforms."""
    enabled_value = pr.ffi.new("int *", int(light.enabled))
    type_value = pr.ffi.new("int *", light.light_type)
    position_value = pr.ffi.new(
        "float[3]", [float(light.position.x), float(light.position.y), float(light.position.z)]
    )
    target_value = pr.ffi.new(
        "float[3]", [float(light.target.x), float(light.target.y), float(light.target.z)]
    )

    normalized = pr.color_normalize(light.color)
    color_value = pr.ffi.new("float[4]", [normalized.x, normalized.y, normalized.z, normalized.w])

    pr.set_shader_value(shader, light.enabled_loc, enabled_value, SHADER_UNIFORM_INT)
    pr.set_shader_value(shader, light.type_loc, type_value, SHADER_UNIFORM_INT)
    pr.set_shader_value(shader, light.position_loc, position_value, SHADER_UNIFORM_VEC3)
    pr.set_shader_value(shader, light.target_loc, target_value, SHADER_UNIFORM_VEC3)
    pr.set_shader_value(shader, light.color_loc, color_value, SHADER_UNIFORM_VEC4)


def init_gbuffer(width: int, height: int) -> GBuffer:
    """Create framebuffer and textures used by deferred rendering."""
    gbuffer = GBuffer()
    gbuffer.framebuffer_id = pr.rl_load_framebuffer()
    if gbuffer.framebuffer_id == 0:
        pr.trace_log(LOG_WARNING, "Failed to create framebufferId")

    pr.rl_enable_framebuffer(gbuffer.framebuffer_id)

    gbuffer.position_texture_id = pr.rl_load_texture(
        pr.ffi.NULL,
        width,
        height,
        RL_PIXELFORMAT_UNCOMPRESSED_R16G16B16,
        1,
    )
    gbuffer.normal_texture_id = pr.rl_load_texture(
        pr.ffi.NULL,
        width,
        height,
        RL_PIXELFORMAT_UNCOMPRESSED_R16G16B16,
        1,
    )
    gbuffer.albedo_spec_texture_id = pr.rl_load_texture(
        pr.ffi.NULL,
        width,
        height,
        RL_PIXELFORMAT_UNCOMPRESSED_R8G8B8A8,
        1,
    )

    pr.rl_active_draw_buffers(3)
    pr.rl_framebuffer_attach(
        gbuffer.framebuffer_id,
        gbuffer.position_texture_id,
        RL_ATTACHMENT_COLOR_CHANNEL0,
        RL_ATTACHMENT_TEXTURE2D,
        0,
    )
    pr.rl_framebuffer_attach(
        gbuffer.framebuffer_id,
        gbuffer.normal_texture_id,
        RL_ATTACHMENT_COLOR_CHANNEL1,
        RL_ATTACHMENT_TEXTURE2D,
        0,
    )
    pr.rl_framebuffer_attach(
        gbuffer.framebuffer_id,
        gbuffer.albedo_spec_texture_id,
        RL_ATTACHMENT_COLOR_CHANNEL2,
        RL_ATTACHMENT_TEXTURE2D,
        0,
    )

    gbuffer.depth_renderbuffer_id = pr.rl_load_texture_depth(width, height, True)
    pr.rl_framebuffer_attach(
        gbuffer.framebuffer_id,
        gbuffer.depth_renderbuffer_id,
        RL_ATTACHMENT_DEPTH,
        RL_ATTACHMENT_RENDERBUFFER,
        0,
    )

    if not pr.rl_framebuffer_complete(gbuffer.framebuffer_id):
        pr.trace_log(LOG_WARNING, "Framebuffer is not complete")

    return gbuffer


def draw_scene(
    model: pr.Model,
    cube: pr.Model,
    cube_positions: list[glm.vec3],
    cube_rotations: list[float],
) -> None:
    """Render all geometry for G-buffer and forward overlay passes."""
    pr.draw_model(model, pr.Vector3(0.0, 0.0, 0.0), 1.0, pr.WHITE)
    pr.draw_model(cube, pr.Vector3(0.0, 1.0, 0.0), 1.0, pr.WHITE)

    for index in range(MAX_CUBES):
        pr.draw_model_ex(
            cube,
            glm_to_pr_vec3(cube_positions[index]),
            pr.Vector3(1.0, 1.0, 1.0),
            cube_rotations[index],
            pr.Vector3(CUBE_SCALE, CUBE_SCALE, CUBE_SCALE),
            pr.WHITE,
        )


def main() -> None:
    """Run the deferred rendering demo."""
    pr.init_window(
        SCREEN_WIDTH, SCREEN_HEIGHT, "raylib [shaders] example - deferred rendering"
    )

    resources = Path(__file__).resolve().parent / "resources"
    shader_dir = resources / "shaders" / f"glsl{GLSL_VERSION}"

    camera = pr.Camera3D(
        pr.Vector3(5.0, 4.0, 5.0),
        pr.Vector3(0.0, 1.0, 0.0),
        pr.Vector3(0.0, 1.0, 0.0),
        60.0,
        CAMERA_PERSPECTIVE,
    )

    model = pr.load_model_from_mesh(pr.gen_mesh_plane(10.0, 10.0, 3, 3))
    cube = pr.load_model_from_mesh(pr.gen_mesh_cube(2.0, 2.0, 2.0))

    gbuffer_shader = pr.load_shader(
        str(shader_dir / "gbuffer.vs"),
        str(shader_dir / "gbuffer.fs"),
    )
    deferred_shader = pr.load_shader(
        str(shader_dir / "deferred_shading.vs"),
        str(shader_dir / "deferred_shading.fs"),
    )
    deferred_shader.locs[SHADER_LOC_VECTOR_VIEW] = pr.get_shader_location(
        deferred_shader, "viewPosition"
    )

    gbuffer = init_gbuffer(SCREEN_WIDTH, SCREEN_HEIGHT)

    pr.rl_enable_shader(deferred_shader.id)
    tex_unit_position = 0
    tex_unit_normal = 1
    tex_unit_albedo_spec = 2
    g_position_loc = pr.rl_get_location_uniform(deferred_shader.id, "gPosition")
    g_normal_loc = pr.rl_get_location_uniform(deferred_shader.id, "gNormal")
    g_albedo_spec_loc = pr.rl_get_location_uniform(deferred_shader.id, "gAlbedoSpec")
    pr.set_shader_value(
        deferred_shader,
        g_position_loc,
        pr.ffi.new("int *", tex_unit_position),
        RL_SHADER_UNIFORM_SAMPLER2D,
    )
    pr.set_shader_value(
        deferred_shader,
        g_normal_loc,
        pr.ffi.new("int *", tex_unit_normal),
        RL_SHADER_UNIFORM_SAMPLER2D,
    )
    pr.set_shader_value(
        deferred_shader,
        g_albedo_spec_loc,
        pr.ffi.new("int *", tex_unit_albedo_spec),
        RL_SHADER_UNIFORM_SAMPLER2D,
    )
    pr.rl_disable_shader()

    model.materials[0].shader = gbuffer_shader
    cube.materials[0].shader = gbuffer_shader

    lights = [
        create_light(
            0, LIGHT_POINT, glm.vec3(-2.0, 1.0, -2.0), glm.vec3(0.0, 0.0, 0.0), pr.YELLOW, deferred_shader
        ),
        create_light(
            1, LIGHT_POINT, glm.vec3(2.0, 1.0, 2.0), glm.vec3(0.0, 0.0, 0.0), pr.RED, deferred_shader
        ),
        create_light(
            2, LIGHT_POINT, glm.vec3(-2.0, 1.0, 2.0), glm.vec3(0.0, 0.0, 0.0), pr.GREEN, deferred_shader
        ),
        create_light(
            3, LIGHT_POINT, glm.vec3(2.0, 1.0, -2.0), glm.vec3(0.0, 0.0, 0.0), pr.BLUE, deferred_shader
        ),
    ]

    cube_positions: list[glm.vec3] = []
    cube_rotations: list[float] = []
    for _ in range(MAX_CUBES):
        cube_positions.append(
            glm.vec3(float(random.randrange(10) - 5), float(random.randrange(5)), float(random.randrange(10) - 5))
        )
        cube_rotations.append(float(random.randrange(360)))

    mode = DeferredMode.SHADING

    position_texture = create_debug_texture(
        gbuffer.position_texture_id,
        SCREEN_WIDTH,
        SCREEN_HEIGHT,
        RL_PIXELFORMAT_UNCOMPRESSED_R16G16B16,
    )
    normal_texture = create_debug_texture(
        gbuffer.normal_texture_id,
        SCREEN_WIDTH,
        SCREEN_HEIGHT,
        RL_PIXELFORMAT_UNCOMPRESSED_R16G16B16,
    )
    albedo_texture = create_debug_texture(
        gbuffer.albedo_spec_texture_id,
        SCREEN_WIDTH,
        SCREEN_HEIGHT,
        RL_PIXELFORMAT_UNCOMPRESSED_R8G8B8A8,
    )

    pr.rl_enable_depth_test()
    pr.set_target_fps(60)

    while not pr.window_should_close():
        pr.update_camera(camera, CAMERA_ORBITAL)

        camera_pos_uniform = pr.ffi.new(
            "float[3]", [camera.position.x, camera.position.y, camera.position.z]
        )
        pr.set_shader_value(
            deferred_shader,
            deferred_shader.locs[SHADER_LOC_VECTOR_VIEW],
            camera_pos_uniform,
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

        if pr.is_key_pressed(KEY_ONE):
            mode = DeferredMode.POSITION
        if pr.is_key_pressed(KEY_TWO):
            mode = DeferredMode.NORMAL
        if pr.is_key_pressed(KEY_THREE):
            mode = DeferredMode.ALBEDO
        if pr.is_key_pressed(KEY_FOUR):
            mode = DeferredMode.SHADING

        for light in lights:
            update_light_values(deferred_shader, light)

        pr.begin_drawing()

        pr.rl_enable_framebuffer(gbuffer.framebuffer_id)
        pr.rl_clear_color(0, 0, 0, 0)
        pr.rl_clear_screen_buffers()
        pr.rl_disable_color_blend()

        pr.begin_mode_3d(camera)
        pr.rl_enable_shader(gbuffer_shader.id)
        draw_scene(model, cube, cube_positions, cube_rotations)
        pr.rl_disable_shader()
        pr.end_mode_3d()

        pr.rl_enable_color_blend()
        pr.rl_disable_framebuffer()
        pr.rl_clear_screen_buffers()

        match mode:
            case DeferredMode.SHADING:
                pr.begin_mode_3d(camera)
                pr.rl_disable_color_blend()
                pr.rl_enable_shader(deferred_shader.id)

                pr.rl_active_texture_slot(tex_unit_position)
                pr.rl_enable_texture(gbuffer.position_texture_id)
                pr.rl_active_texture_slot(tex_unit_normal)
                pr.rl_enable_texture(gbuffer.normal_texture_id)
                pr.rl_active_texture_slot(tex_unit_albedo_spec)
                pr.rl_enable_texture(gbuffer.albedo_spec_texture_id)
                pr.rl_load_draw_quad()

                pr.rl_disable_shader()
                pr.rl_enable_color_blend()
                pr.end_mode_3d()

                pr.rl_bind_framebuffer(RL_READ_FRAMEBUFFER, gbuffer.framebuffer_id)
                pr.rl_bind_framebuffer(RL_DRAW_FRAMEBUFFER, 0)
                pr.rl_blit_framebuffer(
                    0,
                    0,
                    SCREEN_WIDTH,
                    SCREEN_HEIGHT,
                    0,
                    0,
                    SCREEN_WIDTH,
                    SCREEN_HEIGHT,
                    DEPTH_BUFFER_BIT,
                )
                pr.rl_disable_framebuffer()

                pr.begin_mode_3d(camera)
                pr.rl_enable_shader(pr.rl_get_shader_id_default())
                for light in lights:
                    light_position = glm_to_pr_vec3(light.position)
                    if light.enabled:
                        pr.draw_sphere_ex(light_position, 0.2, 8, 8, light.color)
                    else:
                        pr.draw_sphere_wires(
                            light_position,
                            0.2,
                            8,
                            8,
                            pr.color_alpha(light.color, 0.3),
                        )
                pr.rl_disable_shader()
                pr.end_mode_3d()

                pr.draw_text("FINAL RESULT", 10, SCREEN_HEIGHT - 30, 20, pr.DARKGREEN)
            case DeferredMode.POSITION:
                pr.draw_texture_rec(
                    position_texture,
                    pr.Rectangle(0.0, 0.0, float(SCREEN_WIDTH), -float(SCREEN_HEIGHT)),
                    pr.Vector2(0.0, 0.0),
                    pr.RAYWHITE,
                )
                pr.draw_text("POSITION TEXTURE", 10, SCREEN_HEIGHT - 30, 20, pr.DARKGREEN)
            case DeferredMode.NORMAL:
                pr.draw_texture_rec(
                    normal_texture,
                    pr.Rectangle(0.0, 0.0, float(SCREEN_WIDTH), -float(SCREEN_HEIGHT)),
                    pr.Vector2(0.0, 0.0),
                    pr.RAYWHITE,
                )
                pr.draw_text("NORMAL TEXTURE", 10, SCREEN_HEIGHT - 30, 20, pr.DARKGREEN)
            case DeferredMode.ALBEDO:
                pr.draw_texture_rec(
                    albedo_texture,
                    pr.Rectangle(0.0, 0.0, float(SCREEN_WIDTH), -float(SCREEN_HEIGHT)),
                    pr.Vector2(0.0, 0.0),
                    pr.RAYWHITE,
                )
                pr.draw_text("ALBEDO TEXTURE", 10, SCREEN_HEIGHT - 30, 20, pr.DARKGREEN)

        pr.draw_text("Toggle lights keys: [Y][R][G][B]", 10, 40, 20, pr.DARKGRAY)
        pr.draw_text("Switch G-buffer textures: [1][2][3][4]", 10, 70, 20, pr.DARKGRAY)
        pr.draw_fps(10, 10)

        pr.end_drawing()

    pr.unload_model(model)
    pr.unload_model(cube)
    pr.unload_shader(deferred_shader)
    pr.unload_shader(gbuffer_shader)

    pr.rl_unload_framebuffer(gbuffer.framebuffer_id)
    pr.rl_unload_texture(gbuffer.position_texture_id)
    pr.rl_unload_texture(gbuffer.normal_texture_id)
    pr.rl_unload_texture(gbuffer.albedo_spec_texture_id)
    pr.rl_unload_texture(gbuffer.depth_renderbuffer_id)

    pr.close_window()


if __name__ == "__main__":
    main()
