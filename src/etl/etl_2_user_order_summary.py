"""
1. Reading from database
2. Aggregate orders
3. Write reslts bac
"""

import pandas as pd
from helpers.db import get_engine
from sqlalchemy import create_engine, text


# Read from database
def count_user_order_summary(engine):
    orders = pd.read_sql_query("SELECT * FROM restaurant.orders", engine)
    users = pd.read_sql("SELECT id, name, email FROM restaurant.users", engine)

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

    print(summary)
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
