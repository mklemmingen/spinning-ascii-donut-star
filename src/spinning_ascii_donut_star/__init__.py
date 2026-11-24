"""A spinning 3D donut-style star in your terminal, rendered as ASCII art."""

from .render import render_frame
from .cli import spin

__all__ = ["render_frame", "spin"]
__version__ = "0.1.0"
