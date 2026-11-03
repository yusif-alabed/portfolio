from shared.database import get_connection, init_db

QUESTIONS = [
    (
        "maths", "addition", 1, "What is 7 + 5?", "12",
        "10", "12", "13", "14"
    ),
    (
        "maths", "subtraction", 1, "What is 15 - 6?", "9",
        "7", "8", "9", "10"
    ),
    (
        "maths", "multiplication", 1, "What is 4 x 3?", "12",
        "7", "10", "12", "14"
    ),
    (
        "maths", "division", 1, "What is 20 divided by 4?", "5",
        "4", "5", "6", "8"
    ),
    (
        "maths", "addition", 1, "What is 18 + 7?", "25",
        "23", "24", "25", "26"
    ),
    (
        "maths", "subtraction", 1, "What is 30 - 12?", "18",
        "16", "18", "20", "22"
    ),
    (
        "maths", "multiplication", 1, "What is 5 x 6?", "30",
        "25", "30", "35", "40"
    ),
    (
        "maths", "division", 1, "What is 24 divided by 6?", "4",
        "3", "4", "5", "6"
    ),
    (
        "maths", "place_value", 1, "What is the value of 5 in 352?", "50",
        "5", "50", "300", "500"
    ),
    (
        "maths", "sequence", 1, "What comes next: 2, 4, 6, 8?", "10",
        "9", "10", "11", "12"
    ),
    (
        "maths", "multiplication", 2, "What is 8 x 7?", "56",
        "48", "54", "56", "64"
    ),
    (
        "maths", "subtraction", 2, "What is 72 - 28?", "44",
        "42", "44", "46", "54"
    ),
    (
        "maths", "division", 2, "What is 81 divided by 9?", "9",
        "7", "8", "9", "10"
    ),
    (
        "maths", "sequence", 2, "What comes next: 5, 10, 15, 20?", "25",
        "21", "22", "25", "30"
    ),
    (
        "maths", "fractions", 2, "What is half of 36?", "18",
        "16", "17", "18", "20"
    ),
    (
        "maths", "addition", 2, "What is 125 + 76?", "201",
        "191", "199", "201", "211"
    ),
    (
        "maths", "multiplication", 2, "What is 9 x 12?", "108",
        "96", "99", "108", "118"
    ),
    (
        "maths", "fractions", 2, "What is one quarter of 60?", "15",
        "10", "15", "20", "25"
    ),
    (
        "maths", "decimals", 2, "What is 2.5 + 1.5?", "4",
        "3", "3.5", "4", "4.5"
    ),
    (
        "maths", "perimeter", 2, "A square has 6 cm sides. What is its perimeter?", "24 cm",
        "12 cm", "18 cm", "24 cm", "36 cm"
    ),
    (
        "maths", "multiplication", 3, "What is 14 x 6?", "84",
        "74", "80", "84", "96"
    ),
    (
        "maths", "division", 3, "What is 144 divided by 12?", "12",
        "10", "11", "12", "14"
    ),
    (
        "maths", "percentages", 3, "What is 25% of 80?", "20",
        "15", "20", "25", "40"
    ),
    (
        "maths", "sequence", 3, "What comes next: 3, 6, 12, 24?", "48",
        "30", "36", "42", "48"
    ),
    (
        "maths", "fractions", 3, "What is three quarters of 40?", "30",
        "10", "20", "30", "35"
    ),
    (
        "maths", "percentages", 3, "What is 15% of 200?", "30",
        "15", "20", "30", "40"
    ),
    (
        "maths", "algebra", 3, "If x + 7 = 19, what is x?", "12",
        "10", "11", "12", "26"
    ),
    (
        "maths", "decimals", 3, "What is 3.6 x 5?", "18",
        "8", "15", "18", "20"
    ),
    (
        "maths", "area", 3, "What is the area of a 9 cm by 7 cm rectangle?", "63 cm2",
        "16 cm2", "32 cm2", "63 cm2", "72 cm2"
    ),
    (
        "maths", "ratio", 3, "Simplify the ratio 12:18.", "2:3",
        "1:2", "2:3", "3:4", "6:9"
    ),
    (
        "maths", "addition", 1, "What is 26 + 13?", "39",
        "37", "38", "39", "40"
    ),
    (
        "maths", "subtraction", 1, "What is 42 - 17?", "25",
        "23", "24", "25", "26"
    ),
    (
        "maths", "multiplication", 1, "What is 7 x 4?", "28",
        "21", "24", "28", "32"
    ),
    (
        "maths", "division", 1, "What is 35 divided by 5?", "7",
        "5", "6", "7", "8"
    ),
    (
        "maths", "time", 1, "How many minutes are in one hour?", "60",
        "30", "45", "60", "100"
    ),
    (
        "maths", "subtraction", 2, "What is 250 - 87?", "163",
        "153", "163", "167", "173"
    ),
    (
        "maths", "division", 2, "What is 132 divided by 11?", "12",
        "10", "11", "12", "13"
    ),
    (
        "maths", "fractions", 2, "Which fraction is equal to one half?", "3/6",
        "2/3", "3/6", "4/6", "5/6"
    ),
    (
        "maths", "money", 2, "A map costs 45 coins. What change from 60?", "15 coins",
        "5 coins", "10 coins", "15 coins", "25 coins"
    ),
    (
        "maths", "angles", 2, "How many degrees are in a right angle?", "90",
        "45", "60", "90", "180"
    ),
    (
        "maths", "algebra", 3, "If 4x = 36, what is x?", "9",
        "8", "9", "10", "32"
    ),
    (
        "maths", "percentages", 3, "Increase 50 by 20%.", "60",
        "55", "60", "65", "70"
    ),
    (
        "maths", "negative_numbers", 3, "What is -4 + 11?", "7",
        "-15", "-7", "7", "15"
    ),
    (
        "maths", "averages", 3, "What is the mean of 4, 7 and 10?", "7",
        "6", "7", "8", "21"
    ),
    (
        "maths", "probability", 3, "What is the chance of rolling an even number?", "1/2",
        "1/6", "1/3", "1/2", "2/3"
    ),
]


def add_questions():
    init_db()

    with get_connection() as connection:
        added = 0

        for question in QUESTIONS:
            exists = connection.execute(
                """
                SELECT question_id
                FROM questions
                WHERE topic = ?
                  AND difficulty = ?
                  AND question_text = ?
                """,
                (question[0], question[2], question[3]),
            ).fetchone()

            if exists is None:
                connection.execute(
                    """
                    INSERT INTO questions (
                        topic, subtopic, difficulty, question_text,
                        correct_answer, choice_a, choice_b, choice_c,
                        choice_d
                    )
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                    """,
                    question,
                )
                added += 1

        print(str(added) + " Maths questions added.")


if __name__ == "__main__":
    add_questions()
