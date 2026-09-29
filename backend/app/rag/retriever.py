from langchain_core.documents import Document as LCDocument
from app.rag.vector_store import load_vector_store

DEFAULT_K = 4

def format_retrieved_context(documents: list[LCDocument]) -> str:
    return "\n\n".join(
        f"[Source: {document.metadata["title"]}\n{document.page_content}]"
        for document in documents
    )

def get_similarity_retriever(k: int = DEFAULT_K, category: str | None = None):
    vector_store = load_vector_store()

    search_kwargs: dict = {"k": k}
    if category is not None:
        search_kwargs["filter"] = {"category": category}

    return vector_store.as_retriever(search_type="similarity", search_kwargs=search_kwargs)