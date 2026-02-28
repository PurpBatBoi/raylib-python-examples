from __future__ import annotations

from pathlib import Path

import pyray as pr

# Version checked: raylib 5.x/pyray API parity (reviewed 2026-02-28).

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 450
FLAG_VSYNC_HINT = getattr(pr, "FLAG_VSYNC_HINT", 64)
FLAG_MSAA_4X_HINT = getattr(pr, "FLAG_MSAA_4X_HINT", 32)
TEXTURE_FILTER_BILINEAR = getattr(pr, "TEXTURE_FILTER_BILINEAR", 1)
KEY_SPACE = getattr(pr, "KEY_SPACE", 32)
KEY_EQUAL = getattr(pr, "KEY_EQUAL", 61)
KEY_MINUS = getattr(pr, "KEY_MINUS", 45)
KEY_LEFT = getattr(pr, "KEY_LEFT", 263)
KEY_RIGHT = getattr(pr, "KEY_RIGHT", 262)
MOUSE_LEFT_BUTTON = getattr(pr, "MOUSE_LEFT_BUTTON", 0)
RL_QUADS = getattr(pr, "RL_QUADS", 7)


def draw_textured_curve(
    tex_road: pr.Texture,
    curve_width: float,
    curve_segments: int,
    curve_start_position: pr.Vector2,
    curve_start_position_tangent: pr.Vector2,
    curve_end_position: pr.Vector2,
    curve_end_position_tangent: pr.Vector2,
) -> None:
    """Draw textured cubic bezier strip using quad segments."""
    step = 1.0 / curve_segments
    previous = curve_start_position
    previous_tangent = pr.Vector2(0.0, 0.0)
    previous_v = 0.0
    tangent_set = False

    for i in range(1, curve_segments + 1):
        t = step * float(i)
        a = (1.0 - t) ** 3
        b = 3.0 * ((1.0 - t) ** 2) * t
        c = 3.0 * (1.0 - t) * (t**2)
        d = t**3

        current = pr.Vector2(
            a * curve_start_position.x
            + b * curve_start_position_tangent.x
            + c * curve_end_position_tangent.x
            + d * curve_end_position.x,
            a * curve_start_position.y
            + b * curve_start_position_tangent.y
            + c * curve_end_position_tangent.y
            + d * curve_end_position.y,
        )

        delta = pr.Vector2(current.x - previous.x, current.y - previous.y)
        normal = pr.vector2_normalize(pr.Vector2(-delta.y, delta.x))
        v_coord = previous_v + pr.vector2_length(delta) / float(tex_road.height * 2)

        if not tangent_set:
            previous_tangent = normal
            tangent_set = True

        prev_pos_normal = pr.vector2_add(
            previous, pr.vector2_scale(previous_tangent, curve_width)
        )
        prev_neg_normal = pr.vector2_add(
            previous, pr.vector2_scale(previous_tangent, -curve_width)
        )
        curr_pos_normal = pr.vector2_add(current, pr.vector2_scale(normal, curve_width))
        curr_neg_normal = pr.vector2_add(
            current, pr.vector2_scale(normal, -curve_width)
        )

        pr.rl_set_texture(tex_road.id)
        pr.rl_begin(RL_QUADS)
        pr.rl_color4ub(255, 255, 255, 255)
        pr.rl_normal3f(0.0, 0.0, 1.0)

        pr.rl_tex_coord2f(0.0, previous_v)
        pr.rl_vertex2f(prev_neg_normal.x, prev_neg_normal.y)
        pr.rl_tex_coord2f(1.0, previous_v)
        pr.rl_vertex2f(prev_pos_normal.x, prev_pos_normal.y)
        pr.rl_tex_coord2f(1.0, v_coord)
        pr.rl_vertex2f(curr_pos_normal.x, curr_pos_normal.y)
        pr.rl_tex_coord2f(0.0, v_coord)
        pr.rl_vertex2f(curr_neg_normal.x, curr_neg_normal.y)

        pr.rl_end()

        previous = current
        previous_tangent = normal
        previous_v = v_coord


