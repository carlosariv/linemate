
from dataclasses import dataclass, field

from langchain_core.messages import AIMessage, BaseMessage, HumanMessage
from langchain_core.runnables import RunnablePassthrough
from langchain_core.documents import Document as LCDocument
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_ollama import ChatOllama

from app.rag.retriever import (
    DEFAULT_K,
    format_retrieved_context,
    get_similarity_retriever,
)

_llm = ChatOllama(
    model="llama3.2",
    base_url="http://localhost:11434",
    temperature=0.0
)

_rag_prompt = ChatPromptTemplate.from_messages([
    (
        "system",
        "You are LineMate, an internal engineering assistant for a restaurant team."
        "Answer the engineer's question using ONLY the context below - "
        "do not use any outside knowledge, and do not invent details that"
        "aren't in the context. If the context doesn't contain enough"
        "information to answer the question, say so plainly instead of"
        "guessing. \n\nContext:\n{context}",
    ),
    (
        "human", "{question}",
    )
])

rag_answer_chain = _rag_prompt | _llm | StrOutputParser()

_rag_prompt_with_history = ChatPromptTemplate.from_messages([
    (
        "system",
        "You are LineMate, an internal engineering assistant for a restaurant team. "
        "Answer the engineer's question using ONLY the context below - "
        "do not use any outside knowledge, and do not invent details that "
        "aren't in the context. If the context does not contain enough information "
        "to answer the question, say so plainly instead of guessing. \n\nContext:\n{context}\n"
        "Summary of context so far (empty if this is the first question): {summary}"
    ),
    MessagesPlaceholder("recent_messages"),
    ("human", "{question}")
])

rag_answer_chain_with_history = _rag_prompt_with_history | _llm | StrOutputParser()

@dataclass
class AskResult:
    answer: str
    sources: list[str]

def _citation_titles(documents: list[LCDocument]) -> list[str]:
    seen: set[str] = set()
    titles: list[str] = []

    for document in documents:
        title = document.metadata["title"]
        if title not in seen:
            seen.add(title)
            titles.append(title)

    return titles

def _retrieve(input_dict: dict) -> list[LCDocument]:
    retriever = get_similarity_retriever(k=DEFAULT_K)
    documents = retriever.invoke(input_dict["question"])
    return documents


def answer_question(question: str, k: int = DEFAULT_K) -> AskResult:
    """
    The full RAG path: retreive, format, generate, cite. Always calls the llm,
    even if the retrieved context turns out to be a weak match(because we are using
    the get_similarity_retriever)
    """
    retriever = get_similarity_retriever(k=k)
    documents = retriever.invoke(question)
    context = format_retrieved_context(documents)
    answer = rag_answer_chain.invoke({"context": context, "question": question})
    return AskResult(answer=answer, sources=_citation_titles(documents))


retrieval_chain = (
    RunnablePassthrough.assign(documents=_retrieve)
    | RunnablePassthrough.assign(context=lambda x: format_retrieved_context(x["documents"]))
    | RunnablePassthrough.assign(answer=rag_answer_chain_with_history)
)

@dataclass
class ConversationMemory:
    summary: str = ""
    recent_messages: list[BaseMessage] = field(default_factory=list)


MAX_RECENT_MESSAGES = 4

_summary_prompt = ChatPromptTemplate.from_messages([
    (
        "system",
        "Summarize the conversation below in 2-3 sentences, preserving "
        "anything factual an engineer would need to answer a follow-up question. "
        "If an existing summary is given, build on it rather than starting over from"
        " nothing. Write only the summary itself - do not mention whether a summary "
        "already exists or comment on these instructions. \n\n Existing summary (empty "
        "if there isn't one yet): {existing_summary}"
    ),
    MessagesPlaceholder("messages_to_summarize"),
    ("human", "Summarize the conversation above, following the instructions given.")
])

summarization_chain = _summary_prompt | _llm | StrOutputParser()

def record_message(memory: ConversationMemory, question: str, answer: str) -> None:
    memory.recent_messages.append(HumanMessage(content=question))
    memory.recent_messages.append(AIMessage(content=answer))

    if len(memory.recent_messages) > MAX_RECENT_MESSAGES:
        overflow = memory.recent_messages[:-MAX_RECENT_MESSAGES]
        memory.recent_messages[-MAX_RECENT_MESSAGES:]
        memory.summary = summarization_chain.invoke({
            "existing_summary": memory.summary,
            "messages_to_summarize": overflow,
        })

def ask_with_memory(memory: ConversationMemory, question: str) -> AskResult:
    result = retrieval_chain.invoke({
        "question": question,
        "summary": memory.summary,
        "recent_messages": memory.recent_messages
    })

    record_message(memory, question, result["answer"])
    return AskResult(answer=result["answer"], sources=_citation_titles(result["documents"]))

_conversations: dict[str, ConversationMemory] = {}

def get_conversation_memory(id: str) -> ConversationMemory:
    if id not in _conversations:
        _conversations[id] = ConversationMemory()
    return _conversations[id]