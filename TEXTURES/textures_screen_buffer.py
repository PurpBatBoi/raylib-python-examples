from __future__ import annotations

import pyray as pr

# Version checked: raylib 5.5/pyray API parity (reviewed 2026-02-28).

SCREEN_WIDTH: int = 800
SCREEN_HEIGHT: int = 450
MAX_COLORS: int = 256
SCALE_FACTOR: int = 2


def main() -> None:
    """Run flame simulation with low-resolution screen-index buffer.

    A palette-indexed fire algorithm is simulated on a half-resolution buffer
    and scaled up 2× for display.  Each frame the index buffer is converted
    directly to a flat RGBA bytearray and uploaded to the GPU in one call via
    ``update_texture``, avoiding the 89,600 per-frame ``image_draw_pixel``
    calls that the naïve port would require and which make the simulation run
    at effectively 0 fps in Python.

    ``update_texture`` requires a CFFI pointer rather than a plain Python
    bytes-like object. ``pr.ffi.from_buffer`` wraps the bytearray as a
    zero-copy buffer view, and ``pr.ffi.cast`` converts it to
    ``unsigned char *`` for the pyray binding.
    """
    pr.init_window(
        SCREEN_WIDTH, SCREEN_HEIGHT, "raylib [textures] example - screen buffer"
    )

    image_width: int = SCREEN_WIDTH // SCALE_FACTOR
    image_height: int = SCREEN_HEIGHT // SCALE_FACTOR
    flame_width: int = SCREEN_WIDTH // SCALE_FACTOR

    # Build the colour palette as flat (r, g, b, a) tuples for fast lookup.
    # Index 0 maps to black; higher indices graduate through deep purple to
    # bright yellow-white via ColorFromHSV.
    palette: list[tuple[int, int, int, int]] = []
    for i in range(MAX_COLORS):
        t: float = float(i) / float(MAX_COLORS - 1)
        hue: float = t * t
        color = pr.color_from_hsv(250.0 + 150.0 * hue, t, t)
        palette.append((color.r, color.g, color.b, color.a))

    index_buffer: list[int] = [0] * (image_width * image_height)
    flame_root_buffer: list[int] = [0] * flame_width

    # Reusable RGBA pixel buffer (4 bytes per pixel).  Built in Python each
    # frame and uploaded to the GPU in a single update_texture call.
    pixel_data: bytearray = bytearray(image_width * image_height * 4)

    # Wrap pixel_data once as a CFFI pointer so it can be passed to
    # update_texture without re-wrapping or copying every frame.
    # from_buffer yields a `char[]` view; cast to `unsigned char *` because
    # this pyray binding path expects an explicit pointer type.
    pixel_data_ptr = pr.ffi.cast("unsigned char *", pr.ffi.from_buffer(pixel_data))

    screen_image = pr.gen_image_color(image_width, image_height, pr.BLACK)
    screen_texture = pr.load_texture_from_image(screen_image)
    pr.unload_image(screen_image)  # CPU-side image is no longer needed.

    pr.set_target_fps(60)

    while not pr.window_should_close():
        # --- Grow flame root (skip x=0 and x=1 to leave edges dark) --------
        for x in range(2, flame_width):
            flame_root_buffer[x] = min(
                255, flame_root_buffer[x] + pr.get_random_value(0, 2)
            )

        # --- Seed the bottom row of the index buffer from flame_root --------
        base: int = (image_height - 1) * image_width
        for x in range(flame_width):
            index_buffer[base + x] = flame_root_buffer[x]

        # --- Clear the top row (pixels cannot rise any higher) --------------
        for x in range(image_width):
            index_buffer[x] = 0

        # --- Propagate fire upward (skip top row, already cleared) ----------
        for y in range(1, image_height):
            row_base: int = y * image_width
            for x in range(image_width):
                idx: int = row_base + x
                color_index: int = index_buffer[idx]
                if color_index == 0:
                    continue

                index_buffer[idx] = 0
                move_x: int = pr.get_random_value(0, 2) - 1
                new_x: int = x + move_x

                if 0 < new_x < image_width:
                    above: int = idx - image_width + move_x
                    decay: int = pr.get_random_value(0, 3)
                    color_index -= decay if decay < color_index else color_index
                    index_buffer[above] = color_index

        # --- Build pixel data directly from palette + index buffer ----------
        # Writing into a pre-allocated bytearray avoids per-pixel CFFI calls.
        # Row 0 is left as zeros (black) — it is cleared every frame anyway.
        for y in range(1, image_height):
            row_base = y * image_width
            buf_base: int = row_base * 4
            for x in range(image_width):
                r, g, b, a = palette[index_buffer[row_base + x]]
                offset: int = buf_base + x * 4
                pixel_data[offset] = r
                pixel_data[offset + 1] = g
                pixel_data[offset + 2] = b
                pixel_data[offset + 3] = a

        # Upload the pixel buffer to the GPU in a single call.
        # pixel_data_ptr is an unsigned char* view of pixel_data, required
        # because pyray's update_texture does not accept a plain bytearray.
        pr.update_texture(screen_texture, pixel_data_ptr)

        # --- Draw -----------------------------------------------------------
        pr.begin_drawing()
        pr.clear_background(pr.RAYWHITE)
        pr.draw_texture_ex(
            screen_texture, pr.Vector2(0.0, 0.0), 0.0, float(SCALE_FACTOR), pr.WHITE
        )
        pr.end_drawing()

    pr.unload_texture(screen_texture)
    pr.close_window()


if __name__ == "__main__":
    main()
