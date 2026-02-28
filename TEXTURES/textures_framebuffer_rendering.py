from __future__ import annotations

from math import pi

import pyray as pr

# Version checked: raylib 5.x/pyray API parity (reviewed 2026-02-28).

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 450
SPLIT_WIDTH = SCREEN_WIDTH // 2
CAMERA_PERSPECTIVE = getattr(pr, "CAMERA_PERSPECTIVE", 0)
CAMERA_FREE = getattr(pr, "CAMERA_FREE", 1)
CAMERA_ORBITAL = getattr(pr, "CAMERA_ORBITAL", 2)
KEY_R = getattr(pr, "KEY_R", 82)


def draw_camera_prism(camera: pr.Camera3D, aspect: float, color: pr.Color) -> None:
    """Draw the camera frustum-like prism lines up to target distance."""
    length = pr.vector3_distance(camera.position, camera.target)
    plane_ndc = [
        pr.Vector3(-1.0, -1.0, 1.0),
        pr.Vector3(1.0, -1.0, 1.0),
        pr.Vector3(1.0, 1.0, 1.0),
        pr.Vector3(-1.0, 1.0, 1.0),
    ]

    view = pr.get_camera_matrix(camera)
    proj = pr.matrix_perspective(camera.fovy * pi / 180.0, aspect, 0.05, length)
    view_proj = pr.matrix_multiply(view, proj)
    inverse_view_proj = pr.matrix_invert(view_proj)

    corners: list[pr.Vector3] = []
    for ndc in plane_ndc:
        x = ndc.x
        y = ndc.y
        z = ndc.z

        vx = (
            inverse_view_proj.m0 * x
            + inverse_view_proj.m4 * y
            + inverse_view_proj.m8 * z
            + inverse_view_proj.m12
        )
        vy = (
            inverse_view_proj.m1 * x
            + inverse_view_proj.m5 * y
            + inverse_view_proj.m9 * z
            + inverse_view_proj.m13
        )
        vz = (
            inverse_view_proj.m2 * x
            + inverse_view_proj.m6 * y
            + inverse_view_proj.m10 * z
            + inverse_view_proj.m14
        )
        vw = (
            inverse_view_proj.m3 * x
            + inverse_view_proj.m7 * y
            + inverse_view_proj.m11 * z
            + inverse_view_proj.m15
        )
        corners.append(pr.Vector3(vx / vw, vy / vw, vz / vw))

    pr.draw_line_3d(corners[0], corners[1], color)
    pr.draw_line_3d(corners[1], corners[2], color)
    pr.draw_line_3d(corners[2], corners[3], color)
    pr.draw_line_3d(corners[3], corners[0], color)

    for corner in corners:
        pr.draw_line_3d(camera.position, corner, color)


