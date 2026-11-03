import sqlite3
from datetime import date, datetime
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
DATABASE_PATH = PROJECT_ROOT / "scholar_seas.db"


def get_connection():
    connection = sqlite3.connect(DATABASE_PATH)
    connection.row_factory = sqlite3.Row
    connection.execute("PRAGMA foreign_keys = ON")

    return connection


def init_db():
    with get_connection() as connection:
        connection.executescript(
            """
            CREATE TABLE IF NOT EXISTS users (
                user_id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT NOT NULL UNIQUE,
                password_hash TEXT NOT NULL,
                role TEXT NOT NULL CHECK (
                    role IN ('student', 'parent')
                )
            );

            CREATE TABLE IF NOT EXISTS students (
                student_id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL UNIQUE,
                display_name TEXT NOT NULL,
                grade INTEGER NOT NULL CHECK (
                    grade BETWEEN 1 AND 13
                ),
                coins INTEGER NOT NULL DEFAULT 0 CHECK (
                    coins >= 0
                ),
                level INTEGER NOT NULL DEFAULT 1 CHECK (
                    level >= 1
                ),
                xp INTEGER NOT NULL DEFAULT 0 CHECK (
                    xp >= 0
                ),
                equipped_hat TEXT,
                equipped_coat TEXT,
                equipped_weapon TEXT,
                FOREIGN KEY (user_id)
                    REFERENCES users(user_id)
                    ON DELETE CASCADE
            );

            CREATE TABLE IF NOT EXISTS parents (
                parent_id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL UNIQUE,
                FOREIGN KEY (user_id)
                    REFERENCES users(user_id)
                    ON DELETE CASCADE
            );

            CREATE TABLE IF NOT EXISTS parent_child (
                parent_id INTEGER NOT NULL,
                student_id INTEGER NOT NULL,
                PRIMARY KEY (parent_id, student_id),
                FOREIGN KEY (parent_id)
                    REFERENCES parents(parent_id)
                    ON DELETE CASCADE,
                FOREIGN KEY (student_id)
                    REFERENCES students(student_id)
                    ON DELETE CASCADE
            );

            CREATE TABLE IF NOT EXISTS questions (
                question_id INTEGER PRIMARY KEY AUTOINCREMENT,
                topic TEXT NOT NULL,
                subtopic TEXT NOT NULL,
                difficulty INTEGER NOT NULL CHECK (
                    difficulty BETWEEN 1 AND 5
                ),
                question_text TEXT NOT NULL,
                correct_answer TEXT NOT NULL,
                choice_a TEXT NOT NULL,
                choice_b TEXT NOT NULL,
                choice_c TEXT NOT NULL,
                choice_d TEXT NOT NULL,
                question_type TEXT NOT NULL
                    DEFAULT 'multiple_choice'
            );

            CREATE TABLE IF NOT EXISTS results (
                result_id INTEGER PRIMARY KEY AUTOINCREMENT,
                student_id INTEGER NOT NULL,
                question_id INTEGER NOT NULL,
                is_correct INTEGER NOT NULL CHECK (
                    is_correct IN (0, 1)
                ),
                time_taken_ms INTEGER NOT NULL CHECK (
                    time_taken_ms >= 0
                ),
                answered_at TEXT NOT NULL,
                FOREIGN KEY (student_id)
                    REFERENCES students(student_id)
                    ON DELETE CASCADE,
                FOREIGN KEY (question_id)
                    REFERENCES questions(question_id)
                    ON DELETE CASCADE
            );

            CREATE TABLE IF NOT EXISTS settings (
                student_id INTEGER PRIMARY KEY,
                weekday_limit_min INTEGER NOT NULL DEFAULT 60
                    CHECK (weekday_limit_min >= 0),
                weekend_limit_min INTEGER NOT NULL DEFAULT 180
                    CHECK (weekend_limit_min >= 0),
                override_code TEXT,
                FOREIGN KEY (student_id)
                    REFERENCES students(student_id)
                    ON DELETE CASCADE
            );

            CREATE TABLE IF NOT EXISTS sessions (
                session_id INTEGER PRIMARY KEY AUTOINCREMENT,
                student_id INTEGER NOT NULL,
                play_date TEXT NOT NULL,
                seconds_played INTEGER NOT NULL DEFAULT 0
                    CHECK (seconds_played >= 0),
                UNIQUE (student_id, play_date),
                FOREIGN KEY (student_id)
                    REFERENCES students(student_id)
                    ON DELETE CASCADE
            );

            CREATE TABLE IF NOT EXISTS items (
                item_id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL UNIQUE,
                slot TEXT NOT NULL CHECK (
                    slot IN ('hat', 'coat', 'weapon')
                ),
                price INTEGER NOT NULL CHECK (price >= 0),
                rarity TEXT NOT NULL,
                sprite_path TEXT NOT NULL
            );

            CREATE TABLE IF NOT EXISTS inventory (
                student_id INTEGER NOT NULL,
                item_id INTEGER NOT NULL,
                PRIMARY KEY (student_id, item_id),
                FOREIGN KEY (student_id)
                    REFERENCES students(student_id)
                    ON DELETE CASCADE,
                FOREIGN KEY (item_id)
                    REFERENCES items(item_id)
                    ON DELETE CASCADE
            );

            CREATE TABLE IF NOT EXISTS topic_progress (
                student_id INTEGER NOT NULL,
                topic TEXT NOT NULL,
                difficulty INTEGER NOT NULL DEFAULT 1
                    CHECK (difficulty BETWEEN 1 AND 5),
                correct_streak INTEGER NOT NULL DEFAULT 0
                    CHECK (correct_streak >= 0),
                wrong_streak INTEGER NOT NULL DEFAULT 0
                    CHECK (wrong_streak >= 0),
                PRIMARY KEY (student_id, topic),
                FOREIGN KEY (student_id)
                    REFERENCES students(student_id)
                    ON DELETE CASCADE
            );

            CREATE TABLE IF NOT EXISTS story_progress (
                student_id INTEGER PRIMARY KEY,
                current_chapter INTEGER NOT NULL DEFAULT 1,
                FOREIGN KEY (student_id)
                    REFERENCES students(student_id)
                    ON DELETE CASCADE
            );
            """
        )


