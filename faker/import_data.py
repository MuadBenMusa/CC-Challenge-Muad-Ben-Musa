import json
import os
from pathlib import Path

from psycopg import connect

DATA_DIR = Path(os.environ.get("DATA_DIR", "data"))
DATABASE_URL = os.environ.get(
    "DATABASE_URL",
    "postgres://challenge:challenge@postgres:5432/challenge?sslmode=disable",
)


def load_json(filename: str) -> list[dict]:
    return json.loads((DATA_DIR / filename).read_text(encoding="utf-8"))


def main() -> None:
    customers = load_json("customers.json")
    projects = load_json("projects.json")

    print(f"Loaded {len(customers)} customers and {len(projects)} projects")

    with connect(DATABASE_URL) as connection:

        with connection.cursor() as cursor:
            # Rebuild the generated seed dataset so the importer can be rerun safely.
            cursor.execute(
                "TRUNCATE TABLE projects, customers RESTART IDENTITY;"
            )
            for customer in customers:
                cursor.execute(
                    """
                    INSERT INTO customers (id, name, street, postal_code, municipality) 
                    VALUES (%s, %s, %s, %s, %s);
                    """,
                    (
                        customer["id"],
                        customer["name"],
                        customer["street"],
                        customer["postal_code"],
                        customer["municipality"],
                    ),
                )

            for project in projects:
                cursor.execute(
                    """
                    INSERT INTO projects (id, customer_id, date, task, location, description, status) 
                    VALUES (%s, %s, %s, %s, %s, %s, %s);
                    """,
                    (
                        project["id"],
                        project["customer_id"],
                        project["date"],
                        project["task"],
                        project["location"],
                        project["description"],
                        project["status"],
                    ),
                )

            # Explicitly imported IDs do not advance the identity sequence,
            # so synchronize it before POST /projects generates new IDs.
            cursor.execute(
                """
                SELECT setval(
                    pg_get_serial_sequence('customers', 'id'),
                    (SELECT MAX(id) FROM customers)
                );
                """
            )
            cursor.execute(
                """
                SELECT setval(
                    pg_get_serial_sequence('projects', 'id'),
                    (SELECT MAX(id) FROM projects)
                );
                """
            )

    print("Import script finished")


if __name__ == "__main__":
    main()