def main() -> None:
    """Run split-screen framebuffer rendering with observer/subject cameras."""
    pr.init_window(
        SCREEN_WIDTH, SCREEN_HEIGHT, "raylib [textures] example - framebuffer rendering"
    )

    subject_camera = pr.Camera3D(
        pr.Vector3(5.0, 5.0, 5.0),
        pr.Vector3(0.0, 0.0, 0.0),
        pr.Vector3(0.0, 1.0, 0.0),
        45.0,
        CAMERA_PERSPECTIVE,
    )
    observer_camera = pr.Camera3D(
        pr.Vector3(10.0, 10.0, 10.0),
        pr.Vector3(0.0, 0.0, 0.0),
        pr.Vector3(0.0, 1.0, 0.0),
        45.0,
        CAMERA_PERSPECTIVE,
    )

    observer_target = pr.load_render_texture(SPLIT_WIDTH, SCREEN_HEIGHT)
    observer_source = pr.Rectangle(
        0.0,
        0.0,
        float(observer_target.texture.width),
        float(-observer_target.texture.height),
    )
    observer_dest = pr.Rectangle(0.0, 0.0, float(SPLIT_WIDTH), float(SCREEN_HEIGHT))

    subject_target = pr.load_render_texture(SPLIT_WIDTH, SCREEN_HEIGHT)
    subject_source = pr.Rectangle(
        0.0,
        0.0,
        float(subject_target.texture.width),
        float(-subject_target.texture.height),
    )
    subject_dest = pr.Rectangle(
        float(SPLIT_WIDTH), 0.0, float(SPLIT_WIDTH), float(SCREEN_HEIGHT)
    )
    texture_aspect_ratio = float(subject_target.texture.width) / float(
        subject_target.texture.height
    )

    capture_size = 128.0
    crop_source = pr.Rectangle(
        (subject_target.texture.width - capture_size) / 2.0,
        (subject_target.texture.height - capture_size) / 2.0,
        capture_size,
        -capture_size,
    )
    crop_dest = pr.Rectangle(SPLIT_WIDTH + 20.0, 20.0, capture_size, capture_size)

    pr.set_target_fps(60)
    pr.disable_cursor()

    while not pr.window_should_close():
        pr.update_camera(observer_camera, CAMERA_FREE)
        pr.update_camera(subject_camera, CAMERA_ORBITAL)
        if pr.is_key_pressed(KEY_R):
            observer_camera.target = pr.Vector3(0.0, 0.0, 0.0)

        pr.begin_texture_mode(observer_target)
        pr.clear_background(pr.RAYWHITE)
        pr.begin_mode_3d(observer_camera)
        pr.draw_grid(10, 1.0)
        pr.draw_cube(pr.Vector3(0.0, 0.0, 0.0), 2.0, 2.0, 2.0, pr.GOLD)
        pr.draw_cube_wires(pr.Vector3(0.0, 0.0, 0.0), 2.0, 2.0, 2.0, pr.PINK)
        draw_camera_prism(subject_camera, texture_aspect_ratio, pr.GREEN)
        pr.end_mode_3d()
        pr.draw_text(
            "Observer View", 10, observer_target.texture.height - 30, 20, pr.BLACK
        )
        pr.draw_text("WASD + Mouse to Move", 10, 10, 20, pr.DARKGRAY)
        pr.draw_text("Scroll to Zoom", 10, 30, 20, pr.DARKGRAY)
        pr.draw_text("R to Reset Observer Target", 10, 50, 20, pr.DARKGRAY)
        pr.end_texture_mode()

        pr.begin_texture_mode(subject_target)
        pr.clear_background(pr.RAYWHITE)
        pr.begin_mode_3d(subject_camera)
        pr.draw_cube(pr.Vector3(0.0, 0.0, 0.0), 2.0, 2.0, 2.0, pr.GOLD)
        pr.draw_cube_wires(pr.Vector3(0.0, 0.0, 0.0), 2.0, 2.0, 2.0, pr.PINK)
        pr.draw_grid(10, 1.0)
        pr.end_mode_3d()
        pr.draw_rectangle_lines(
            int((subject_target.texture.width - capture_size) / 2.0),
            int((subject_target.texture.height - capture_size) / 2.0),
            int(capture_size),
            int(capture_size),
            pr.GREEN,
        )
        pr.draw_text(
            "Subject View", 10, subject_target.texture.height - 30, 20, pr.BLACK
        )
        pr.end_texture_mode()

        pr.begin_drawing()
        pr.clear_background(pr.BLACK)
        pr.draw_texture_pro(
            observer_target.texture,
            observer_source,
            observer_dest,
            pr.Vector2(0.0, 0.0),
            0.0,
            pr.WHITE,
        )
        pr.draw_texture_pro(
            subject_target.texture,
            subject_source,
            subject_dest,
            pr.Vector2(0.0, 0.0),
            0.0,
            pr.WHITE,
        )
        pr.draw_texture_pro(
            subject_target.texture,
            crop_source,
            crop_dest,
            pr.Vector2(0.0, 0.0),
            0.0,
            pr.WHITE,
        )
        pr.draw_rectangle_lines_ex(crop_dest, 2.0, pr.BLACK)
        pr.draw_line(SPLIT_WIDTH, 0, SPLIT_WIDTH, SCREEN_HEIGHT, pr.BLACK)
        pr.end_drawing()

    pr.unload_render_texture(observer_target)
    pr.unload_render_texture(subject_target)
    pr.close_window()


if __name__ == "__main__":
    main()
