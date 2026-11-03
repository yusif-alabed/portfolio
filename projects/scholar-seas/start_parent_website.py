import os
from pathlib import Path

PROJECT_FOLDER = Path(__file__).resolve().parent
os.chdir(PROJECT_FOLDER)

from shared.add_english_questions import add_english_questions
from shared.add_items import add_items
from shared.add_questions import add_questions
from shared.database import init_db
from web.app import app


def prepare_website():
    init_db()
    add_questions()
    add_english_questions()
    add_items()

if __name__ == "__main__":
    prepare_website()
    print("Parent website: http://127.0.0.1:5000")
    app.run(debug=False, use_reloader=False)
