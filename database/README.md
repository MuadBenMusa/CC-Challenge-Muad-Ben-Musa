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

This creates JSON files:

- `data/customers.json`
- `data/projects.json`

Use those files to design and populate your schema.

## Python Import Starter

The repository includes `faker/import_data.py` as a starter import script. It loads the generated JSON files and connects to PostgreSQL, but the insert loops and SQL are left for you to implement based on your schema.

Run it with:

```sh
make import-data
```
