from typing import ClassVar

from app.models.enums import CrewStation

class CrewMember:
    registry: ClassVar[list["CrewMember"]] = []

    def __init__(self, id: int, name: str, station: CrewStation):
        self.id = id
        self.name = name
        self.station = station
        CrewMember.registry.append(self)