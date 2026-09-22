from datetime import date

class Comment:
    def __init__(self, id: int, ticket_id: int, author_id: int, body: str, created_at: date):
        self.id = id
        self.ticket_id = ticket_id
        self.author_id = author_id
        self.body = body
        self.created_at = created_at