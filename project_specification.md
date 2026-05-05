
---

## Project Overview

Build a restaurant analytics platform that ingests restaurant, user, menu, and order data through ETL pipelines, transforms it into analytical models, and serves insights. The project starts locally with Docker and PostgreSQL, then migrates key components to AWS.

**Domain:** Restaurant order analytics (users, restaurants, menus, orders, order items)

**Data Model:** Normalized relational schema with derived analytical tables (star schema for analytics layer)

---

## Phase 1: Foundation (Local)

### 1.1 Data Modeling

- Design a normalized relational schema for the restaurant domain:
  - `users` (id, name, email)
  - `restaurants` (id, name, address, phone)
  - `menu_items` (id, restaurant_id FK, name, description, price)
  - `orders` (id, user_id FK, restaurant_id FK, total_price, order_time)
  - `order_items` (id, order_id FK, menu_item_id FK, quantity, price)
- Create an ER diagram (draw.io or similar) documenting all tables and relationships
- Design a star schema analytics layer with:
  - **Fact table:** `fact_orders` (order-level metrics: total_price, item_count, order_time)
  - **Dimension tables:** `dim_users`, `dim_restaurants`, `dim_menu_items`, `dim_time`
  - **Derived summary tables:** `user_order_summary`, `popular_menu_items`
- Document SCD Type 2 strategy for `dim_restaurants` (track address/phone changes over time)

### 1.2 Data Storage

- Store raw source data as CSV files in `/data/raw/`
- Use PostgreSQL as the relational database for the operational/analytical layer

### 1.3 SQL

- Write all DDL scripts in `/sql/create/`:
  - `drop_old_schema.sql` - Clean slate
  - `create_schema.sql` - Create `restaurant` schema
  - `create_users_table.sql`, `create_restaurants_table.sql`, `create_menu_items_table.sql`, `create_orders_table.sql`, `create_order_items_table.sql`
  - `create_user_order_summary_table.sql`, `create_popular_menu_items_table.sql`
- Write analytical SQL queries in `/sql/analytics/`:
  - Top restaurants by revenue (using window functions)
  - User spending trends over time (using CTEs)
  - Menu item performance ranking (using RANK/DENSE_RANK)
  - Revenue by time period (GROUP BY with date functions)
- Use transactions and understand isolation levels when loading data

### 1.4 Python for Data Engineering

- Build ETL pipeline modules in `/src/etl/`:
  - **ETL 1 - Load CSV** (`etl_1_load_csv.py`): Read raw CSVs with pandas, execute DDL scripts, insert data into PostgreSQL using parameterized queries via psycopg2
  - **ETL 2 - User Order Summary** (`etl_2_user_order_summary.py`): Read from DB with pandas, aggregate orders per user (total_orders, total_spent), write results back
  - **ETL 3 - Popular Menu Items** (`etl_3_popular_menu_items.py`): Join order_items with menu_items, calculate total_revenue per item, write ranked results
- Use pandas for all transformations (filtering, grouping, joining, aggregation)
- Use SQLAlchemy or psycopg2 for database connections with proper connection management
- Handle missing data, type conversions, and deduplication in the transform steps

### 1.5 Containerization

- Write a `Dockerfile` for the project based on the Apache Airflow image:
  - Install Python dependencies from `requirements.txt`
  - Copy project source code into the container
  - Set PYTHONPATH appropriately
- Write a `docker-compose.yml` with the following services:
  - **db** - PostgreSQL 16 (application database, port 5433)
  - **airflow** - All services needed for running Airflow
- Create `.env.example` with all required environment variables
- Create `.dockerignore` to exclude unnecessary files

---

## Phase 2: Orchestration & Processing (Local)

### 2.1 Orchestration with Airflow

- Create an Airflow DAG (`dags/restaurant_pipeline.py`):
  - DAG ID: `restaurant_pipeline`
  - Schedule: daily (or manual trigger for development)
  - Tasks chained sequentially: `start` -> `etl_1_load_csv` -> `etl_2_user_order_summary` -> `etl_3_popular_menu_items`
  - Use `PythonOperator` for each ETL step
  - Configure retries and retry delays

### 2.2 Batch vs Stream Concepts

- *(Optional)* Add a simple Kafka producer/consumer demo that streams order events

---

## Phase 3: Quality & Engineering Practices (Local)

### 3.1 Version Control & Git

- Initialize a Git repository with a proper `.gitignore`:
  - Exclude: `.env`, `__pycache__`, `data/large_csv/`, `data/parquet/`, `data/join/`, IDE files
  - Include: pipeline code, SQL scripts, DAGs, Dockerfiles, tests, CI config
- Use feature branches for development
- Write meaningful commit messages
- Protect the main branch (require PR reviews)

### 3.2 Schema Migrations

