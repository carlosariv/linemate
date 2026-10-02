from fastapi import APIRouter, Depends

from app.api.deps import KnowledgeBaseService, get_knowledge_base_service
from app.api.security import require_api_key
from app.api.schemas import AskRequest, AskConversationRequest, AskResponse
from app.rag.qa_chain import answer_question, ask_with_memory, get_conversation_memory

router = APIRouter(
    prefix="/ask",
    tags=["ask"],
    dependencies=[Depends(require_api_key)]
)

@router.post("/", response_model=AskResponse)
def get_answer(request: AskRequest) -> AskResponse:
    result = answer_question(request.question)
    return AskResponse(answer=result.answer, sources=result.sources)
    

@router.post("/conversation", response_model=AskResponse)
def get_answer_conversation(request: AskConversationRequest) -> AskResponse:
    memory = get_conversation_memory(request.conversation_id)
    result = ask_with_memory(memory, request.question)
    return AskResponse(answer=result.answer, sources=result.sources)