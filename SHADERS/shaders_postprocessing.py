from __future__ import annotations

from enum import IntEnum
from pathlib import Path

import pyray as pr

# Version checked: raylib 5.x/pyray API parity (reviewed 2026-02-28).

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 450
GLSL_VERSION = 330

FLAG_MSAA_4X_HINT = getattr(pr, "FLAG_MSAA_4X_HINT", 32)
CAMERA_PERSPECTIVE = getattr(pr, "CAMERA_PERSPECTIVE", 0)
CAMERA_ORBITAL = getattr(pr, "CAMERA_ORBITAL", 2)
MATERIAL_MAP_DIFFUSE = getattr(pr, "MATERIAL_MAP_DIFFUSE", 0)
KEY_RIGHT = getattr(pr, "KEY_RIGHT", 262)
KEY_LEFT = getattr(pr, "KEY_LEFT", 263)


class PostprocessShader(IntEnum):
    """Supported postprocessing effects."""

    GRAYSCALE = 0
    POSTERIZATION = 1
    DREAM_VISION = 2
    PIXELIZER = 3
    CROSS_HATCHING = 4
    CROSS_STITCHING = 5
    PREDATOR_VIEW = 6
    SCANLINES = 7
    FISHEYE = 8
    SOBEL = 9
    BLOOM = 10
    BLUR = 11


SHADER_LABELS: tuple[str, ...] = (
    "GRAYSCALE",
    "POSTERIZATION",
    "DREAM_VISION",
    "PIXELIZER",
    "CROSS_HATCHING",
    "CROSS_STITCHING",
    "PREDATOR_VIEW",
    "SCANLINES",
    "FISHEYE",
    "SOBEL",
    "BLOOM",
    "BLUR",
)

SHADER_FILES: tuple[str, ...] = (
    "grayscale.fs",
    "posterization.fs",
    "dream_vision.fs",
    "pixelizer.fs",
    "cross_hatching.fs",
    "cross_stitching.fs",
    "predator.fs",
    "scanlines.fs",
    "fisheye.fs",
    "sobel.fs",
    "bloom.fs",
    "blur.fs",
)


def main() -> None:
    """Run the postprocessing shader showcase."""
    pr.set_config_flags(FLAG_MSAA_4X_HINT)
    pr.init_window(
        SCREEN_WIDTH,
        SCREEN_HEIGHT,
        "raylib [shaders] example - postprocessing",
    )

    resources = Path(__file__).resolve().parent / "resources"
    shader_dir = resources / "shaders" / f"glsl{GLSL_VERSION}"

    camera = pr.Camera3D(
        pr.Vector3(2.0, 3.0, 2.0),
        pr.Vector3(0.0, 1.0, 0.0),
        pr.Vector3(0.0, 1.0, 0.0),
        45.0,
        CAMERA_PERSPECTIVE,
    )

    model = pr.load_model(str(resources / "models" / "church.obj"))
    texture = pr.load_texture(str(resources / "models" / "church_diffuse.png"))
    model.materials[0].maps[MATERIAL_MAP_DIFFUSE].texture = texture

    shaders = [
        pr.load_shader("", str(shader_dir / filename)) for filename in SHADER_FILES
    ]

    current_shader = int(PostprocessShader.GRAYSCALE)
    target = pr.load_render_texture(SCREEN_WIDTH, SCREEN_HEIGHT)

    pr.set_target_fps(60)

    while not pr.window_should_close():
        pr.update_camera(camera, CAMERA_ORBITAL)

        if pr.is_key_pressed(KEY_RIGHT):
            current_shader += 1
        elif pr.is_key_pressed(KEY_LEFT):
            current_shader -= 1

        if current_shader >= len(shaders):
            current_shader = 0
        elif current_shader < 0:
            current_shader = len(shaders) - 1

        pr.begin_texture_mode(target)
        pr.clear_background(pr.RAYWHITE)

        pr.begin_mode_3d(camera)
        pr.draw_model(model, pr.Vector3(0.0, 0.0, 0.0), 0.1, pr.WHITE)
        pr.draw_grid(10, 1.0)
        pr.end_mode_3d()

        pr.end_texture_mode()

        pr.begin_drawing()
        pr.clear_background(pr.RAYWHITE)

        pr.begin_shader_mode(shaders[current_shader])
        pr.draw_texture_rec(
            target.texture,
            pr.Rectangle(
                0.0,
                0.0,
                float(target.texture.width),
                -float(target.texture.height),
            ),
            pr.Vector2(0.0, 0.0),
            pr.WHITE,
        )
        pr.end_shader_mode()

        pr.draw_rectangle(0, 9, 580, 30, pr.fade(pr.LIGHTGRAY, 0.7))

        pr.draw_text(
            "(c) Church 3D model by Alberto Cano",
            SCREEN_WIDTH - 200,
            SCREEN_HEIGHT - 20,
            10,
            pr.GRAY,
        )
        pr.draw_text("CURRENT POSTPRO SHADER:", 10, 15, 20, pr.BLACK)
        pr.draw_text(SHADER_LABELS[current_shader], 330, 15, 20, pr.RED)
        pr.draw_text("< >", 540, 10, 30, pr.DARKBLUE)
        pr.draw_fps(700, 15)

        pr.end_drawing()

    for shader in shaders:
        pr.unload_shader(shader)

    pr.unload_texture(texture)
    pr.unload_model(model)
    pr.unload_render_texture(target)
    pr.close_window()


if __name__ == "__main__":
    main()
