# Sewage Pipe Project Challenge

Welcome to the Sewage Pipe Project Challenge.

The goal of the challenge is to build an application that visualizes sewage pipe projects and their statuses.

The provided stack consists of:

- PostgreSQL 17
- FastAPI
- Svelte with Vite and TypeScript
- Adminer
- dbmate
- Faker data generation
- Docker Compose

The backend and frontend directories are mounted into their containers so that changes are reflected by the development servers while the stack is running.

## Task

Implement a project overview feature:

- Generate the source data.
- Create a PostgreSQL schema with a dbmate SQL migration.
- Load the generated project data into PostgreSQL.
- Implement `GET /projects` and `POST /projects` in FastAPI.
- Implement the Svelte project page.
- Show the project list sorted by date.
- Add filtering by project status.

The database schema, API payload fields, table columns, and filtering approach may be chosen as part of the implementation.

---

## Solution

The challenge is implemented as a small project overview application using the provided stack.

The implementation intentionally stays compact and focuses on the requested functionality without introducing unnecessary infrastructure or application layers.

### Data Model

The PostgreSQL schema contains two main tables:

- `customers`
- `projects`

A customer can have multiple projects.

Each project references its customer through a foreign key.

Database IDs are treated as internal technical identifiers and are therefore not exposed in the public project overview response.

The project table contains:

- customer reference
- date
- task
- optional location
- optional description
- status

The schema also uses:

- PostgreSQL identity columns for generated IDs
- a foreign-key constraint between projects and customers
- `CHECK` constraints for supported task values
- `CHECK` constraints for supported status values
- appropriate nullable fields for optional source data

The schema is managed through a dbmate migration in:

```text
database/migrations/
```

### Data Generation

The Faker generator creates deterministic source data consisting of:

- 10 customers
- 100 projects

Generate the data with:

```sh
make data
```

The fixed Faker seed makes the generated dataset reproducible.

### Data Import

After applying the database migration, import the generated JSON data with:

```sh
make import-data
```

The importer intentionally resets the seeded customer and project data before importing it again.

This makes the development dataset repeatable and allows the import command to be executed multiple times safely.

The import process:

1. loads the generated customer and project JSON files
2. resets the seeded tables
3. inserts customers first
4. inserts projects with their customer references
5. synchronizes the PostgreSQL identity sequences

The identity sequences are synchronized because the generated source data contains explicit IDs, while projects created later through the API should still receive automatically generated IDs.

The import runs inside a database transaction and uses parameterized SQL.

---

### Backend

The backend is implemented with FastAPI and async psycopg using raw parameterized SQL.

The project-specific backend structure is intentionally lightweight:

```text
app/
├── config.py
├── db.py
├── main.py
└── projects/
    ├── __init__.py
    ├── router.py
    ├── schemas.py
    └── service.py
```

Responsibilities:

- `main.py` — FastAPI application setup and CORS configuration
- `config.py` — environment configuration
- `db.py` — asynchronous database connection handling
- `projects/router.py` — HTTP routes and HTTP status handling
- `projects/schemas.py` — Pydantic request and response models
- `projects/service.py` — project database operations

#### GET /projects

Returns the project overview sorted by `date` in ascending order.

```http
GET /projects
```

Example response item:

```json
{
  "customer_name": "Example Customer GmbH",
  "date": "2027-07-12",
  "task": "inspection",
  "location": "Hamburg",
  "description": "Inspection of the sewer section.",
  "status": "open"
}
```

The overview intentionally does not expose internal project or customer IDs.

The customer name is obtained through a SQL `JOIN` between `projects` and `customers`.

##### Status Filtering

Projects can be filtered by status:

```http
GET /projects?status=open
```

```http
GET /projects?status=in%20progress
```

```http
GET /projects?status=done
```

Supported status values are:

- `open`
- `in progress`
- `done`

Status filtering and date sorting are performed in PostgreSQL.

Invalid status values are rejected by FastAPI validation.

#### POST /projects

Creates a new project.

Example request:

```http
POST /projects
Content-Type: application/json
```

```json
{
  "customer_id": 1,
  "date": "2027-08-14",
  "task": "inspection",
  "location": "Hamburg",
  "description": "Inspection of a new sewer section.",
  "status": "open"
}
```

A successful request returns:

```text
201 Created
```

The created project is returned using the same public `ProjectRead` representation as `GET /projects`.

Example:

