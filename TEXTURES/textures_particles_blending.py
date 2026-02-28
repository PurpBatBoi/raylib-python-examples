from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

import pyray as pr

# Version checked: raylib 5.x/pyray API parity (reviewed 2026-02-28).

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 450
MAX_PARTICLES = 200

KEY_SPACE = getattr(pr, "KEY_SPACE", 32)
BLEND_ALPHA = getattr(pr, "BLEND_ALPHA", 0)
BLEND_ADDITIVE = getattr(pr, "BLEND_ADDITIVE", 1)


@dataclass
class Particle:
    """Particle state for tail rendering."""

    position: pr.Vector2
    color: pr.Color
    alpha: float
    size: float
    rotation: float
    active: bool


def main() -> None:
    """Run particle blending mode example."""
    pr.init_window(
        SCREEN_WIDTH, SCREEN_HEIGHT, "raylib [textures] example - particles blending"
    )

    particles: list[Particle] = []
    for _ in range(MAX_PARTICLES):
        particles.append(
            Particle(
                position=pr.Vector2(0.0, 0.0),
                color=pr.Color(
                    pr.get_random_value(0, 255),
                    pr.get_random_value(0, 255),
                    pr.get_random_value(0, 255),
                    255,
                ),
                alpha=1.0,
                size=float(pr.get_random_value(1, 30)) / 20.0,
                rotation=float(pr.get_random_value(0, 360)),
                active=False,
            )
        )

    gravity = 3.0
    resources = Path(__file__).resolve().parent / "resources"
    smoke = pr.load_texture(str(resources / "spark_flame.png"))
    blending = BLEND_ALPHA

    source = pr.Rectangle(0.0, 0.0, float(smoke.width), float(smoke.height))

    pr.set_target_fps(60)

    while not pr.window_should_close():
        for particle in particles:
            if not particle.active:
                particle.active = True
                particle.alpha = 1.0
                particle.position = pr.get_mouse_position()
                break

        for particle in particles:
            if particle.active:
                particle.position.y += gravity / 2.0
                particle.alpha -= 0.005
                particle.rotation += 2.0
                if particle.alpha <= 0.0:
                    particle.active = False

        if pr.is_key_pressed(KEY_SPACE):
            blending = BLEND_ADDITIVE if blending == BLEND_ALPHA else BLEND_ALPHA

        pr.begin_drawing()
        pr.clear_background(pr.DARKGRAY)
        pr.begin_blend_mode(blending)

        for particle in particles:
            if not particle.active:
                continue

            width = smoke.width * particle.size
            height = smoke.height * particle.size
            dest = pr.Rectangle(particle.position.x, particle.position.y, width, height)
            origin = pr.Vector2(width / 2.0, height / 2.0)
            pr.draw_texture_pro(
                smoke,
                source,
                dest,
                origin,
                particle.rotation,
                pr.fade(particle.color, particle.alpha),
            )

        pr.end_blend_mode()
        pr.draw_text("PRESS SPACE to CHANGE BLENDING MODE", 180, 20, 20, pr.BLACK)
        if blending == BLEND_ALPHA:
            pr.draw_text("ALPHA BLENDING", 290, SCREEN_HEIGHT - 40, 20, pr.BLACK)
        else:
            pr.draw_text("ADDITIVE BLENDING", 280, SCREEN_HEIGHT - 40, 20, pr.RAYWHITE)
        pr.end_drawing()

    pr.unload_texture(smoke)
    pr.close_window()


if __name__ == "__main__":
    main()
