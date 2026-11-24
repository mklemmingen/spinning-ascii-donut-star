"""Terminal animation and command-line entry point."""

import argparse
import math
import sys
import time

from .render import render_frame


def spin(duration: float = 0.0, fps: int = 20, width: int = 70, height: int = 35,
         speed: float = 0.04, color: bool = True, *, points: int = 5, ring: bool = True,
         hub: bool = True, chars: str = ".,:;oO0Q@#") -> None:
    """Spin the star in the terminal. ``duration`` 0 runs until Ctrl+C."""
    out = sys.stdout
    A, B = math.pi / 2, 0.0
    frame_time = 1.0 / fps
    start = time.time()
    out.write("\033[?25l\033[2J")  # hide cursor, clear screen
    try:
        while duration <= 0 or time.time() - start < duration:
            t0 = time.time()
            frame = "\n".join(render_frame(A, B, width, height, points=points, ring=ring, hub=hub, chars=chars))
            if color:
                frame = "\033[97m" + frame + "\033[0m"
            out.write("\033[H" + frame + "\n")
            out.flush()
            B = (B + speed) % (2 * math.pi)
            time.sleep(max(0.0, frame_time - (time.time() - t0)))
    except KeyboardInterrupt:
        pass
    finally:
        out.write("\033[?25h\n")
        out.flush()


def main(argv=None) -> None:
    p = argparse.ArgumentParser(prog="spinning-ascii-donut-star",
                                description="A spinning 3D donut-style star in ASCII.")
    p.add_argument("-d", "--duration", type=float, default=0.0, help="seconds to run (0 = until Ctrl+C)")
    p.add_argument("-f", "--fps", type=int, default=20, help="frames per second (default 20)")
    p.add_argument("-W", "--width", type=int, default=70, help="width in characters (default 70)")
    p.add_argument("-H", "--height", type=int, default=35, help="height in characters (default 35)")
    p.add_argument("-s", "--speed", type=float, default=0.04, help="radians per frame (default 0.04)")
    p.add_argument("-p", "--points", type=int, default=5, help="number of star points (default 5)")
    p.add_argument("--no-ring", action="store_true", help="leave out the outer ring")
    p.add_argument("--no-hub", action="store_true", help="leave out the centre sphere")
    p.add_argument("-c", "--chars", default=".,:;oO0Q@#", help="shading ramp, dim to bright (min 4 chars)")
    p.add_argument("--no-color", action="store_true", help="plain output without ANSI colour")
    a = p.parse_args(argv)
    if a.points < 1:
        p.error("--points must be at least 1")
    if len(a.chars) < 4:
        p.error("--chars needs at least 4 characters")
    spin(a.duration, a.fps, a.width, a.height, a.speed, not a.no_color,
         points=a.points, ring=not a.no_ring, hub=not a.no_hub, chars=a.chars)


if __name__ == "__main__":
    main()
