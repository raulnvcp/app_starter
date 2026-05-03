
# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Commands

```bash
# Start the MCP server
uv run main.py

# Run all tests
uv run pytest

# Run a single test
uv run pytest tests/test_document.py::test_binary_document_to_markdown_with_pdf

# Install dependencies (after cloning)
uv venv && source .venv/bin/activate
uv pip install -e .
```

## Architecture

This is a **FastMCP server** — a Python MCP server that exposes tools to AI assistants.

- `main.py` — entry point: creates the `FastMCP` instance, imports tools, registers them, and calls `mcp.run()`
- `tools/` — one module per domain (e.g. `math.py`, `document.py`); each module contains plain Python functions
- `tests/` — pytest tests with `tests/fixtures/` for binary test data (DOCX, PDF)

### Registering a new tool

Define a function in `tools/`, then register it in `main.py`:

```python
mcp.tool()(my_function)
```

### Tool definition conventions (from README)

Tools must follow this pattern:

```python
from pydantic import Field

def my_tool(
    param1: str = Field(description="Detailed description of this parameter"),
    param2: int = Field(description="Explain what this parameter does"),
) -> ReturnType:
    """One-line summary.

    Detailed explanation of functionality.
    When to use (and not use) this tool.
    Usage examples with expected input/output.
    """
    # implementation
```

- Docstrings must include: one-line summary, detailed explanation, when to use/avoid, and usage examples.
- Use `Field` from pydantic for all parameter descriptions — this is how MCP surfaces parameter metadata to AI assistants.
- Tools should be stateless pure functions.
