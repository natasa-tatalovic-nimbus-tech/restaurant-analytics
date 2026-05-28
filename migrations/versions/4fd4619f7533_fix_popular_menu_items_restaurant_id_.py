"""fix_popular_menu_items_restaurant_id_type

Revision ID: 4fd4619f7533
Revises: 268d037cb159
Create Date: 2026-05-28 15:57:28.531394

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '4fd4619f7533'
down_revision: Union[str, Sequence[str], None] = '268d037cb159'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.alter_column(
        "popular_menu_items",
        "restaurant_id",
        type_=sa.Integer(),
        schema="analytics",
        postgresql_using="restaurant_id::integer"
    )

def downgrade() -> None:
    op.alter_column(
        "popular_menu_items",
        "restaurant_id",
        type_=sa.String(100),
        schema="analytics",
        postgresql_using="restaurant_id::varchar"
    )