```json
{
  "customer_name": "Example Customer GmbH",
  "date": "2027-08-14",
  "task": "inspection",
  "location": "Hamburg",
  "description": "Inspection of a new sewer section.",
  "status": "open"
}
```

The `customer_id` is required in the creation payload because it establishes the relationship between the new project and an existing customer.

It is not returned in the public project representation.

If the referenced customer does not exist, the API returns:

```text
404 Not Found
```

Task and status values are validated through Pydantic and are additionally protected by PostgreSQL constraints.

---

### Frontend

The frontend is implemented as a single Svelte project overview page.

It includes:

- project table
- customer names
- project dates
- German task labels
- German status labels
- status badges
- status filtering
- loading state
- error state
- empty-result state
- responsive horizontal table scrolling

The frontend uses a small typed API layer and TypeScript models matching the public backend response.

When a status is selected, the frontend sends the selected value to the FastAPI backend:

```text
Svelte
  ↓
GET /projects?status=...
  ↓
FastAPI
  ↓
PostgreSQL filtering
  ↓
Filtered project overview
```

The frontend therefore does not fetch the complete dataset and filter it locally for every status selection.

---

### Design Decisions

#### Internal IDs

Database IDs are treated as technical identifiers.

They are required internally for relationships but are not displayed or returned in the project overview because the frontend does not need them.

If a business-facing project identifier were required later, it should be introduced as a separate `project_number` rather than using the database primary key.

#### Customer Name

The customer name is retrieved through a SQL `JOIN` instead of being duplicated into the project table.

#### Filtering and Sorting

Status filtering and date sorting are performed directly in SQL.

This keeps the API behavior deterministic and the frontend simple.

#### Identity Strategy

The schema uses:

```sql
GENERATED BY DEFAULT AS IDENTITY
```

This allows the generated source dataset to import explicit IDs while still allowing `POST /projects` to generate new IDs automatically.

#### Import Strategy

The importer is intentionally designed as a repeatable development seed reset.

Rerunning:

```sh
make import-data
```

replaces the current seeded dataset.

Projects created manually through the API are therefore removed when the seed data is imported again.

#### Backend Structure

The backend uses a small router/schema/service separation.

Additional repository, domain, or application layers were intentionally not introduced because they would add unnecessary complexity for the size of this challenge.

---

## Setup

### Requirements

- Docker
- Docker Compose
- Make

### Start the Stack

```sh
make up
```

The command starts the development stack.

### Generate Source Data

```sh
make data
```

### Apply Database Migration

```sh
make migrate-up
```

### Import Generated Data

```sh
make import-data
```

The importer resets and reloads the seeded customer and project dataset.

### Reset the Database

```sh
make reset
```

After resetting the database, apply the migration and import the source data again:

```sh
make migrate-up
make data
make import-data
```

---

## Local URLs

- Frontend: `http://localhost:15173`
- API: `http://localhost:18000`
- API docs: `http://localhost:18000/docs`
- Adminer: `http://localhost:18080`
- PostgreSQL: `localhost:15432`

---

## Database Login

Use these values for PostgreSQL and Adminer:

- System: `PostgreSQL`
- Server: `postgres`
- Database: `challenge`
- Username: `challenge`
- Password: `challenge`

When connecting from a host-side database tool, use `localhost` as the server and port `15432`.

---

## Useful Commands

```sh
make up              # start the stack
make down            # stop the stack
make logs            # follow service logs

make reset           # remove the database volume and restart PostgreSQL

make data            # generate customer and project source data
make import-data     # import generated customer and project data

make migrate-new     # create a new dbmate migration
make migrate-up      # apply migrations
make migrate-down    # roll back the latest migration
make migrate-status  # show migration status
```

---

## Adding Packages

If a backend package is added, update `backend/pyproject.toml`, then rebuild the backend container:

```sh
docker compose up --build backend
```

If a frontend package is added, update `frontend/package.json` and `frontend/package-lock.json`, then rebuild the frontend container:

```sh
docker compose up --build frontend
```

The frontend uses a Docker volume for `node_modules`.

Avoid:

```sh
docker compose down -v
```

unless the PostgreSQL data volume should also be deleted.

---

## API Documentation

Interactive FastAPI documentation is available at:

```text
http://localhost:18000/docs
```

It documents:

- `GET /projects`
- the optional status filter
- `POST /projects`
- `ProjectCreate`
- `ProjectRead`

---

## Submission

The completed solution can be submitted either as a Git repository or as a ZIP archive via email.