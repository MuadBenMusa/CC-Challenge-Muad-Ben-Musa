import json
import random
from datetime import date, timedelta
from pathlib import Path

from faker import Faker

OUTPUT_DIR = Path("data")
CUSTOMER_COUNT = 10
PROJECT_COUNT = 100
SEED = 20260730

START_DATE = date(2027, 7, 1)
END_DATE = date(2027, 8, 30)

MUNICIPALITIES = [
    "Hamburg",
    "Bremen",
    "Kiel",
    "Luebeck",
    "Barsbuettel",
    "Flensburg",
    "Rostock",
    "Schwerin",
    "Ploen",
    "Oldenburg",
    "Lueneburg",
    "Cuxhaven",
    "Wilhelmshaven",
    "Bremerhaven",
]

TASKS = ["cleaning", "inspection", "repair"]
STATUSES = ["open", "in progress", "done"]
DESCRIPTIONS = [
    "Routinemaessige Wartung nach starkem Regen.",
    "Folgearbeit aus dem kommunalen Inspektionsplan.",
    "Gemeldete Verstopfung in der Naehe eines Wohngebiets.",
    "Kamerainspektion vor geplanten Strassenarbeiten.",
    "Reparaturabstimmung mit dem lokalen Versorger.",
    "Vorbeugende Reinigung eines wichtigen Rohrabschnitts.",
]


def random_date() -> str:
    days = (END_DATE - START_DATE).days
    return (START_DATE + timedelta(days=random.randint(0, days))).isoformat()


def maybe(value: str, probability: float = 0.9) -> str | None:
    return value if random.random() <= probability else None


def main() -> None:
    random.seed(SEED)
    fake = Faker()
    Faker.seed(SEED)

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    customers = []
    for index in range(1, CUSTOMER_COUNT + 1):
        municipality = random.choice(MUNICIPALITIES)
        customers.append(
            {
                "id": index,
                "name": fake.company(),
                "street": fake.street_address(),
                "postal_code": fake.postcode(),
                "municipality": municipality,
            }
        )

    projects = []
    for index in range(1, PROJECT_COUNT + 1):
        customer = random.choice(customers)
        municipality = random.choice(MUNICIPALITIES)
        task = random.choice(TASKS)
        projects.append(
            {
                "id": index,
                "customer_id": customer["id"],
                "date": random_date(),
                "task": task,
                "location": maybe(f"{municipality}, {fake.street_name()}", 0.94),
                "description": maybe(random.choice(DESCRIPTIONS), 0.86),
                "status": random.choice(STATUSES),
            }
        )

    (OUTPUT_DIR / "customers.json").write_text(
        json.dumps(customers, indent=2, ensure_ascii=True) + "\n",
        encoding="utf-8",
    )
    (OUTPUT_DIR / "projects.json").write_text(
        json.dumps(projects, indent=2, ensure_ascii=True) + "\n",
        encoding="utf-8",
    )

    print(f"Wrote {len(customers)} customers and {len(projects)} projects to {OUTPUT_DIR}")


if __name__ == "__main__":
    main()
