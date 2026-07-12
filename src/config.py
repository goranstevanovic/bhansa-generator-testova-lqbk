"""Configuration constants for test generator."""

from pathlib import Path

# Program information
PROGRAM_TITLE = "ГЕНЕРАТОР ТЕСТОВА"

# Question number generator file
QUESTIONS_GENERATOR = "FORM.xlsm"

# Cell addresses for employees' data
CANDIDATE_CELL = "B4"
ASSESSOR_CELL = "B5"

# Cell ranges for subject data
SUBJECT_NAME_RANGE = "A10:A29"
TOTAL_QUESTIONS_RANGE = "D10:D29"
PERCENTAGE_RANGE = "E10:E29"
GENERATED_NUMBERS_RANGE = "F10:F29"

# Folder paths
BASE_PATH = Path("baza")
QUESTIONS_PATH = BASE_PATH / "pitanja"
ANSWERS_PATH = BASE_PATH / "odgovori"
TEMPLATES_PATH = BASE_PATH / "predlosci"
OUTPUT_PATH = Path("generisani-testovi")
TEMPORARY_PATH = Path("tmp")

# Cover page template file
MAIN_COVER_PAGE = TEMPLATES_PATH / "naslovna-strana-za-teorijsku-provjeru-znanja.docx"
SUBJECT_COVER_TEMPLATE = TEMPLATES_PATH / "template-oblast-naslovna.docx"
SUBJECT_COVER_TEMPLATE_ANSWERS = (
    TEMPLATES_PATH / "template-oblast-naslovna-odgovori.docx"
)
TEMPLATE_TITLE_STRING = "naziv"
TEMPLATE_ABBREVIATION_STRING = "skracenica"
