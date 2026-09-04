# LRU Cache Visualizer

A small Python + FastAPI + JavaScript app that demonstrates how a Least Recently Used cache behaves in real time.

## Features

- O(1)-style LRU access using a hash map + doubly linked list
- REST API for PUT, GET, state, and reset
- Browser-based visual ordering of items from LRU to MRU
- Hit rate, miss counting, and eviction tracking
- Dockerized backend and frontend setup

## Run locally

### Backend

```bash
cd /Users/likhith/Documents/lru-cache-visualizer
. .venv/bin/activate
uvicorn backend.main:app --host 0.0.0.0 --port 8000 --reload
```

Then open the frontend in a browser or serve it with a static file host.

### Docker

```bash
docker compose up --build
```

Then visit:

- Frontend: http://localhost:8080
- Backend API: http://localhost:8000

## API

- POST /cache/put
- GET /cache/get/{key}
- GET /cache/state
- POST /cache/reset

## Testing

```bash
cd /Users/likhith/Documents/lru-cache-visualizer
. .venv/bin/activate
pytest -q
```
# lru-cache-visualizer
