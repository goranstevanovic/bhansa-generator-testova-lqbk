#!/usr/bin/env python3
"""Build script"""

import sys
import subprocess
import os
import shutil
import time
from pathlib import Path
from datetime import datetime

import PyInstaller.__main__

from _version import VERSION

# Base name of the release archive file
ARCHIVE_BASE_NAME = "bhansa-generator-testova-lqbk"

# Root and base folders used when creating archives
ARCHIVE_ROOT_FOLDER = Path("dist")
ARCHIVE_BASE_FODLER = Path("generator-testova-lqbk")

# File containing version number and date
VERSION_FILE_PATH = Path("src", "_version.py")

# Bundle folder temporary and final names
BUNDLE_ROOT_FOLDER_TEMP_NAME = Path("dist", "generator-testova-lqbk-bundle")
BUNDLE_ROOT_FOLDER_FINAL_NAME = Path("dist", "generator-testova-lqbk")

# Relases base folder
RELEASES_BASE_FOLDER = Path("releases")

# Generated executable files paths
WINDOWS_EXE_PATH = Path("dist", "generator-testova.exe")
LINUX_EXE_PATH = Path("dist", "generator-testova")

# Templates, questions, answers, generated tests folder paths
FOLDERS_TEMPLATES = ["baza/predlosci"]
FOLDERS_QUESTIONS = [
    "baza/pitanja/ass",
    "baza/pitanja/emr",
    "baza/pitanja/eqp",
    "baza/pitanja/hr",
    "baza/pitanja/lgc",
    "baza/pitanja/lnf",
    "baza/pitanja/lpi",
    "baza/pitanja/proc",
]
FOLDERS_ANSWERS = [
    "baza/odgovori/ass",
    "baza/odgovori/emr",
    "baza/odgovori/eqp",
    "baza/odgovori/hr",
    "baza/odgovori/lgc",
    "baza/odgovori/lnf",
    "baza/odgovori/lpi",
    "baza/odgovori/proc",
]
FOLDERS_GENERATED_TESTS = ["generisani-testovi"]

# Question number generator file
QUESTIONS_GENERATOR = "FORM.xlsm"

# User guide file
USER_GUIDE = "uputstvo.html"


def get_platform() -> str:
    """Get OS/platform as a string."""
    return sys.platform


def check_if_platform_supported(platform_type: str) -> bool:
    """Check if current OS/platform is supported by this build script."""
    if platform_type == "win32" or platform_type == "linux":
        return True
    else:
        raise Exception(
            f"{platform_type} is not supported. Only Windows and Linux are supported."
        )


def get_current_commit_tag() -> str:
    """Get tag of current commit, if any."""
    cmd = ["git", "tag", "--points-at", "HEAD"]

    result = subprocess.run(cmd, capture_output=True, text=True)
    return result.stdout.strip()


def get_current_commit_hash() -> str:
    """Get short hash of current commit."""
    cmd = ["git", "rev-parse", "--short", "HEAD"]

    result = subprocess.run(cmd, capture_output=True, text=True)
    return result.stdout.strip()


def get_current_commit_date() -> str:
    """Get YYYY-MM-DD date of current commit."""
    cmd = ["git", "show", "-s", "--format=%cs"]

    result = subprocess.run(cmd, capture_output=True, text=True)
    return result.stdout.strip()


def create_version_number() -> str:
    """
    Get current version number, either a version number from tag,
    or previous version number plus short commit hash.
    """
    tag = get_current_commit_tag()
    hash = get_current_commit_hash()

    if tag.startswith("v"):
        return tag[1:]
    else:
        # Use only x.x.x part, ignore - and rest
        return f"{VERSION.split("-")[0]}-dev+{hash}"


def update_version_file(is_test_build) -> str:
    """Update version file with correct version umber and date."""
    version_file_content = f'VERSION = "{create_version_number()}"\n'
    version_file_content += f'DATE = "{get_current_commit_date()}"\n'

    if is_test_build:
        version_file_content += "IS_TEST_BUILD = True\n"
    else:
        version_file_content += "IS_TEST_BUILD = False\n"

    with open(VERSION_FILE_PATH, "w") as file:
        file.write(version_file_content)

    return version_file_content


