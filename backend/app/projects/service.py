from ..db import get_connection

from psycopg.errors import ForeignKeyViolation
from .schemas import ProjectCreate, ProjectRead

class CustomerNotFoundError(Exception):
    pass


async def get_projects(status: str | None = None) -> list[ProjectRead]:
    async with get_connection() as connection:
        async with connection.cursor() as cursor:
            if status:
                await cursor.execute(
                    """
                    SELECT
                        c.name AS customer_name,
                        p.date,
                        p.task,
                        p.location,
                        p.description,
                        p.status
                    FROM projects p
                    JOIN customers c ON c.id = p.customer_id
                    WHERE p.status = %s
                    ORDER BY p.date ASC;
                    """,
                    (status,),
                )
            else:
                await cursor.execute(
                    """
                    SELECT
                        c.name AS customer_name,
                        p.date,
                        p.task,
                        p.location,
                        p.description,
                        p.status
                    FROM projects p
                    JOIN customers c ON c.id = p.customer_id
                    ORDER BY p.date ASC;
                    """
                )

            rows = await cursor.fetchall()
            return [ProjectRead.model_validate(row) for row in rows]


async def create_project(project: ProjectCreate) -> ProjectRead:
    try:
        async with get_connection() as connection:
            async with connection.cursor() as cursor:
                await cursor.execute(
                    """
                    WITH inserted AS (
                        INSERT INTO projects (
                            customer_id,
                            date,
                            task,
                            location,
                            description,
                            status
                        )
                        VALUES (%s, %s, %s, %s, %s, %s)
                        RETURNING
                            customer_id,
                            date,
                            task,
                            location,
                            description,
                            status
                    )
                    SELECT
                        c.name AS customer_name,
                        i.date,
                        i.task,
                        i.location,
                        i.description,
                        i.status
                    FROM inserted i
                    JOIN customers c ON c.id = i.customer_id;
                    """,
                    (
                        project.customer_id,
                        project.date,
                        project.task,
                        project.location,
                        project.description,
                        project.status,
                    ),
                )

                row = await cursor.fetchone()

                if row is None:
                    raise RuntimeError("Created project could not be returned.")

                return ProjectRead.model_validate(row)

    except ForeignKeyViolation as exc:
        raise CustomerNotFoundError from exc