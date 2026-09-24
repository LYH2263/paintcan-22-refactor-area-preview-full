from app.engines.paint_volume import paint_liters
from app.engines.wall_area import build_area_detail, truncate_preview


def area_breakdown(length, width, height, openings, preview_limit=None):
    """步骤一+二：先生成全量面积明细，再按需截断预览。

    全量明细用于合计扣除与净面积；预览仅返回前若干条开洞。
    返回中的合计与净面积不受 preview_limit 影响。
    """
    detail = build_area_detail(length, width, height, openings)
    return truncate_preview(detail, preview_limit)


def estimate_room(length, width, height, openings, coverage, coats, preview_limit=None):
    area = area_breakdown(length, width, height, openings, preview_limit)
    # 升数始终基于全量净面积（截断只影响预览列表）。
    vol = paint_liters(area["net_m2"], coverage, coats)
    return {**area, **vol}
