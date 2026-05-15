"""add_index_orders_order_time

Revision ID: 268d037cb159
Revises: e5fc064582ee
Create Date: 2026-05-14 14:11:34.510156

"""

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = "268d037cb159"
down_revision: Union[str, Sequence[str], None] = "e5fc064582ee"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_index(
        "index_orders_order_time",
        "orders",
        ["order_time"],
        schema="restaurant",
    )


def downgrade() -> None:
    op.drop_index(
        "index_orders_order_time",
        table_name="orders",
        schema="restaurant",
    )
