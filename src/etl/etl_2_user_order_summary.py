"""
1. Reading from database
2. Aggregate orders
3. Write reslts bac
"""

import logging
import time

import pandas as pd
from sqlalchemy import create_engine, text

from helpers.db import get_engine

logger = logging.getLogger(__name__)


# Read from database
def count_user_order_summary(engine):
    logger.info("ETL-2 started")
    start = time.perf_counter()

    orders = pd.read_sql_query("SELECT * FROM restaurant.orders", engine)
    users = pd.read_sql("SELECT id, name, email FROM restaurant.users", engine)

    logger.info("Read rows: orders=%d users=%d", len(orders), len(users))

    # Data quality checks
    assert orders["id"].notna().all(), "Null primary keys in orders"
    assert users["id"].notna().all(), "Null primary keys in users"
    assert (orders["total_price"] > 0).all(), "total_price must be > 0"

    # print(orders)
    # print("---")
    # print(users)

    df = orders.merge(users, left_on="user_id", right_on="id", how="left")
    print("-----")
    # print(df)

    summary = (
        df.groupby(["user_id", "name", "email"])
        .agg(total_orders=("id_x", "count"), total_spent=("total_price", "sum"))
        .reset_index()
    )

    # summary = summary.rename(columns={"user_id": "user_key"})
    summary = summary[["user_id", "name", "email", "total_orders", "total_spent"]]

    assert not summary["user_id"].duplicated().any(), "Duplicate user_ids in summary"
    assert (summary["total_orders"] > 0).all(), "total_orders must be > 0"

    print(summary)
    duration = time.perf_counter() - start
    logger.info(
        "ETL-2 complete | rows_written=%d | duration=%.2fs", len(summary), duration
    )
    return summary


def main():

    # engine = create_engine("postgresql://natasatatalovic:@localhost:5432/postgres")
    engine = get_engine()

    summary = count_user_order_summary(engine)
    summary.to_sql(
        "user_order_summary",
        engine,
        schema="analytics",
        index=False,
        if_exists="replace",
    )


if __name__ == "__main__":
    main()
