"""
-- LOAD CVS INTO DATABASE TABLE --
1. Read CSV
2. DDL scripts
3. Insert in PostgreSQL - parameterized querires
"""

import os

import pandas as pd
from sqlalchemy import create_engine, text

from helpers.db import get_engine
from helpers.paths import (
    MENU_ITEMS_CSV,
    ORDER_ITEMS_CSV,
    ORDERS_CSV,
    RAW_DATA_DIR,
    RESTAURANTS_CSV,
    ROOT,
    SQL_ANALYTICS_DIR,
    SQL_CREATE_DIR,
    USERS_CSV,
)


def main():

    # Run all
    # files = os.listdir("sql/create")
    files = os.listdir(SQL_CREATE_DIR)
    print(files)
    # Extracts the number before the first underscore and converts to int
    sorted_files = sorted(files, key=lambda x: int(x.split("_")[0]))
    print(sorted_files)

    # engine = create_engine("postgresql://natasatatalovic:@localhost:5432/postgres")
    engine = get_engine()

    with engine.begin() as conn:
        for file in sorted_files:
            with open(os.path.join(SQL_CREATE_DIR, file), "r") as f:
                for statement in f.read().split(";"):
                    if statement.strip():
                        conn.execute(text(statement))

    files = {
        "users": USERS_CSV,
        "restaurants": RESTAURANTS_CSV,
        "menu_items": MENU_ITEMS_CSV,
        "orders": ORDERS_CSV,
        "order_items": ORDER_ITEMS_CSV,
    }

    for table, path in files.items():
        print(files.items())
        print(table, path)
        df = pd.read_csv(path)
        # insert df into table
        print(df)
        print("---")
        df.to_sql(table, engine, schema="restaurant", index=False, if_exists="replace")


if __name__ == "__main__":
    main()
