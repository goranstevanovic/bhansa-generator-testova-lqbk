"""Tests for reader module."""

from pathlib import Path

from reader import (
    _load_cell_value,
    _parse_subject_abbreviation,
    _parse_subject_title,
    load_employee_data,
    load_subject_titles,
    _load_numeric_values,
    load_total_questions,
    load_percentages,
    load_generated_numbers,
    load_all_subject_data,
)

SAMPLE_FORM = Path("tests/fixtures/test-form.xlsm")
SAMPLE_SUBJECT_NAME_RANGE = "A10:A29"
SAMPLE_TOTAL_QUESTIONS_RANGE = "D10:D29"
SAMPLE_PERCENTAGE_RANGE = "E10:E29"
SAMPLE_GENERATED_NUMBERS_RANGE = "F10:F29"


# Tests for _load_cell_value()
class TestLoadCellValue:
    def test_loads_cell_value(self):
        result = _load_cell_value(SAMPLE_FORM, "B4")
        expected_result = "Marko Marković ATCO.0123"

        assert result == expected_result


# Tests for _parse_subject_abbreviation()
class TestParseSubjectAbbreviations:
    def test_with_valid_abbreviation(self):
        result1 = _parse_subject_abbreviation("naziv prve oblasti (npo)")
        expected_result1 = "npo"

        result2 = _parse_subject_abbreviation("NAZIV DRUGE OBLASTI (NDO)")
        expected_result2 = "ndo"

        result3 = _parse_subject_abbreviation("Naziv TrEćE OBlaSti (nTo)")
        expected_result3 = "nto"

        assert result1 == expected_result1
        assert result2 == expected_result2
        assert result3 == expected_result3

    def test_without_abbreviation(self):
        assert _parse_subject_abbreviation("NAZIV OBLASTI") is None
        assert _parse_subject_abbreviation("") is None


# Tests for _parse_subject_title()
class TestParseSubjectTitle:
    def test_with_abbreviation(self):
        result1 = _parse_subject_title("naziv prve oblasti (npo)")
        expected_result1 = "naziv prve oblasti"

        result2 = _parse_subject_title("NAZIV DRUGE OBLASTI (NDO)")
        expected_result2 = "NAZIV DRUGE OBLASTI"

        result3 = _parse_subject_title("Naziv TrEćE OBlaSti (nTo)")
        expected_result3 = "Naziv TrEćE OBlaSti"

        assert result1 == expected_result1
        assert result2 == expected_result2
        assert result3 == expected_result3

    def test_newline_replacement(self):
        result = _parse_subject_title("NAZIV\nOBLASTI\n(NOB)")
        expected_result = "NAZIV OBLASTI"

        assert result == expected_result


# Tests for load_employee_data()
class TestLoadEmployeeData:
    def test_load_candidate_data(self):
        result = load_employee_data(SAMPLE_FORM, "B4")
        expected_result = {"name": "Marko Marković", "license": "ATCO.0123"}

        assert result == expected_result

    def test_load_assessor_data(self):
        result = load_employee_data(SAMPLE_FORM, "B5")
        expected_result = {"name": "Petar Petrović-Petrić", "license": "ATCO.4567"}

        assert result == expected_result

    def test_load_employee_data_from_empty_cell(self):
        result = load_employee_data(SAMPLE_FORM, "A1")
        expected_result = {"name": "", "license": ""}

        assert result == expected_result


# Tests for load_subject_titles()
class TestLoadSubjectTitles:
    def test_returns_list(self):
        result = load_subject_titles(SAMPLE_FORM, SAMPLE_SUBJECT_NAME_RANGE)

        assert isinstance(result, list)

    def test_list_contains_dicts(self):
        result = load_subject_titles(SAMPLE_FORM, SAMPLE_SUBJECT_NAME_RANGE)

        print(result)

        assert "abbreviation" in result[0]
        assert "title" in result[0]

    def test_loads_correct_abbreviations_and_titles(self):
        subjects = load_subject_titles(SAMPLE_FORM, SAMPLE_SUBJECT_NAME_RANGE)
        subject1, subject2, subject3 = subjects

        expected_subject1_abbreviation = "npo"
        expected_subject1_title = "NAZIV PRVE OBLASTI"
        expected_subject2_abbreviation = "ndo"
        expected_subject2_title = "NAZIV DRUGE OBLASTI"
        expected_subject3_abbreviation = "nto"
        expected_subject3_title = "NAZIV TREĆE OBLASTI"

        assert subject1["abbreviation"] == expected_subject1_abbreviation
        assert subject1["title"] == expected_subject1_title
        assert subject2["abbreviation"] == expected_subject2_abbreviation
        assert subject2["title"] == expected_subject2_title
        assert subject3["abbreviation"] == expected_subject3_abbreviation
        assert subject3["title"] == expected_subject3_title


