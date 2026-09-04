from pydantic import BaseModel
from typing import Any


class PutRequest(BaseModel):
    key: str
    value: Any


class ResetRequest(BaseModel):
    capacity: int | None = None


class CacheGetResponse(BaseModel):
    key: str
    value: Any | None = None
    hit: bool


class CacheStateResponse(BaseModel):
    capacity: int
    size: int
    items: list[dict[str, Any]]
    hits: int
    misses: int
    hit_rate: float
    evictions: int
