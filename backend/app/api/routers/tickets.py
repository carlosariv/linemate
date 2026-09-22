from fastapi import APIRouter, Depends

from app.models import Document
from app.api.schemas import DocumentOut, TicketOut

from app.api.deps import KnowledgeBaseService, get_knowledge_base_service

from datetime import timedelta, date

router = APIRouter(
    prefix='/tickets',
    tags=['tickets']
)

@router.get('', response_model=list[TicketOut])
def get_all_tickets(
    service: KnowledgeBaseService = Depends(get_knowledge_base_service)
) -> list[TicketOut]:
    return [
        TicketOut(
            id=ticket.id,
            title=ticket.title,
            status=ticket.status,
            priority=ticket.priority,
            assignee_id=ticket.assignee_id,
            related_document_id=ticket.related_document_id
        ) for ticket in service.get_all_tickets()
    ]

@router.get('/{ticket_id}', response_model=TicketOut)
def get_ticket(
    ticket_id: int,
    service: KnowledgeBaseService = Depends(get_knowledge_base_service)
) -> TicketOut | None:
    ticket = service.get_ticket_by_id(ticket_id)
    if ticket:
        return TicketOut(
            id = ticket.id,
            title = ticket.title,
            status = ticket.status,
            priority = ticket.priority,
            assignee_id = ticket.assignee_id,
            related_document_id = ticket.related_document_id
        )
    return None