def empty_dist_folder() -> None:
    """Delete contents of dist folder before building to start fresh."""
    # Check if folder with temp name exists
    if os.path.exists(BUNDLE_ROOT_FOLDER_TEMP_NAME):
        shutil.rmtree(BUNDLE_ROOT_FOLDER_TEMP_NAME)
    # Check if folder or file with final name exists
    elif os.path.exists(BUNDLE_ROOT_FOLDER_FINAL_NAME):
        # Check if it is folder
        if os.path.isdir(BUNDLE_ROOT_FOLDER_FINAL_NAME):
            shutil.rmtree(BUNDLE_ROOT_FOLDER_FINAL_NAME)
        # Check if it is file
        elif os.path.isfile(BUNDLE_ROOT_FOLDER_FINAL_NAME):
            os.remove(BUNDLE_ROOT_FOLDER_FINAL_NAME)


def run_pyinstaller(platform: str) -> None:
    """Run PyInstaller using appropriate spec file."""
    if platform == "win32":
        spec_file = "generator-testova-win.spec"
    elif platform == "linux":
        spec_file = "generator-testova-linux.spec"

    PyInstaller.__main__.run(["--clean", spec_file])


def create_folders(folders: list[str]) -> list[Path]:
    """Create folders from provided list of folders."""
    created_folders = []

    for folder in folders:
        os.makedirs(BUNDLE_ROOT_FOLDER_FINAL_NAME / folder)
        created_folders.append(BUNDLE_ROOT_FOLDER_FINAL_NAME / folder)

    return created_folders


def create_folder_structure() -> list[list[Path]]:
    """Create empty folder structure and copy template files."""
    # Create bundle folder
    os.makedirs(BUNDLE_ROOT_FOLDER_TEMP_NAME)

    # Move executable file into bundle folder
    if get_platform() == "win32":
        shutil.move(
            WINDOWS_EXE_PATH, BUNDLE_ROOT_FOLDER_TEMP_NAME / "generator-testova.exe"
        )
    elif get_platform() == "linux":
        shutil.move(LINUX_EXE_PATH, BUNDLE_ROOT_FOLDER_TEMP_NAME)

    # Rename bundle root folder
    shutil.move(BUNDLE_ROOT_FOLDER_TEMP_NAME, BUNDLE_ROOT_FOLDER_FINAL_NAME)

    # Create template, questions, answers, and generated tests folders
    created_folders = []
    created_folders.append(create_folders(FOLDERS_TEMPLATES))
    created_folders.append(create_folders(FOLDERS_QUESTIONS))
    created_folders.append(create_folders(FOLDERS_ANSWERS))
    created_folders.append(create_folders(FOLDERS_GENERATED_TESTS))

    return created_folders


def copy_files(sources: list, dest_root: Path) -> list[tuple[Path, Path]]:
    """Copy files from source folders to destination folders."""
    copied_files_sources = []
    copied_files_destinations = []
    copied_files = []

    for source in sources:
        source = Path(source)
        destination = dest_root / source
        for file in os.listdir(source):
            shutil.copy2(source / file, destination)
            copied_files_sources.append(source / file)
            copied_files_destinations.append(destination / file)

    for i in range(len(copied_files_sources)):
        copied_file = (copied_files_sources[i], copied_files_destinations[i])
        copied_files.append(copied_file)

    return copied_files


def copy_basic_release_files(
    sources: list, dest_root: Path
) -> tuple[list[tuple[Path, Path]], str]:
    """
    Copy basic release files from source to destination folders.
    Basic release files are template files, that don't contain sensitive
    information.

    """
    # Copy template files
    copied_templates = copy_files(sources, dest_root)

    # Copy user guide
    copied_user_guide = shutil.copy2(USER_GUIDE, BUNDLE_ROOT_FOLDER_FINAL_NAME)

    return copied_templates, copied_user_guide


def copy_full_release_files() -> (
    tuple[list[tuple[Path, Path]], list[tuple[Path, Path]], str]
):
    """
    Copy full release files from source to destination folders.
    Full release files include questions generator form,
    question documents, and answer documents
    """
    copied_questions = copy_files(FOLDERS_QUESTIONS, BUNDLE_ROOT_FOLDER_FINAL_NAME)
    copied_answers = copy_files(FOLDERS_ANSWERS, BUNDLE_ROOT_FOLDER_FINAL_NAME)
    copied_form = shutil.copy2(QUESTIONS_GENERATOR, BUNDLE_ROOT_FOLDER_FINAL_NAME)

    return copied_questions, copied_answers, copied_form


