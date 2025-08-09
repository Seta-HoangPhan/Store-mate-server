# FastAPI Server Setup Guide

This project uses **FastAPI** for the backend, **SQLAlchemy** with **PostgreSQL** for database operations, and **Pydantic** for data validation.

## Prerequisites
- Python 3.x
- Poetry
- PostgreSQL

## Installation & Setup

1. **Install dependencies**
   ```bash
   poetry install
2. **Activate Poetry environment**
    ```bash
    eval $(poetry env activate)
3. **Apply database migrations**
    ```bash
    alembic upgrade head
4. **Configure environment variables**
    ```bash
    Create a .env file in the project root based on the .env.example template.
5. **Run the application**
    ```bash
    cd src
    uvicorn main:app --reload
