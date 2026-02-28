from __future__ import annotations

from datetime import datetime

import pyray as pr

# Version checked: raylib 5.x/pyray API parity (reviewed 2026-02-28).

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 450

# Keep a strong reference so CFFI callback is not garbage-collected.
TRACE_LOG_CALLBACK_CDATA = None


def custom_trace_log(msg_type: int, text: str) -> None:
    """Print raylib logs with timestamp and level prefix."""
    time_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    level = {
        int(getattr(pr, "LOG_INFO", 2)): "[INFO] : ",
        int(getattr(pr, "LOG_ERROR", 4)): "[ERROR]: ",
        int(getattr(pr, "LOG_WARNING", 3)): "[WARN] : ",
        int(getattr(pr, "LOG_DEBUG", 1)): "[DEBUG]: ",
    }.get(msg_type, "")
    print(f"[{time_str}] {level}{text}")


def _custom_trace_log_c(msg_type: int, text_ptr: object, _args_ptr: object) -> None:
    """CFFI-compatible callback bridge for raylib trace logging."""
    text = ""
    if text_ptr != pr.ffi.NULL:
        text = pr.ffi.string(text_ptr).decode("utf-8", errors="replace")
    custom_trace_log(msg_type, text)


def main() -> None:
    """Run the custom logging example."""
    global TRACE_LOG_CALLBACK_CDATA

    if hasattr(pr, "set_trace_log_callback"):
        TRACE_LOG_CALLBACK_CDATA = pr.ffi.callback("void(int, char *, void *)")(
            _custom_trace_log_c
        )
        pr.set_trace_log_callback(TRACE_LOG_CALLBACK_CDATA)

    pr.init_window(
        SCREEN_WIDTH,
        SCREEN_HEIGHT,
        "raylib [core] example - custom logging",
    )
    pr.set_target_fps(60)

    while not pr.window_should_close():
        pr.begin_drawing()
        pr.clear_background(pr.RAYWHITE)
        pr.draw_text(
            "Check out the console output to see the custom logger in action!",
            60,
            200,
            20,
            pr.LIGHTGRAY,
        )
        pr.end_drawing()

    pr.close_window()


if __name__ == "__main__":
    main()