def main() -> None:
    """Run textured bezier-curve editing demo."""
    pr.set_config_flags(FLAG_VSYNC_HINT | FLAG_MSAA_4X_HINT)
    pr.init_window(
        SCREEN_WIDTH, SCREEN_HEIGHT, "raylib [textures] example - textured curve"
    )

    resources = Path(__file__).resolve().parent / "resources"
    tex_road = pr.load_texture(str(resources / "road.png"))
    pr.set_texture_filter(tex_road, TEXTURE_FILTER_BILINEAR)

    show_curve = False
    curve_width = 50.0
    curve_segments = 24

    curve_start_position = pr.Vector2(80.0, 100.0)
    curve_start_position_tangent = pr.Vector2(100.0, 300.0)
    curve_end_position = pr.Vector2(700.0, 350.0)
    curve_end_position_tangent = pr.Vector2(600.0, 100.0)
    curve_selected_point: str | None = None

    pr.set_target_fps(60)

    while not pr.window_should_close():
        if pr.is_key_pressed(KEY_SPACE):
            show_curve = not show_curve
        if pr.is_key_pressed(KEY_EQUAL):
            curve_width += 2.0
        if pr.is_key_pressed(KEY_MINUS):
            curve_width -= 2.0
        curve_width = max(2.0, curve_width)

        if pr.is_key_pressed(KEY_LEFT):
            curve_segments -= 2
        if pr.is_key_pressed(KEY_RIGHT):
            curve_segments += 2
        curve_segments = max(2, curve_segments)

        if not pr.is_mouse_button_down(MOUSE_LEFT_BUTTON):
            curve_selected_point = None

        if curve_selected_point is not None:
            delta = pr.get_mouse_delta()
            match curve_selected_point:
                case "start":
                    curve_start_position = pr.vector2_add(curve_start_position, delta)
                case "start_tangent":
                    curve_start_position_tangent = pr.vector2_add(
                        curve_start_position_tangent, delta
                    )
                case "end":
                    curve_end_position = pr.vector2_add(curve_end_position, delta)
                case "end_tangent":
                    curve_end_position_tangent = pr.vector2_add(
                        curve_end_position_tangent, delta
                    )

        mouse = pr.get_mouse_position()
        if pr.check_collision_point_circle(mouse, curve_start_position, 6.0):
            curve_selected_point = "start"
        elif pr.check_collision_point_circle(mouse, curve_start_position_tangent, 6.0):
            curve_selected_point = "start_tangent"
        elif pr.check_collision_point_circle(mouse, curve_end_position, 6.0):
            curve_selected_point = "end"
        elif pr.check_collision_point_circle(mouse, curve_end_position_tangent, 6.0):
            curve_selected_point = "end_tangent"

        pr.begin_drawing()
        pr.clear_background(pr.RAYWHITE)

        draw_textured_curve(
            tex_road,
            curve_width,
            curve_segments,
            curve_start_position,
            curve_start_position_tangent,
            curve_end_position,
            curve_end_position_tangent,
        )

        if show_curve:
            pr.draw_spline_segment_bezier_cubic(
                curve_start_position,
                curve_end_position,
                curve_start_position_tangent,
                curve_end_position_tangent,
                2.0,
                pr.BLUE,
            )

        pr.draw_line_v(curve_start_position, curve_start_position_tangent, pr.SKYBLUE)
        pr.draw_line_v(
            curve_start_position_tangent,
            curve_end_position_tangent,
            pr.fade(pr.LIGHTGRAY, 0.4),
        )
        pr.draw_line_v(curve_end_position, curve_end_position_tangent, pr.PURPLE)

        if pr.check_collision_point_circle(mouse, curve_start_position, 6.0):
            pr.draw_circle_v(curve_start_position, 7.0, pr.YELLOW)
        pr.draw_circle_v(curve_start_position, 5.0, pr.RED)

        if pr.check_collision_point_circle(mouse, curve_start_position_tangent, 6.0):
            pr.draw_circle_v(curve_start_position_tangent, 7.0, pr.YELLOW)
        pr.draw_circle_v(curve_start_position_tangent, 5.0, pr.MAROON)

        if pr.check_collision_point_circle(mouse, curve_end_position, 6.0):
            pr.draw_circle_v(curve_end_position, 7.0, pr.YELLOW)
        pr.draw_circle_v(curve_end_position, 5.0, pr.GREEN)

        if pr.check_collision_point_circle(mouse, curve_end_position_tangent, 6.0):
            pr.draw_circle_v(curve_end_position_tangent, 7.0, pr.YELLOW)
        pr.draw_circle_v(curve_end_position_tangent, 5.0, pr.DARKGREEN)

        pr.draw_text(
            "Drag points to move curve, press SPACE to show/hide base curve",
            10,
            10,
            10,
            pr.DARKGRAY,
        )
        pr.draw_text(
            f"Curve width: {curve_width:2.0f} (Use + and - to adjust)",
            10,
            30,
            10,
            pr.DARKGRAY,
        )
        pr.draw_text(
            f"Curve segments: {curve_segments} (Use LEFT and RIGHT to adjust)",
            10,
            50,
            10,
            pr.DARKGRAY,
        )

        pr.end_drawing()

    pr.unload_texture(tex_road)
    pr.close_window()


if __name__ == "__main__":
    main()
