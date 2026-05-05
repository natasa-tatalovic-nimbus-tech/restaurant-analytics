import sys
from datetime import datetime, timedelta

sys.path.insert(0, "/opt/airflow/src")

from airflow import DAG
from airflow.providers.standard.operators.empty import EmptyOperator
from airflow.providers.standard.operators.python import PythonOperator

from etl.etl_1_load_csv import main as etl_1
from etl.etl_2_user_order_summary import main as etl_2
from etl.etl_3_popular_menu_items import main as etl_3

default_args = {
    "owner": "airflow",
    "depends_on_past": False,
    "retries": 3,
    "retry_delay": timedelta(minutes=5),
    "email_on_failure": False,
    "email_on_retry": False,
}

with DAG(
    dag_id="restaurant_pipeline",
    default_args=default_args,
    description="Restaurant analytics ETL pipeline",
    schedule=None,
    start_date=datetime(2024, 1, 1),
    catchup=False,
    tags=["restaurant", "etl"],
) as dag:

    start = EmptyOperator(task_id="start")

    load_csv = PythonOperator(
        task_id="etl_1_load_csv",
        python_callable=etl_1,
    )

    user_summary = PythonOperator(
        task_id="etl_2_user_order_summary",
        python_callable=etl_2,
    )

    popular_items = PythonOperator(
        task_id="etl_3_popular_menu_items",
        python_callable=etl_3,
    )

    start >> load_csv >> user_summary >> popular_items
