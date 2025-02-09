from __future__ import annotations
import contextlib
import mimetypes
from collections.abc import Generator
from io import BufferedReader, BytesIO
from pathlib import PurePath
from typing import Any, Literal, Optional, Union, cast, List
from pydantic import ConfigDict, Field, field_validator, model_validator
from langchain_core.load.serializable import Serializable
import json
import os
import re

class BaseMedia(Serializable):
    """Use to represent media content.

    Media objects can be used to represent raw data, such as text or binary data.

    LangChain Media objects allow associating metadata and an optional identifier
    with the content.

    The presence of an ID and metadata make it easier to store, index, and search
    over the content in a structured way.
    """

    # The ID field is optional at the moment.
    # It will likely become required in a future major release after
    # it has been adopted by enough vectorstore implementations.
    id: Optional[str] = None
    """An optional identifier for the document.

    Ideally this should be unique across the document collection and formatted
    as a UUID, but this will not be enforced.

    .. versionadded:: 0.2.11
    """

    metadata: dict = Field(default_factory=dict)
    """Arbitrary metadata associated with the content."""

    @field_validator("id", mode="before")
    def cast_id_to_str(cls, id_value: Any) -> Optional[str]:
        if id_value is not None:
            return str(id_value)
        else:
            return id_value




class CameraDocument(BaseMedia):
    """Class for storing a piece of text and associated metadata.

    Example:

        .. code-block:: python

            from langchain_core.documents import Document

            document = Document(
                page_content="Hello, world!",
                metadata={"source": "https://example.com"}
            )
    """

    metadata: dict = Field(default_factory=dict)  # 기본값: 빈 딕셔너리
    parsing_result: str = "No parsing result"     # 기본값: 문자열
    # chunking_result: list = Field(default_factory=list)  # 기본값: 빈 리스트
    embedding_result: list = Field(default_factory=list)  # 기본값: 빈 리스트
    """String text."""
    type: Literal["Document"] = "Document"

    def __init__(self, **kwargs: Any) -> None:
        """Pass page_content in as positional or named arg."""
        # my-py is complaining that page_content is not defined on the base class.
        # Here, we're relying on pydantic base class to handle the validation.
        super().__init__( **kwargs)  # type: ignore[call-arg]

    def load_json(self, json_path):
        with open(json_path, "r", encoding="utf-8") as file:
            json_data = json.load(file)
            self.parsing_result= json_data["parsing_result"]
            self.metadata = json_data['metadata']
    
    def load_json_with_vector(self, json_path):
        with open(json_path, "r", encoding="utf-8") as file:
            json_data = json.load(file)
            self.parsing_result= json_data["parsing_result"]
            self.metadata = json_data['metadata']
            self.embedding_result = json_data['embedding_result']

    def save_json(self, save_path):
        with open(save_path, "w", encoding="utf-8") as file:
            doc2dict = {
                'parsing_result': self.parsing_result,
                'embedding_result': self.embedding_result,
                'metadata': self.metadata
            }
            json.dump(doc2dict, file, ensure_ascii=False, indent=4)
        print(f"{save_path} complete")

    @classmethod
    def is_lc_serializable(cls) -> bool:
        """Return whether this class is serializable."""
        return True

    @classmethod
    def get_lc_namespace(cls) -> list[str]:
        """Get the namespace of the langchain object."""
        return ["langchain", "schema", "document"]

    def __str__(self) -> str:
        """Override __str__ to restrict it to page_content and metadata."""
        # The format matches pydantic format for __str__.
        #
        # The purpose of this change is to make sure that user code that
        # feeds Document objects directly into prompts remains unchanged
        # due to the addition of the id field (or any other fields in the future).
        #
        # This override will likely be removed in the future in favor of
        # a more general solution of formatting content directly inside the prompts.
        return "만드는중"
        # if self.metadata:
        #     return f"page_content='{self.page_content}' metadata={self.metadata}"
        # else:
        #     return f"page_content='{self.page_content}'"

class CameraDocumentCollection():
    """Class for managing a collection of CameraDocument objects."""

    documents: List[CameraDocument] = []  # 기본값: 빈 리스트

    def add_document(self, document: CameraDocument) -> None:
        """Add a new CameraDocument to the collection."""
        self.documents.append(document)

    def remove_document(self, index: int) -> None:
        """Remove a CameraDocument from the collection by index."""
        if 0 <= index < len(self.documents):
            del self.documents[index]
        else:
            raise IndexError("Invalid index for document removal.")

    def get_document(self, index: int) -> CameraDocument:
        """Retrieve a CameraDocument from the collection by index."""
        if 0 <= index < len(self.documents):
            return self.documents[index]
        else:
            raise IndexError("Invalid index for document retrieval.")

    def search_documents(self, keyword: str) -> List[CameraDocument]:
        """Search for documents containing a specific keyword in page_content."""
        return [
            doc for doc in self.documents
            if keyword.lower() in doc.page_content.lower()
        ]

    def list_metadata(self) -> List[Dict[str, Any]]:
        """List the metadata of all documents."""
        return [doc.metadata for doc in self.documents]

    def summarize_collection(self) -> str:
        """Provide a summary of the collection."""
        total_docs = len(self.documents)
        return f"This collection contains {total_docs} document(s)."

    def clear_collection(self) -> None:
        """Remove all documents from the collection."""
        self.documents.clear()

# Example usage
if __name__ == "__main__":
    doc1 = CameraDocument(page_content="This is a test document.", metadata={"author": "Alice"})
    doc2 = CameraDocument(page_content="Another document with text.", metadata={"author": "Bob"})

    collection = CameraDocumentCollection()
    collection.add_document(doc1)
    collection.add_document(doc2)

    print(collection.summarize_collection())
    results = collection.search_documents("test")
    for doc in results:
        print(doc.page_content)

    collection.remove_document(0)
    print(collection.summarize_collection())