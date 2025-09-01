"""Add seed data

Revision ID: 500aa448381a
Revises: 5fdb96de961e
Create Date: 2025-09-01 15:15:33.329013

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.sql import table, column
from sqlalchemy.dialects.postgresql import UUID
import uuid

# revision identifiers, used by Alembic.
revision: str = "500aa448381a"
down_revision: Union[str, None] = "5fdb96de961e"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Define table for seed data
    patients_table = table(
        "patients",
        column("id", UUID),
        column("name", sa.String),
        column("age", sa.Integer),
        column("diagnosis", sa.String),
    )

    # Insert seed data
    op.bulk_insert(
        patients_table,
        [
            {
                "id": str(uuid.uuid4()),
                "name": "John",
                "age": 22,
                "diagnosis": "What happened?",
            },
            {
                "id": str(uuid.uuid4()),
                "name": "Jack",
                "age": 23,
                "diagnosis": "Experiments",
            },
        ],
    )


def downgrade() -> None:
    op.execute("DELETE FROM patients WHERE name IN ('John', 'Jack')")