def create_user(username, password_hash, role):
    with get_connection() as connection:
        cursor = connection.execute(
            """
            INSERT INTO users (username, password_hash, role)
            VALUES (?, ?, ?)
            """,
            (username, password_hash, role),
        )

        return cursor.lastrowid


def get_user_by_username(username):
    with get_connection() as connection:
        user = connection.execute(
            """
            SELECT user_id, username, password_hash, role
            FROM users
            WHERE username = ?
            """,
            (username,),
        ).fetchone()

        return user


def reset_student_password(student_id, password_hash):
    with get_connection() as connection:
        connection.execute(
            """
            UPDATE users
            SET password_hash = ?
            WHERE user_id = (
                SELECT user_id
                FROM students
                WHERE student_id = ?
            )
            """,
            (password_hash, student_id),
        )


def create_student(user_id, display_name, grade):
    with get_connection() as connection:
        cursor = connection.execute(
            """
            INSERT INTO students (user_id, display_name, grade)
            VALUES (?, ?, ?)
            """,
            (user_id, display_name, grade),
        )

        student_id = cursor.lastrowid

        connection.execute(
            """
            INSERT INTO settings (student_id)
            VALUES (?)
            """,
            (student_id,),
        )

        return student_id


def create_parent(user_id):
    with get_connection() as connection:
        cursor = connection.execute(
            """
            INSERT INTO parents (user_id)
            VALUES (?)
            """,
            (user_id,),
        )

        return cursor.lastrowid


def get_student_by_user(user_id):
    with get_connection() as connection:
        student = connection.execute(
            """
            SELECT student_id, display_name, grade, coins, level, xp
            FROM students
            WHERE user_id = ?
            """,
            (user_id,),
        ).fetchone()

        return student


def get_student(student_id):
    with get_connection() as connection:
        student = connection.execute(
            """
            SELECT student_id,
                   display_name,
                   grade,
                   coins,
                   level,
                   xp,
                   equipped_hat,
                   equipped_coat,
                   equipped_weapon
            FROM students
            WHERE student_id = ?
            """,
            (student_id,),
        ).fetchone()

        return student


def get_questions_by_topic(topic, difficulty):
    with get_connection() as connection:
        questions = connection.execute(
            """
            SELECT question_id,
                   topic,
                   subtopic,
                   difficulty,
                   question_text,
                   correct_answer,
                   choice_a,
                   choice_b,
                   choice_c,
                   choice_d
            FROM questions
            WHERE topic = ? AND difficulty = ?
            """,
            (topic, difficulty),
        ).fetchall()

        return questions


def record_result(
    student_id,
    question_id,
    is_correct,
    time_taken_ms,
):
    with get_connection() as connection:
        connection.execute(
            """
            INSERT INTO results (
                student_id,
                question_id,
                is_correct,
                time_taken_ms,
                answered_at
            )
            VALUES (?, ?, ?, ?, ?)
            """,
            (
                student_id,
                question_id,
                int(is_correct),
                time_taken_ms,
                datetime.now().isoformat(),
            ),
        )


