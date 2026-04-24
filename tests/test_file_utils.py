"""Tests for file utils module."""

from pathlib import Path
from unittest.mock import patch

import pytest

from file_utils import check_file_availability, check_document_availability

FIXTURES_PATH = Path("tests/fixtures")
SAMPLE_QUESTIONS_PATH = FIXTURES_PATH / "baza" / "pitanja"
SAMPLE_ANSWERS_PATH = FIXTURES_PATH / "baza" / "odgovori"


@pytest.fixture
def sample_subjects_all_documents_available():
    return [
        {
            "abbreviation": "npo",
            "title": "naziv prve oblasti",
            "total_questions": 10,
            "percentage": 40,
            "generated_numbers": [1, 4, 7, 10],
        },
        {
            "abbreviation": "ndo",
            "title": "naziv druge oblasti",
            "total_questions": 8,
            "percentage": 50,
            "generated_numbers": [1, 3, 5, 7],
        },
    ]


@pytest.fixture
def sample_subjects_all_documents_not_available():
    return [
        {
            "abbreviation": "npo",
            "title": "naziv prve oblasti",
            "total_questions": 10,
            "percentage": 40,
            "generated_numbers": [1, 4, 7, 10],
        },
        {
            "abbreviation": "ndo",
            "title": "naziv druge oblasti",
            "total_questions": 8,
            "percentage": 50,
            "generated_numbers": [1, 3, 5, 7, 10, 50, 100],
        },
    ]


@pytest.fixture
def sample_subjects_all_questions_not_available_expected_result():
    return (
        [
            {
                "abbreviation": "npo",
                "title": "naziv prve oblasti",
                "total_questions": 10,
                "percentage": 40,
                "generated_numbers": [1, 4, 7, 10],
            }
        ],
        [
            {
                "abbreviation": "ndo",
                "title": "naziv druge oblasti",
                "total_questions": 8,
                "percentage": 50,
                "generated_numbers": [1, 3, 5, 7, 10, 50, 100],
                "non_available_questions": [10, 50, 100],
            },
        ],
    )


@pytest.fixture
def sample_subjects_all_answers_not_available_expected_result():
    return (
        [
            {
                "abbreviation": "npo",
                "title": "naziv prve oblasti",
                "total_questions": 10,
                "percentage": 40,
                "generated_numbers": [1, 4, 7, 10],
            }
        ],
        [
            {
                "abbreviation": "ndo",
                "title": "naziv druge oblasti",
                "total_questions": 8,
                "percentage": 50,
                "generated_numbers": [1, 3, 5, 7, 10, 50, 100],
                "non_available_answers": [10, 50, 100],
            },
        ],
    )


# Tests for check_file_availability()
class TestCheckFileAvailability:
    @patch("file_utils.QUESTIONS_PATH", SAMPLE_QUESTIONS_PATH)
    def test_all_files_are_available(self):
        result = check_file_availability("npo", [1, 2, 6, 8, 10])
        expected_result = []

        assert result == expected_result

    @patch("file_utils.QUESTIONS_PATH", SAMPLE_QUESTIONS_PATH)
    def test_not_all_files_are_available(self):
        result = check_file_availability("ndo", [1, 2, 3, 10, 50, 100])
        expected_result = [10, 50, 100]

        assert result.sort() == expected_result.sort()


# Tests for check_document_availability()
class TestCheckDocumentAvailability:
    @patch("file_utils.QUESTIONS_PATH", SAMPLE_QUESTIONS_PATH)
    def test_all_questions_are_available(self, sample_subjects_all_documents_available):
        result = check_document_availability(sample_subjects_all_documents_available)
        expected_result = (sample_subjects_all_documents_available, [])

        assert result == expected_result

    @patch("file_utils.QUESTIONS_PATH", SAMPLE_QUESTIONS_PATH)
    def test_all_questions_are_not_available(
        self,
        sample_subjects_all_documents_not_available,
        sample_subjects_all_questions_not_available_expected_result,
    ):
        result = check_document_availability(
            sample_subjects_all_documents_not_available
        )
        expected_result = sample_subjects_all_questions_not_available_expected_result

        assert result == expected_result

    @patch("file_utils.ANSWERS_PATH", SAMPLE_ANSWERS_PATH)
    def test_all_answers_are_available(self, sample_subjects_all_documents_available):
        result = check_document_availability(
            sample_subjects_all_documents_available, True
        )
        expected_result = (sample_subjects_all_documents_available, [])

        assert result == expected_result

    @patch("file_utils.ANSWERS_PATH", SAMPLE_ANSWERS_PATH)
    def test_all_answers_are_not_available(
        self,
        sample_subjects_all_documents_not_available,
        sample_subjects_all_answers_not_available_expected_result,
    ):
        result = check_document_availability(
            sample_subjects_all_documents_not_available, True
        )
        expected_result = sample_subjects_all_answers_not_available_expected_result

        assert result == expected_result
