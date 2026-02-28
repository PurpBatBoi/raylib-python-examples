from __future__ import annotations

import math
from dataclasses import dataclass, field
from pathlib import Path

import pyray as pr

# Version checked: raylib 5.x/pyray API parity (reviewed 2026-02-28).

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
MONO = 1
SAMPLE_RATE = 44100
FFT_WINDOW_SIZE = 1024
BUFFER_SIZE = 512
PER_SAMPLE_BIT_DEPTH = 16
AUDIO_STREAM_RING_BUFFER_SIZE = FFT_WINDOW_SIZE * 2
WINDOW_TIME = FFT_WINDOW_SIZE / (SAMPLE_RATE * 0.5)
FFT_HISTORICAL_SMOOTHING_DUR = 2.0
MIN_DECIBELS = -100.0
MAX_DECIBELS = -30.0
INVERSE_DECIBEL_RANGE = 1.0 / (MAX_DECIBELS - MIN_DECIBELS)
DB_TO_LINEAR_SCALE = 20.0 / 2.302585092994046
SMOOTHING_TIME_CONSTANT = 0.8
TEXTURE_HEIGHT = 1
FFT_ROW = 0
SHADER_UNIFORM_VEC2 = getattr(pr, "SHADER_UNIFORM_VEC2", 1)


@dataclass
class FFTData:
    prev_magnitudes: list[float] = field(default_factory=lambda: [0.0] * BUFFER_SIZE)
    fft_history: list[list[float]] = field(default_factory=list)
    fft_history_len: int = 0
    history_pos: int = 0
    tapback_pos: float = 0.01


