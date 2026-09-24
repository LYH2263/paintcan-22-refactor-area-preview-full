def opening_details(openings: list[dict]) -> list[dict]:
    """第一步：生成开洞全量明细，逐条记录尺寸与单洞面积，顺序与入参一致。

    全量明细是合计扣除与净面积的唯一计算依据，预览截断不得基于此步结果做减法。
    """
    details = []
    for i, o in enumerate(openings):
        w, h = float(o["w"]), float(o["h"])
        details.append({"index": i, "kind": o.get("kind"), "w": w, "h": h, "area_m2": w * h})
    return details


def area_from_details(length: float, width: float, height: float, details: list[dict]) -> dict:
    """第二步：基于全量明细计算毛面积、开洞扣除合计与净面积（钉选合计）。"""
    walls = 2 * (float(length) + float(width)) * float(height)
    hole = sum(float(d["area_m2"]) for d in details)
    net = max(0.0, walls - hole)
    return {"gross_m2": round(walls, 2), "openings_m2": round(hole, 2), "net_m2": round(net, 2)}


def preview_openings(details: list[dict], limit: int | None = None) -> list[dict]:
    """第三步：预览截断，只返回前 limit 条开洞供界面展示。

    截断仅影响展示列表长度，不回写到全量明细，因此不改变扣除合计与净面积。
    limit 为 None 或不小于全量条数时返回全量副本。
    """
    if limit is None:
        return [dict(d) for d in details]
    if limit <= 0:
        return []
    return [dict(d) for d in details[:limit]]


def wall_area(length: float, width: float, height: float, openings: list[dict]) -> dict:
    """兼容旧调用：全量明细 -> 合计，一步到位。"""
    details = opening_details(openings)
    return area_from_details(length, width, height, details)
