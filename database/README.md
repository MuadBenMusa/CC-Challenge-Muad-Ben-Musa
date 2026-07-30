# Database

PostgreSQL starts with an empty application schema. Create the schema with dbmate SQL migrations.

## Stack

- PostgreSQL 17
- dbmate 2.34
- Pure SQL migrations

## Migration Folder

```text
database/migrations
```

## Database URLs

Use this URL from commands running inside Docker Compose containers:

```text
postgres://challenge:challenge@postgres:5432/challenge?sslmode=disable
```

Use this URL from tools running on your host machine:

```text
postgres://challenge:challenge@localhost:5432/challenge?sslmode=disable
```

The hostname differs because `postgres` is the Docker Compose service name inside the Docker network, while `localhost` points to your host machine.

If you override `POSTGRES_PORT`, adjust the host-side URL to use that port.

## Commands

Create a migration:

```sh
make migrate-new
```

Apply migrations:

```sh
make migrate-up
```

Roll back the latest migration:

```sh
make migrate-down
```

Show migration status:

```sh
make migrate-status
```

Reset the database:

```sh
make reset
```

## Data

Generate source files with:

```sh
make data
```

This creates `data/customers.json` and `data/projects.json`. Use those files to design and populate your schema.
