"""create_base_schema

Revision ID: 3d135084e268
Revises:
Create Date: 2026-05-14 11:02:11.556895

"""

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = "3d135084e268"
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute("CREATE SCHEMA IF NOT EXISTS restaurant")
    op.execute("CREATE SCHEMA IF NOT EXISTS analytics")

    # restaurant.users
    op.create_table(
        "users",
        sa.Column("id", sa.Integer, primary_key=True, autoincrement=True),
        sa.Column("name", sa.String(100), nullable=False),
        sa.Column("email", sa.String(100), nullable=False, unique=True),
        schema="restaurant",
    )

    # restaurant.restaurants
    op.create_table(
        "restaurants",
        sa.Column("id", sa.Integer, primary_key=True, autoincrement=True),
        sa.Column("name", sa.String(100), nullable=False),
        sa.Column("address", sa.Text),
        sa.Column("phone", sa.String(50)),
        schema="restaurant",
    )

    # restaurant.menu_items
    op.create_table(
        "menu_items",
        sa.Column("id", sa.Integer, primary_key=True, autoincrement=True),
        sa.Column(
            "restaurant_id",
            sa.Integer,
            sa.ForeignKey("restaurant.restaurants.id"),
            nullable=False,
        ),
        sa.Column("name", sa.String(100), nullable=False),
        sa.Column("description", sa.Text),
        sa.Column("price", sa.Numeric(10, 2), nullable=False),
        schema="restaurant",
    )

    # restaurant.orders
    op.create_table(
        "orders",
        sa.Column("id", sa.Integer, primary_key=True, autoincrement=True),
        sa.Column(
            "user_id", sa.Integer, sa.ForeignKey("restaurant.users.id"), nullable=False
        ),
        sa.Column(
            "restaurant_id",
            sa.Integer,
            sa.ForeignKey("restaurant.restaurants.id"),
            nullable=False,
        ),
        sa.Column("total_price", sa.Numeric(10, 2)),
        sa.Column(
            "order_time", sa.TIMESTAMP, nullable=False, server_default=sa.func.now()
        ),
        schema="restaurant",
    )

    # restaurant.order_items
    op.create_table(
        "order_items",
        sa.Column("id", sa.Integer, primary_key=True, autoincrement=True),
        sa.Column(
            "order_id",
            sa.Integer,
            sa.ForeignKey("restaurant.orders.id"),
            nullable=False,
        ),
        sa.Column(
            "menu_item_id",
            sa.Integer,
            sa.ForeignKey("restaurant.menu_items.id"),
            nullable=False,
        ),
        sa.Column("quantity", sa.Integer, nullable=False),
        sa.Column("price", sa.Numeric(10, 2), nullable=False),
        schema="restaurant",
    )

    # analytics.dim_users
    op.create_table(
        "dim_users",
        sa.Column("user_key", sa.Integer, primary_key=True, autoincrement=True),
        sa.Column("user_id", sa.Integer, nullable=False),
        sa.Column("name", sa.String(100), nullable=False),
        sa.Column("email", sa.String(100), nullable=False),
        schema="analytics",
    )

    # analytics.dim_restaurants
    op.create_table(
        "dim_restaurants",
        sa.Column("restaurant_key", sa.Integer, primary_key=True, autoincrement=True),
        sa.Column("restaurant_id", sa.Integer, nullable=False),
        sa.Column("name", sa.String(100), nullable=False),
        sa.Column("adress", sa.Text),
        sa.Column("phone", sa.String(100), nullable=False),
        sa.Column(
            "valid_from", sa.Date, nullable=False, server_default=sa.func.current_date()
        ),
        sa.Column("valid_to", sa.Date),
        sa.Column("is_current", sa.Boolean, nullable=False, server_default="true"),
        schema="analytics",
    )

    # analytics.dim_menu_items
    op.create_table(
        "dim_menu_items",
        sa.Column("menu_item_key", sa.Integer, primary_key=True, autoincrement=True),
        sa.Column("menu_item_id", sa.Integer, nullable=False),
        sa.Column("restaurant_id", sa.Integer, nullable=False),
        sa.Column("name", sa.String(100), nullable=False),
        sa.Column("description", sa.Text),
        sa.Column("price", sa.Numeric(10, 2), nullable=False),
        schema="analytics",
    )

    # analytics.dim_time
    op.create_table(
        "dim_time",
        sa.Column("time_key", sa.Integer, primary_key=True, autoincrement=True),
        sa.Column("full_date", sa.Date, nullable=False, unique=True),
        sa.Column("year", sa.Integer, nullable=False),
        sa.Column("month", sa.Integer, nullable=False),
        sa.Column("is_weekend", sa.Boolean, nullable=False, server_default="true"),
        schema="analytics",
    )

    # analytics.fact_orders
    op.create_table(
        "fact_orders",
        sa.Column("order_key", sa.Integer, primary_key=True, autoincrement=True),
        sa.Column(
            "user_key", sa.Integer, sa.ForeignKey("analytics.dim_users.user_key")
        ),
        sa.Column(
            "restaurant_key",
            sa.Integer,
            sa.ForeignKey("analytics.dim_restaurants.restaurant_key"),
        ),
        sa.Column("time_key", sa.Integer, sa.ForeignKey("analytics.dim_time.time_key")),
        sa.Column("total_price", sa.Numeric(10, 2)),
        sa.Column("item_count", sa.Integer),
        sa.Column("order_time", sa.TIMESTAMP(timezone=True)),
        schema="analytics",
    )

    # analytics.popular_menu_items
    op.create_table(
        "popular_menu_items",
        sa.Column(
            "menu_item_id", sa.Integer, sa.ForeignKey("restaurant.menu_items.id")
        ),
        sa.Column("name", sa.String(100)),
        sa.Column("restaurant_id", sa.String(100)),
        sa.Column("total_quantity", sa.Integer),
        sa.Column("total_revenue", sa.Numeric(10, 2)),
        sa.Column("revene_rank", sa.Integer),
        schema="analytics",
    )

    # analytics.user_order_summary
    op.create_table(
        "user_order_summary",
        sa.Column("user_id", sa.Integer, primary_key=True),
        sa.Column("name", sa.String(100), nullable=False),
        sa.Column("email", sa.String(100), nullable=False, unique=True),
        sa.Column("total_orders", sa.Integer, nullable=False, server_default="0"),
        sa.Column(
            "total_spent", sa.Numeric(10, 2), nullable=False, server_default="0.00"
        ),
        schema="analytics",
    )


def downgrade() -> None:
    op.drop_table("user_order_summary", schema="analytics")
    op.drop_table("popular_menu_items", schema="analytics")
    op.drop_table("fact_orders", schema="analytics")
    op.drop_table("dim_time", schema="analytics")
    op.drop_table("dim_menu_items", schema="analytics")
    op.drop_table("dim_restaurants", schema="analytics")
    op.drop_table("dim_users", schema="analytics")
    op.drop_table("order_items", schema="restaurant")
    op.drop_table("orders", schema="restaurant")
    op.drop_table("menu_items", schema="restaurant")
    op.drop_table("restaurants", schema="restaurant")
    op.drop_table("users", schema="restaurant")
    op.execute("DROP SCHEMA IF EXISTS analytics CASCADE")
    op.execute("DROP SCHEMA IF EXISTS restaurant CASCADE")
