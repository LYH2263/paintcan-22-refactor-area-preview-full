from app.db import connect
from app.engines.estimate import estimate_room
from app.repositories import openings, rooms, runs, settings

# 钉选落库的字段：合计、净面积、升数均以全量开洞明细计算，与预览截断无关。
_PINNED_KEYS = (
    "gross_m2", "openings_m2", "net_m2", "liters", "coats", "coverage",
    "openings_count", "openings_detail",
)


class PaintService:
    def __init__(self): self._c = connect()
    def close(self): self._c.close()
    def __enter__(self): return self
    def __exit__(self, *a): self.close()
    def list_rooms(self): return rooms.list_all(self._c)
    def room_detail(self, rid):
        r = rooms.get(self._c, rid)
        if not r: return None
        return {"room": r, "openings": openings.for_room(self._c, rid)}
    def settings(self): return settings.get_map(self._c)
    def history(self, limit=50): return runs.list_recent(self._c, limit)
    def estimate(self, room_id, persist, coats=None, coverage=None, preview_limit=None):
        detail = self.room_detail(room_id)
        if not detail: return None
        r = detail["room"]
        cov, ct = settings.coverage_coats(self._c)
        cov = float(coverage or cov)
        ct = int(coats or ct)
        ops = [{"w": o["w"], "h": o["h"], "kind": o.get("kind")} for o in detail["openings"]]
        result = estimate_room(r["length"], r["width"], r["height"], ops, cov, ct, preview_limit)

        # persist 时只落钉选结果（含全量明细），绝不能把截断预览当成全量扣除。
        pinned = {k: result[k] for k in _PINNED_KEYS}
        rid = runs.insert(
            self._c, "estimate",
            {"room_id": room_id, "coats": ct, "coverage": cov, "preview_limit": preview_limit},
            pinned, room_id,
        ) if persist else None
        # 回包：钉选合计不变，开洞列表只给截断后的预览。
        return {
            "run_id": rid,
            "room_id": room_id,
            "gross_m2": result["gross_m2"],
            "openings_m2": result["openings_m2"],
            "net_m2": result["net_m2"],
            "liters": result["liters"],
            "coats": result["coats"],
            "coverage": result["coverage"],
            "openings_count": result["openings_count"],
            "openings_preview": result["openings_preview"],
            "preview_truncated": result["preview_truncated"],
        }
    def dashboard(self):
        rs = rooms.list_all(self._c)
        return {"room_count": len(rs), "clean": len([x for x in rs if "种子" not in x["name"] and "多种" not in x["name"]]), "dirty": len([x for x in rs if "多种" in x["name"]])}
