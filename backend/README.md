# Backend

FastAPI starter service for the sewage pipe project challenge.

## Stack

- Python 3.12
- FastAPI
- `uv`
- async raw SQL with `psycopg`

## Local URL

- API: `http://localhost:8000`
- OpenAPI docs: `http://localhost:8000/docs`

## Applicant Task

Implement project endpoints:

- `GET /projects`
- `POST /projects`

Use raw SQL against PostgreSQL.

## Adding Packages

Add backend dependencies to `backend/pyproject.toml`, then rebuild and restart the backend container:

```sh
docker compose up --build backend
```

If you use `uv` locally, you can also add a package from the `backend/` directory:

```sh
uv add package-name
```

Then rebuild the container.
