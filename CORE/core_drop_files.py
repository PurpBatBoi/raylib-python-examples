from __future__ import annotations

import pyray as pr

# Version checked: raylib 5.x/pyray API parity (reviewed 2026-02-28).

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 450
MAX_FILEPATH_RECORDED = 4096


def main() -> None:
    """Run the drop-files example."""
    pr.init_window(SCREEN_WIDTH, SCREEN_HEIGHT, "raylib [core] example - drop files")

    file_paths: list[str] = []
    pr.set_target_fps(60)

    while not pr.window_should_close():
        if pr.is_file_dropped():
            dropped_files = pr.load_dropped_files()
            try:
                for i in range(int(dropped_files.count)):
                    if len(file_paths) >= MAX_FILEPATH_RECORDED - 1:
                        break
                    path_ptr = dropped_files.paths[i]
                    if path_ptr != pr.ffi.NULL:
                        path = pr.ffi.string(path_ptr).decode("utf-8", errors="replace")
                        file_paths.append(path)
            finally:
                pr.unload_dropped_files(dropped_files)

        pr.begin_drawing()
        pr.clear_background(pr.RAYWHITE)

        if not file_paths:
            pr.draw_text("Drop your files to this window!", 100, 40, 20, pr.DARKGRAY)
        else:
            pr.draw_text("Dropped files:", 100, 40, 20, pr.DARKGRAY)
            for i, path in enumerate(file_paths):
                alpha = 0.5 if i % 2 == 0 else 0.3
                pr.draw_rectangle(
                    0, 85 + 40 * i, SCREEN_WIDTH, 40, pr.fade(pr.LIGHTGRAY, alpha)
                )
                pr.draw_text(path, 120, 100 + 40 * i, 10, pr.GRAY)
            pr.draw_text(
                "Drop new files...", 100, 110 + 40 * len(file_paths), 20, pr.DARKGRAY
            )

        pr.end_drawing()

    pr.close_window()


if __name__ == "__main__":
    main()
