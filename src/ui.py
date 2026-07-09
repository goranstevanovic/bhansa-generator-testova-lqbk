"""User interface functions."""

import os
from pathlib import Path

from _version import VERSION, DATE, IS_TEST_BUILD
from config import PROGRAM_TITLE
from models import EmployeeData, SubjectData


def print_title() -> None:
    print()
    print(PROGRAM_TITLE)
    print(f"Верзија: {VERSION} ({DATE})")

    if IS_TEST_BUILD:
        print("[TEST BUILD]")

    print()


def print_candidate_info(candidate: EmployeeData) -> None:
    print("КВС име, презиме, серијски број дозволе:")
    print(candidate["name"], candidate["license"])
    print()


def print_assessor_info(assessor: EmployeeData) -> None:
    print("ASSE име, презиме, серијски број дозволе:")
    print(assessor["name"], assessor["license"])
    print()


def print_subjects_summary(subjects: list[SubjectData]) -> None:
    print(f"Број пронађених области у генератору питања: {len(subjects)}")
    print()

    for i, subject in enumerate(subjects, 1):
        abbrev = subject["abbreviation"]
        title = subject["title"]
        total_questions = subject["total_questions"]
        percentage = subject["percentage"]
        generated_questions_qty = round(total_questions * percentage / 100)
        generated_numbers = ", ".join(str(num) for num in subject["generated_numbers"])

        print(f"{i}. {abbrev.upper()}")
        print(f"   {title}")
        print(f"       Укупан број питања: {total_questions}")
        print(f"       Проценат питања за генерисање: {percentage}%")
        print(f"       Број питања за генерисање: {generated_questions_qty}")
        print(f"       Генерисани бројеви питања:")
        print(f"         {generated_numbers}")
        print()


def print_document_generation_done(
    generated_documents: list[Path], is_answers_documents: bool = False
) -> None:
    normalized_path = os.path.normpath(generated_documents[0])
    output_folder, candidate_folder, _ = normalized_path.split(os.sep)

    if is_answers_documents:
        print("Одговори су генерисани.")
        print(
            f"Одговори су сачувани у фолдеру '{output_folder}' / '{candidate_folder}'"
        )
    else:
        print("Тестови су генерисани.")
        print(f"Тестови су сачувани у фолдеру '{output_folder}' / '{candidate_folder}'")

    for document in generated_documents:
        normalized_path = os.path.normpath(document)
        file_name = normalized_path.split(os.sep)[2]

        print(f"  - {file_name}")


def print_document_generation_not_done(
    not_generated_documents: list, is_answers_documents: bool = False
) -> None:
    if is_answers_documents:
        print()
        print("Одговори нису генерисани за сљедеће области:")
    else:
        print()
        print("Тестови нису генерисани за сљедеће области:")

    for document in not_generated_documents:
        abbreviation = document["abbreviation"].upper()
        title = document["title"].capitalize()

        if is_answers_documents:
            missing_documents_list = document["non_available_answers"]
        else:
            missing_documents_list = document["non_available_questions"]

        # Convert question/answer numbers from strings to numbers, so they can be joined
        missing_documents_list = [str(number) for number in missing_documents_list]
        missing_documents_str = ", ".join(missing_documents_list)

        print(f"- {abbreviation} {title}")

        if is_answers_documents:
            print(f"  Одговори који недостају у бази: {missing_documents_str}")
        else:
            print(f"  Питања која недостају у бази: {missing_documents_str}")


def wait_for_exit() -> None:
    input("\nПритисните Ентер за излаз из програма...")
