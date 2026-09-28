
import pytest

from fastapi.testclient import TestClient

from app.api.main import app
from app.models import Document, Ticket, CrewMember
from app.api.deps import get_knowledge_base_service

AUTH_HEADERS = {"X-API-Key": "linemate-local-key"}

@pytest.fixture(autouse=True)
def reset_registries():

    yield
    Document.registry.clear()
    Ticket.registry.clear()
    CrewMember.registry.clear()

    get_knowledge_base_service.cache_clear()

@pytest.fixture
def client() -> TestClient:
    return TestClient(app)

@pytest.fixture
def auth_headers() -> dict[str, str]:
    return AUTH_HEADERS