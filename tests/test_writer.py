"""Tests for writer module."""

from pathlib import Path
from unittest.mock import patch

import pytest
from docx import Document

from writer import (
    create_output_document_path,
    create_cover_page,
    generate_test_for_subject,
    generate_all_tests,
)

FIXTURES_PATH = Path("tests/fixtures")
SAMPLE_QUESTIONS_PATH = FIXTURES_PATH / "baza" / "pitanja"
SAMPLE_OUTPUT_PATH = FIXTURES_PATH / "output"
SAMPLE_TEMPORARY_PATH = FIXTURES_PATH / "tmp"
SAMPLE_COVER_TEMPLATE = FIXTURES_PATH / "baza" / "predlosci" / "template-naslovna.docx"
SAMPLE_TEMPLATE_TITLE_STRING = "naziv"
SAMPLE_TEMPLATE_ABBREVIATION_STRING = "skracenica"


# Sample employee
@pytest.fixture
def sample_employee():
    return {"name": "Marko Marković", "license": "ATCO.0123"}


# Sample subject
@pytest.fixture
def sample_subject():
    return {
        "abbreviation": "npo",
        "title": "naziv prve oblasti",
        "total_questions": 10,
        "percentage": 40,
        "generated_numbers": [1, 4, 7, 10],
    }


# Sample subject 2
@pytest.fixture
def sample_subject_2():
    return {
        "abbreviation": "ndo",
        "title": "naziv druge oblasti",
        "total_questions": 8,
        "percentage": 50,
        "generated_numbers": [1, 3, 5, 7],
    }


# Sample subject 3
@pytest.fixture
def sample_subject_3():
    return {
        "abbreviation": "nto",
        "title": "naziv treće oblasti",
        "total_questions": 6,
        "percentage": 60,
        "generated_numbers": [2, 3, 4, 5],
    }


# Sample questions
@pytest.fixture
def sample_questions():
    return {
        "pitanje1": "1. Naziv prve oblasti: Prvo pitanje",
        "pitanje2": "Naziv prve oblasti: Drugo pitanje",
        "pitanje3": "Naziv prve oblasti: Treće pitanje",
        "pitanje4": "2. Naziv prve oblasti: Četvrto pitanje",
        "pitanje5": "Naziv prve oblasti: Peto pitanje",
        "pitanje6": "Naziv prve oblasti: Šesto pitanje",
        "pitanje7": "3. Naziv prve oblasti: Sedmo pitanje",
        "pitanje8": "Naziv prve oblasti: Osmo pitanje",
        "pitanje9": "Naziv prve oblasti: Deveto pitanje",
        "pitanje10": "4. Naziv prve oblasti: Deseto pitanje",
    }


# Tests for create_output_document_path()
class TestCreateOutputDocumentPath:
    @patch("writer.OUTPUT_PATH", SAMPLE_OUTPUT_PATH)
    def test_creates_correct_output_document_path(
        self, sample_employee, sample_subject
    ):
        result = create_output_document_path(sample_subject, sample_employee)

        expected_result = (
            Path(SAMPLE_OUTPUT_PATH)
            / f"{sample_employee['name']} {sample_employee['license']}"
            / f"{sample_employee['name']} {sample_employee['license']} "
            f"{sample_subject['abbreviation'].upper()}.docx"
        )

        assert result == expected_result

    @patch("writer.OUTPUT_PATH", SAMPLE_OUTPUT_PATH)
    def test_creates_folder_if_not_exists(self, sample_subject, sample_employee):
        result = create_output_document_path(sample_subject, sample_employee)

        assert result.parent.exists()


# Tests for create_cover_page()
class TestCreateCoverPage:
    @patch("writer.COVER_TEMPLATE", SAMPLE_COVER_TEMPLATE)
    @patch("writer.TEMPORARY_PATH", SAMPLE_TEMPORARY_PATH)
    @patch("writer.TEMPLATE_TITLE_STRING", SAMPLE_TEMPLATE_TITLE_STRING)
    @patch("writer.TEMPLATE_ABBREVIATION_STRING", SAMPLE_TEMPLATE_ABBREVIATION_STRING)
    def test_creates_cover_page_file(self, sample_subject):
        result = create_cover_page(sample_subject)

        assert result.exists()
        assert result.suffix == ".docx"

    @patch("writer.COVER_TEMPLATE", SAMPLE_COVER_TEMPLATE)
    @patch("writer.TEMPORARY_PATH", SAMPLE_TEMPORARY_PATH)
    @patch("writer.TEMPLATE_TITLE_STRING", SAMPLE_TEMPLATE_TITLE_STRING)
    @patch("writer.TEMPLATE_ABBREVIATION_STRING", SAMPLE_TEMPLATE_ABBREVIATION_STRING)
    def test_cover_page_contains_correct_text(self, sample_subject):
        result = create_cover_page(sample_subject)

        # Open created document
        doc = Document(result)

        # Get all text from document
        full_text = "\n".join([paragraph.text for paragraph in doc.paragraphs])

        # Assert text is present
        assert "naziv prve oblasti" in full_text
        assert "npo" in full_text


