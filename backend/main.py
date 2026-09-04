from pathlib import Path

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from backend.lru_cache import LRUCache
from backend.models import CacheGetResponse, CacheStateResponse, PutRequest, ResetRequest

BASE_DIR = Path(__file__).resolve().parent.parent
FRONTEND_DIR = BASE_DIR / "frontend"

app = FastAPI(title="LRU Cache Visualizer API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

cache = LRUCache(5)


def set_cache_capacity(capacity: int | None):
    global cache
    if capacity is None:
        return

    if capacity <= 0:
        raise HTTPException(status_code=400, detail="Capacity must be greater than 0")

    cache = LRUCache(capacity)


@app.get("/health")
def health_check():
    return {"status": "ok"}


@app.post("/cache/put")
def put_item(payload: PutRequest):
    set_cache_capacity(payload.capacity)
    cache.put(payload.key, payload.value)
    return cache.state()


@app.get("/cache/get/{key}", response_model=CacheGetResponse)
def get_item(key: str):
    value = cache.get(key)
    if value is None:
        return {"key": key, "value": None, "hit": False}
    return {"key": key, "value": value, "hit": True}


@app.get("/cache/state", response_model=CacheStateResponse)
def get_state():
    return cache.state()


@app.post("/cache/reset")
def reset_cache(payload: ResetRequest | None = None):
    global cache
    capacity = payload.capacity if payload and payload.capacity is not None else cache.cap
    if capacity <= 0:
        raise HTTPException(status_code=400, detail="Capacity must be greater than 0")

    cache = LRUCache(capacity)
    return cache.state()


app.mount("/", StaticFiles(directory=str(FRONTEND_DIR), html=True), name="frontend")
