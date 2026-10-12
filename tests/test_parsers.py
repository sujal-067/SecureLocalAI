import sys
import types

import pytest

from pathlib import Path

from backend.ingestion.parsers import parse_pdf, parse_text


def test_parse_text_splits_on_blank_lines(tmp_path: Path) -> None:
    path = tmp_path / "notes.md"
    path.write_text("First paragraph\n\nSecond paragraph\n\n\nThird", encoding="utf-8")

    assert parse_text(path) == ["First paragraph", "Second paragraph", "Third"]


def test_parse_pdf_preserves_empty_page(monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> None:
    """Blank PDF pages must remain represented for page-aware ingestion."""
    class BlankPage:
        def extract_text(self) -> None:
            return None

    class Reader:
        def __init__(self, path: str) -> None:
            assert path == str(tmp_path / "blank.pdf")
            self.pages = [BlankPage()]

    monkeypatch.setitem(sys.modules, "pypdf", types.SimpleNamespace(PdfReader=Reader))

    assert parse_pdf(tmp_path / "blank.pdf") == [""]
