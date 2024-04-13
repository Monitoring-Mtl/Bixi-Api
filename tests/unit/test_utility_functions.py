import pytest

from trips.repository import create_segments

@pytest.mark.parametrize("minStartTimeMs, maxStartTimeMs, segment_length_ms, expected", [
    (0, 86400000, 86400000, [(0, 86399999)]),
    (0, 172800000, 86400000, [(0, 86399999), (86400000, 172799999)]),
    (0, 100000000, 86400000, [(0, 86399999), (86400000, 100000000)]),
    (100000, 100000, 86400000, []),
    (100000, 86400100, 86400000, [(100000, 86400100)]),
    (500000, 172800000, 86400000, [(500000, 86899999), (86900000, 172800000)]),
    (-100000, 100000, 86400000, [(-100000, 100000)]),
])
def test_create_segments(minStartTimeMs, maxStartTimeMs, segment_length_ms, expected):
    assert create_segments(minStartTimeMs, maxStartTimeMs, segment_length_ms) == expected

def test_zero_segment_length():
    with pytest.raises(ValueError):
        create_segments(0, 86400000, 0)
