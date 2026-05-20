import os

import pytest
from dotenv import load_dotenv
from sqlalchemy import create_engine, text

# pytest file
load_dotenv()

TEST_DB_URL = (
    f"postgresql://{os.getenv('TEST_DB_USER')}:{os.getenv('TEST_DB_PASSWORD')}"
    f"@{os.getenv('TEST_DB_HOST')}:{os.getenv('TEST_DB_PORT')}/{os.getenv('TEST_DB_NAME')}"
)
# postgresql://airflow:airflow@localhost:5433/restaurant_test


@pytest.fixture(scope="session")  # created once
def test_engine():
    engine = create_engine(TEST_DB_URL)
    yield engine
    engine.dispose()


@pytest.fixture()
def clean_db(test_engine):
    with test_engine.begin() as conn:
        conn.execute(text("DROP SCHEMA IF EXISTS restaurant CASCADE"))
        conn.execute(text("DROP SCHEMA IF EXISTS analytics CASCADE"))
        conn.execute(text("CREATE SCHEMA restaurant"))
        conn.execute(text("CREATE SCHEMA analytics"))
    yield
