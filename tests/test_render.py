import math

import pytest

from spinning_ascii_donut_star import render_frame

FACE = math.pi / 2


def filled(lines):
    return sum(c != " " for line in lines for c in line)


def test_frame_shape_and_content():
    lines = render_frame(FACE, 0.0, width=40, height=20)
    assert len(lines) == 20
    assert all(len(line) == 40 for line in lines)
    assert filled(lines) > 100


def test_rotation_changes_frame():
    assert render_frame(FACE, 0.0, 40, 20) != render_frame(FACE, 1.0, 40, 20)


def test_points_change_the_shape():
    assert render_frame(FACE, 0.3, 40, 20, points=3) != render_frame(FACE, 0.3, 40, 20, points=7)


def test_ring_and_hub_can_be_left_out():
    full = filled(render_frame(FACE, 0.3, 40, 20))
    assert filled(render_frame(FACE, 0.3, 40, 20, ring=False)) < full
    assert filled(render_frame(FACE, 0.3, 40, 20, ring=False, hub=False)) > 0


def test_custom_chars_are_used():
    lines = render_frame(FACE, 0.3, 40, 20, chars="abcd")
    assert set("".join(lines)) <= set("abcd ")


@pytest.mark.parametrize("kwargs", [{"points": 0}, {"chars": "ab"}])
def test_invalid_arguments(kwargs):
    with pytest.raises(ValueError):
        render_frame(FACE, 0.0, 40, 20, **kwargs)
