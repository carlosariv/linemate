from fastapi import APIRouter, Depends

from app.models import Document
from app.api.schemas import DocumentOut, StaleDocumentOut

from app.api.deps import KnowledgeBaseService, get_knowledge_base_service

from datetime import timedelta, date

router = APIRouter(
    prefix="/documents",
    tags=["documents"],
)

@router.get("", response_model=list[DocumentOut])
def get_documents(service: KnowledgeBaseService = Depends(get_knowledge_base_service)) -> list[DocumentOut]:
    all_documents = service.get_all_documents()

    return [
        DocumentOut(
            id = document.id,
            title = document.title,
            category = document.category,
            owner_id = document.owner_id,
            days_since_reviewed = (date.today() - document.last_reviewed_at).days
        ) for document in all_documents
    ]

@router.get("/{document_id}", response_model=DocumentOut)
def get_document(
    document_id: int,
    service: KnowledgeBaseService = Depends(get_knowledge_base_service)
) -> DocumentOut | None:
    document = service.get_document_by_id(document_id)
    if document:
        return DocumentOut(
            id = document.id,
            title = document.title,
            category = document.category,
            days_since_last_reviewed = document.days_since_last_reviewed(),
            owner_id = document.owner_id
        )
    return None

@router.get("/stale", response_model=list[StaleDocumentOut])
def get_stale_documents(
    service: KnowledgeBaseService = Depends(get_knowledge_base_service)
) -> list[StaleDocumentOut]:
    stale_documents = service.get_stale_documents()
    return [
        StaleDocumentOut(
            id = document.id,
            title = document.title,
            category = document.category,
            days_since_last_reviewed = document.days_since_last_reviewed()
        ) for document in stale_documents
    ]