"""Functions for working with files and folders."""

import shutil
import os

from config import TEMPORARY_PATH, QUESTIONS_PATH
from models import SubjectData


def delete_tmp_folder() -> None:
    """Delete temporary folder if it exists."""
    if TEMPORARY_PATH.exists():
        shutil.rmtree(TEMPORARY_PATH)


def check_file_availability(folder: str, files: list, kind: str = "pitanja"):
    """Check if folder contains all provided files."""
    if kind == "pitanja":
        folder_path = QUESTIONS_PATH / folder
    files_in_folder = sorted(os.listdir(folder_path))
    files_in_folder_stripped = []

    for file in files_in_folder:
        # Remove file extension and convert file name to number
        file_name_stripped = int(file.split(".")[0])
        files_in_folder_stripped.append(file_name_stripped)

    files_not_available = list(set(files) - set(files_in_folder_stripped))

    return files_not_available


def check_questions_availability(
    subjects: list[SubjectData],
) -> tuple[list[SubjectData], list[dict]]:
    """Return tuple containing two lists:
    one with subjects that have all selected questions available,
    another one with subjects that don't have all selected questions available, including missing question numbers.
    """
    question_files_available = []
    question_files_not_available = []

    for subject in subjects:
        non_available_questions = check_file_availability(
            subject["abbreviation"], subject["generated_numbers"]
        )
        non_available_questions.sort()

        if non_available_questions:
            subject_updated = dict(
                subject, **{"non_available_questions": non_available_questions}
            )
            question_files_not_available.append(subject_updated)
        else:
            question_files_available.append(subject)

    return question_files_available, question_files_not_available
