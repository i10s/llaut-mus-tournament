
# Llaut Mus Tournament

![Build Status](https://github.com/i10s/llaut-mus-tournament/actions/workflows/main.yml/badge.svg)
[![Coverage Status](https://codecov.io/github/i10s/llaut-mus-tournament/main/graph/badge.svg)](https://codecov.io/github/i10s/llaut-mus-tournament)
![Dependencies](https://img.shields.io/librariesio/github/i10s/llaut-mus-tournament)
![Python Version](https://img.shields.io/badge/python-3.8%2B-blue)
![License](https://img.shields.io/github/license/i10s/llaut-mus-tournament)

Llaut Mus Tournament is a Python-based web application designed to manage and visualize mus card game tournaments. The app provides features for user management, random pair generation, bracket creation, leaderboard tracking, and predictions.

---

## Features

- **User Management**: Register, update, and delete users.
- **Pair Management**: Generate random pairs, update, and delete pairs.
- **Tournament Bracket**: Create and visualize brackets, and register match results.
- **Leaderboards**: Display leaderboards for users and pairs based on performance.
- **Statistics**: View detailed stats for players and pairs.

---

## Backend Setup

The backend is built with FastAPI. To run the backend:

1. Install dependencies:
   ```bash
   poetry install
   ```

2. Start the backend server:
   ```bash
   poetry run uvicorn app.main:app --reload
   ```

---

## Testing

Run all tests for the backend using pytest:
```bash
poetry run pytest
```

---

## Deployment

- **Backend**: Deployed to Fly.io with `fly.toml` configuration.

---

## License

This project is licensed under the MIT License.
