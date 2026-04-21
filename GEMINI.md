# FIPI Bank Solve Platform Project Overview

This document provides an overview of the "FIPI Bank Solve Platform" project, outlining its purpose, architecture, main technologies, and instructions for building and running the application.

## Project Purpose

The "FIPI Bank Solve Platform" is a Python project designed to assist users in preparing for exams by providing access to tasks from the official ege.fipi.ru website. It achieves this by:
1.  **Parsing Tasks:** Collecting and extracting educational tasks from the FIPI website.
2.  **Storing Data:** Persisting these tasks in a structured database.
3.  **Providing an API:** Offering a FastAPI backend for clients to retrieve tasks and verify user-submitted answers against the FIPI's own checking mechanism.

## Main Technologies

*   **Backend Framework:** FastAPI (for building the web API)
*   **Database:** SQLAlchemy (ORM for database interactions, defaulting to SQLite)
*   **Web Scraping/Parsing:** `requests` (for HTTP requests) and `BeautifulSoup` (for HTML parsing)
*   **Data Validation & Serialization:** Pydantic (for defining API schemas and data validation)
*   **Data Models:** Python dataclasses (for internal representation of parsed task data)
*   **Dependency Management:** `uv`

## Architecture

The application is logically divided into several key components:

*   **`app/main.py`**: The entry point for the FastAPI application, responsible for initializing the app and including API routers.
*   **`app/api/`**: Contains the API routers (`routers/tasts.py`) which define the HTTP endpoints for interacting with tasks (e.g., retrieving tasks, submitting answers for checking).
*   **`app/database/`**: Manages database connectivity, defines SQLAlchemy ORM models (`models/tasks.py`) for the `Task` entity, and provides session management (`session.py`).
*   **`app/parser/`**: Houses the core logic for web scraping.
    *   **`run_parse.py`**: The script to initiate the parsing process.
    *   **`src/parser.py`**: Implements the `FIPIParser` class, which handles fetching HTML pages from FIPI, extracting task details using `BeautifulSoup`, and determining task types.
    *   **`src/checker.py`**: Implements the `FIPIChecker` class, responsible for formatting user answers and sending them to the FIPI website's `solve.php` endpoint for verification.
    *   **`src/models.py`**: Defines Python dataclasses (`Task`, `AnswerVariant`, `MatchingOption`, `CheckResponse`, etc.) for a structured representation of the parsed data.
    *   **`src/config.py`**: Stores configuration parameters for the parser, such as base URLs, API endpoints, subject IDs, request headers, timeouts, and delays.
    *   **`data/math_tasks.json`**: The output file where parsed tasks are temporarily stored before being potentially loaded into the database.
*   **`app/schemas/`**: Contains Pydantic models (`tasks.py`) that define the data structures for API requests and responses, ensuring data consistency and validation.
*   **`app/config.py`**: Defines application-wide settings, including database URL and paths, and potentially AI-related settings loaded from an `.env` file.
*   **`app/utils/`**: A directory for various utility scripts, such as `load_json_to_db.py` for populating the database from JSON files.

## Building and Running

Follow these steps to set up and run the FIPI Bank Solve Platform locally:

### 1. Install Dependencies

The project uses `uv` for efficient dependency management. Ensure `uv` is installed (e.g., `pip install uv`), then synchronize the project dependencies:

```bash
uv pip sync app/pyproject.toml
```

### 2. Parse Tasks (Populate Data)

Before the API can serve tasks, they must be parsed from the FIPI website. This step fetches the tasks and saves them into a JSON file.

```bash
python app/parser/run_parse.py
```

This command will generate `app/parser/data/math_tasks.json`.

**Note:** The `README.md` only mentions generating the JSON file. To make tasks available via the API, they need to be loaded from this JSON file into the SQLite database. This can typically be done using the `app/utils/load_json_to_db.py` script, though its execution isn't explicitly documented for initial setup.

```bash
# Example command (verify script usage if needed)
python app/utils/load_json_to_db.py
```

### 3. Run the FastAPI Application

Once the database is populated, you can start the FastAPI application:

```bash
uvicorn app.main:app --reload
```

Alternatively, you can run the `main.py` directly:

```bash
python app/main.py
```

The API will typically be available at `http://127.0.0.1:8000`. You can access the interactive API documentation (Swagger UI) at `http://127.0.0.1:8000/docs`.

## Development Conventions

*   **Modular Design:** The project adheres to a modular structure, separating concerns into distinct directories for API, database, parsing logic, schemas, and utilities.
*   **Type Hinting:** Python's type hints are used extensively to improve code clarity, enable static analysis, and reduce potential bugs.
*   **Pydantic for Schemas:** Pydantic models are used for defining clear and validated data structures for API requests and responses, ensuring robust data handling.
*   **SQLAlchemy ORM:** The Object-Relational Mapper (ORM) provided by SQLAlchemy is utilized for abstracting database operations, promoting maintainability and reducing boilerplate SQL.
*   **External API Interaction:** Direct interaction with the FIPI website is managed through dedicated parser and checker modules, encapsulating external dependencies.
*   **Configuration Management:** Application and parser-specific configurations are centralized in `app/config.py` and `app/parser/src/config.py`, respectively.
*   **Multilingual Comments:** Code comments are primarily in Russian, providing context and explanations for the implementation details.
*   **Known Optimization:** The parser currently loads all tasks into memory before saving to JSON; future work should focus on streaming writes for memory efficiency.
