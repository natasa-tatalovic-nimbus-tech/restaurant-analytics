from unittest.mock import MagicMock, patch

import pandas as pd
import pytest

from etl.etl_2_user_order_summary import count_user_order_summary


@pytest.mark.unit
class TestCountUserOrderSummary:

    def _data(self):
        orders = pd.DataFrame(
            {
                "id": [1, 2, 3],
                "user_id": [1, 1, 2],
                "restaurant_id": [10, 20, 10],
                "total_price": [12.99, 9.99, 14.99],
                "order_time": ["2024-01-01", "2024-01-02", "2024-01-03"],
            }
        )
        users = pd.DataFrame(
            {
                "id": [1, 2],
                "name": ["Alice", "Bob"],
                "email": ["alice@example.com", "bob@example.com"],
            }
        )
        return orders, users

    def _run(self, orders, users):
        with patch(
            "etl.etl_2_user_order_summary.pd.read_sql_query", return_value=orders
        ), patch("etl.etl_2_user_order_summary.pd.read_sql", return_value=users):
            return count_user_order_summary(MagicMock())

    def test_one_row_per_user(self):
        result = self._run(*self._data())
        assert len(result) == 2

    def test_required_columns_present(self):
        result = self._run(*self._data())
        for col in ["user_id", "name", "email", "total_orders", "total_spent"]:
            assert col in result.columns

    def test_order_count(self):
        result = self._run(*self._data())
        assert result[result["user_id"] == 1].iloc[0]["total_orders"] == 2
        assert result[result["user_id"] == 2].iloc[0]["total_orders"] == 1

    def test_total_spent(self):
        result = self._run(*self._data())
        assert float(
            result[result["user_id"] == 1].iloc[0]["total_spent"]
        ) == pytest.approx(22.98)
        assert float(
            result[result["user_id"] == 2].iloc[0]["total_spent"]
        ) == pytest.approx(14.99)

    def test_empty_orders_returns_empty(self):
        orders = pd.DataFrame(
            columns=["id", "user_id", "restaurant_id", "total_price", "order_time"]
        )
        users = pd.DataFrame(columns=["id", "name", "email"])
        assert len(self._run(orders, users)) == 0

    def test_single_user_single_order(self):
        orders = pd.DataFrame(
            {
                "id": [1],
                "user_id": [1],
                "restaurant_id": [1],
                "total_price": [25.00],
                "order_time": ["2024-01-01"],
            }
        )
        users = pd.DataFrame(
            {"id": [1], "name": ["Alice"], "email": ["alice@example.com"]}
        )
        result = self._run(orders, users)
        assert result.iloc[0]["total_orders"] == 1
        assert float(result.iloc[0]["total_spent"]) == pytest.approx(25.00)
