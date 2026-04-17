"""Main entry point for test generator."""

from pathlib import Path

from config import (
    QUESTIONS_GENERATOR,
    CANDIDATE_CELL,
    ASSESSOR_CELL,
    SUBJECT_NAME_RANGE,
    TOTAL_QUESTIONS_RANGE,
    PERCENTAGE_RANGE,
    GENERATED_NUMBERS_RANGE,
)
from reader import load_employee_data, load_all_subject_data
from writer import generate_all_tests
from ui import (
    print_title,
    print_candidate_info,
    print_assessor_info,
    print_subjects_summary,
    print_test_generation_done,
    print_test_generation_not_done,
    wait_for_exit,
)
from file_utils import (
    delete_tmp_folder,
    check_questions_availability,
)


def main() -> None:
    """Run test generator."""
    # Load questions generator form file
    form_file = Path(QUESTIONS_GENERATOR)

    # Load employee data
    candidate = load_employee_data(form_file, CANDIDATE_CELL)
    assessor = load_employee_data(form_file, ASSESSOR_CELL)

    # Load all subject data
    subjects = load_all_subject_data(
        form_file,
        SUBJECT_NAME_RANGE,
        TOTAL_QUESTIONS_RANGE,
        PERCENTAGE_RANGE,
        GENERATED_NUMBERS_RANGE,
    )

    print_title()
    print_candidate_info(candidate)
    print_assessor_info(assessor)
    print_subjects_summary(subjects)

    # Check which subjects have all selected questions available, and which do not
    subjects_with_all_questions, subjects_without_all_questions = (
        check_questions_availability(subjects)
    )

    # Generate tests
    generated_tests = generate_all_tests(subjects_with_all_questions, candidate)

    print_test_generation_done(generated_tests)

    # List subjects without all necessary question files, if applicable
    if subjects_without_all_questions:
        print_test_generation_not_done(subjects_without_all_questions)

    # Delete temporay folder
    delete_tmp_folder()

    wait_for_exit()


if __name__ == "__main__":
    main()
