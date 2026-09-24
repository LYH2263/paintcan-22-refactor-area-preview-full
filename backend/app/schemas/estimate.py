from pydantic import BaseModel
class EstimateRequest(BaseModel):
    room_id: int
    coats: int | None = None
    coverage: float | None = None
    preview_limit: int | None = None
    persist: bool = True
