"""add_users_phone

Revision ID: e5fc064582ee
Revises: 3d135084e268
Create Date: 2026-05-14 14:11:12.736370

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'e5fc064582ee'
down_revision: Union[str, Sequence[str], None] = '3d135084e268'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column(
    "users",
    sa.Column("phone", sa.String(20), nullable=True),
    schema="restaurant",
    )

def downgrade() -> None:
    op.drop_column("users", "phone", schema="restaurant")