# Tests for generate_test_for_subject()
class TestGenerateTestForSubject:
    @patch("writer.OUTPUT_PATH", SAMPLE_OUTPUT_PATH)
    @patch("writer.COVER_TEMPLATE", SAMPLE_COVER_TEMPLATE)
    @patch("writer.TEMPORARY_PATH", SAMPLE_TEMPORARY_PATH)
    @patch("writer.TEMPLATE_TITLE_STRING", SAMPLE_TEMPLATE_TITLE_STRING)
    @patch("writer.TEMPLATE_ABBREVIATION_STRING", SAMPLE_TEMPLATE_ABBREVIATION_STRING)
    @patch("writer.QUESTIONS_PATH", SAMPLE_QUESTIONS_PATH)
    def test_generates_test_file_for_single_subject(
        self, sample_subject, sample_employee
    ):
        result = generate_test_for_subject(sample_subject, sample_employee)

        assert result.exists()
        assert result.suffix == ".docx"

    @patch("writer.OUTPUT_PATH", SAMPLE_OUTPUT_PATH)
    @patch("writer.COVER_TEMPLATE", SAMPLE_COVER_TEMPLATE)
    @patch("writer.TEMPORARY_PATH", SAMPLE_TEMPORARY_PATH)
    @patch("writer.TEMPLATE_TITLE_STRING", SAMPLE_TEMPLATE_TITLE_STRING)
    @patch("writer.TEMPLATE_ABBREVIATION_STRING", SAMPLE_TEMPLATE_ABBREVIATION_STRING)
    @patch("writer.QUESTIONS_PATH", SAMPLE_QUESTIONS_PATH)
    def test_generated_test_file_contains_selected_questions(
        self, sample_subject, sample_employee, sample_questions
    ):
        result = generate_test_for_subject(sample_subject, sample_employee)

        # Open created document
        doc = Document(result)

        # Get all text from documents
        full_text = "\n".join([paragraph.text for paragraph in doc.paragraphs])

        # Assert selcted questions are in document
        assert sample_questions["pitanje4"] in full_text
        assert sample_questions["pitanje1"] in full_text
        assert sample_questions["pitanje7"] in full_text
        assert sample_questions["pitanje10"] in full_text

        # Assert non-selected questions are not in document
        assert sample_questions["pitanje2"] not in full_text
        assert sample_questions["pitanje3"] not in full_text
        assert sample_questions["pitanje5"] not in full_text
        assert sample_questions["pitanje6"] not in full_text
        assert sample_questions["pitanje8"] not in full_text
        assert sample_questions["pitanje9"] not in full_text


# Tests for generate_all_tests()
class TestGenerateAllTests:
    @patch("writer.OUTPUT_PATH", SAMPLE_OUTPUT_PATH)
    @patch("writer.COVER_TEMPLATE", SAMPLE_COVER_TEMPLATE)
    @patch("writer.TEMPORARY_PATH", SAMPLE_TEMPORARY_PATH)
    @patch("writer.TEMPLATE_TITLE_STRING", SAMPLE_TEMPLATE_TITLE_STRING)
    @patch("writer.TEMPLATE_ABBREVIATION_STRING", SAMPLE_TEMPLATE_ABBREVIATION_STRING)
    @patch("writer.QUESTIONS_PATH", SAMPLE_QUESTIONS_PATH)
    def test_generates_test_files_for_all_subjects(
        self, sample_subject, sample_subject_2, sample_subject_3, sample_employee
    ):
        subjects = [sample_subject, sample_subject_2, sample_subject_3]

        results = generate_all_tests(subjects, sample_employee)

        assert len(results) == 3
        assert all(res.exists() for res in results)
