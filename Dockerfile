# Use the official Apache Airflow image as the base
FROM apache/airflow:3.2.1-python3.11

# Switch to
USER airflow

# Install dependencies
COPY requirements.txt /requirements.txt
RUN pip install --no-cache-dir -r /requirements.txt

USER root
COPY src/ /opt/airflow/src/
COPY sql/ /opt/airflow/sql/
COPY data/ /opt/airflow/data/

ENV PYTHONPATH="/opt/airflow/src:${PYTHONPATH}"

# switch back to airflow
USER airflow