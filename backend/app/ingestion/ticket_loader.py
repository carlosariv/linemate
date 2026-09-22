from pathlib import Path
from csv import DictReader

from app.models.enums import TicketPriority, TicketStatus
from app.models import Ticket
from app.core.exceptions import TicketLoadError

def _row_to_ticket(row: dict[str, str]) -> Ticket:
    try:
        priority = TicketPriority(row.get('priority'))
    except ValueError as exc:
        raise TicketLoadError(f'row {row['id']}: Invalid priority: {row['priority']!r}') from exc

    try:
        status = TicketStatus(row['status'])
    except ValueError as exc:
        raise TicketLoadError(f'row {row['id']}: Invalid status: {row['status']!r}') from exc

    try:
        ticket_id = int(row['id'])
        assignee_id = int(row['assignee_id'])
        related_document_id = (
            int(row['related_document_id']) if row['related_document_id'] else None
        )
    except ValueError as exc:
       raise TicketLoadError(f'row {row['id']}: id, assignee_id and related_document_id must be integers') 

    return Ticket(ticket_id, row['title'], priority, status, assignee_id, related_document_id)

def load_tickets_from_csv(csv_path: str | Path) -> list[Ticket]:
    tickets: list[Ticket] = []
    with open(csv_path, encoding = "utf-8", newline="") as handle:
        reader = DictReader(handle)
        for row in reader:
            try:
                tickets.append(_row_to_ticket(row))
            except TicketLoadError as exc:
                print(f'SKIPPED {exc}')

    return tickets