def add_rewards(student_id, coins, xp):
    with get_connection() as connection:
        connection.execute(
            """
            UPDATE students
            SET coins = coins + ?,
                xp = xp + ?
            WHERE student_id = ?
            """,
            (coins, xp, student_id),
        )


def get_topic_progress(student_id, topic):
    with get_connection() as connection:
        connection.execute(
            """
            INSERT OR IGNORE INTO topic_progress (
                student_id,
                topic
            )
            VALUES (?, ?)
            """,
            (student_id, topic),
        )

        progress = connection.execute(
            """
            SELECT difficulty,
                   correct_streak,
                   wrong_streak
            FROM topic_progress
            WHERE student_id = ? AND topic = ?
            """,
            (student_id, topic),
        ).fetchone()

        return progress


def save_topic_progress(
    student_id,
    topic,
    difficulty,
    correct_streak,
    wrong_streak,
):
    with get_connection() as connection:
        connection.execute(
            """
            INSERT INTO topic_progress (
                student_id,
                topic,
                difficulty,
                correct_streak,
                wrong_streak
            )
            VALUES (?, ?, ?, ?, ?)
            ON CONFLICT (student_id, topic)
            DO UPDATE SET
                difficulty = excluded.difficulty,
                correct_streak = excluded.correct_streak,
                wrong_streak = excluded.wrong_streak
            """,
            (
                student_id,
                topic,
                difficulty,
                correct_streak,
                wrong_streak,
            ),
        )

def get_shop_items():
    with get_connection() as connection:
        items = connection.execute(
            """
            SELECT item_id, name, slot, price, rarity, sprite_path
            FROM items
            ORDER BY price
            """
        ).fetchall()

        return items


def get_inventory(student_id):
    with get_connection() as connection:
        items = connection.execute(
            """
            SELECT items.item_id,
                   items.name,
                   items.slot,
                   items.price,
                   items.rarity,
                   items.sprite_path
            FROM inventory
            JOIN items
                ON inventory.item_id = items.item_id
            WHERE inventory.student_id = ?
            """,
            (student_id,),
        ).fetchall()

        return items


def buy_item(student_id, item_id):
    with get_connection() as connection:
        owned_item = connection.execute(
            """
            SELECT item_id
            FROM inventory
            WHERE student_id = ? AND item_id = ?
            """,
            (student_id, item_id),
        ).fetchone()

        if owned_item is not None:
            return False, "You already own this item."

        item = connection.execute(
            """
            SELECT name, price
            FROM items
            WHERE item_id = ?
            """,
            (item_id,),
        ).fetchone()

        student = connection.execute(
            """
            SELECT coins
            FROM students
            WHERE student_id = ?
            """,
            (student_id,),
        ).fetchone()

        if item is None or student is None:
            return False, "The item could not be found."

        if student["coins"] < item["price"]:
            return False, "You do not have enough coins."

        connection.execute(
            """
            UPDATE students
            SET coins = coins - ?
            WHERE student_id = ?
            """,
            (item["price"], student_id),
        )

        connection.execute(
            """
            INSERT INTO inventory (student_id, item_id)
            VALUES (?, ?)
            """,
            (student_id, item_id),
        )

        return True, item["name"] + " purchased!"

def equip_item(student_id, item_id):
    with get_connection() as connection:
        item = connection.execute(
            """
            SELECT items.name, items.slot
            FROM inventory
            JOIN items
                ON inventory.item_id = items.item_id
            WHERE inventory.student_id = ?
              AND inventory.item_id = ?
            """,
            (student_id, item_id),
        ).fetchone()

        if item is None:
            return False, "You do not own this item."

        if item["slot"] == "hat":
            connection.execute(
                """
                UPDATE students
                SET equipped_hat = ?
                WHERE student_id = ?
                """,
                (item["name"], student_id),
            )

        elif item["slot"] == "coat":
            connection.execute(
                """
                UPDATE students
                SET equipped_coat = ?
                WHERE student_id = ?
                """,
                (item["name"], student_id),
            )

        elif item["slot"] == "weapon":
            connection.execute(
                """
                UPDATE students
                SET equipped_weapon = ?
                WHERE student_id = ?
                """,
                (item["name"], student_id),
            )

        return True, item["name"] + " equipped!"


