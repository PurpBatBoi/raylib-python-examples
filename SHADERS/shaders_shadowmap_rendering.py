from __future__ import annotations

from pathlib import Path
from typing import Any

import glm
import pyray as pr

# Version checked: raylib 5.x/pyray API parity (reviewed 2026-02-28).

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 450
SHADOWMAP_RESOLUTION = 1024

# GLSL version for desktop, 330 is safe on PC.  Substitute 100 for Web/Android.
GLSL_VERSION = 330

FLAG_MSAA_4X_HINT = getattr(pr, "FLAG_MSAA_4X_HINT", 32)
KEY_LEFT = getattr(pr, "KEY_LEFT", 263)
KEY_RIGHT = getattr(pr, "KEY_RIGHT", 262)
KEY_UP = getattr(pr, "KEY_UP", 265)
KEY_DOWN = getattr(pr, "KEY_DOWN", 264)
KEY_F = getattr(pr, "KEY_F", 70)

# constants that are not statically visible to mypy
RL_ATTACHMENT_DEPTH = getattr(pr, "RL_ATTACHMENT_DEPTH", 0)
RL_ATTACHMENT_TEXTURE2D = getattr(pr, "RL_ATTACHMENT_TEXTURE2D", 0)
LOG_INFO = getattr(pr, "LOG_INFO", 0)
LOG_WARNING = getattr(pr, "LOG_WARNING", 0)

CAMERA_PERSPECTIVE = getattr(pr, "CAMERA_PERSPECTIVE", 0)
CAMERA_ORTHOGRAPHIC = getattr(pr, "CAMERA_ORTHOGRAPHIC", 1)
CAMERA_ORBITAL = getattr(pr, "CAMERA_ORBITAL", 2)

SHADER_LOC_VECTOR_VIEW = getattr(pr, "SHADER_LOC_VECTOR_VIEW", 0)
SHADER_UNIFORM_VEC3 = getattr(pr, "SHADER_UNIFORM_VEC3", 0)
SHADER_UNIFORM_VEC4 = getattr(pr, "SHADER_UNIFORM_VEC4", 0)
SHADER_UNIFORM_INT = getattr(pr, "SHADER_UNIFORM_INT", 0)


def load_shadowmap_render_texture(width: int, height: int) -> pr.RenderTexture:
    """Create a depth-only render texture for shadow map generation."""
    target = pr.RenderTexture()

    target.id = pr.rl_load_framebuffer()
    target.texture.width = width
    target.texture.height = height

    if target.id > 0:
        pr.rl_enable_framebuffer(target.id)

        target.depth.id = pr.rl_load_texture_depth(width, height, False)
        target.depth.width = width
        target.depth.height = height
        target.depth.format = 19
        target.depth.mipmaps = 1

        pr.rl_framebuffer_attach(
            target.id,
            target.depth.id,
            RL_ATTACHMENT_DEPTH,
            RL_ATTACHMENT_TEXTURE2D,
            0,
        )
        if pr.rl_framebuffer_complete(target.id):
            pr.trace_log(
                LOG_INFO,
                f"FBO: [ID {target.id}] Framebuffer object created successfully",
            )

        pr.rl_disable_framebuffer()
    else:
        pr.trace_log(LOG_WARNING, "FBO: Framebuffer object can not be created")

    return target


def unload_shadowmap_render_texture(target: pr.RenderTexture) -> None:
    """Release shadow map framebuffer resources from VRAM."""
    if target.id > 0:
        pr.rl_unload_framebuffer(target.id)


def draw_scene(cube: pr.Model, robot: pr.Model) -> None:
    """Draw the scene geometry used for both depth and color passes."""
    pr.draw_model_ex(
        cube,
        pr.Vector3(0.0, 0.0, 0.0),
        pr.Vector3(0.0, 1.0, 0.0),
        0.0,
        pr.Vector3(10.0, 1.0, 10.0),
        pr.BLUE,
    )
    pr.draw_model_ex(
        cube,
        pr.Vector3(1.5, 1.0, -1.5),
        pr.Vector3(0.0, 1.0, 0.0),
        0.0,
        pr.Vector3(1.0, 1.0, 1.0),
        pr.WHITE,
    )
    pr.draw_model_ex(
        robot,
        pr.Vector3(0.0, 0.5, 0.0),
        pr.Vector3(0.0, 1.0, 0.0),
        0.0,
        pr.Vector3(1.0, 1.0, 1.0),
        pr.RED,
    )


