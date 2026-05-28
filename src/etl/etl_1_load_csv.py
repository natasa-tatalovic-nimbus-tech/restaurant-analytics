"""
-- LOAD CVS INTO DATABASE TABLE --
1. Read CSV
2. DDL scripts
3. Insert in PostgreSQL - parameterized querires
"""

import logging
import os
import time

import pandas as pd
from sqlalchemy import create_engine, text

from helpers.db import get_engine
from helpers.paths import (
    MENU_ITEMS_CSV,
    ORDER_ITEMS_CSV,
    ORDERS_CSV,
    RESTAURANTS_CSV,
    SQL_CREATE_DIR,
    USERS_CSV,
)

logger = logging.getLogger(__name__)


def run_ddl(engine):
    files = os.listdir(SQL_CREATE_DIR)
    print(files)
    # Extracts the number before the first underscore and converts to int
    sorted_files = sorted(files, key=lambda x: int(x.split("_")[0]))
    print(sorted_files)

    with engine.begin() as conn:
        for file in sorted_files:
            with open(os.path.join(SQL_CREATE_DIR, file), "r") as f:
                for statement in f.read().split(";"):
                    if statement.strip():
                        conn.execute(text(statement))
    return sorted_files


def load_csv(engine):
    # -- Logging --
    logger.info("ETL-1 started")
    start = time.perf_counter()

    files = {
        "users": USERS_CSV,
        "restaurants": RESTAURANTS_CSV,
        "menu_items": MENU_ITEMS_CSV,
        "orders": ORDERS_CSV,
        "order_items": ORDER_ITEMS_CSV,
    }
    with engine.begin() as conn:
        # truncate in reverse dependency order to avoid FK violations
        conn.execute(
            text(
                "TRUNCATE TABLE restaurant.order_items, restaurant.orders, restaurant.menu_items, restaurant.restaurants, restaurant.users RESTART IDENTITY CASCADE"
            )
        )

    for table, path in files.items():
        # print(files.items())
        # print(table, path)
        df = pd.read_csv(path)
        # insert df into table
        # print(df)
        # print("---")
        # df.to_sql(table, engine, schema="restaurant", index=False, if_exists="append")
        # Data quality checks
        assert df["id"].notna().all(), f"Null primary keys found in {table}"
        assert not df["id"].duplicated().any(), f"Duplicate IDs found in {table}"
        if "price" in df.columns:
            assert (df["price"] > 0).all(), f"Price must be > 0 in {table}"

        row_count_before = len(df)
        if row_count_before == 0:
            continue
        df.to_sql(table, engine, schema="restaurant", index=False, if_exists="append")
        logger.info("Loaded table=%s rows=%d", table, row_count_before)
        assert row_count_before > 0, f"No rows written for {table}"

        # -- Duration --
        duration = time.perf_counter() - start
        logger.info("ETL-1 started")

    return list(files.keys())


def main():

    # Run all
    # files = os.listdir("sql/create")
    # engine = create_engine("postgresql://natasatatalovic:@localhost:5432/postgres")
    engine = get_engine()  # SQl Alchemy  engine to Docker PostgreSQL
    # run_ddl(engine)
    load_csv(engine)


if __name__ == "__main__":
    main()