def create_release_archive(platform_type: str, release_type: str = "basic") -> str:
    """Create release archives for basic and full releases."""
    version = create_version_number()
    archive_name = f"{ARCHIVE_BASE_NAME}-v{version}"

    if platform_type == "win32":
        archive_name += "-windows"

        if release_type == "full":
            archive_name += "-full"

        archive_path = str(RELEASES_BASE_FOLDER / Path(version) / Path(archive_name))
        shutil.make_archive(
            archive_path, "zip", ARCHIVE_ROOT_FOLDER, ARCHIVE_BASE_FODLER
        )
    elif platform_type == "linux":
        archive_name += "-linux"

        if release_type == "full":
            archive_name += "-full"

        archive_path = str(RELEASES_BASE_FOLDER / Path(version) / Path(archive_name))
        shutil.make_archive(
            archive_path, "gztar", ARCHIVE_ROOT_FOLDER, ARCHIVE_BASE_FODLER
        )

    return archive_path


def get_time_string(start_time: float, end_time: float) -> str:
    """Get time string in format h:mm:ss."""

    time_string = ""

    total_time = end_time - start_time

    hours = round(total_time // 3600)
    remaining = total_time - hours * 3600
    minutes = round(remaining // 60)
    seconds = round(remaining - minutes * 60)

    if hours > 0:
        time_string += f"{hours}h "

    if minutes > 0:
        time_string += f"{minutes:02}m "

    time_string += f"{seconds:02}s"

    return time_string


def main() -> None:
    # Get start time
    start_time = time.time()

    # Get current time neatly formatted
    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")

    # Show starting message and start time
    print("Building and packaging process started")
    print("at", current_time)
    print()

    # Get OS/platform
    platform_type = get_platform()

    # Show which platform is the release for
    print("Creating release for", platform_type)
    print()

    # Check if script is running on supported OS/platform
    try:
        check_if_platform_supported(platform_type)
    except Exception as err:
        print(err)
        sys.exit(1)

    # Show which commit is used
    current_commit_hash = get_current_commit_hash()
    print("Using commit:", current_commit_hash)

    # Determine if creating test build or not
    if get_current_commit_tag().startswith("v"):
        is_test_build = False
        print("Creating PRODUCTION release")
    else:
        is_test_build = True
        print("Creating TEST release")
    print()

    # Update vesion file
    if is_test_build:
        version_file_content = update_version_file(True)
    else:
        version_file_content = update_version_file(False)

    # Show version file content
    print("Version file updated to:")
    print(version_file_content)
    print()

    # Empty dist folder before building
    empty_dist_folder()
    print("dist folder cleared")
    print()

    # Run PyInstaller using platform-specific spec file
    print("Starting PyInstaller...")
    run_pyinstaller(platform_type)
    print("PyInstaller completed")
    print()

    # Create basic folder structure, empty folders, without files
    folder_structure = create_folder_structure()

    # Show which folders are created for basic folder structure
    print("Created basic folder structure:")
    for folders in folder_structure:
        for folder in folders:
            print(str(folder))
    print()

    # Copy basic release files (templates)
    basic_release_files = copy_basic_release_files(
        FOLDERS_TEMPLATES, BUNDLE_ROOT_FOLDER_FINAL_NAME
    )

    # Show which files are copied for basic release
    print("Copied files for basic release:")
    for file_pair in basic_release_files:
        print(file_pair[0], "->", file_pair[1])
    print()

    # Create basic release archive
    basic_release_path = create_release_archive(platform_type)
    print("Basic release archive created at", basic_release_path)
    print()

    # Copy full release files (.xlsm form, .docx questions and answers)
    full_release_files = copy_full_release_files()
    full_release_questions, full_release_answers, full_release_form = full_release_files

    # Show which files are copied for full release
    print("Copied files for full release:")

    # Show copied questions
    full_release_questions.sort()
    for file_pair in full_release_questions:
        print(file_pair[0], "->", file_pair[1])

    # Show copied answers
    if len(full_release_answers) == 0:
        full_release_answers.sort()
        for file_pair in full_release_answers:
            print(file_pair[0], "->", file_pair[1])

    # Show copied form
    print(full_release_form)
    print()

    # Create full release archive
    full_release_path = create_release_archive(platform_type, "full")
    print("Full release archive created at", full_release_path)
    print()

    # Get current time neatly formatted
    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")

    # Get end time
    end_time = time.time()

    # Display completed message, end time and total build time
    time_string = get_time_string(start_time, end_time)
    print("Building and packaging process completed")
    print("at", current_time)
    print("total run time:", time_string)


if __name__ == "__main__":
    main()
