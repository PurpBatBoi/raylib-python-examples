from __future__ import annotations

from pathlib import Path

import pyray as pr

# Version checked: raylib 5.x/pyray API parity (reviewed 2026-02-28).

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 450


def normalize_kernel(kernel: list[float]) -> list[float]:
    """Normalize a convolution kernel if its sum is non-zero."""
    total = sum(kernel)
    if total == 0.0:
        return kernel
    return [value / total for value in kernel]


def make_c_float_ptr(values: list[float]):
    """Create a C float* pointer from Python values for pyray FFI calls."""
    buffer = pr.ffi.new("float[]", values)
    return buffer, pr.ffi.cast("float *", buffer)


def main() -> None:
    """Run image kernel convolution demo."""
    pr.init_window(
        SCREEN_WIDTH, SCREEN_HEIGHT, "raylib [textures] example - image kernel"
    )

    resources = Path(__file__).resolve().parent / "resources"
    image = pr.load_image(str(resources / "cat.png"))

    gaussian_kernel = normalize_kernel([1.0, 2.0, 1.0, 2.0, 4.0, 2.0, 1.0, 2.0, 1.0])
    sobel_kernel = normalize_kernel([1.0, 0.0, -1.0, 2.0, 0.0, -2.0, 1.0, 0.0, -1.0])
    sharpen_kernel = normalize_kernel([0.0, -1.0, 0.0, -1.0, 5.0, -1.0, 0.0, -1.0, 0.0])
    gaussian_kernel_buf, gaussian_kernel_c = make_c_float_ptr(gaussian_kernel)
    sobel_kernel_buf, sobel_kernel_c = make_c_float_ptr(sobel_kernel)
    sharpen_kernel_buf, sharpen_kernel_c = make_c_float_ptr(sharpen_kernel)
    _ = (gaussian_kernel_buf, sobel_kernel_buf, sharpen_kernel_buf)

    cat_sharpened = pr.image_copy(image)
    pr.image_kernel_convolution(cat_sharpened, sharpen_kernel_c, 9)

    cat_sobel = pr.image_copy(image)
    pr.image_kernel_convolution(cat_sobel, sobel_kernel_c, 9)

    cat_gaussian = pr.image_copy(image)
    for _ in range(6):
        pr.image_kernel_convolution(cat_gaussian, gaussian_kernel_c, 9)

    crop_rect = pr.Rectangle(0.0, 0.0, 200.0, 450.0)
    pr.image_crop(image, crop_rect)
    pr.image_crop(cat_gaussian, crop_rect)
    pr.image_crop(cat_sobel, crop_rect)
    pr.image_crop(cat_sharpened, crop_rect)

    texture = pr.load_texture_from_image(image)
    cat_sharpened_texture = pr.load_texture_from_image(cat_sharpened)
    cat_sobel_texture = pr.load_texture_from_image(cat_sobel)
    cat_gaussian_texture = pr.load_texture_from_image(cat_gaussian)

    pr.unload_image(image)
    pr.unload_image(cat_gaussian)
    pr.unload_image(cat_sobel)
    pr.unload_image(cat_sharpened)

    pr.set_target_fps(60)

    while not pr.window_should_close():
        pr.begin_drawing()
        pr.clear_background(pr.RAYWHITE)
        pr.draw_texture(cat_sharpened_texture, 0, 0, pr.WHITE)
        pr.draw_texture(cat_sobel_texture, 200, 0, pr.WHITE)
        pr.draw_texture(cat_gaussian_texture, 400, 0, pr.WHITE)
        pr.draw_texture(texture, 600, 0, pr.WHITE)
        pr.end_drawing()

    pr.unload_texture(texture)
    pr.unload_texture(cat_gaussian_texture)
    pr.unload_texture(cat_sobel_texture)
    pr.unload_texture(cat_sharpened_texture)
    pr.close_window()


if __name__ == "__main__":
    main()
