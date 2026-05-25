from unittest.mock import MagicMock, patch

# Mock -> all is fakeOay
import pandas as pd
import pytest

from etl.etl_1_load_csv import load_csv, run_ddl

# pytest with mocked database cursor

# assert raising error if not true, debbuging and testing reasons


@pytest.mark.unit
class TestLoadCsv:

    def _engine(self):
        return MagicMock()

    def _df(self):
        return pd.DataFrame({"id": [1, 2], "name": ["a", "b"]})

    def test_to_sql_called_five_times(self):
        with patch(
            "etl.etl_1_load_csv.pd.read_csv", return_value=self._df()
        ), patch.object(pd.DataFrame, "to_sql") as mock_to_sql:
            load_csv(self._engine())
        assert mock_to_sql.call_count == 5

    def test_schema_is_restaurant(self):
        with patch(
            "etl.etl_1_load_csv.pd.read_csv", return_value=self._df()
        ), patch.object(pd.DataFrame, "to_sql") as mock_to_sql:
            load_csv(self._engine())
        for c in mock_to_sql.call_args_list:
            assert c.kwargs.get("schema") == "restaurant"

    def test_if_exists_append(self):
        with patch(
            "etl.etl_1_load_csv.pd.read_csv", return_value=self._df()
        ), patch.object(pd.DataFrame, "to_sql") as mock_to_sql:
            load_csv(self._engine())
        for c in mock_to_sql.call_args_list:
            assert c.kwargs.get("if_exists") == "append"  # this is corr a

    def test_empty_csv_does_not_crash(self):
        empty = pd.DataFrame(columns=["id", "name"])
        with patch("etl.etl_1_load_csv.pd.read_csv", return_value=empty), patch.object(
            pd.DataFrame, "to_sql"
        ):
            load_csv(self._engine())

    def test_returns_five_table_names(self):
        with patch(
            "etl.etl_1_load_csv.pd.read_csv", return_value=self._df()
        ), patch.object(pd.DataFrame, "to_sql"):
            result = load_csv(self._engine())
        assert set(result) == {
            "users",
            "restaurants",
            "menu_items",
            "orders",
            "order_items",
        }


@pytest.mark.unit
class TestRunDdl:

    def test_executes_sql_statements(self):
        mock_conn = MagicMock()
        mock_engine = MagicMock()
        mock_engine.begin.return_value.__enter__.return_value = mock_conn
        mock_engine.begin.return_value.__exit__.return_value = False

        fake_sql = "CREATE TABLE foo (id INT);\nCREATE TABLE bar (id INT);"
        mock_file = MagicMock()
        mock_file.__enter__.return_value.read.return_value = fake_sql
        mock_file.__exit__.return_value = False

        with patch("etl.etl_1_load_csv.os.listdir", return_value=["1_foo.sql"]), patch(
            "builtins.open", return_value=mock_file
        ):
            run_ddl(mock_engine)

        assert mock_conn.execute.call_count == 2

    def test_files_run_in_numeric_order(self):
        mock_conn = MagicMock()
        mock_engine = MagicMock()
        mock_engine.begin.return_value.__enter__ = MagicMock(return_value=mock_conn)
        mock_engine.begin.return_value.__exit__ = MagicMock(return_value=False)

        with patch(
            "etl.etl_1_load_csv.os.listdir",
            return_value=["3_c.sql", "1_a.sql", "2_b.sql"],
        ), patch(
            "builtins.open",
            MagicMock(
                __enter__=MagicMock(
                    return_value=MagicMock(read=MagicMock(return_value="SELECT 1"))
                ),
                __exit__=MagicMock(return_value=False),
            ),
        ):
            result = run_ddl(mock_engine)

        assert result == ["1_a.sql", "2_b.sql", "3_c.sql"]
