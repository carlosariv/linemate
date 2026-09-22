from datetime import date
from typing import ClassVar

from app.models.enums import DocumentCategory

class Document:
    registry: ClassVar[list["Document"]] = []

    def __init__(self, id: int, title: str, category: DocumentCategory, body: str, owner_id: int, last_reviewed_at: date | None = None):
        self.id = id
        self.title = title
        self.category = category
        self.body = body
        self.owner_id = owner_id
        self.last_reviewed_at = last_reviewed_at or date.today()
        Document.registry.append(self)

    def days_since_last_reviewed(self):
        return (date.today() - self.last_reviewed_at).days

    def is_stale(self, threshold: int = 90) -> bool:
        return self.days_since_last_reviewed() > threshold

    @classmethod
    def find_by_id(cls, id: int) -> "Document | None":
        for document in Document.registry:
            if document.id == id:
                return document
        return None

    def __repr__(self):
        return (
            f'Document(id={self.id}, title={self.title}, category={self.category},'
            f'last_reviewed_at={self.last_reviewed_at!r}'
        )