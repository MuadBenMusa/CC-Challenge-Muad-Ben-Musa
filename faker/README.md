# Faker Data

Generates source data for the challenge.

## Output

Running the generator creates:

- `data/customers.json`
- `data/projects.json`

The files are overwritten on each run and are not committed to the applicant branch.

## Command

From the repository root:

```sh
make data
```

## Import Script

`faker/import_data.py` is a starter script for importing the generated JSON files into PostgreSQL with Python.

The script already:

- Reads `data/customers.json`
- Reads `data/projects.json`
- Opens a PostgreSQL connection

You still need to add the insert loops and SQL statements for your schema.

Run it from the repository root:

```sh
make import-data
```