def glm_to_pr_vec3(value: glm.vec3) -> pr.Vector3:
    """Convert glm vec3 to pyray Vector3."""
    return pr.Vector3(float(value.x), float(value.y), float(value.z))


def main() -> None:
    """Run the shadow-map rendering example."""
    pr.set_config_flags(FLAG_MSAA_4X_HINT)
    pr.init_window(
        SCREEN_WIDTH,
        SCREEN_HEIGHT,
        "raylib [shaders] example - shadowmap rendering",
    )

    resources = Path(__file__).resolve().parent / "resources"
    shader_dir = resources / "shaders" / f"glsl{GLSL_VERSION}"

    camera = pr.Camera3D(
        pr.Vector3(10.0, 10.0, 10.0),
        pr.Vector3(0.0, 0.0, 0.0),
        pr.Vector3(0.0, 1.0, 0.0),
        45.0,
        CAMERA_PERSPECTIVE,
    )

    shadow_shader = pr.load_shader(
        str(shader_dir / "shadowmap.vs"),
        str(shader_dir / "shadowmap.fs"),
    )
    shadow_shader.locs[SHADER_LOC_VECTOR_VIEW] = pr.get_shader_location(
        shadow_shader, "viewPos"
    )

    light_dir = glm.normalize(glm.vec3(0.35, -1.0, -0.35))
    light_color = pr.color_normalize(pr.WHITE)

    light_dir_loc = pr.get_shader_location(shadow_shader, "lightDir")
    light_col_loc = pr.get_shader_location(shadow_shader, "lightColor")
    ambient_loc = pr.get_shader_location(shadow_shader, "ambient")
    light_vp_loc = pr.get_shader_location(shadow_shader, "lightVP")
    shadow_map_loc = pr.get_shader_location(shadow_shader, "shadowMap")
    shadow_map_resolution_loc = pr.get_shader_location(
        shadow_shader, "shadowMapResolution"
    )

    light_dir_uniform = pr.ffi.new("float[3]", [light_dir.x, light_dir.y, light_dir.z])
    light_color_uniform = pr.ffi.new(
        "float[4]", [light_color.x, light_color.y, light_color.z, light_color.w]
    )
    ambient_uniform = pr.ffi.new("float[4]", [0.1, 0.1, 0.1, 1.0])
    shadow_res_uniform = pr.ffi.new("int *", SHADOWMAP_RESOLUTION)

    pr.set_shader_value(
        shadow_shader, light_dir_loc, light_dir_uniform, SHADER_UNIFORM_VEC3
    )
    pr.set_shader_value(
        shadow_shader, light_col_loc, light_color_uniform, SHADER_UNIFORM_VEC4
    )
    pr.set_shader_value(
        shadow_shader, ambient_loc, ambient_uniform, SHADER_UNIFORM_VEC4
    )
    pr.set_shader_value(
        shadow_shader,
        shadow_map_resolution_loc,
        shadow_res_uniform,
        SHADER_UNIFORM_INT,
    )

    cube = pr.load_model_from_mesh(pr.gen_mesh_cube(1.0, 1.0, 1.0))
    cube.materials[0].shader = shadow_shader

    robot_path = resources / "models" / "robot.glb"
    robot = pr.load_model(str(robot_path))
    for i in range(robot.materialCount):
        robot.materials[i].shader = shadow_shader

    anim_count = pr.ffi.new("int *", 0)
    anims: Any = pr.load_model_animations(str(robot_path), anim_count)

    shadow_map = load_shadowmap_render_texture(
        SHADOWMAP_RESOLUTION, SHADOWMAP_RESOLUTION
    )

    light_camera = pr.Camera3D(
        glm_to_pr_vec3(light_dir * -15.0),
        pr.Vector3(0.0, 0.0, 0.0),
        pr.Vector3(0.0, 1.0, 0.0),
        20.0,
        CAMERA_ORTHOGRAPHIC,
    )

    frame_counter = 0
    light_view = pr.Matrix()
    light_proj = pr.Matrix()
    light_view_proj = pr.Matrix()
    texture_active_slot = 10
    texture_slot_uniform = pr.ffi.new("int *", texture_active_slot)

    pr.set_target_fps(60)

    while not pr.window_should_close():
        delta_time = pr.get_frame_time()

        view_pos_uniform = pr.ffi.new(
            "float[3]", [camera.position.x, camera.position.y, camera.position.z]
        )
        pr.set_shader_value(
            shadow_shader,
            shadow_shader.locs[SHADER_LOC_VECTOR_VIEW],
            view_pos_uniform,
            SHADER_UNIFORM_VEC3,
        )
        pr.update_camera(camera, CAMERA_ORBITAL)

        if anim_count[0] > 0:
            frame_counter = (frame_counter + 1) % max(1, anims[0].frameCount)
            pr.update_model_animation(robot, anims[0], frame_counter)

        camera_speed = 0.05
        if pr.is_key_down(KEY_LEFT) and light_dir.x < 0.6:
            light_dir.x += camera_speed * 60.0 * delta_time
        if pr.is_key_down(KEY_RIGHT) and light_dir.x > -0.6:
            light_dir.x -= camera_speed * 60.0 * delta_time
        if pr.is_key_down(KEY_UP) and light_dir.z < 0.6:
            light_dir.z += camera_speed * 60.0 * delta_time
        if pr.is_key_down(KEY_DOWN) and light_dir.z > -0.6:
            light_dir.z -= camera_speed * 60.0 * delta_time

        light_dir = glm.normalize(light_dir)
        light_camera.position = glm_to_pr_vec3(light_dir * -15.0)
        light_dir_uniform[0] = light_dir.x
        light_dir_uniform[1] = light_dir.y
        light_dir_uniform[2] = light_dir.z
        pr.set_shader_value(
            shadow_shader, light_dir_loc, light_dir_uniform, SHADER_UNIFORM_VEC3
        )

        pr.begin_texture_mode(shadow_map)
        pr.clear_background(pr.WHITE)

        pr.begin_mode_3d(light_camera)
        light_view = pr.rl_get_matrix_modelview()
        light_proj = pr.rl_get_matrix_projection()
        draw_scene(cube, robot)
        pr.end_mode_3d()

        pr.end_texture_mode()

        light_view_proj = pr.matrix_multiply(light_view, light_proj)

        pr.begin_drawing()
        pr.clear_background(pr.RAYWHITE)

        pr.set_shader_value_matrix(shadow_shader, light_vp_loc, light_view_proj)
        pr.rl_enable_shader(shadow_shader.id)
        pr.rl_active_texture_slot(texture_active_slot)
        pr.rl_enable_texture(shadow_map.depth.id)
        pr.rl_set_uniform(shadow_map_loc, texture_slot_uniform, SHADER_UNIFORM_INT, 1)

        pr.begin_mode_3d(camera)
        draw_scene(cube, robot)
        pr.end_mode_3d()

        pr.rl_disable_texture()
        pr.rl_disable_shader()

        pr.draw_text("Use the arrow keys to rotate the light!", 10, 10, 30, pr.RED)
        fps_text = f"FPS: {pr.get_fps()}"
        fps_text_width = pr.measure_text(fps_text, 20)
        pr.draw_text(fps_text, SCREEN_WIDTH - fps_text_width - 10, 10, 20, pr.DARKGREEN)
        pr.draw_text(
            "Shadows in raylib using the shadowmapping algorithm!",
            SCREEN_WIDTH - 280,
            SCREEN_HEIGHT - 20,
            10,
            pr.GRAY,
        )

        pr.end_drawing()

        if pr.is_key_pressed(KEY_F):
            pr.take_screenshot("shaders_shadowmap.png")

    pr.unload_shader(shadow_shader)
    pr.unload_model(cube)
    pr.unload_model(robot)
    pr.unload_model_animations(anims, anim_count[0])
    unload_shadowmap_render_texture(shadow_map)
    pr.close_window()


if __name__ == "__main__":
    main()
