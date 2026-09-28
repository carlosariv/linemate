from fastapi import APIRouter, Depends, status, HTTPException, Query

from app.models import Document
from app.api.schemas import DocumentOut, TicketOut, TicketPage, MismatchOut
from app.api.deps import KnowledgeBaseService, get_knowledge_base_service
from app.api.security import require_api_key

router = APIRouter(
    prefix='/tickets',
    tags=['tickets'],
    dependencies=[Depends(require_api_key)]
)

@router.get('', response_model=TicketPage, status_code=status.HTTP_200_OK)
def list_tickets(
    skip: int = Query(0, ge=0, desription="Number of tickets to skip"),
    limit: int = Query(10, ge=1, le=100, description = "Max tickets to return"),
    service: KnowledgeBaseService = Depends(get_knowledge_base_service)
) -> TicketPage:
    all_tickets = service.get_all_tickets()
    page = all_tickets[skip: skip + limit]

    return TicketPage(
        items = [TicketOut.model_validate(ticket) for ticket in page],
        total = len(all_tickets),
        limit = limit,
        skip = skip
    )

@router.get("/mismatches", response_model=list[MismatchOut])
def get_station_mismtaches(
    service: KnowledgeBaseService = Depends(get_knowledge_base_service)
) -> list[MismatchOut]:
    mismatches = service.get_station_mismatches()

    return [
        MismatchOut(
            ticket_id = mismatch[0].id,
            ticket_title = mismatch[0].title,
            assignee_name = mismatch[2].name,
            assignee_station = mismatch[2].station,
            owner_name = mismatch[3].name,
            owner_station = mismatch[3].station
        ) for mismatch in mismatches
    ]

@router.get("/{ticket_id}", response_model=TicketOut)
def get_ticket(
    ticket_id: int,
    service: KnowledgeBaseService = Depends(get_knowledge_base_service)
) -> TicketOut | None:
    ticket = service.get_ticket_by_id(ticket_id)
    if ticket is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No ticket with id {ticket_id}"
        )

    return TicketOut(
        id = ticket.id,
        title = ticket.title,
        status = ticket.status,
        priority = ticket.priority,
        assignee_id = ticket.assignee_id,
        related_document_id = ticket.related_document_id
    )