- Set up Alembic for schema migrations in `/migrations/`:
  - Configure `alembic.ini` and `env.py` for the project database
  - Create an initial migration that sets up the base schema
  - Create a migration that adds a new column (e.g., `users.phone`)
  - Create a migration that adds an index on `orders.order_time`
  - Demonstrate UP and DOWN (rollback) migrations

### 3.3 Data Quality & Testing

- **Unit Tests** (`/tests/unit/`):
  - `test_etl_1_load_csv.py` - Test CSV loading with mocked cursor, validate INSERT query construction
  - `test_etl_2_user_order_summary.py` - Test aggregation logic with sample DataFrames, test edge cases (empty data, single user)
  - `test_etl_3_popular_menu_items.py` - Test revenue calculation and ranking logic
  - Use pytest with mocked database connections
- **Integration Tests** (`/tests/integration/`):
  - `test_etl_1_load_csv_integration.py` - Full ETL1 against a real test database, validate schema creation and row counts
  - `test_etl_2_user_order_summary_integration.py` - Run ETL1 then ETL2, validate aggregated results
  - `test_etl_3_popular_menu_items_integration.py` - Run ETL1 then ETL3, validate revenue calculations
  - Use a separate test database with dedicated credentials
  - Include test fixture data in `/tests/data/`
- **Data Quality Checks:**
  - Add assertions in ETL steps: no null primary keys, valid foreign key references, price > 0
  - Validate row counts before and after transformations
  - Check for duplicates after loads

### 3.4 CI/CD Pipeline

- Create `.github/workflows/ci.yml`:
  - Trigger on pull requests
  - Spin up a PostgreSQL 16 service container for integration tests
  - Steps:
    1. Checkout code
    2. Set up Python
    3. Install dependencies
    4. Lint with `black --check .`
    5. Lint with `isort --check-only .`
    6. Run all tests with `pytest`
- Configure `pyproject.toml` for black (line-length=88) and isort (black profile)
- Configure `pytest.ini` with pythonpath

### 3.5 Monitoring & Observability

- Add structured logging to all ETL steps:
  - Log start/end times, row counts processed, success/failure status
  - Use Python's `logging` module with consistent format
- Track pipeline metrics:
  - Execution duration per ETL step
  - Rows read / rows written per step
  - Data freshness (time since last successful run)
- *(Optional)* Set up a dashboard to visualize pipeline metrics

---

## Phase 4: AWS Cloud Deployment

### 4.1 Infrastructure as Code

- Set up Terraform in `/terraform/` for all AWS resources:
  - Provider configuration for AWS
  - Modular structure: `main.tf`, `variables.tf`, `outputs.tf`, per-service modules

### 4.2 AWS S3 - Data Lake

- Create an S3 bucket as the project's data lake:
  - Bucket structure:
    ```
    s3://restaurant-analytics-<env>/
      raw/           # Raw CSV files (landing zone)
      processed/     # Parquet files (processed zone)
      analytics/     # Analytical outputs
    ```
  - Enable versioning on the bucket
  - Upload raw CSV files to `raw/` prefix
  - Store Parquet outputs in `processed/` prefix
- Provision via Terraform

### 4.3 AWS RDS - Managed PostgreSQL

- Deploy a PostgreSQL 16 RDS instance:
  - Instance class: `db.t3.micro` (free tier eligible)
  - Multi-AZ: disabled (cost savings for dev)
  - Automated backups enabled
  - Security group allowing access from Glue and local IP
  - Store credentials in AWS Secrets Manager
- Migrate the local database schema to RDS
- Run schema migrations (Alembic) against RDS
- Provision via Terraform

### 4.4 AWS Glue - ETL Jobs

- Create AWS Glue jobs to replace local ETL scripts:
  - **Glue Job 1 - Ingest:** Read CSVs from S3 `raw/`, write to RDS tables (replaces `etl_1_load_csv.py`)
  - **Glue Job 2 - User Summary:** Read from RDS, compute user_order_summary, write back to RDS (replaces `etl_2_user_order_summary.py`)
  - **Glue Job 3 - Popular Items:** Read from RDS, compute popular_menu_items, write back to RDS (replaces `etl_3_popular_menu_items.py`)
