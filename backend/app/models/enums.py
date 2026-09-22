
from enum import Enum

class CrewStation(str, Enum):
    GRILL = 'Grill'
    PASTRY = 'Pastry'
    PREP = 'Prep'
    FRONT_OF_HOUSE = 'Front Of House'

class DocumentCategory(str, Enum):
    RECIPE = 'Recipe'
    SOP = 'SOP'
    INCIDENT_REPORT = 'Incident Report'
    ONBOARDING = 'Onboarding'

class TicketPriority(str, Enum):
    LOW = 'Low'
    MEDIUM = 'Medium'
    HIGH = 'High'
    CRITICAL = 'Critical'

class TicketStatus(str, Enum):
    OPEN = 'Open'
    IN_PROGRESS = 'In-Progress'
    RESOLVED = 'Resolved'
    Closed = 'Closed'
