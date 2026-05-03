import os
import shutil
import pytest
from tools.document import binary_document_to_markdown, document_path_to_markdown


class TestBinaryDocumentToMarkdown:
    # Define fixture paths
    FIXTURES_DIR = os.path.join(os.path.dirname(__file__), "fixtures")
    DOCX_FIXTURE = os.path.join(FIXTURES_DIR, "mcp_docs.docx")
    PDF_FIXTURE = os.path.join(FIXTURES_DIR, "mcp_docs.pdf")

    def test_fixture_files_exist(self):
        """Verify test fixtures exist."""
        assert os.path.exists(self.DOCX_FIXTURE), (
            f"DOCX fixture not found at {self.DOCX_FIXTURE}"
        )
        assert os.path.exists(self.PDF_FIXTURE), (
            f"PDF fixture not found at {self.PDF_FIXTURE}"
        )

    def test_binary_document_to_markdown_with_docx(self):
        """Test converting a DOCX document to markdown."""
        # Read binary content from the fixture
        with open(self.DOCX_FIXTURE, "rb") as f:
            docx_data = f.read()

        # Call function
        result = binary_document_to_markdown(docx_data, "docx")

        # Basic assertions to check the conversion was successful
        assert isinstance(result, str)
        assert len(result) > 0
        # Check for typical markdown formatting - this will depend on your actual test file
        assert "#" in result or "-" in result or "*" in result

    def test_binary_document_to_markdown_with_pdf(self):
        """Test converting a PDF document to markdown."""
        # Read binary content from the fixture
        with open(self.PDF_FIXTURE, "rb") as f:
            pdf_data = f.read()

        # Call function
        result = binary_document_to_markdown(pdf_data, "pdf")

        # Basic assertions to check the conversion was successful
        assert isinstance(result, str)
        assert len(result) > 0
        # Check for typical markdown formatting - this will depend on your actual test file
        assert "#" in result or "-" in result or "*" in result


class TestDocumentPathToMarkdown:
    FIXTURES_DIR = os.path.join(os.path.dirname(__file__), "fixtures")
    DOCX_FIXTURE = os.path.join(FIXTURES_DIR, "mcp_docs.docx")
    PDF_FIXTURE = os.path.join(FIXTURES_DIR, "mcp_docs.pdf")

    def test_convert_docx(self):
        result = document_path_to_markdown(self.DOCX_FIXTURE)
        assert isinstance(result, str)
        assert len(result) > 0
        assert "#" in result or "-" in result or "*" in result

    def test_convert_pdf(self):
        result = document_path_to_markdown(self.PDF_FIXTURE)
        assert isinstance(result, str)
        assert len(result) > 0
        assert "#" in result or "-" in result or "*" in result

    def test_content_validation_pdf(self):
        """Result contains known text from the fixture file."""
        result = document_path_to_markdown(self.PDF_FIXTURE)
        assert "Model Context Protocol" in result

    def test_content_validation_docx(self):
        """Result contains known text from the fixture file."""
        result = document_path_to_markdown(self.DOCX_FIXTURE)
        assert "Model Context Protocol" in result

    def test_result_is_not_only_whitespace(self):
        result = document_path_to_markdown(self.PDF_FIXTURE)
        assert result.strip()

    def test_file_not_found(self):
        with pytest.raises(ValueError, match="File not found"):
            document_path_to_markdown("/nonexistent/path/file.pdf")

    def test_empty_string_path(self):
        with pytest.raises(ValueError):
            document_path_to_markdown("")

    def test_unsupported_extension(self):
        with pytest.raises(ValueError, match="Unsupported file type"):
            document_path_to_markdown(os.path.join(self.FIXTURES_DIR, "file.txt"))

    @pytest.mark.parametrize("ext", [".png", ".xlsx", ".csv"])
    def test_unsupported_extensions(self, ext):
        with pytest.raises(ValueError, match="Unsupported file type"):
            document_path_to_markdown(os.path.join(self.FIXTURES_DIR, f"file{ext}"))

    def test_relative_path(self):
        """Relative paths are resolved correctly."""
        rel_path = os.path.join("tests", "fixtures", "mcp_docs.pdf")
        result = document_path_to_markdown(rel_path)
        assert isinstance(result, str)
        assert result.strip()

    def test_path_with_spaces(self, tmp_path):
        """Paths containing spaces are handled without error."""
        dest = tmp_path / "my docs" / "mcp docs.pdf"
        dest.parent.mkdir()
        shutil.copy(self.PDF_FIXTURE, dest)
        result = document_path_to_markdown(str(dest))
        assert isinstance(result, str)
        assert result.strip()

    def test_uppercase_pdf_extension(self, tmp_path):
        """Extension matching is case-insensitive (.PDF treated as .pdf)."""
        dest = tmp_path / "mcp_docs.PDF"
        shutil.copy(self.PDF_FIXTURE, dest)
        result = document_path_to_markdown(str(dest))
        assert isinstance(result, str)
        assert result.strip()

    def test_uppercase_docx_extension(self, tmp_path):
        """Extension matching is case-insensitive (.DOCX treated as .docx)."""
        dest = tmp_path / "mcp_docs.DOCX"
        shutil.copy(self.DOCX_FIXTURE, dest)
        result = document_path_to_markdown(str(dest))
        assert isinstance(result, str)
        assert result.strip()
