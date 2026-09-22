
from fastapi import FastAPI, APIRouter, Depends

from app.api.deps import get_knowledge_base_service

from app.api.routers import documents, tickets

app = FastAPI(title="linemate", version="0.1.0")

router = APIRouter(dependencies=[Depends(get_knowledge_base_service)])

@router.get("/")
def health_check() -> dict[str, str]:
    return {"status": "Ok", "Service": "LineMate"}

app.include_router(documents.router)
app.include_router(tickets.router)