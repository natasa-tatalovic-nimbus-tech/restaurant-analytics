import logging
import time

import pandas as pd
from sqlalchemy import create_engine, text

from helpers.db import get_engine

logger = logging.getLogger(__name__)


def create_popular_menu_items(engine):
    logger.info("ETL-3 started")
    start = time.perf_counter()

    orders_df = pd.read_sql_query("SELECT * FROM restaurant.order_items", engine)
    menu_items_df = pd.read_sql("SELECT * FROM restaurant.menu_items", engine)

    # Data quality checks
    assert orders_df["id"].notna().all(), "Null primary keys in order_items"
    assert menu_items_df["id"].notna().all(), "Null primary keys in menu_items"
    assert (orders_df["quantity"] > 0).all(), "quantity must be > 0"

    merged_table_df = orders_df.merge(
        menu_items_df, left_on="menu_item_id", right_on="id", how="left"
    )
    print(merged_table_df)
    print("*****")
    merged_table_df["revenue"] = (
        merged_table_df["quantity"] * merged_table_df["price_x"]
    )
    print(merged_table_df)

    # result = (
    #     # changed
    #     # merged_table_df.groupby(["menu_item_id", "name", "restaurant_id"])
    #     # to
    #     merged_table_df.groupby(["menu_item_id", "name", "restaurant_id_x"])
    #     .agg(total_revenue=("revenue", "sum"), total_quantity=("quantity", "sum"))
    #     .reset_index()
    # )
    # changed 2
    result = (
        merged_table_df.groupby(["menu_item_id", "name", "restaurant_id"])
        .agg(total_revenue=("revenue", "sum"), total_quantity=("quantity", "sum"))
        .reset_index()
    )

    result["revenue_rank"] = (
        result["total_revenue"].rank(method="dense", ascending=False).astype(int)
    )
    # select only the columns that i want to list
    result = result[
        [
            "menu_item_id",
            "name",
            # changed restarant_id
            "restaurant_id",
            "total_revenue",
            "total_quantity",
            "revenue_rank",
        ]
    ]
    # changed
    # result = result.rename(columns={"restaurant_id_x": "restaurant_id"})

    result = result[
        [
            "menu_item_id",
            "name",
            "restaurant_id",
            "total_revenue",
            "total_quantity",
            "revenue_rank",
        ]
    ]

    assert (
        not result["menu_item_id"].duplicated().any()
    ), "Duplicate menu_item_ids in result"
    assert (result["total_revenue"] > 0).all(), "total_revenue must be > 0"

    duration = time.perf_counter() - start
    logger.info(
        "ETL-3 complete | rows_written=%d | duration=%.2fs", len(result), duration
    )

    return result


def main():

    # engine = create_engine("postgresql://natasatatalovic:@localhost:5432/postgres")
    engine = get_engine()
    # print(orders_df)
    # print("----")
    # print(menu_items_df)

    # left_dataframe.merge(right_dataframe, left_on="column_in_left", right_on="column_in_right", how="join_type")

    result = create_popular_menu_items(engine)
    result.to_sql(
        "popular_menu_items",
        engine,
        schema="analytics",
        if_exists="replace",
        index=False,
    )


if __name__ == "__main__":
    main()
