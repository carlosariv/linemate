import time
from fastapi import FastAPI, APIRouter, Depends, Request
from fastapi.responses import JSONResponse

from app.api.routers import documents, tickets, analytics, ask

API_KEY = "linemate-local-key"
PATHS_EXEMPT_FROM_AUTH = ["/", "/docs", "/openapi.json", "/redoc"]

app = FastAPI(title="linemate", version="0.1.0")

@app.middleware("http")
async def log_and_check_api_key(request: Request, call_next):
    start = time.perf_counter()

    if request.url.path not in PATHS_EXEMPT_FROM_AUTH:
        if request.headers.get("X-API-Key") != API_KEY:
            duration_ms = (time.perf_counter() - start) * 1000
            print(f"{request.method} {request.url} -> 401 {duration_ms:.1f}ms")
            return JSONResponse(
                status_code = 401,
                content = { "detail": "Missing or invalid X-API-Key header"}
            )

    response = await call_next(request)
    duration_ms = (time.perf_counter() - start) * 1000
    print(f"{request.method} {request.url} -> {response.status_code} {duration_ms:.1f}ms")
    return response

@app.get("/")
def health_check() -> dict[str, str]:
    return {"status": "Ok", "Service": "LineMate"}

app.include_router(documents.router)
app.include_router(tickets.router)
app.include_router(analytics.router)
app.include_router(ask.router)