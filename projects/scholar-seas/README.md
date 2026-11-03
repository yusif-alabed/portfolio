# Scholar Seas | CS NEA

Scholar Seas is my A-Level Computer Science NEA project: an educational, pirate-themed game designed to make revision more interactive. It is still in development, so I will keep this section updated as I finish the project.

## What I built

- A Python game built with Pygame, structured around scenes, characters, challenges, and a story progression system.
- Question queues and subject-based learning challenges, including Maths and English content.
- Pathfinding and game-state systems for gameplay logic.
- A Flask parent website with a dashboard, settings, and student-account management.
- An SQLite data layer for accounts, learning questions, progress, rewards, and play-time tracking.

## Code in this folder

| Folder or file | Purpose |
| --- | --- |
| `game/` | Pygame application, scenes, entities, interface components, and gameplay systems |
| `shared/` | Database schema and scripts that prepare questions and items |
| `web/` | Flask application and parent-dashboard templates |
| `start_game.py` | Prepares the local data and starts the game |
| `start_parent_website.py` | Prepares the local data and starts the parent website |
| `requirements.txt` | Python dependencies |

## Public source snapshot

This portfolio contains the code only. I have intentionally left out my NEA write-up, local SQLite database, virtual environment, and large game-media files. That keeps personal data and unfinished supporting material out of the public repository while allowing the architecture and implementation to be reviewed.

Once the project is finished, I plan to add a short demo, screenshots, and a polished setup guide.
