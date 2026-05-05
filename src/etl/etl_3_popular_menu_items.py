import pandas as pd
from helpers.db import get_engine
from sqlalchemy import create_engine, text


def main():

    # engine = create_engine("postgresql://natasatatalovic:@localhost:5432/postgres")
    engine = get_engine()
    orders_df = pd.read_sql_query("SELECT * FROM restaurant.order_items", engine)
    menu_items_df = pd.read_sql("SELECT * FROM restaurant.menu_items", engine)
    print(orders_df)
    print("----")
    print(menu_items_df)

    # left_dataframe.merge(right_dataframe, left_on="column_in_left", right_on="column_in_right", how="join_type")

    merged_table_df = orders_df.merge(
        menu_items_df, left_on="menu_item_id", right_on="id", how="left"
    )
    print(merged_table_df)
    print("*****")
    merged_table_df["revenue"] = (
        merged_table_df["quantity"] * merged_table_df["price_x"]
    )
    print(merged_table_df)

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
            "restaurant_id",
            "total_revenue",
            "total_quantity",
            "revenue_rank",
        ]
    ]

    result.to_sql(
        "popular_menu_items",
        engine,
        schema="analytics",
        if_exists="replace",
        index=False,
    )
    print(f"Done. Written {len(result)} rows to analytics.popular_menu_items")


if __name__ == "__main__":
    main()
