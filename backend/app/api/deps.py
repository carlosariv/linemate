from functools import lru_cache

from app.models.enums import TicketPriority, TicketStatus, CrewStation
from app.models import Document, Ticket, CrewMember
from app.ingestion.document_loader import load_documents_from_folder
from app.ingestion.ticket_loader import load_tickets_from_csv

class KnowledgeBaseService:
    def __init__(self, documents: list[Document], tickets: list[Ticket]):
        self._documents = documents
        self._tickets = tickets

    def get_all_documents(self) -> list[Document]:
        return self._documents

    def get_document_by_id(self, id: int) -> Document | None:
        for document in self._documents:
            if document.id == id:
                return document
        return None

    def get_stale_documents(self) -> list[Document]:
        stale: list[Document] = []
        for document in self._documents:
            if document.is_stale():
                stale.append(document)
        return stale

    def get_all_tickets(self) -> list[Ticket]:
        return self._tickets

    def get_ticket_by_id(self, id: int) -> Ticket | None:
        for ticket in self._tickets:
            if ticket.id == id:
                return ticket
        return None

def _seed_data():
    CrewMember(1, 'John D.', CrewStation.GRILL)
    CrewMember(2, 'Sal R.', CrewStation.GRILL)
    CrewMember(3, 'David M.', CrewStation.PASTRY)
    CrewMember(4, 'April G.', CrewStation.FRONT_OF_HOUSE)
    CrewMember(5, 'Kyle N.', CrewStation.GRILL)

@lru_cache
def get_knowledge_base_service() -> KnowledgeBaseService:
    documents = load_documents_from_folder('docs')
    tickets = load_tickets_from_csv('tickets.csv')
    _seed_data()
    return KnowledgeBaseService(documents, tickets)