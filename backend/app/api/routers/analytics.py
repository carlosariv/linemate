from fastapi import APIRouter, Depends

from app.api.deps import KnowledgeBaseService, get_knowledge_base_service
from app.api.security import require_api_key
from app.api.schemas import WorkloadReport, OwnershipReport

router = APIRouter(
    prefix="/analytics",
    tags=["analytics"],
    dependencies=[Depends(require_api_key)]
)

@router.get("/workload", response_model=WorkloadReport)
def get_station_workload(
    service: KnowledgeBaseService = Depends(get_knowledge_base_service)
) -> WorkloadReport:
    report = service.get_station_workload_report()
    return WorkloadReport(**report)

@router.get("/ownership", response_model=OwnershipReport)
def get_document_ownership(
    service: KnowledgeBaseService = Depends(get_knowledge_base_service)
) -> OwnershipReport:
    report = service.get_document_ownership_report()
    return OwnershipReport(**report)
