# Frontend

Svelte frontend starter for the sewage pipe project challenge.

## Stack

- Vite
- Svelte
- TypeScript
- Plain CSS

## Local URL

- Frontend: `http://localhost:5173`

## Applicant Task

Implement the single project page. It should fetch projects directly from the FastAPI backend, show them in a table, sort them by date, and allow filtering by status.

You may decide:

- Which project columns to show.
- Whether the status filter is a select, tabs, or buttons.
- Whether filtering happens in the frontend or through the API.

No frontend tests or create-project form are required.

## Adding Packages

Add frontend dependencies to `frontend/package.json`, then rebuild and restart the frontend container:

```sh
docker compose up --build frontend
```

The frontend uses a Docker volume for `node_modules`. If a newly added package is still missing after rebuilding, remove that volume and start the frontend again:

```sh
docker compose down
docker volume rm cc-challenge_frontend_node_modules
docker compose up --build frontend
```

