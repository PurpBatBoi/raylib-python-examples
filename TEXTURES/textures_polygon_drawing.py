from __future__ import annotations

import math
from pathlib import Path

import pyray as pr
from raylib import rl

# Version checked: raylib 5.5/pyray API parity (reviewed 2026-02-28).

SCREEN_WIDTH: int = 800
SCREEN_HEIGHT: int = 450
MAX_POINTS: int = 11  # 10 edge vertices + closing repeat of the first.

# RL_TRIANGLES lives in the rlgl layer; fall back to its documented value (4)
# if the installed pyray bindings do not yet re-export it.
RL_TRIANGLES: int = int(getattr(rl, "RL_TRIANGLES", getattr(pr, "RL_TRIANGLES", 4)))


def draw_texture_poly(
    texture: pr.Texture,
    center: pr.Vector2,
    points: list[pr.Vector2],
    texcoords: list[pr.Vector2],
    point_count: int,
    tint: pr.Color | tuple[int, int, int, int],
) -> None:
    """Draw a textured polygon as a triangle fan using rlgl primitives.

    The polygon is defined by *point_count* vertices in *points* (offsets from
    *center*) paired with their UV coordinates in *texcoords*.  The last entry
    of both lists must repeat the first to close the fan.

    .. warning::
        ``rlSetTexture`` **must** be called *after* ``rlBegin``.  When the
        current draw mode changes (e.g. from the quad-based ``ClearBackground``
        to ``RL_TRIANGLES`` here), rlgl flushes the batch and resets the active
        texture to the 1 × 1 default white pixel *inside* ``rlBegin``.  Any
        ``rlSetTexture`` call made before ``rlBegin`` is therefore silently
        discarded, causing the polygon to render as a plain white shape instead
        of the intended texture.  See raylib issue #4347 for full details.

    Parameters
    ----------
    texture:
        Source texture to map onto the polygon.
    center:
        Screen-space position of the polygon centre (the fan origin).
    points:
        Vertex offsets from *center*, one entry per texcoord.
    texcoords:
        UV coordinates in [0, 1] space, parallel to *points*.
    point_count:
        Number of entries in both *points* and *texcoords*.
    tint:
        Colour multiplier applied to every vertex.  Accepts either a
        :class:`pyray.Color`-like object (``r, g, b, a`` attributes) or a
        plain 4-tuple ``(r, g, b, a)`` such as ``pr.WHITE``.
    """
    if isinstance(tint, tuple):
        r, g, b, a = int(tint[0]), int(tint[1]), int(tint[2]), int(tint[3])
    else:
        r, g, b, a = int(tint.r), int(tint.g), int(tint.b), int(tint.a)

    # rlBegin flushes the previous batch and may reset the active texture to
    # the default white pixel when the draw mode changes.  rlSetTexture must
    # therefore be called *after* rlBegin so the assignment is not clobbered.
    rl.rlBegin(RL_TRIANGLES)
    rl.rlSetTexture(int(texture.id))  # Must come after rlBegin — see docstring.

    for i in range(point_count - 1):
        rl.rlColor4ub(r, g, b, a)
        rl.rlTexCoord2f(0.5, 0.5)
        rl.rlVertex2f(float(center.x), float(center.y))

        rl.rlColor4ub(r, g, b, a)
        rl.rlTexCoord2f(float(texcoords[i].x), float(texcoords[i].y))
        rl.rlVertex2f(float(points[i].x + center.x), float(points[i].y + center.y))

        rl.rlColor4ub(r, g, b, a)
        rl.rlTexCoord2f(float(texcoords[i + 1].x), float(texcoords[i + 1].y))
        rl.rlVertex2f(
            float(points[i + 1].x + center.x),
            float(points[i + 1].y + center.y),
        )

    rl.rlEnd()
    rl.rlSetTexture(0)


def main() -> None:
    """Run the textured-polygon example: a cat texture mapped to a rotating polygon."""
    pr.init_window(
        SCREEN_WIDTH, SCREEN_HEIGHT, "raylib [textures] example - polygon drawing"
    )

    # UV coordinates that map the texture onto the polygon vertices.
    texcoords: list[pr.Vector2] = [
        pr.Vector2(0.75, 0.0),
        pr.Vector2(0.25, 0.0),
        pr.Vector2(0.0, 0.5),
        pr.Vector2(0.0, 0.75),
        pr.Vector2(0.25, 1.0),
        pr.Vector2(0.375, 0.875),
        pr.Vector2(0.625, 0.875),
        pr.Vector2(0.75, 1.0),
        pr.Vector2(1.0, 0.75),
        pr.Vector2(1.0, 0.5),
        pr.Vector2(0.75, 0.0),  # Closes the fan back to the first vertex.
    ]

    # Base vertex offsets derived from the UVs (scaled to a 256 × 256 region).
    points: list[pr.Vector2] = [
        pr.Vector2((uv.x - 0.5) * 256.0, (uv.y - 0.5) * 256.0) for uv in texcoords
    ]

    # Per-frame rotated copy of *points*; base positions are never modified.
    positions: list[pr.Vector2] = [pr.Vector2(p.x, p.y) for p in points]

    resources = Path(__file__).resolve().parent / "resources"
    texture = pr.load_texture(str(resources / "cat.png"))

    angle: float = 0.0

    pr.set_target_fps(60)

    while not pr.window_should_close():
        # Rotate all vertices around the origin by the accumulated angle.
        angle += 1.0
        angle_rad: float = angle * (math.pi / 180.0)
        for i in range(MAX_POINTS):
            positions[i] = pr.vector2_rotate(points[i], angle_rad)

        pr.begin_drawing()
        pr.clear_background(pr.RAYWHITE)
        draw_texture_poly(
            texture,
            pr.Vector2(pr.get_screen_width() / 2.0, pr.get_screen_height() / 2.0),
            positions,
            texcoords,
            MAX_POINTS,
            pr.WHITE,
        )
        pr.draw_text("textured polygon", 20, 20, 20, pr.DARKGRAY)
        pr.end_drawing()

    pr.unload_texture(texture)
    pr.close_window()


if __name__ == "__main__":
    main()
