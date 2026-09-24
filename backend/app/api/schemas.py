from datetime import date

from pydantic import BaseModel, ConfigDict

from app.models import DocumentCategory, Ticket, TicketStatus, TicketPriority

class DocumentOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    title: str
    category: DocumentCategory
    owner_id: int
    last_reviewed_at: date

class DocumentPage(BaseModel):
    items: list[DocumentOut]
    total: int
    skip: int
    limit: int

class TicketPage(BaseModel):
    items: list[TicketOut]
    total: int
    limit: int
    skip: int

class TicketOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    title: str
    status: TicketStatus
    priority: TicketPriority
    assignee_id: int
    related_document_id: int

class StaleDocumentOut(BaseModel):
    id: int
    title: str
    category: str
    days_since_last_reviewed: int

class MismatchOut(BaseModel):
    ticket_id: int
    ticket_title: str
    assignee_name: str
    assignee_station: str
    owner_name: str
    owner_station: str
    