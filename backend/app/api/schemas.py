from pydantic import BaseModel, ConfigDict

from app.models import DocumentCategory, Ticket, TicketStatus, TicketPriority

class DocumentOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    title: str
    category: DocumentCategory
    days_since_last_reviewed: int
    owner_id: int

class DocumentPage(BaseModel):
    id: int

class StaleDocumentOut(BaseModel):
    id: int
    title: str
    category: str
    days_since_last_reviewed: int

class TicketOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    title: str
    status: TicketStatus
    priority: TicketPriority
    assignee_id: int
    related_document_id: int