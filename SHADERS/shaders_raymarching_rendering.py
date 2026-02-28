from __future__ import annotations

from pathlib import Path

import glm
import pyray as pr

# Version checked: raylib 5.x/pyray API parity (reviewed 2026-02-28).

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 450
GLSL_VERSION = 330

FLAG_WINDOW_RESIZABLE = getattr(pr, "FLAG_WINDOW_RESIZABLE", 4)
CAMERA_PERSPECTIVE = getattr(pr, "CAMERA_PERSPECTIVE", 0)
CAMERA_FIRST_PERSON = getattr(pr, "CAMERA_FIRST_PERSON", 3)
SHADER_UNIFORM_VEC2 = getattr(pr, "SHADER_UNIFORM_VEC2", 1)
SHADER_UNIFORM_VEC3 = getattr(pr, "SHADER_UNIFORM_VEC3", 2)
SHADER_UNIFORM_FLOAT = getattr(pr, "SHADER_UNIFORM_FLOAT", 0)


def glm_to_pr_vec3(value: glm.vec3) -> pr.Vector3:
    """Convert glm vec3 values to pyray Vector3."""
    return pr.Vector3(float(value.x), float(value.y), float(value.z))


def main() -> None:
    """Run the raymarching rendering shader example."""
    pr.set_config_flags(FLAG_WINDOW_RESIZABLE)
    pr.init_window(
        SCREEN_WIDTH,
        SCREEN_HEIGHT,
        "raylib [shaders] example - raymarching rendering",
    )

    resources = Path(__file__).resolve().parent / "resources"
    shader_dir = resources / "shaders" / f"glsl{GLSL_VERSION}"

    camera = pr.Camera3D(
        glm_to_pr_vec3(glm.vec3(2.5, 2.5, 3.0)),
        glm_to_pr_vec3(glm.vec3(0.0, 0.0, 0.7)),
        pr.Vector3(0.0, 1.0, 0.0),
        65.0,
        CAMERA_PERSPECTIVE,
    )

    shader = pr.load_shader("", str(shader_dir / "raymarching.fs"))

    view_eye_loc = pr.get_shader_location(shader, "viewEye")
    view_center_loc = pr.get_shader_location(shader, "viewCenter")
    run_time_loc = pr.get_shader_location(shader, "runTime")
    resolution_loc = pr.get_shader_location(shader, "resolution")

    resolution_uniform = pr.ffi.new(
        "float[2]", [float(SCREEN_WIDTH), float(SCREEN_HEIGHT)]
    )
    pr.set_shader_value(shader, resolution_loc, resolution_uniform, SHADER_UNIFORM_VEC2)

    run_time = 0.0

    pr.disable_cursor()
    pr.set_target_fps(60)

    while not pr.window_should_close():
        pr.update_camera(camera, CAMERA_FIRST_PERSON)

        delta_time = pr.get_frame_time()
        run_time += delta_time

        view_eye_uniform = pr.ffi.new(
            "float[3]", [camera.position.x, camera.position.y, camera.position.z]
        )
        view_center_uniform = pr.ffi.new(
            "float[3]", [camera.target.x, camera.target.y, camera.target.z]
        )
        run_time_uniform = pr.ffi.new("float *", run_time)

        pr.set_shader_value(shader, view_eye_loc, view_eye_uniform, SHADER_UNIFORM_VEC3)
        pr.set_shader_value(
            shader,
            view_center_loc,
            view_center_uniform,
            SHADER_UNIFORM_VEC3,
        )
        pr.set_shader_value(
            shader, run_time_loc, run_time_uniform, SHADER_UNIFORM_FLOAT
        )

        if pr.is_window_resized():
            resolution_uniform[0] = float(pr.get_screen_width())
            resolution_uniform[1] = float(pr.get_screen_height())
            pr.set_shader_value(
                shader,
                resolution_loc,
                resolution_uniform,
                SHADER_UNIFORM_VEC2,
            )

        pr.begin_drawing()
        pr.clear_background(pr.RAYWHITE)

        pr.begin_shader_mode(shader)
        pr.draw_rectangle(0, 0, pr.get_screen_width(), pr.get_screen_height(), pr.WHITE)
        pr.end_shader_mode()

        pr.draw_text(
            "(c) Raymarching shader by Inigo Quilez. MIT License.",
            pr.get_screen_width() - 280,
            pr.get_screen_height() - 20,
            10,
            pr.BLACK,
        )

        pr.end_drawing()

    pr.unload_shader(shader)
    pr.close_window()


if __name__ == "__main__":
    main()
