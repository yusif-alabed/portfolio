from shared.database import get_connection, init_db

ITEMS = [
    (
        "Deckhand Bandana",
        "hat",
        10,
        "Common",
        "game/assets/sprites/items/deckhand_bandana.png",
    ),
    (
        "Navigator Hat",
        "hat",
        25,
        "Rare",
        "game/assets/sprites/items/navigator_hat.png",
    ),
    (
        "Captain's Tricorn",
        "hat",
        50,
        "Epic",
        "game/assets/sprites/items/captain_tricorn.png",
    ),
    (
        "Sailor Coat",
        "coat",
        20,
        "Common",
        "game/assets/sprites/items/sailor_coat.png",
    ),
    (
        "Royal Captain Coat",
        "coat",
        60,
        "Epic",
        "game/assets/sprites/items/captain_coat.png",
    ),
    (
        "Wooden Cutlass",
        "weapon",
        15,
        "Common",
        "game/assets/sprites/items/wooden_cutlass.png",
    ),
    (
        "Golden Cutlass",
        "weapon",
        75,
        "Legendary",
        "game/assets/sprites/items/golden_cutlass.png",
    ),
]


def add_items():
    init_db()

    with get_connection() as connection:
        for item in ITEMS:
            connection.execute(
                """
                INSERT OR IGNORE INTO items (
                    name,
                    slot,
                    price,
                    rarity,
                    sprite_path
                )
                VALUES (?, ?, ?, ?, ?)
                """,
                item,
            )

        print(str(len(ITEMS)) + " shop items are ready.")


if __name__ == "__main__":
    add_items()