# Document Manager

A small application that imports document metadata from XML, stores it in SQLite, and displays it through a FastAPI API and a React frontend.

## Stack


- Backend: Python, FastAPI, Pydantic, SQLAlchemy
- Database: SQLite
- Frontend: React, TypeScript, Vite
- Backend tests: pytest

## How it works

1. A Python script generates 25 sample document records in `data/documents.xml`.
2. `GET /source/documents.xml` serves that file as a simulated remote source.
3. `POST /api/import` downloads the XML over HTTP using httpx.
4. The backend parses and validates the records, then saves them in SQLite.
5. `GET /api/documents` returns the stored metadata.
6. React displays the documents and performs filtering and sorting locally.

## Requirements

- Python 3.10 or later
- Node.js 22.12 or later
- npm

The following commands are for Linux or Ubuntu WSL.
  
## Backend setup

Create and activate a virtual environment:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

Install dependencies:

```bash
python -m pip install -r backend/requirements.txt
```

Generate sample XML and create the database tables:

```bash
python scripts/generate_xml.py
python -m scripts.init_db
```

The generator uses a fixed random seed, so repeated runs produce the same
sample data. Running it overwrites `data/documents.xml`.

Start the API:

```bash
python -m uvicorn backend.app.main:app --reload
```

API documentation: http://127.0.0.1:8000/docs

## Import documents

With the backend running, open another terminal and run:

```bash
curl -X POST http://127.0.0.1:8000/api/import
```

For a new database, the expected response is:

```json
{"created":25,"updated":0,"total":25}
```

Alternatively, open the API documentation and execute `POST /api/import`.

Fetch the saved records:

```bash
curl http://127.0.0.1:8000/api/documents
```


## Frontend setup

In another terminal, start from the project root:

```bash
cd frontend
npm ci
npm run dev
```

Open http://localhost:5173.

The backend must remain running. Import documents before opening the
frontend, or refresh the page after importing them.

The interface supports:

- Searching document titles and descriptions
- Filtering by importance, category, and active status
- Sorting by creation date, title, or reading time
- Resetting filters

Document URLs use example.com as sample data; actual document files are
not included or downloaded.


## API endpoints

| Method | Path | Purpose |
| --- | --- | --- |
| GET | `/source/documents.xml` | Serve the sample XML source |
| POST | `/api/import` | Fetch, validate, and store XML records |
| GET | `/api/documents` | Return stored document metadata      |

The import endpoint returns HTTP 502 if downloading the source fails
and HTTP 422 if the XML or document data is invalid.


## Storage and document identity

The database is stored at `data/documents.db`.

Each XML `<document>` has an `id` attribute, saved as the unique
`external_id` column.

- A new external ID creates a database record.
- An existing external ID updates that record's metadata.
- Matching uses the external ID, not the title or XML filename.
- Records missing from a later import remain in the database.
- The `updated` count includes all existing records processed, even if
  their values did not change.

All records are validated before database changes begin. Database writes
are committed together and rolled back if a storage operation fails.


## Tests and checks

From the project root, with the Python environment activated:

```bash
python -m pytest backend/tests
```

Backend tests cover:

- Complete and reproducible generated XML
- Document field validation
- XML parsing and Latvian value mapping
- Creating records and updating existing records without duplicates

Frontend checks, from the `frontend` directory:


## MVP limitations
- Frontend automated tests are not included.
- The API returns all documents.Filtering and sorting happen in the browser.
- Imports are triggered manually.
- There is no authentication or access control.
- There is no import history, XML archive, or document version history.
- XML is parsed in memory, which is suitable for the small demonstration file.
- Database schema changes require manual handling; migrations are not included
