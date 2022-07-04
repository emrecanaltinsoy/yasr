import sys
from yasr.logger import logger
from pydantic import BaseModel, validator


class Answers(BaseModel):
    path: str = "."
    file_extension: str = "*"
    source_str: str
    target_str: str
    backup: bool

    @validator("source_str", "target_str")
    def check_empty_string(cls, val):
        if not val:
            logger.info("Source or target strings cannot be empty!!!")
            sys.exit(0)
        return val

    @validator("path")
    def check_path(cls, val):
        if not val:
            return "."
        return val


questions = [
    {
        "type": "list",
        "name": "first_choice",
        "message": "What would you like to do?",
        "choices": ["Change String (cs)", "Remove Backup Files (rb)", "Quit (q)"],
    },
    {
        "type": "input",
        "name": "path",
        "message": "Please enter the absolute/relative path:",
        "when": lambda answers: "(q)" not in answers["first_choice"],
    },
    {
        "type": "input",
        "name": "file_extension",
        "message": "Enter file types comma separated:",
        "when": lambda answers: "(cs)" in answers["first_choice"],
    },
    {
        "type": "input",
        "name": "source_str",
        "message": "Enter the source string:",
        "when": lambda answers: "(cs)" in answers["first_choice"],
    },
    {
        "type": "input",
        "name": "target_str",
        "message": "Enter the target string:",
        "when": lambda answers: "(cs)" in answers["first_choice"],
    },
    {
        "type": "confirm",
        "message": "Would you like to create backup files?",
        "name": "backup",
        "default": True,
        "when": lambda answers: "(cs)" in answers["first_choice"],
    },
]
