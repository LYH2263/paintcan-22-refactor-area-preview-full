from pydantic import BaseModel, Field


class EstimateRequest(BaseModel):
    room_id: int
    coats: int | None = None
    coverage: float | None = None
    persist: bool = True
    # 预览开洞条数上限；None 或不小于全量条数时返回全量，小于时预览截断但合计不变。
    preview_limit: int | None = Field(default=None, ge=0)
