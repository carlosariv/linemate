from datetime import date
from pathlib import Path

from app.models import Document, DocumentCategory
from app.core.exceptions import DocumentLoadError, UnsupportedFileTypeError

REQUIRED_FIELDS = ["id", "title", "category", "last_reviewed_at"]

def _parse_frontmatter(text: str, source: Path) -> tuple[dict[str, str], str]:
    if "---" not in text:
        raise DocumentLoadError(f"{source.name}: missing '---' frontmatter separator")

    header_block, _, body = text.partition('---')

    fields: dict[str, str] = {}

    for line in header_block.strip().splitlines():
        if ':' not in line:
            raise DocumentLoadError(f"{source.name}: malformed header line {line!r}")

        key, _, value = line.partition(':')
        fields[key.strip()] = value.strip()

    missing = [field for field in REQUIRED_FIELDS if field not in fields]

    if missing:
        raise DocumentLoadError('{source.name}: missing required field(s) {missing}')

    return (fields, body)


def load_one_document(path: Path) -> Document:
    if path.suffix != '.md':
        raise UnsupportedFileTypeError(f'unsupported file type {path.suffix} (only .md is supported)')

    text = path.read_text(encoding="utf-8")

    fields, body = _parse_frontmatter(text, path)

    try:
        category = DocumentCategory(fields['category'])
    except ValueError as exc:
        raise DocumentLoadError(f"{path.name}: unknown category {fields['category']!r}")

    try:
        last_reviewed_at = date.fromisoformat(fields['last_reviewed_at'])
    except ValueError as exc:
        raise DocumentLoadError(f'{path.name}: invalid last_reviewed_at date {fields['last_reviewed_at']}')

    try:
        id = int(fields['id'])
        owner_id = int(fields['owner_id'])
    except ValueError as exc:
        print(f'{path.name}: id and owner_id must be integers')

    return Document(
        id, fields['title'], category, body, owner_id, last_reviewed_at
    )

def load_documents_from_folder(folder_path: str | Path) -> list[Document]:
    folder = Path(folder_path)
    documents: list[Document] = []

    for path in sorted(folder.iterdir()):
        if path.is_dir():
            continue

        try:
            document = load_one_document(path)
            documents.append(document)
        except DocumentLoadError as exc:
            print(f'SKIPPED: {path.name} {exc}')

    return documents