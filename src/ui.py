"""User interface functions."""

import os
from pathlib import Path

from _version import VERSION, DATE, IS_TEST_BUILD
from config import PROGRAM_TITLE
from models import EmployeeData, SubjectData


def print_title() -> None:
    print()
    print(PROGRAM_TITLE)
    print(f"Verzija: {VERSION} ({DATE})")

    if IS_TEST_BUILD:
        print("[TEST BUILD]")

    print()


def print_candidate_info(candidate: EmployeeData) -> None:
    print("KVS ime, prezime, serijski broj dozvole:")
    print(candidate["name"], candidate["license"])
    print()


def print_assessor_info(assessor: EmployeeData) -> None:
    print("ASSE ime, prezime, serijski broj dozvole:")
    print(assessor["name"], assessor["license"])
    print()


def print_subjects_summary(subjects: list[SubjectData]) -> None:
    print(f"Broj pronađenih oblasti u generatoru pitanja: {len(subjects)}")
    print()

    for i, subject in enumerate(subjects, 1):
        abbrev = subject["abbreviation"]
        title = subject["title"]
        total_questions = subject["total_questions"]
        percentage = subject["percentage"]
        generated_questions_qty = round(total_questions * percentage / 100)
        generated_numbers = ", ".join(str(num) for num in subject["generated_numbers"])

        print(f"{i}. {abbrev.upper()}")
        print(f"   {title.capitalize()}")
        print(f"       Ukupan broj pitanja: {total_questions}")
        print(f"       Procenat pitanja za generisanje: {percentage}%")
        print(f"       Broj pitanja za generisanje: {generated_questions_qty}")
        print(f"       Generisani brojevi pitanja:")
        print(f"         {generated_numbers}")
        print()


def print_test_generation_done(generated_tests: list[Path]) -> None:
    normalized_path = os.path.normpath(generated_tests[0])
    output_folder, candidate_folder, _ = normalized_path.split(os.sep)

    print("Testovi su generisani.")
    print()
    print(f"Testovi su sačuvani u folderu '{output_folder}' / '{candidate_folder}'")

    for test in generated_tests:
        normalized_path = os.path.normpath(test)
        file_name = normalized_path.split(os.sep)[2]

        print(f"  - {file_name}")


def print_test_generation_not_done(not_generated_tests: list) -> None:
    print()
    print("Testovi nisu generisani za sljedeće oblasti:")
    for subject in not_generated_tests:
        abbreviation = subject["abbreviation"].upper()
        title = subject["title"].capitalize()
        missing_questions_list = subject["non_available_questions"]

        # Convert question numbers from strings to numbers, so they can be joined
        missing_questions_list = [str(number) for number in missing_questions_list]
        missing_questions_str = ", ".join(missing_questions_list)

        print(f"- {abbreviation} {title}")
        print(f"  Pitanja koja nedostaju u bazi: {missing_questions_str}")


def wait_for_exit() -> None:
    input("\nPritisnite Enter za izlaz iz programa...")
