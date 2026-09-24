from app.engines.paint_volume import paint_liters
from app.engines.wall_area import (
    area_from_details,
    opening_details,
    preview_openings,
)


def estimate_room(length, width, height, openings, coverage, coats, preview_limit=None):
    # 步骤一：开洞全量明细；步骤二：以全量明细钉选合计扣除与净面积。
    details = opening_details(openings)
    area = area_from_details(length, width, height, details)
    vol = paint_liters(area["net_m2"], coverage, coats)
    # 步骤三：预览仅做截断展示，不参与上面任何合计与升数计算。
    preview = preview_openings(details, preview_limit)
    return {
        **area,
        **vol,
        "openings_count": len(details),
        "openings_detail": details,
        "openings_preview": preview,
        "preview_truncated": len(preview) < len(details),
    }