def unequip_item(student_id, slot):
    column_names = {
        "hat": "equipped_hat",
        "coat": "equipped_coat",
        "weapon": "equipped_weapon",
    }

    if slot not in column_names:
        return False, "That equipment slot does not exist."

    column_name = column_names[slot]

    with get_connection() as connection:
        connection.execute(
            "UPDATE students SET " + column_name + " = NULL "
            "WHERE student_id = ?",
            (student_id,),
        )

    return True, slot.title() + " unequipped!"

def get_parent_by_user(user_id):
    with get_connection() as connection:
        parent = connection.execute(
            """
            SELECT parent_id, user_id
            FROM parents
            WHERE user_id = ?
            """,
            (user_id,),
        ).fetchone()

        return parent


def link_parent_to_student(parent_id, student_username):
    with get_connection() as connection:
        student = connection.execute(
            """
            SELECT students.student_id
            FROM students
            JOIN users
                ON students.user_id = users.user_id
            WHERE users.username = ?
            """,
            (student_username,),
        ).fetchone()

        if student is None:
            return False, "Student account not found."

        connection.execute(
            """
            INSERT OR IGNORE INTO parent_child (
                parent_id,
                student_id
            )
            VALUES (?, ?)
            """,
            (parent_id, student["student_id"]),
        )

        return True, "Student linked successfully."


def get_parent_children(parent_id):
    with get_connection() as connection:
        children = connection.execute(
            """
            SELECT students.student_id,
                   students.display_name,
                   students.grade,
                   students.coins,
                   students.level,
                   students.xp
            FROM parent_child
            JOIN students
                ON parent_child.student_id = students.student_id
            WHERE parent_child.parent_id = ?
            ORDER BY students.display_name
            """,
            (parent_id,),
        ).fetchall()

        return children


def get_topic_accuracy(student_id):
    with get_connection() as connection:
        results = connection.execute(
            """
            SELECT questions.topic,
                   COUNT(results.result_id) AS total,
                   SUM(results.is_correct) AS correct,
                   AVG(results.time_taken_ms) AS average_time
            FROM results
            JOIN questions
                ON results.question_id = questions.question_id
            WHERE results.student_id = ?
            GROUP BY questions.topic
            ORDER BY questions.topic
            """,
            (student_id,),
        ).fetchall()

        return results


def get_settings(student_id):
    with get_connection() as connection:
        settings = connection.execute(
            """
            SELECT weekday_limit_min,
                   weekend_limit_min,
                   override_code
            FROM settings
            WHERE student_id = ?
            """,
            (student_id,),
        ).fetchone()

        return settings


def save_settings(
    student_id,
    weekday_limit,
    weekend_limit,
):
    with get_connection() as connection:
        connection.execute(
            """
            UPDATE settings
            SET weekday_limit_min = ?,
                weekend_limit_min = ?
            WHERE student_id = ?
            """,
            (
                weekday_limit,
                weekend_limit,
                student_id,
            ),
        )

def add_play_seconds(student_id, seconds):
    today = date.today().isoformat()

    with get_connection() as connection:
        connection.execute(
            """
            INSERT INTO sessions (
                student_id,
                play_date,
                seconds_played
            )
            VALUES (?, ?, ?)
            ON CONFLICT (student_id, play_date)
            DO UPDATE SET
                seconds_played =
                    sessions.seconds_played
                    + excluded.seconds_played
            """,
            (student_id, today, seconds),
        )


def get_seconds_played_today(student_id):
    today = date.today().isoformat()

    with get_connection() as connection:
        session_row = connection.execute(
            """
            SELECT seconds_played
            FROM sessions
            WHERE student_id = ?
              AND play_date = ?
            """,
            (student_id, today),
        ).fetchone()

        if session_row is None:
            return 0

        return session_row["seconds_played"]


def get_story_chapter(student_id):
    with get_connection() as connection:
        progress = connection.execute(
            """
            SELECT current_chapter
            FROM story_progress
            WHERE student_id = ?
            """,
            (student_id,),
        ).fetchone()

        if progress is None:
            return 1

        return progress["current_chapter"]


def save_story_chapter(student_id, chapter):
    with get_connection() as connection:
        connection.execute(
            """
            INSERT INTO story_progress (
                student_id,
                current_chapter
            )
            VALUES (?, ?)
            ON CONFLICT (student_id)
            DO UPDATE SET
                current_chapter = MAX(
                    story_progress.current_chapter,
                    excluded.current_chapter
                )
            """,
            (student_id, chapter),
        )

if __name__ == "__main__":
    init_db()
    print(f"Database ready: {DATABASE_PATH.name}")
