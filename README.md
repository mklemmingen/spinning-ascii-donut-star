# spinning-ascii-donut-star

A spinning 3D star in your terminal, rendered as z-buffered ASCII art in the style of `donut.c`. The star is built from tapered spokes, an optional torus ring and an optional hub sphere, each with surface normals and lighting. You choose the number of points. Pure Python, no dependencies.

```bash
pip install spinning-ascii-donut-star
spinning-ascii-donut-star                 # five points with ring, Ctrl+C to stop
spinning-ascii-donut-star -p 8 --no-ring  # eight-pointed star, no ring
spinning-ascii-donut-star -p 6 -c " .:-=+*#%@" -d 10
```

```python
import math
from spinning_ascii_donut_star import render_frame, spin

print("\n".join(render_frame(math.pi / 2, 0.6, width=60, height=30, points=6)))
spin(duration=5, points=4, ring=False)
```

| Option | Default | |
|---|---|---|
| `-p, --points` | 5 | number of star points |
| `--no-ring` / `--no-hub` | | leave out the outer ring or the centre sphere |
| `-c, --chars` | `.,:;oO0Q@#` | shading ramp, dim to bright (at least 4 characters) |
| `-d, --duration` | 0 | seconds to run (0 = until Ctrl+C) |
| `-f, --fps` | 20 | frames per second |
| `-W, --width` / `-H, --height` | 70 / 35 | size in characters |
| `-s, --speed` | 0.04 | rotation in radians per frame |
| `--no-color` | | plain output without ANSI colour |
