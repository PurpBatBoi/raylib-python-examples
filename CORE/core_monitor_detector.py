from __future__ import annotations

from dataclasses import dataclass

import pyray as pr

# Version checked: raylib 5.x/pyray API parity (reviewed 2026-02-28).

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 450
KEY_ENTER = getattr(pr, "KEY_ENTER", 257)
MAX_MONITORS = 10


@dataclass
class MonitorInfo:
    """Store monitor information used by the detector view."""

    position: pr.Vector2
    name: str
    width: int
    height: int
    physical_width: int
    physical_height: int
    refresh_rate: int


def main() -> None:
    """Run the monitor detector example."""
    pr.init_window(
        SCREEN_WIDTH,
        SCREEN_HEIGHT,
        "raylib [core] example - monitor detector",
    )

    current_monitor_index = pr.get_current_monitor()
    pr.set_target_fps(60)

    while not pr.window_should_close():
        max_width = 1
        max_height = 1
        monitor_offset_x = 0

        monitor_count = min(pr.get_monitor_count(), MAX_MONITORS)
        monitors: list[MonitorInfo] = []
        for i in range(monitor_count):
            info = MonitorInfo(
                position=pr.get_monitor_position(i),
                name=pr.get_monitor_name(i),
                width=pr.get_monitor_width(i),
                height=pr.get_monitor_height(i),
                physical_width=pr.get_monitor_physical_width(i),
                physical_height=pr.get_monitor_physical_height(i),
                refresh_rate=pr.get_monitor_refresh_rate(i),
            )
            monitors.append(info)

            if info.position.x < monitor_offset_x:
                monitor_offset_x = -int(info.position.x)

            width = int(info.position.x) + info.width
            height = int(info.position.y) + info.height
            max_width = max(max_width, width)
            max_height = max(max_height, height)

        if pr.is_key_pressed(KEY_ENTER) and monitor_count > 1:
            current_monitor_index += 1
            if current_monitor_index == monitor_count:
                current_monitor_index = 0
            pr.set_window_monitor(current_monitor_index)
        else:
            current_monitor_index = pr.get_current_monitor()

        monitor_scale = 0.6
        if max_height > (max_width + monitor_offset_x):
            monitor_scale *= float(SCREEN_HEIGHT) / float(max_height)
        else:
            monitor_scale *= float(SCREEN_WIDTH) / float(max_width + monitor_offset_x)

        pr.begin_drawing()
        pr.clear_background(pr.RAYWHITE)
        pr.draw_text(
            "Press [Enter] to move window to next monitor available",
            20,
            20,
            20,
            pr.DARKGRAY,
        )
        pr.draw_rectangle_lines(
            20, 60, SCREEN_WIDTH - 40, SCREEN_HEIGHT - 100, pr.DARKGRAY
        )

        for i, monitor in enumerate(monitors):
            rec = pr.Rectangle(
                (monitor.position.x + monitor_offset_x) * monitor_scale + 140.0,
                monitor.position.y * monitor_scale + 80.0,
                monitor.width * monitor_scale,
                monitor.height * monitor_scale,
            )

            pr.draw_text(
                f"[{i}] {monitor.name}",
                int(rec.x) + 10,
                int(rec.y + 100 * monitor_scale),
                int(120 * monitor_scale),
                pr.BLUE,
            )
            pr.draw_text(
                f"Resolution: [{monitor.width}px x {monitor.height}px]\n"
                f"RefreshRate: [{monitor.refresh_rate}hz]\n"
                f"Physical Size: [{monitor.physical_width}mm x {monitor.physical_height}mm]\n"
                f"Position: {monitor.position.x:3.0f} x {monitor.position.y:3.0f}",
                int(rec.x) + 10,
                int(rec.y + 200 * monitor_scale),
                int(120 * monitor_scale),
                pr.DARKGRAY,
            )

            if i == current_monitor_index:
                pr.draw_rectangle_lines_ex(rec, 5.0, pr.RED)
                window_pos = pr.get_window_position()
                pr.draw_rectangle_v(
                    pr.Vector2(
                        (window_pos.x + monitor_offset_x) * monitor_scale + 140.0,
                        window_pos.y * monitor_scale + 80.0,
                    ),
                    pr.Vector2(
                        SCREEN_WIDTH * monitor_scale, SCREEN_HEIGHT * monitor_scale
                    ),
                    pr.fade(pr.GREEN, 0.5),
                )
            else:
                pr.draw_rectangle_lines_ex(rec, 5.0, pr.GRAY)

        pr.end_drawing()

    pr.close_window()


if __name__ == "__main__":
    main()
