import os
from pathlib import Path

PROJECT_FOLDER = Path(__file__).resolve().parent
os.chdir(PROJECT_FOLDER)

from game.main import main
from shared.add_english_questions import add_english_questions
from shared.add_items import add_items
from shared.add_questions import add_questions
from shared.database import init_db


def prepare_game():
    init_db()
    add_questions()
    add_english_questions()
    add_items()


if __name__ == "__main__":
    prepare_game()
    main()
