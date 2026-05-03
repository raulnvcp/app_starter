from pathlib import Path
from io import BytesIO

from markitdown import MarkItDown, StreamInfo
from pydantic import Field


def binary_document_to_markdown(binary_data: bytes, file_type: str) -> str:
    """Converts binary document data to markdown-formatted text."""
    md = MarkItDown()
    file_obj = BytesIO(binary_data)
    stream_info = StreamInfo(extension=file_type)
    result = md.convert(file_obj, stream_info=stream_info)
    return result.text_content


SUPPORTED_EXTENSIONS = {".pdf", ".docx"}


def document_path_to_markdown(
    file_path: str = Field(description="Absolute or relative path to a PDF or DOCX file to convert"),
) -> str:
    """Converts a PDF or DOCX file at a given path to markdown.

    Reads the file from disk, detects the format from its extension (.pdf or .docx),
    and converts the contents to markdown text using MarkItDown.

    Use this tool when you have a local file path and need its contents as markdown.
    Do not use for URLs or binary data already in memory — use the appropriate tool instead.

    Examples:
        document_path_to_markdown("/reports/summary.pdf")
        -> "# Summary\\n\\nThis report covers..."

        document_path_to_markdown("./docs/spec.docx")
        -> "# Specification\\n\\n## Overview\\n..."
    """
    path = Path(file_path)

    ext = path.suffix.lower()
    if ext not in SUPPORTED_EXTENSIONS:
        raise ValueError(
            f"Unsupported file type '{ext}'. Supported extensions: {', '.join(sorted(SUPPORTED_EXTENSIONS))}"
        )

    if not path.exists():
        raise ValueError(f"File not found: {file_path}")

    binary_data = path.read_bytes()
    return binary_document_to_markdown(binary_data, ext.lstrip("."))
