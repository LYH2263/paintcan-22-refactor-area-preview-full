def build_area_detail(length: float, width: float, height: float, openings: list[dict]) -> dict:
    """全量开洞明细与面积合计（不做任何截断）。

    合计扣除 openings_m2 与净面积 net_m2 始终基于全量开洞计算，
    预览截断只能在本结果之上派生，不得反算合计。
    """
    walls = 2 * (float(length) + float(width)) * float(height)
    items = []
    hole = 0.0
    for i, o in enumerate(openings):
        w, h = float(o["w"]), float(o["h"])
        area = w * h
        hole += area
        items.append({"index": i, "w": w, "h": h, "area_m2": round(area, 2)})
    net = max(0.0, walls - hole)
    return {
        "gross_m2": round(walls, 2),
        "openings_m2": round(hole, 2),
        "net_m2": round(net, 2),
        "opening_count": len(items),
        "opening_items": items,
    }


def truncate_preview(detail: dict, limit: int | None = None) -> dict:
    """从全量明细派生开洞预览。

    只截断 openings_preview 列表；openings_m2 / net_m2 等合计字段
    原样钉选全量结果，不随预览长度变化。
    """
    items = detail["opening_items"]
    total = detail["opening_count"]
    if limit is None:
        k = total
    else:
        k = max(0, min(total, int(limit)))
    return {
        **{key: val for key, val in detail.items() if key != "opening_items"},
        "openings_preview": items[:k],
        "preview_count": k,
        "preview_truncated": k < total,
    }


def wall_area(length: float, width: float, height: float, openings: list[dict]) -> dict:
    d = build_area_detail(length, width, height, openings)
    return {"gross_m2": d["gross_m2"], "openings_m2": d["openings_m2"], "net_m2": d["net_m2"]}
