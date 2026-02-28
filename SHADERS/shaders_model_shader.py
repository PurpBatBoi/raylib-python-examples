from __future__ import annotations

from pathlib import Path

import pyray as pr

# Version checked: raylib 5.x/pyray API parity (reviewed 2026-02-28).

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 450
GLSL_VERSION = 330

FLAG_MSAA_4X_HINT = getattr(pr, "FLAG_MSAA_4X_HINT", 32)
CAMERA_PERSPECTIVE = getattr(pr, "CAMERA_PERSPECTIVE", 0)
CAMERA_FREE = getattr(pr, "CAMERA_FREE", 1)
MATERIAL_MAP_DIFFUSE = getattr(pr, "MATERIAL_MAP_DIFFUSE", 0)


def main() -> None:
    """Run the model shader sample."""
    pr.set_config_flags(FLAG_MSAA_4X_HINT)
    pr.init_window(
        SCREEN_WIDTH,
        SCREEN_HEIGHT,
        "raylib [shaders] example - model shader",
    )

    resources = Path(__file__).resolve().parent / "resources"
    shader_dir = resources / "shaders" / f"glsl{GLSL_VERSION}"

    camera = pr.Camera3D(
        pr.Vector3(4.0, 4.0, 4.0),
        pr.Vector3(0.0, 1.0, -1.0),
        pr.Vector3(0.0, 1.0, 0.0),
        45.0,
        CAMERA_PERSPECTIVE,
    )

    model = pr.load_model(str(resources / "models" / "watermill.obj"))
    texture = pr.load_texture(str(resources / "models" / "watermill_diffuse.png"))

    shader = pr.load_shader("", str(shader_dir / "grayscale.fs"))

    model.materials[0].shader = shader
    model.materials[0].maps[MATERIAL_MAP_DIFFUSE].texture = texture

    pr.disable_cursor()
    pr.set_target_fps(60)

    while not pr.window_should_close():
        pr.update_camera(camera, CAMERA_FREE)

        pr.begin_drawing()
        pr.clear_background(pr.RAYWHITE)

        pr.begin_mode_3d(camera)
        pr.draw_model(model, pr.Vector3(0.0, 0.0, 0.0), 0.2, pr.WHITE)
        pr.draw_grid(10, 1.0)
        pr.end_mode_3d()

        pr.draw_text(
            "(c) Watermill 3D model by Alberto Cano",
            SCREEN_WIDTH - 210,
            SCREEN_HEIGHT - 20,
            10,
            pr.GRAY,
        )
        pr.draw_fps(10, 10)

        pr.end_drawing()

    pr.unload_shader(shader)
    pr.unload_texture(texture)
    pr.unload_model(model)
    pr.close_window()


if __name__ == "__main__":
    main()
