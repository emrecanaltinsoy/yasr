import sys
from pathlib import Path
from typing import Dict, List
from PyInquirer import prompt
from tqdm import tqdm
from typer import Typer
from yasr.logger import logger
from yasr.models import Answers, questions

app = Typer()


def change_string(file_paths: List[str], answers: Answers) -> None:
    logger.info(f"Changing {answers.source_str} with {answers.target_str}")
    for file_path in tqdm(file_paths):
        if not file_path.is_file():
            continue

        with open(file_path, "r") as f:
            source_text = f.read()

        with open(file_path, "w") as f:
            f.write(
                source_text.replace(
                    answers.source_str,
                    answers.target_str,
                )
            )

        if answers.backup:
            with open(f"{file_path}.bak", "w") as f:
                f.write(source_text)
    logger.info("Done.")


def remove_backup(path: str) -> None:
    logger.info(f"Removing backup files in {Path(path).resolve()}")
    for file_path in tqdm(Path(path).glob("*.bak")):
        file_path.unlink()
    logger.info("Backup files removed.")


def get_answers(questions: List[Dict]) -> dict:
    answers = prompt(questions)
    return answers


@app.command()
def run() -> None:
    a = get_answers(questions)
    if "(q)" in a.get("first_choice"):
        sys.exit(0)
    elif "(cs)" in a.get("first_choice"):
        answers = Answers(**a)
        file_paths = list(Path(answers.path).glob(f"*{answers.file_extension}"))
        change_string(file_paths, answers)
    else:
        remove_backup(a.get("path"))


if __name__ == "__main__":
    app()
