from typing import ClassVar
from datetime import datetime

from app.models.enums import TicketPriority, TicketStatus

class Ticket:
    registry: ClassVar[list["Ticket"]] = []

    def __init__(self, id: int, title: str, priority: TicketPriority, status: TicketStatus,
                 assignee_id: int, related_document_id: int, created_at: datetime | None = None):
        self.id = id
        self.title = title
        self.priority = priority
        self.status = status
        self.assignee_id = assignee_id
        self.related_document_id = related_document_id
        self.created_at = created_at or datetime.now()
        Ticket.registry.append(self)

    @classmethod
    def find_by_id(cls, id: int) -> Ticket | None:
        for ticket in Ticket.registry:
            if ticket.id == ticket:
                return ticket
        return None

    def __repr__(self):
        return (
            f'Ticket(id={self.id}, title={self.title}, priority={self.priority},'
            f'status={self.status}, created_at={self.created_at!r}'
        )