def cooley_tukey_fft_slow(spectrum: list[complex]) -> None:
    n = len(spectrum)

    j = 0
    for i in range(1, n - 1):
        bit = n >> 1
        while j >= bit:
            j -= bit
            bit >>= 1
        j += bit
        if i < j:
            spectrum[i], spectrum[j] = spectrum[j], spectrum[i]

    length = 2
    while length <= n:
        angle = -2.0 * math.pi / length
        twiddle_unit = complex(math.cos(angle), math.sin(angle))

        for i in range(0, n, length):
            twiddle_current = 1.0 + 0.0j
            for k in range(length // 2):
                even = spectrum[i + k]
                odd = spectrum[i + k + length // 2]
                twiddled_odd = odd * twiddle_current

                spectrum[i + k] = even + twiddled_odd
                spectrum[i + k + length // 2] = even - twiddled_odd

                twiddle_current *= twiddle_unit

        length <<= 1


def capture_frame(fft_data: FFTData, audio_samples: list[float]) -> None:
    work_buffer = [0.0j] * FFT_WINDOW_SIZE

    for i in range(FFT_WINDOW_SIZE):
        x = (2.0 * math.pi * i) / (FFT_WINDOW_SIZE - 1.0)
        blackman_weight = 0.42 - 0.5 * math.cos(x) + 0.08 * math.cos(2.0 * x)
        work_buffer[i] = complex(audio_samples[i] * blackman_weight, 0.0)

    cooley_tukey_fft_slow(work_buffer)

    smoothed_spectrum = [0.0] * BUFFER_SIZE

    for bin_index in range(BUFFER_SIZE):
        value = work_buffer[bin_index]
        linear_magnitude = abs(value) / FFT_WINDOW_SIZE

        smoothed_magnitude = (
            SMOOTHING_TIME_CONSTANT * fft_data.prev_magnitudes[bin_index]
            + (1.0 - SMOOTHING_TIME_CONSTANT) * linear_magnitude
        )
        fft_data.prev_magnitudes[bin_index] = smoothed_magnitude

        db = math.log(max(smoothed_magnitude, 1e-40)) * DB_TO_LINEAR_SCALE
        normalized = (db - MIN_DECIBELS) * INVERSE_DECIBEL_RANGE
        smoothed_spectrum[bin_index] = max(0.0, min(1.0, normalized))

    fft_data.fft_history[fft_data.history_pos] = smoothed_spectrum
    fft_data.history_pos = (fft_data.history_pos + 1) % fft_data.fft_history_len


def render_frame(fft_data: FFTData, fft_image: pr.Image) -> None:
    frames_since_tapback = math.floor(fft_data.tapback_pos / WINDOW_TIME)
    frames_since_tapback = max(
        0, min(fft_data.fft_history_len - 1, frames_since_tapback)
    )

    history_position = (
        fft_data.history_pos - 1 - int(frames_since_tapback)
    ) % fft_data.fft_history_len

    amplitude = fft_data.fft_history[history_position]
    for bin_index in range(BUFFER_SIZE):
        color = pr.color_from_normalized(
            pr.Vector4(amplitude[bin_index], 0.0, 0.0, 0.0)
        )
        pr.image_draw_pixel(fft_image, bin_index, FFT_ROW, color)


def main() -> None:
    pr.init_window(
        SCREEN_WIDTH, SCREEN_HEIGHT, "raylib [audio] example - spectrum visualizer"
    )

    fft_image = pr.gen_image_color(BUFFER_SIZE, TEXTURE_HEIGHT, pr.WHITE)
    fft_texture = pr.load_texture_from_image(fft_image)
    buffer_a = pr.load_render_texture(SCREEN_WIDTH, SCREEN_HEIGHT)

    resources = Path(__file__).resolve().parent / "resources"
    shader_path = resources / "shaders" / "glsl330" / "fft.fs"
    shader = pr.load_shader("", str(shader_path))

    i_resolution_location = pr.get_shader_location(shader, "iResolution")
    i_channel0_location = pr.get_shader_location(shader, "iChannel0")

    i_resolution = pr.ffi.new("float[2]", [float(SCREEN_WIDTH), float(SCREEN_HEIGHT)])
    pr.set_shader_value(
        shader,
        i_resolution_location,
        i_resolution,
        SHADER_UNIFORM_VEC2,
    )
    pr.set_shader_value_texture(shader, i_channel0_location, fft_texture)

    pr.init_audio_device()
    pr.set_audio_stream_buffer_size_default(AUDIO_STREAM_RING_BUFFER_SIZE)

    wav = pr.load_wave(str(resources / "country.mp3"))
    pr.wave_format(wav, SAMPLE_RATE, PER_SAMPLE_BIT_DEPTH, MONO)

    audio_stream = pr.load_audio_stream(SAMPLE_RATE, PER_SAMPLE_BIT_DEPTH, MONO)
    pr.play_audio_stream(audio_stream)

    fft_history_len = math.ceil(FFT_HISTORICAL_SMOOTHING_DUR / WINDOW_TIME) + 1
    fft_data = FFTData(
        fft_history=[[0.0] * BUFFER_SIZE for _ in range(fft_history_len)],
        fft_history_len=fft_history_len,
    )

    wav_cursor = 0
    wav_pcm16 = pr.ffi.cast("short *", wav.data)

    chunk_samples = pr.ffi.new("short[]", AUDIO_STREAM_RING_BUFFER_SIZE)
    audio_samples = [0.0] * FFT_WINDOW_SIZE

    source_rect = pr.Rectangle(0.0, 0.0, float(SCREEN_WIDTH), float(-SCREEN_HEIGHT))
    source_pos = pr.Vector2(0.0, 0.0)

    pr.set_target_fps(60)

    while not pr.window_should_close():
        while pr.is_audio_stream_processed(audio_stream):
            for i in range(AUDIO_STREAM_RING_BUFFER_SIZE):
                if wav.channels == 2:
                    left = int(wav_pcm16[wav_cursor * 2])
                    right = int(wav_pcm16[wav_cursor * 2 + 1])
                else:
                    left = int(wav_pcm16[wav_cursor])
                    right = left

                chunk_samples[i] = int((left + right) / 2)

                wav_cursor += 1
                if wav_cursor >= wav.frameCount:
                    wav_cursor = 0

            pr.update_audio_stream(
                audio_stream, chunk_samples, AUDIO_STREAM_RING_BUFFER_SIZE
            )

            for i in range(FFT_WINDOW_SIZE):
                audio_samples[i] = (
                    (chunk_samples[i * 2] + chunk_samples[i * 2 + 1]) * 0.5 / 32767.0
                )

        capture_frame(fft_data, audio_samples)
        render_frame(fft_data, fft_image)
        pr.update_texture(fft_texture, fft_image.data)

        pr.begin_drawing()
        pr.clear_background(pr.RAYWHITE)

        pr.begin_shader_mode(shader)
        pr.set_shader_value_texture(shader, i_channel0_location, fft_texture)
        pr.draw_texture_rec(buffer_a.texture, source_rect, source_pos, pr.WHITE)
        pr.end_shader_mode()

        pr.end_drawing()

    pr.unload_shader(shader)
    pr.unload_render_texture(buffer_a)
    pr.unload_texture(fft_texture)
    pr.unload_image(fft_image)
    pr.unload_audio_stream(audio_stream)
    pr.unload_wave(wav)
    pr.close_audio_device()
    pr.close_window()


if __name__ == "__main__":
    main()
