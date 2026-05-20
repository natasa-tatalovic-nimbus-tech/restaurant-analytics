import os
from unittest.mock import patch

import pytest
from sqlalchemy import text

from etl.etl_1_load_csv import load_csv, run_ddl
from etl.etl_3_popular_menu_items import create_popular_menu_items

DATA_DIR = os.path.join(os.path.dirname(__file__), "../data")


def load_fixtures(engine):
    run_ddl(engine)
    with patch("helpers.paths.USERS_CSV", os.path.join(DATA_DIR, "users.csv")), patch(
        "helpers.paths.RESTAURANTS_CSV", os.path.join(DATA_DIR, "restaurants.csv")
    ), patch(
        "helpers.paths.MENU_ITEMS_CSV", os.path.join(DATA_DIR, "menu_items.csv")
    ), patch(
        "helpers.paths.ORDERS_CSV", os.path.join(DATA_DIR, "orders.csv")
    ), patch(
        "helpers.paths.ORDER_ITEMS_CSV", os.path.join(DATA_DIR, "order_items.csv")
    ):
        load_csv(engine)


@pytest.mark.integration
def test_popular_items_row_count(clean_db, test_engine):
    load_fixtures(test_engine)
    result = create_popular_menu_items(test_engine)
    assert len(result) == 3
    # 3 distinct menu items in fixture order_items


@pytest.mark.integration
def test_margherita_revenue(clean_db, test_engine):
    load_fixtures(test_engine)
    result = create_popular_menu_items(test_engine)

    margherita = result[result["name"] == "Margherita"].iloc[0]
    assert float(margherita["total_revenue"]) == pytest.approx(20.00)
    # order_item 1: qty 1 * price 10.00 = 10.00
    # order_item 4: qty 1 * price 10.00 = 10.00
    # total = 20.00


@pytest.mark.integration
def test_highest_revenue_gets_rank_1(clean_db, test_engine):
    load_fixtures(test_engine)
    result = create_popular_menu_items(test_engine)

    top_item = result[result["revenue_rank"] == 1].iloc[0]
    assert float(top_item["total_revenue"]) == result["total_revenue"].max()
    # rank 1 must be the item with highest total_revenue


@pytest.mark.integration
def test_result_written_to_analytics(clean_db, test_engine):
    load_fixtures(test_engine)
    result = create_popular_menu_items(test_engine)
    result.to_sql(
        "popular_menu_items",
        test_engine,
        schema="analytics",
        if_exists="replace",
        index=False,
    )

    with test_engine.connect() as conn:
        count = conn.execute(
            text("SELECT COUNT(*) FROM analytics.popular_menu_items")
        ).scalar()
    assert count == 3
