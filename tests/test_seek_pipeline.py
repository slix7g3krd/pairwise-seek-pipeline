import pytest
from audio import seek_pipeline as mod

CASES = [
    ("seek_after", 'm.seek_position(5, 3) == 5'),
    ("seek_before", 'm.seek_position(2, 3) == 3'),
    ("timestamp", 'm.timestamp_reset(10, 5) == 15'),
    ("fade", 'm.fade_curve(0.5, 1.0) == approx(0.5)'),
    ("buffer", 'm.buffer_clear([1, 2]) == []'),
    ("timebase", 'm.timebase_convert(1, 1, 2) == approx(0.5)'),
    ("preroll", 'm.preroll_drop([0, 1, 2], 1) == [1, 2]'),
    ("multitrack", 'm.multitrack_seek([1, 2], 5) == [5, 5]'),
    ("confirm_ready", 'm.async_confirm("ready", 10) == 10'),
    ("confirm_pending", 'm.async_confirm("pending", 10) == -1'),
    ("merge", 'm.merge_requests([1, 3, 2]) == 3'),
    ("clock", 'm.av_clock(10, 8) == 2'),
    ("cache", 'm.cache_isolation("a", "b") == "a:b"'),
    ("subtitle", 'm.subtitle_sync(1, 5) == 6'),
    ("buffer_clock", 'm.buffer_clock(10, True) == 0')
]

@pytest.mark.parametrize("name,expr", CASES, ids=[c[0] for c in CASES])
def test_contract(name, expr):
    assert eval(expr, {"m": mod, "approx": pytest.approx})
