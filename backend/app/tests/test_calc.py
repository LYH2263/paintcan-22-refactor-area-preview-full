import pytest
from app.engines.estimate import estimate_room
from app.engines.paint_volume import paint_liters
from app.engines.wall_area import build_area_detail, truncate_preview, wall_area

OPENINGS = [{"w": 0.9, "h": 2.1}, {"w": 1.5, "h": 1.4}]

def test_living_room_net():
    a = wall_area(5, 4, 2.8, OPENINGS)
    assert a["gross_m2"] == 50.4
    assert a["net_m2"] == 46.41

def test_liters_two_coats():
    v = paint_liters(46.41, 8, 2)
    assert v["liters"] == 11.6

def test_estimate_combined():
    e = estimate_room(5, 4, 2.8, OPENINGS, 8, 2)
    assert e["liters"] == 11.6

def test_bad_coverage():
    with pytest.raises(ValueError):
        paint_liters(10, 0, 2)

def test_full_detail_has_every_opening():
    d = build_area_detail(5, 4, 2.8, OPENINGS)
    assert d["opening_count"] == 2
    assert [x["area_m2"] for x in d["opening_items"]] == [1.89, 2.1]
    assert d["openings_m2"] == 3.99
    assert d["net_m2"] == 46.41

def test_preview_truncation_keeps_totals_pinned():
    d = build_area_detail(5, 4, 2.8, OPENINGS)
    p = truncate_preview(d, 1)
    assert len(p["openings_preview"]) == 1
    assert p["preview_count"] == 1
    assert p["preview_truncated"] is True
    # 截断不改变合计扣除与净面积
    assert p["openings_m2"] == d["openings_m2"] == 3.99
    assert p["net_m2"] == d["net_m2"] == 46.41

def test_limit_above_full_returns_all():
    d = build_area_detail(5, 4, 2.8, OPENINGS)
    p = truncate_preview(d, 10)
    assert len(p["openings_preview"]) == 2
    assert p["preview_truncated"] is False

def test_estimate_preview_limit_does_not_change_liters():
    full = estimate_room(5, 4, 2.8, OPENINGS, 8, 2)
    short = estimate_room(5, 4, 2.8, OPENINGS, 8, 2, preview_limit=1)
    assert len(short["openings_preview"]) == 1
    assert short["preview_truncated"] is True
    # 上限小于全量时预览变短，但净面积/扣除合计/升数钉选不变
    assert short["net_m2"] == full["net_m2"] == 46.41
    assert short["openings_m2"] == full["openings_m2"] == 3.99
    assert short["liters"] == full["liters"] == 11.6
