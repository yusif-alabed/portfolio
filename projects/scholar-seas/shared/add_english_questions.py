from shared.database import get_connection, init_db

QUESTIONS = [
    ("english", "spelling", 1, "Which word is spelled correctly?", "because", "becaus", "because", "becose", "beacause"),
    ("english", "nouns", 1, "Which word is a noun?", "island", "quickly", "island", "bright", "gently"),
    ("english", "verbs", 1, "Which word is a verb?", "swim", "ocean", "blue", "swim", "quiet"),
    ("english", "adjectives", 1, "Which word describes the ship?", "wooden", "sailed", "wooden", "captain", "slowly"),
    ("english", "punctuation", 1, "Which mark ends a question?", "?", ".", "!", ",", "?"),
    ("english", "synonyms", 1, "Which word means the same as big?", "large", "tiny", "large", "short", "slow"),
    ("english", "antonyms", 1, "Which word is the opposite of hot?", "cold", "warm", "cold", "bright", "dry"),
    ("english", "plurals", 1, "What is the plural of ship?", "ships", "shipes", "ships", "ship's", "shipp"),
    ("english", "sentences", 1, "Which word should begin with a capital?", "Pirate", "and", "the", "Pirate", "ran"),
    ("english", "pronouns", 1, "Which word can replace Captain Coral?", "she", "ship", "her", "she", "sail"),

    ("english", "spelling", 2, "Which word is spelled correctly?", "treasure", "tresure", "treasure", "treasur", "treazure"),
    ("english", "adverbs", 2, "Which word is an adverb?", "carefully", "carefully", "careful", "captain", "caution"),
    ("english", "conjunctions", 2, "Choose the best joining word: tired ___ happy.", "but", "because", "when", "but", "under"),
    ("english", "apostrophes", 2, "Which phrase shows Sam owns the sword?", "Sam's sword", "Sams sword", "Sams' sword", "Sam's sword", "Sams sword's"),
    ("english", "homophones", 2, "The pirates sailed ___ the island.", "to", "too", "two", "to", "tow"),
    ("english", "synonyms", 2, "Which word is closest in meaning to brave?", "courageous", "worried", "courageous", "careless", "silent"),
    ("english", "antonyms", 2, "Which word is the opposite of ancient?", "modern", "broken", "modern", "valuable", "hidden"),
    ("english", "prefixes", 2, "Which prefix changes possible to impossible?", "im-", "re-", "un-", "im-", "pre-"),
    ("english", "suffixes", 2, "Add a suffix to turn quick into an adverb.", "quickly", "quicker", "quickly", "quickness", "quickful"),
    ("english", "grammar", 2, "Which sentence is in the past tense?", "The ship sailed.", "The ship sails.", "The ship sailed.", "The ship will sail.", "Sail the ship."),

    ("english", "vocabulary", 3, "What does reluctant mean?", "unwilling", "excited", "unwilling", "confused", "careless"),
    ("english", "figurative", 3, "The sea was a mirror is an example of what?", "metaphor", "simile", "metaphor", "rhyme", "question"),
    ("english", "figurative", 3, "As fast as lightning is an example of what?", "simile", "metaphor", "command", "simile", "fact"),
    ("english", "grammar", 3, "Which sentence uses a semicolon correctly?", "It was late; we sailed home.", "It was; late we sailed home.", "It was late; we sailed home.", "It; was late, we sailed home.", "It was late we; sailed home."),
    ("english", "clauses", 3, "Which word begins the subordinate clause?", "although", "ship", "although", "sailed", "harbour"),
    ("english", "formal_language", 3, "Which word is most formal?", "depart", "go", "leave", "depart", "head off"),
    ("english", "vocabulary", 3, "Which word means very hungry?", "ravenous", "furious", "ravenous", "generous", "nervous"),
    ("english", "punctuation", 3, "Which mark can separate items in a list?", "comma", "apostrophe", "comma", "question mark", "hyphen"),
    ("english", "active_voice", 3, "Which sentence uses the active voice?", "Coral steered the ship.", "The ship was steered by Coral.", "Coral steered the ship.", "The ship had been steered.", "The ship was being steered."),
    ("english", "inference", 3, "Dark clouds gathered. What is likely next?", "a storm", "sunshine", "a storm", "a drought", "a rainbow"),
    ("english", "nouns", 1, "Which word names a person?", "captain", "quickly", "captain", "brave", "sailed"),
    ("english", "verbs", 1, "Which word shows an action?", "climbed", "rope", "climbed", "tall", "quiet"),
    ("english", "adjectives", 1, "Which word describes the ocean?", "deep", "swim", "deep", "sailor", "slowly"),
    ("english", "spelling", 1, "Which spelling means an exciting journey?", "adventure", "adventur", "adventure", "advencher", "advanture"),
    ("english", "punctuation", 1, "Which mark shows excitement?", "!", ".", ",", "?", "!"),

    ("english", "pronouns", 2, "Which pronoun can replace the sailors?", "they", "it", "he", "they", "she"),
    ("english", "conjunctions", 2, "We stayed inside ___ it rained.", "because", "but", "because", "or", "until"),
    ("english", "homophones", 2, "The crew raised ___ sails.", "their", "there", "they're", "their", "thier"),
    ("english", "grammar", 2, "Which sentence is written correctly?", "The pirates are sailing.", "The pirates is sailing.", "The pirates are sailing.", "The pirates am sailing.", "The pirates be sailing."),
    ("english", "vocabulary", 2, "Which word means to look carefully?", "inspect", "ignore", "inspect", "forget", "damage"),

    ("english", "figurative", 3, "The wind whispered is an example of what?", "personification", "simile", "rhyme", "personification", "fact"),
    ("english", "inference", 3, "The deck and sails are wet. What happened?", "it rained", "it snowed", "it rained", "it was hot", "the ship sank"),
    ("english", "punctuation", 3, "Which marks can show extra information?", "brackets", "comma", "apostrophe", "brackets", "question mark"),
    ("english", "formal_language", 3, "Which phrase is the most formal?", "Please respond promptly.", "Reply fast.", "Get back to me.", "Please respond promptly.", "Answer me now."),
    ("english", "clauses", 3, "Which part can stand alone as a sentence?", "main clause", "prefix", "subordinate clause", "main clause", "suffix"),
]


def add_english_questions():
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
            else:
                connection.execute(
                    """
                    UPDATE questions
                    SET subtopic = ?,
                        correct_answer = ?,
                        choice_a = ?,
                        choice_b = ?,
                        choice_c = ?,
                        choice_d = ?
                    WHERE question_id = ?
                    """,
                    (
                        question[1],
                        question[4],
                        question[5],
                        question[6],
                        question[7],
                        question[8],
                        exists["question_id"],
                    ),
                )

        print(str(added) + " English questions added.")


if __name__ == "__main__":
    add_english_questions()
