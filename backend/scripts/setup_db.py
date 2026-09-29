from app.ingestion.document_loader import load_documents_from_folder

from app.rag.vector_store import build_vector_store, search_documents

def main() -> None:
    documents = load_documents_from_folder("docs")
    vector_store = build_vector_store(documents)

    question = "how can i handle raw meat?"
    search_results = search_documents(question)
    for document in search_results:
        print(f"SEARCH: {document}")

if __name__ == "__main__":
    main()