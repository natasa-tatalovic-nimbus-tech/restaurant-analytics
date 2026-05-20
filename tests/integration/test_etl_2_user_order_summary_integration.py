import os
from unittest.mock import patch

import pytest
from sqlalchemy import text

from etl.etl_1_load_csv import load_csv, run_ddl
from etl.etl_2_user_order_summary import count_user_order_summary

DATA_DIR = os.path.join(os.path.dirname(__file__), "../data")

# reusable dict of path patches - avoids repeating this in every test
CSV_PATCHES = {
    "helpers.paths.USERS_CSV": os.path.join(DATA_DIR, "users.csv"),
    "helpers.paths.RESTAURANTS_CSV": os.path.join(DATA_DIR, "restaurants.csv"),
    "helpers.paths.MENU_ITEMS_CSV": os.path.join(DATA_DIR, "menu_items.csv"),
    "helpers.paths.ORDERS_CSV": os.path.join(DATA_DIR, "orders.csv"),
    "helpers.paths.ORDER_ITEMS_CSV": os.path.join(DATA_DIR, "order_items.csv"),
}


def load_fixtures(engine):
    # helper to run ETL1 with fixture data in one line
    # called at the start of every test in this file
    run_ddl(engine)
    with patch.multiple(
        "helpers.paths", **{k.split(".")[-1].upper(): v for k, v in CSV_PATCHES.items()}
    ):
        load_csv(engine)


@pytest.mark.integration
def test_summary_row_count(clean_db, test_engine):
    load_fixtures(test_engine)
    result = count_user_order_summary(test_engine)
    # runs the real aggregation against real data in test DB
    assert len(result) == 2
    # 2 users in fixture data = 2 rows in summary


@pytest.mark.integration
def test_alice_order_count_and_spend(clean_db, test_engine):
    load_fixtures(test_engine)
    result = count_user_order_summary(test_engine)

    alice = result[result["name"] == "Alice"].iloc[0]
    assert alice["total_orders"] == 2
    # Alice has orders 1 and 2 in fixture data
    assert float(alice["total_spent"]) == pytest.approx(30.00)
    # order 1: 22.00, order 2: 8.00, total: 30.00


@pytest.mark.integration
def test_bob_order_count_and_spend(clean_db, test_engine):
    load_fixtures(test_engine)
    result = count_user_order_summary(test_engine)

    bob = result[result["name"] == "Bob"].iloc[0]
    assert bob["total_orders"] == 1
    assert float(bob["total_spent"]) == pytest.approx(10.00)


@pytest.mark.integration
def test_summary_written_to_analytics_schema(clean_db, test_engine):
    load_fixtures(test_engine)
    result = count_user_order_summary(test_engine)

    result.to_sql(
        "user_order_summary",
        test_engine,
        schema="analytics",
        if_exists="replace",
        index=False,
    )
    # writes result to analytics schema in test DB

    with test_engine.connect() as conn:
        count = conn.execute(
            text("SELECT COUNT(*) FROM analytics.user_order_summary")
        ).scalar()
    assert count == 2
    # verifies the write actually happened and row count is correct
