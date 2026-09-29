from langchain_chroma import Chroma
from langchain_core.documents import Document as LCDocument
from langchain_ollama import OllamaEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter

from app.models import Document

CHUNK_SIZE = 500
CHUNK_OVERLAP = 50
EMBEDDING_MODEL = "nomic-embed-text"
PERSIST_DIRECTORY = "chroma_db"

_splitter = RecursiveCharacterTextSplitter(
    chunk_size=CHUNK_SIZE,
    chunk_overlap=CHUNK_OVERLAP
)

_embeddings = OllamaEmbeddings(model=EMBEDDING_MODEL)

def _document_to_metadata(document: Document) -> dict:
    return {
        "id": document.id,
        "title": document.title,
        "category": document.category.value,
        "last_reviewed_at": document.last_reviewed_at.isoformat()
    }

def documents_to_chunk(documents: list[Document]) -> list[LCDocument]:
    lc_documents = [
        LCDocument(page_content=document.body, metadata=_document_to_metadata(document))
        for document in documents
    ]

    return _splitter.split_documents(lc_documents)

def build_vector_store(documents: list[Document], persist_directory: str = PERSIST_DIRECTORY) -> Chroma:
    chunks = documents_to_chunk(documents)

    return Chroma.from_documents(
        documents=chunks,
        embedding=_embeddings,
        persist_directory=persist_directory
    )

def load_vector_store(persist_directory: str = PERSIST_DIRECTORY) -> Chroma:
    return Chroma(
        persist_directory=persist_directory,
        embedding_function=_embeddings
    )

def search_documents(
        query: str, k: int = 3, category: str | None = None
) -> list[LCDocument]:
    vector_store=load_vector_store()
    if category is not None:
        return vector_store.similarity_search(query, k=k, filter={"category": category})
    return vector_store.similarity_search(query, k=k)