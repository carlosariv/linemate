from datetime import timedelta, date

from fastapi import APIRouter, Depends, status, Query, HTTPException

from app.models import Document
from app.api.schemas import DocumentOut, StaleDocumentOut, DocumentPage
from app.api.deps import KnowledgeBaseService, get_knowledge_base_service
from app.api.security import require_api_key

router = APIRouter(
    prefix="/documents",
    tags=["documents"],
    dependencies=[Depends(require_api_key)]
)

@router.get("", response_model=DocumentPage, status_code=status.HTTP_200_OK)
def list_documents(
    skip: int = Query(0, ge=0, desription="Number of documents to skip"),
    limit: int = Query(10, ge=1, le=100, description = "Max number of documents to return"),
    service: KnowledgeBaseService = Depends(get_knowledge_base_service),
) -> list[DocumentOut]:
    all_documents = service.get_all_documents()

    page = all_documents[skip: skip + limit]

    return DocumentPage(
        items = [DocumentOut.model_validate(document) for document in page],
        total = len(all_documents),
        skip = skip,
        limit = limit
    )

@router.get("/stale", response_model=list[StaleDocumentOut])
def list_stale_documents(
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

@router.get("/{document_id}", response_model=DocumentOut)
def get_document(
    document_id: int,
    service: KnowledgeBaseService = Depends(get_knowledge_base_service)
) -> DocumentOut | None:
    document = service.get_document_by_id(document_id)
    if document is None:
        raise HTTPException(
            status_code = status.HTTP_404_NOT_FOUND,
            detail = f"No document with id {document_id}"
        )
    else:
        return DocumentOut.model_validate(document)

