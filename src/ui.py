"""User interface functions."""

import os
from pathlib import Path

from config import PROGRAM_TITLE
from models import EmployeeData, SubjectData


def print_title() -> None:
    print()
    print(PROGRAM_TITLE)
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


def wait_for_exit() -> None:
    input("\nPritisnite Enter za izlaz iz programa...")
