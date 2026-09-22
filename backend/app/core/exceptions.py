
class DocumentLoadError(Exception):
    "Base Class: Error occured during the loading of a document file"

class UnsupportedFileTypeError(DocumentLoadError):
    "A file in docs/ folder is not a valid type that the loader can process"

class TicketLoadError(Exception):
    "Base Class: Error occured during the loading of a document file"