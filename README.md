# Sewage Pipe Project Challenge

Welcome to the Sewage Pipe Project Challenge.

You are tasked with building an app that visualizes sewage pipe projects and their statuses.

The stack is already wired with Docker Compose, so you can focus on the challenge itself. The stack includes:

- PostgreSQL 17
- FastAPI
- Svelte with Vite and TypeScript
- Adminer
- dbmate
- Faker data generation

If you have not used Docker before, the helper containers are there to make the setup easier:

- The Adminer UI is accessible at `http://localhost:8080`. You can use it to inspect and edit the database if you do not have a preferred SQL client.
- The dbmate container manages database migrations, so you can create, apply, and roll back your database schema without manual resets.
- The Faker container can be used to generate dummy data that you should use to populate the database.

The backend and frontend directories are mounted into their containers. Changes you make in those folders are reflected inside the running containers, and the development servers should reload when file changes are detected. Work in these directories while the Docker containers are running.

## Task

Implement a project overview feature:

- Generate the JSON source data.
- Create a PostgreSQL schema with a dbmate SQL migration.
- Load the generated project data into PostgreSQL.
- Implement `GET /projects` and `POST /projects` in FastAPI.
- Implement the Svelte project page.
- Show the project list sorted by date.
- Add filtering by project status.

You may decide the database schema, API payload fields, table columns, and where status filtering happens.

## Setup

Requirements:

- Docker
- Docker Compose
- Make

Start the stack:

```sh
make up
```

Generate source data:

```sh
make data
```

Create or edit your SQL migration in `database/migrations/`, then apply it:

```sh
make migrate-up
```

Reset the database:

```sh
make reset
```

## Local URLs

- Frontend: `http://localhost:5173`
- API: `http://localhost:8000`
- API docs: `http://localhost:8000/docs`
- Adminer: `http://localhost:8080`
- PostgreSQL: `localhost:5432`

If a default port is already in use on your machine, override it before starting the stack:

```sh
POSTGRES_PORT=15432 ADMINER_PORT=18080 make up
```

## Database Login

Use these values for PostgreSQL and Adminer:

- System: `PostgreSQL`
- Server: `postgres`
- Database: `challenge`
- Username: `challenge`
- Password: `challenge`

When connecting from a host-side database tool, use `localhost` as the server.

## Useful Commands

```sh
make up              # start the stack
make down            # stop the stack
make logs            # follow service logs
make reset           # remove database volume and restart PostgreSQL
make data            # generate data/customers.json and data/projects.json
make migrate-new     # create a new dbmate migration named initial-schema
make migrate-up      # apply migrations
make migrate-down    # roll back the latest migration
make migrate-status  # show migration status
```

## Service Docs

- [Backend](./backend/README.md)
- [Frontend](./frontend/README.md)
- [Database](./database/README.md)
- [Faker Data](./faker/README.md)

## Submission

Submit either a Git repository or a zip archive via email.

Have fun!