- Use PySpark (Glue's native runtime) for transformations
- Configure Glue job parameters: worker type, number of workers, timeout
- Set up a Glue Workflow or Step Functions to orchestrate the jobs sequentially
- Set up a Glue Crawler to catalog the S3 data in the Glue Data Catalog
- Provision via Terraform

### 4.5 AWS IAM - Security

- Create IAM roles with least-privilege policies:
  - **Glue execution role:** Access to S3 bucket, RDS, CloudWatch Logs, Secrets Manager
  - **CI/CD role:** Deploy Terraform, update Glue jobs, push to S3
- No hardcoded credentials anywhere - use IAM roles, Secrets Manager, and environment variables
- Provision via Terraform

### 4.6 AWS CloudWatch - Monitoring

- Configure CloudWatch for pipeline monitoring:
  - Glue job metrics: execution time, success/failure, DPU usage
  - RDS metrics: CPU, connections, storage
  - Custom metrics: rows processed per job, data freshness
- Set up CloudWatch Alarms:
  - Glue job failure -> SNS notification
  - RDS CPU > 80% -> SNS notification
- Create a CloudWatch Dashboard with key pipeline health metrics
- Provision via Terraform

### 4.7 CI/CD for Cloud

- Extend `.github/workflows/` with a deployment workflow:
  - On merge to main:
    1. Run all tests (existing CI)
    2. `terraform plan` and `terraform apply` for infrastructure changes
    3. Upload updated Glue scripts to S3
    4. Upload new data files to S3 if changed
  - Use OIDC for GitHub Actions -> AWS authentication (no long-lived keys)

---

## Project Structure

```
restaurant-analytics/
├── dags/
│   └── restaurant_pipeline.py          # Airflow DAG (local orchestration)
├── src/
│   ├── etl/
│   │   ├── etl_1_load_csv.py           # ETL: CSV -> PostgreSQL
│   │   ├── etl_2_user_order_summary.py # ETL: Order aggregation
│   │   └── etl_3_popular_menu_items.py # ETL: Revenue analytics
│   ├── helpers/
│   │   ├── db.py                       # Database connection utilities
│   │   └── paths.py                    # Path and config management
│   ├── benchmarks/
│   │   ├── csv_vs_parquet.py           # Storage format comparison
│   │   └── pandas_vs_spark.py          # Processing framework comparison
│   └── glue_jobs/                      # AWS Glue job scripts
│       ├── glue_etl_1_ingest.py
│       ├── glue_etl_2_user_summary.py
│       └── glue_etl_3_popular_items.py
├── sql/
│   ├── create/                         # DDL scripts
│   └── analytics/                      # Analytical queries
├── migrations/                         # Alembic schema migrations
│   ├── alembic.ini
│   ├── env.py
│   └── versions/
├── data/
│   ├── raw/                            # Source CSV files
│   ├── parquet/                        # Generated Parquet files
│   ├── large_csv/                      # Generated benchmark data
│   └── join/                           # Benchmark join outputs
├── tests/
│   ├── unit/                           # Unit tests (mocked DB)
│   ├── integration/                    # Integration tests (real DB)
│   └── data/                           # Test fixture CSV files
├── diagrams/
│   ├── restaurant.drawio               # ER diagram
│   └── restaurant.png
├── terraform/
│   ├── main.tf
│   ├── variables.tf
│   ├── outputs.tf
│   ├── modules/
│   │   ├── s3/
│   │   ├── rds/
│   │   ├── glue/
│   │   ├── iam/
│   │   └── monitoring/
│   └── environments/
│       ├── dev.tfvars
│       └── prod.tfvars
├── .github/
│   └── workflows/
│       ├── ci.yml                      # Test + lint on PR
│       └── deploy.yml                  # Deploy to AWS on merge
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
├── pyproject.toml                      # black + isort config
├── pytest.ini
├── .env.example
├── .gitignore
└── .dockerignore
```

---

## Technology Stack

| Layer | Local | AWS |
|-------|-------|-----|
| Storage (files) | Local filesystem (CSV, Parquet) | S3 |
| Storage (relational) | PostgreSQL 16 (Docker) | RDS PostgreSQL 16 |
| ETL processing | Python + Pandas | AWS Glue (PySpark) |
| Orchestration | Apache Airflow (Docker) | AWS Glue Workflows / Step Functions |
| Containerization | Docker + Docker Compose | - |
| CI/CD | GitHub Actions | GitHub Actions + Terraform |
| Monitoring | Airflow UI + logging | CloudWatch Dashboards + Alarms |
| Infrastructure | Docker Compose | Terraform |
| Schema migrations | Alembic | Alembic (against RDS) |
| Security | `.env` files, DB roles | IAM roles, Secrets Manager |

---

## Suggested Implementation Order

1. **Data modeling & SQL** - Design schema, write DDL, create ER diagram
2. **Python ETL (local)** - Build ETL 1/2/3 with pandas + psycopg2
3. **Docker setup** - Containerize with Dockerfile + docker-compose
4. **Airflow orchestration** - Create DAG, wire up ETL steps
5. **Testing** - Unit tests, integration tests, data quality checks
6. **CI/CD** - GitHub Actions for linting + testing
7. **Schema migrations** - Alembic setup and migration scripts
8. **Monitoring & logging** - Structured logging, Airflow monitoring
9. **Data governance** - Roles, catalog
10. **Terraform & AWS** - S3, RDS, IAM, Glue jobs, CloudWatch
11. **Cloud CI/CD** - Deployment pipeline for AWS resources
