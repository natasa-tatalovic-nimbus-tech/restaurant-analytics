import os
from unittest.mock import patch

import pytest
from sqlalchemy import inspect, text

from etl.etl_1_load_csv import load_csv

# path to fixture CSVs
DATA_DIR = os.path.join(os.path.dirname(__file__), "../data")


@pytest.mark.integration
def test_ddl_creates_tables(clean_db, test_engine):
    # clean_db fixture drops/recreates schemas before this test runs
    # test_engine is the real connection to restaurant_test DB
    # run_ddl(test_engine)
    # runs all SQL scripts in sql/create/ against the test DB

    inspector = inspect(test_engine)
    # inspect() lets you query the DB schema without writing raw SQL
    tables = inspector.get_table_names(schema="restaurant")
    # returns list of table names that actually exist in the DB

    for table in ["users", "restaurants", "menu_items", "orders", "order_items"]:
        assert table in tables, f"Table {table} was not created"
    # verifies every expected table exists after DDL runs


@pytest.mark.integration
def test_load_csv_row_counts(clean_db, test_engine):
    # run_ddl(test_engine)

    with patch(
        "etl.etl_1_load_csv.USERS_CSV", os.path.join(DATA_DIR, "users.csv")
    ), patch(
        "etl.etl_1_load_csv.RESTAURANTS_CSV", os.path.join(DATA_DIR, "restaurants.csv")
    ), patch(
        "etl.etl_1_load_csv.MENU_ITEMS_CSV", os.path.join(DATA_DIR, "menu_items.csv")
    ), patch(
        "etl.etl_1_load_csv.ORDERS_CSV", os.path.join(DATA_DIR, "orders.csv")
    ), patch(
        "etl.etl_1_load_csv.ORDER_ITEMS_CSV", os.path.join(DATA_DIR, "order_items.csv")
    ):
        # patches the path constants to point at fixture CSVs instead of real data
        # so load_csv reads our small controlled files, not production data
        load_csv(test_engine)

    with test_engine.connect() as conn:
        # query the real DB to verify rows were actually inserted
        assert conn.execute(text("SELECT COUNT(*) FROM restaurant.users")).scalar() == 2
        # .scalar() returns the single value from a single-row single-column result
        assert (
            conn.execute(text("SELECT COUNT(*) FROM restaurant.restaurants")).scalar()
            == 2
        )
        assert (
            conn.execute(text("SELECT COUNT(*) FROM restaurant.menu_items")).scalar()
            == 3
        )
        assert (
            conn.execute(text("SELECT COUNT(*) FROM restaurant.orders")).scalar() == 3
        )
        assert (
            conn.execute(text("SELECT COUNT(*) FROM restaurant.order_items")).scalar()
            == 4
        )


@pytest.mark.integration
def test_no_duplicates_on_rerun(clean_db, test_engine):
    with patch(
        "etl.etl_1_load_csv.USERS_CSV", os.path.join(DATA_DIR, "users.csv")
    ), patch(
        "etl.etl_1_load_csv.RESTAURANTS_CSV", os.path.join(DATA_DIR, "restaurants.csv")
    ), patch(
        "etl.etl_1_load_csv.MENU_ITEMS_CSV", os.path.join(DATA_DIR, "menu_items.csv")
    ), patch(
        "etl.etl_1_load_csv.ORDERS_CSV", os.path.join(DATA_DIR, "orders.csv")
    ), patch(
        "etl.etl_1_load_csv.ORDER_ITEMS_CSV", os.path.join(DATA_DIR, "order_items.csv")
    ):
        load_csv(test_engine)
        load_csv(test_engine)

    with test_engine.connect() as conn:
        assert conn.execute(text("SELECT COUNT(*) FROM restaurant.users")).scalar() == 2
        # still 2 rows, not 4 - proves replace works correctly
