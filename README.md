# Llaut Mus Tournament

![Build Status](https://github.com/username/llaut-mus-tournament/actions/workflows/main.yml/badge.svg)
[![Coverage Status](https://coveralls.io/repos/github/username/llaut-mus-tournament/badge.svg?branch=main)](https://coveralls.io/github/username/llaut-mus-tournament?branch=main)
![Dependency Status](https://img.shields.io/librariesio/github/username/llaut-mus-tournament)
![Python Version](https://img.shields.io/badge/python-3.8%2B-blue)
![License](https://img.shields.io/github/license/username/llaut-mus-tournament)

Llaut Mus Tournament is a Python-based web application designed to manage and visualize mus card game tournaments. 
The app provides features for user management, random pair generation, bracket creation, leaderboard tracking, 
and winner predictions.

## Features
- Register and manage users.
- Generate and manage pairs randomly.
- Create a tournament bracket with elimination rounds.
- Track player and pair statistics.
- Predict winners based on performance.

## Requirements
- Python 3.9+
- Poetry

## Installation
1. Clone the repository:
   ```bash
   git clone https://github.com/i10s/llaut-mus-tournament.git
   cd llaut-mus-tournament
   ```
2. Install dependencies using Poetry:
   ```bash
   poetry install
   ```
3. Run the application:
   ```bash
   poetry run uvicorn app.main:app --reload
   ```

## Testing
Run tests using pytest:
```bash
poetry run pytest
```

## License
This project is licensed under the MIT License.
