import pytest
from app.engines.estimate import estimate_room
from app.engines.paint_volume import paint_liters
from app.engines.wall_area import (
    area_from_details,
    opening_details,
    preview_openings,
    wall_area,
)

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


def test_steps_separable():
    # 三个步骤可单独调用：全量明细 -> 合计 -> 预览截断。
    details = opening_details(OPENINGS)
    assert [d["area_m2"] for d in details] == [1.89, 2.1]
    assert area_from_details(5, 4, 2.8, details)["net_m2"] == 46.41
    assert len(preview_openings(details, 1)) == 1
    assert len(preview_openings(details, None)) == 2
    assert preview_openings(details, 0) == []


def test_preview_truncation_keeps_totals():
    many = [{"kind": "door", "w": 0.9, "h": 2.1},
            {"kind": "window", "w": 1.8, "h": 1.5},
            {"kind": "window", "w": 1.2, "h": 1.5}]
    full = estimate_room(4, 3.2, 2.8, many, 8, 2)
    short = estimate_room(4, 3.2, 2.8, many, 8, 2, preview_limit=1)

    # 截断后预览变短，但净面积、开洞扣除合计与升数钉选不变。
    assert full["openings_count"] == 3
    assert len(short["openings_preview"]) == 1
    assert short["preview_truncated"] is True
    assert full["preview_truncated"] is False
    assert short["net_m2"] == full["net_m2"]
    assert short["openings_m2"] == full["openings_m2"]
    assert short["liters"] == full["liters"]

    # 原有数值仍保持：毛 40.32，洞 1.89+2.7+1.8=6.39，净 33.93，双遍 8.48 升。
    assert full["openings_m2"] == 6.39
    assert full["net_m2"] == 33.93
    assert full["liters"] == 8.48

    # 预览条目面积之和不得被当成全量扣除。
    preview_sum = sum(d["area_m2"] for d in short["openings_preview"])
    assert preview_sum < short["openings_m2"]


def test_limit_greater_than_total_returns_all():
    e = estimate_room(5, 4, 2.8, OPENINGS, 8, 2, preview_limit=99)
    assert len(e["openings_preview"]) == 2
    assert e["preview_truncated"] is False
