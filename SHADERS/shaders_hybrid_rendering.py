"""raylib [shaders] example - hybrid rendering (Python port)."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

import glm
import pyray as pr

# Version checked: raylib 5.x/pyray API parity (reviewed 2026-02-28).

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 450
GLSL_VERSION = 330

# Constants that are not always visible to mypy in pyray stubs.
CAMERA_PERSPECTIVE = getattr(pr, "CAMERA_PERSPECTIVE", 0)
CAMERA_ORBITAL = getattr(pr, "CAMERA_ORBITAL", 2)
SHADER_UNIFORM_VEC2 = getattr(pr, "SHADER_UNIFORM_VEC2", 1)
SHADER_UNIFORM_VEC3 = getattr(pr, "SHADER_UNIFORM_VEC3", 2)
PIXELFORMAT_UNCOMPRESSED_R8G8B8A8 = getattr(pr, "PIXELFORMAT_UNCOMPRESSED_R8G8B8A8", 7)
RL_ATTACHMENT_COLOR_CHANNEL0 = getattr(pr, "RL_ATTACHMENT_COLOR_CHANNEL0", 0)
RL_ATTACHMENT_DEPTH = getattr(pr, "RL_ATTACHMENT_DEPTH", 100)
RL_ATTACHMENT_TEXTURE2D = getattr(pr, "RL_ATTACHMENT_TEXTURE2D", 100)
LOG_INFO = getattr(pr, "LOG_INFO", 1)
LOG_WARNING = getattr(pr, "LOG_WARNING", 2)


@dataclass
class RayLocs:
    """Store uniforms used by the raymarch shader."""

    cam_pos: int
    cam_dir: int
    screen_center: int


def load_render_texture_depth_tex(width: int, height: int) -> pr.RenderTexture:
    """Create a render texture with a writable depth texture attachment."""
    target = pr.RenderTexture()
    target.id = pr.rl_load_framebuffer()

    if target.id > 0:
        pr.rl_enable_framebuffer(target.id)

        target.texture.id = pr.rl_load_texture(
            pr.ffi.NULL,
            width,
            height,
            PIXELFORMAT_UNCOMPRESSED_R8G8B8A8,
            1,
        )
        target.texture.width = width
        target.texture.height = height
        target.texture.format = PIXELFORMAT_UNCOMPRESSED_R8G8B8A8
        target.texture.mipmaps = 1

        target.depth.id = pr.rl_load_texture_depth(width, height, False)
        target.depth.width = width
        target.depth.height = height
        target.depth.format = 19
        target.depth.mipmaps = 1

        pr.rl_framebuffer_attach(
            target.id,
            target.texture.id,
            RL_ATTACHMENT_COLOR_CHANNEL0,
            RL_ATTACHMENT_TEXTURE2D,
            0,
        )
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


def unload_render_texture_depth_tex(target: pr.RenderTexture) -> None:
    """Unload custom color/depth textures and their framebuffer."""
    if target.id > 0:
        pr.rl_unload_texture(target.texture.id)
        pr.rl_unload_texture(target.depth.id)
        pr.rl_unload_framebuffer(target.id)


def pr_to_glm_vec3(value: pr.Vector3) -> glm.vec3:
    """Convert pyray Vector3 to glm vec3 for vector math."""
    return glm.vec3(value.x, value.y, value.z)


def main() -> None:
    """Run the hybrid rendering demo with raymarch + rasterization."""
    pr.init_window(
        SCREEN_WIDTH, SCREEN_HEIGHT, "raylib [shaders] example - hybrid rendering"
    )

    resources = Path(__file__).resolve().parent / "resources"
    shader_dir = resources / "shaders" / f"glsl{GLSL_VERSION}"

    shdr_raymarch = pr.load_shader("", str(shader_dir / "hybrid_raymarch.fs"))
    shdr_raster = pr.load_shader("", str(shader_dir / "hybrid_raster.fs"))

    march_locs = RayLocs(
        cam_pos=pr.get_shader_location(shdr_raymarch, "camPos"),
        cam_dir=pr.get_shader_location(shdr_raymarch, "camDir"),
        screen_center=pr.get_shader_location(shdr_raymarch, "screenCenter"),
    )

    screen_center_uniform = pr.ffi.new(
        "float[2]", [SCREEN_WIDTH / 2.0, SCREEN_HEIGHT / 2.0]
    )
    pr.set_shader_value(
        shdr_raymarch,
        march_locs.screen_center,
        screen_center_uniform,
        SHADER_UNIFORM_VEC2,
    )

    target = load_render_texture_depth_tex(SCREEN_WIDTH, SCREEN_HEIGHT)

    camera = pr.Camera3D(
        pr.Vector3(0.5, 1.0, 1.5),
        pr.Vector3(0.0, 0.5, 0.0),
        pr.Vector3(0.0, 1.0, 0.0),
        45.0,
        CAMERA_PERSPECTIVE,
    )

    cam_dist = 1.0 / float(glm.tan(glm.radians(camera.fovy * 0.5)))

    pr.set_target_fps(60)

    while not pr.window_should_close():
        pr.update_camera(camera, CAMERA_ORBITAL)

        cam_pos_uniform = pr.ffi.new(
            "float[3]", [camera.position.x, camera.position.y, camera.position.z]
        )
        pr.set_shader_value(
            shdr_raymarch,
            march_locs.cam_pos,
            cam_pos_uniform,
            SHADER_UNIFORM_VEC3,
        )

        camera_target = pr_to_glm_vec3(camera.target)
        camera_position = pr_to_glm_vec3(camera.position)
        cam_dir = glm.normalize(camera_target - camera_position) * cam_dist
        cam_dir_uniform = pr.ffi.new("float[3]", [cam_dir.x, cam_dir.y, cam_dir.z])
        pr.set_shader_value(
            shdr_raymarch,
            march_locs.cam_dir,
            cam_dir_uniform,
            SHADER_UNIFORM_VEC3,
        )

        pr.begin_texture_mode(target)
        pr.clear_background(pr.WHITE)

        pr.rl_enable_depth_test()
        pr.begin_shader_mode(shdr_raymarch)
        pr.draw_rectangle_rec(
            pr.Rectangle(0.0, 0.0, float(SCREEN_WIDTH), float(SCREEN_HEIGHT)),
            pr.WHITE,
        )
        pr.end_shader_mode()

        pr.begin_mode_3d(camera)
        pr.begin_shader_mode(shdr_raster)
        pr.draw_cube_wires_v(
            pr.Vector3(0.0, 0.5, 1.0),
            pr.Vector3(1.0, 1.0, 1.0),
            pr.RED,
        )
        pr.draw_cube_v(
            pr.Vector3(0.0, 0.5, 1.0),
            pr.Vector3(1.0, 1.0, 1.0),
            pr.PURPLE,
        )
        pr.draw_cube_wires_v(
            pr.Vector3(0.0, 0.5, -1.0),
            pr.Vector3(1.0, 1.0, 1.0),
            pr.DARKGREEN,
        )
        pr.draw_cube_v(
            pr.Vector3(0.0, 0.5, -1.0),
            pr.Vector3(1.0, 1.0, 1.0),
            pr.YELLOW,
        )
        pr.draw_grid(10, 1.0)
        pr.end_shader_mode()
        pr.end_mode_3d()

        pr.end_texture_mode()

        pr.begin_drawing()
        pr.clear_background(pr.RAYWHITE)
        pr.draw_texture_rec(
            target.texture,
            pr.Rectangle(0.0, 0.0, float(SCREEN_WIDTH), -float(SCREEN_HEIGHT)),
            pr.Vector2(0.0, 0.0),
            pr.WHITE,
        )
        pr.draw_fps(10, 10)
        pr.end_drawing()

    unload_render_texture_depth_tex(target)
    pr.unload_shader(shdr_raymarch)
    pr.unload_shader(shdr_raster)
    pr.close_window()


if __name__ == "__main__":
    main()
