from functools import lru_cache

from app.models.enums import TicketPriority, TicketStatus, CrewStation, DocumentCategory
from app.models import Document, Ticket, CrewMember
from app.ingestion.document_loader import load_documents_from_folder
from app.ingestion.ticket_loader import load_tickets_from_csv
from app.api.schemas import WorkloadReport
from app.analytics.workload import compute_station_workload
from app.analytics.ownership import compute_document_ownership

class KnowledgeBaseService:
    def __init__(self, documents: list[Document], tickets: list[Ticket], crew_members: list[CrewMember]):
        self._documents = documents
        self._tickets = tickets
        self._crew_members = crew_members

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
            if document.category != DocumentCategory.INCIDENT_REPORT and document.is_stale():
                stale.append(document)
        return stale

    def get_all_tickets(self) -> list[Ticket]:
        return self._tickets

    def get_ticket_by_id(self, id: int) -> Ticket | None:
        for ticket in self._tickets:
            if ticket.id == id:
                return ticket
        return None

    def get_all_crew_members(self) -> list[CrewMember]:
        return self._crew_members

    def get_crew_member_by_id(self, id: int) -> CrewMember | None:
        for crew_member in self._crew_members:
            if crew_member.id == id:
                return crew_member
        return None

    def get_station_mismatches(self) -> list[tuple[Ticket, Document, CrewMember, CrewMember]]:
        mismatches: list[tuple[Ticket, Document, CrewMember, CrewMember]] = []
        for ticket in self._tickets:
            document = self.get_document_by_id(ticket.related_document_id)
            assignee = self.get_crew_member_by_id(ticket.assignee_id)
            if document is None or assignee is None:
                continue

            owner = self.get_crew_member_by_id(document.owner_id)
            if owner is None:
                continue

            if assignee.station != owner.station:
                mismatches.append((ticket, document, assignee, owner))
        return mismatches

    def get_station_workload_report(self) -> dict:
        return compute_station_workload(self._tickets, self._crew_members)

    def get_document_ownership_report(self) -> dict:
        return compute_document_ownership(self._documents, self._crew_members)


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
    return KnowledgeBaseService(Document.registry, Ticket.registry, CrewMember.registry)