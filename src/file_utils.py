"""Functions for working with files and folders."""

import shutil
import os

from config import TEMPORARY_PATH, QUESTIONS_PATH, ANSWERS_PATH
from models import SubjectData


def delete_tmp_folder() -> None:
    """Delete temporary folder if it exists."""
    if TEMPORARY_PATH.exists():
        shutil.rmtree(TEMPORARY_PATH)


def check_file_availability(
    folder: str, files: list, is_answers_document: bool = False
):
    """Check if folder contains all provided files."""
    if is_answers_document:
        folder_path = ANSWERS_PATH / folder
    else:
        folder_path = QUESTIONS_PATH / folder

    files_in_folder = sorted(os.listdir(folder_path))
    files_in_folder_stripped = []

    for file in files_in_folder:
        # Remove file extension and convert file name to number
        file_name_stripped = int(file.split(".")[0])
        files_in_folder_stripped.append(file_name_stripped)

    files_not_available = list(set(files) - set(files_in_folder_stripped))

    return files_not_available


def check_document_availability(
    subjects: list[SubjectData], is_answers_documents: bool = False
) -> tuple[list[SubjectData], list[dict]]:
    """Return tuple containing two lists:
    one with subjects that have all selected questions/answers available,
    another one with subjects that don't have all selected questions/answers available, including missing question numbers.
    """
    documents_available = []
    documents_not_available = []

    for subject in subjects:
        if is_answers_documents:
            non_available_files = check_file_availability(
                subject["abbreviation"], subject["generated_numbers"], True
            )
        else:
            non_available_files = check_file_availability(
                subject["abbreviation"], subject["generated_numbers"]
            )
        non_available_files.sort()

        if non_available_files:
            if is_answers_documents:
                subject_updated = dict(
                    subject, **{"non_available_answers": non_available_files}
                )
            else:
                subject_updated = dict(
                    subject, **{"non_available_questions": non_available_files}
                )
            documents_not_available.append(subject_updated)
        else:
            documents_available.append(subject)

    return documents_available, documents_not_available
