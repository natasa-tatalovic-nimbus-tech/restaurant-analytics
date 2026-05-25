from unittest.mock import MagicMock, patch

import pandas as pd
import pytest

from etl.etl_3_popular_menu_items import create_popular_menu_items


@pytest.mark.unit
class TestBuildPopularMenuItems:

    def _data(self):
        order_items = pd.DataFrame(
            {
                "id": [1, 2, 3, 4, 5],
                "order_id": [1, 1, 2, 3, 3],
                "menu_item_id": [101, 102, 101, 102, 103],
                "quantity": [2, 1, 1, 3, 1],
                "price": [5.00, 10.00, 5.00, 10.00, 8.00],
            }
        )
        menu_items = pd.DataFrame(
            {
                "id": [101, 102, 103],
                "name": ["Burger", "Pizza", "Salad"],
                "price": [5.00, 10.00, 8.00],
                "restaurant_id": [1, 1, 2],
            }
        )
        return order_items, menu_items

    def _run(self, order_items, menu_items):
        with patch(
            "etl.etl_3_popular_menu_items.pd.read_sql_query", return_value=order_items
        ), patch("etl.etl_3_popular_menu_items.pd.read_sql", return_value=menu_items):
            return create_popular_menu_items(MagicMock())

    def test_one_row_per_menu_item(self):
        assert len(self._run(*self._data())) == 3

    def test_required_columns_present(self):
        result = self._run(*self._data())
        for col in [
            "menu_item_id",
            "name",
            "restaurant_id",
            "total_revenue",
            "total_quantity",
            "revenue_rank",
        ]:
            assert col in result.columns

    def test_revenue_burger(self):
        result = self._run(*self._data())
        burger = result[result["menu_item_id"] == 101].iloc[0]
        assert float(burger["total_revenue"]) == pytest.approx(15.00)

    def test_revenue_pizza(self):
        result = self._run(*self._data())
        pizza = result[result["menu_item_id"] == 102].iloc[0]
        assert float(pizza["total_revenue"]) == pytest.approx(40.00)

    def test_quantity_burger(self):
        result = self._run(*self._data())
        assert result[result["menu_item_id"] == 101].iloc[0]["total_quantity"] == 3

    def test_highest_revenue_ranked_first(self):
        result = self._run(*self._data())
        assert result[result["menu_item_id"] == 102].iloc[0]["revenue_rank"] == 1

    def test_ranks_are_dense_no_gaps(self):
        result = self._run(*self._data())
        assert sorted(result["revenue_rank"].tolist()) == [1, 2, 3]

    def test_empty_returns_empty(self):
        order_items = pd.DataFrame(
            columns=[
                "id",
                "order_id",
                "menu_item_id",
                "quantity",
                "price",
            ]
        )
        menu_items = pd.DataFrame(columns=["id", "name", "price", "restaurant_id"])
        assert len(self._run(order_items, menu_items)) == 0