# Tests for _load_numeric_values()
class TestLoadNumericValues:
    def test_returns_list_of_ints(self):
        TOTAL_QUESTIONS_RANGE = "D10:D29"
        start, end = TOTAL_QUESTIONS_RANGE.split(":")
        result = _load_numeric_values(SAMPLE_FORM, start, end)

        assert isinstance(result, list)
        assert all(isinstance(x, int) for x in result)


# Tests for load_total_questions()
class TestLoadTotalQuestions:
    def test_returns_list_of_total_questions(self):
        result = load_total_questions(SAMPLE_FORM, SAMPLE_TOTAL_QUESTIONS_RANGE)
        expected_result = [10, 9, 8]

        assert result == expected_result


# Tests for load_percentages()
class TestLoadPercentages:
    def test_returns_list_of_percentages(self):
        result = load_percentages(SAMPLE_FORM, SAMPLE_PERCENTAGE_RANGE)
        expected_result = [50, 55, 60]

        assert result == expected_result


# Tests for load_generated_numbers()
class TestLoadGeneratedNumbers:
    def test_returns_nested_list_of_integers(self):
        result = load_generated_numbers(SAMPLE_FORM, SAMPLE_GENERATED_NUMBERS_RANGE)

        assert isinstance(result, list)
        assert all(isinstance(x, list) for x in result)
        assert all(isinstance(x, int) for nums in result for x in nums)

    def test_returns_list_of_generated_numbers(self):
        results = load_generated_numbers(SAMPLE_FORM, SAMPLE_GENERATED_NUMBERS_RANGE)
        result1, result2, result3 = results

        expected_result1 = [1, 2, 6, 8, 10]
        expected_result2 = [1, 2, 3, 6, 7]
        expected_result3 = [1, 4, 5, 6, 7]

        assert result1 == expected_result1
        assert result2 == expected_result2
        assert result3 == expected_result3


# Tests for load_all_subject_data()
class TestLoadAllSubjectData:
    def test_returns_list_of_subject_data(self):
        result = load_all_subject_data(
            SAMPLE_FORM,
            SAMPLE_SUBJECT_NAME_RANGE,
            SAMPLE_TOTAL_QUESTIONS_RANGE,
            SAMPLE_PERCENTAGE_RANGE,
            SAMPLE_GENERATED_NUMBERS_RANGE,
        )
        subject = result[0]

        assert isinstance(result, list)
        assert "abbreviation" in subject
        assert "title" in subject
        assert "total_questions" in subject
        assert "percentage" in subject
        assert "generated_numbers" in subject

    def test_returns_correct_number_of_subject_data(self):
        result = result = load_all_subject_data(
            SAMPLE_FORM,
            SAMPLE_SUBJECT_NAME_RANGE,
            SAMPLE_TOTAL_QUESTIONS_RANGE,
            SAMPLE_PERCENTAGE_RANGE,
            SAMPLE_GENERATED_NUMBERS_RANGE,
        )

        assert len(result) == 3

    def test_returns_subject_data(self):
        result = result = load_all_subject_data(
            SAMPLE_FORM,
            SAMPLE_SUBJECT_NAME_RANGE,
            SAMPLE_TOTAL_QUESTIONS_RANGE,
            SAMPLE_PERCENTAGE_RANGE,
            SAMPLE_GENERATED_NUMBERS_RANGE,
        )
        subject1 = result[0]
        subject2 = result[1]
        subject3 = result[2]

        assert subject1["abbreviation"] == "npo"
        assert subject1["title"] == "NAZIV PRVE OBLASTI"
        assert subject1["total_questions"] == 10
        assert subject1["percentage"] == 50
        assert subject1["generated_numbers"] == [1, 2, 6, 8, 10]

        assert subject2["abbreviation"] == "ndo"
        assert subject2["title"] == "NAZIV DRUGE OBLASTI"
        assert subject2["total_questions"] == 9
        assert subject2["percentage"] == 55
        assert subject2["generated_numbers"] == [1, 2, 3, 6, 7]

        assert subject3["abbreviation"] == "nto"
        assert subject3["title"] == "NAZIV TREĆE OBLASTI"
        assert subject3["total_questions"] == 8
        assert subject3["percentage"] == 60
        assert subject3["generated_numbers"] == [1, 4, 5, 6, 7]
