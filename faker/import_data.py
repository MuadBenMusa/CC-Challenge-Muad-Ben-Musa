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
            #
            # Example shape:
            # cursor.execute(
            #     "insert into ... values (%s, %s)",
            #     (value_1, value_2),
            # )
            pass

        connection.commit()

    print("Import script finished")


if __name__ == "__main__":
    main()
