
# Restaurant Analytics Platform

---

## Phase 1-3 — Local Development

### Prerequisites

- Docker Desktop
- Python 3.11
- Git

### Setup

```bash
git clone https://github.com/natasa-tatalovic-nimbus-tech/restaurant-analytics.git
cd restaurant-analytics
cp .env.example .env
```

### Start the pipeline

```bash
# Step 1 — Start PostgreSQL + Airflow (fresh start)
docker compose down -v
docker compose up -d
docker compose logs airflow-init -f

# Step 2 — Run migrations
alembic upgrade head
alembic current

# Step 3 — Verify schema was created
docker compose exec db psql -U airflow -d restaurant_db -c "\dt restaurant.*"
docker compose exec db psql -U airflow -d restaurant_db -c "\dt analytics.*"
docker compose exec db psql -U airflow -d restaurant_db -c "\d restaurant.users"

# Step 4 — Trigger the pipeline
# Open http://localhost:8080
# Find restaurant_pipeline DAG and trigger it manually

# Step 5 — Verify data loaded
docker compose exec db psql -U airflow -d restaurant_db -c "SELECT COUNT(*) FROM restaurant.users;"
docker compose exec db psql -U airflow -d restaurant_db -c "SELECT COUNT(*) FROM restaurant.orders;"
docker compose exec db psql -U airflow -d restaurant_db -c "SELECT COUNT(*) FROM analytics.user_order_summary;"
docker compose exec db psql -U airflow -d restaurant_db -c "SELECT COUNT(*) FROM analytics.popular_menu_items;"
```

Expected counts: 10 users, 20 orders, 10 user summaries, 18 popular menu items.

### Run tests

```bash
pip install -r requirements.txt

# Step 1 — Create test database
docker compose exec db psql -U airflow -d postgres -c "CREATE DATABASE restaurant_test;"

# Step 2 — Run migrations against test database
DATABASE_URL=postgresql://airflow:airflow@localhost:5433/restaurant_test alembic upgrade head

# Step 3 — Run tests
pytest tests/unit/ -v       # unit tests — no database needed
pytest tests/integration/ -v # integration tests — requires Docker running
pytest                       # all tests
```

### Schema migrations

```bash
# Apply all pending migrations
alembic upgrade head

# Check current version
alembic current

# Roll back one migration
alembic downgrade -1

# Roll forward again
alembic upgrade head

# See full migration history
alembic history
```

### Verify migration correctness

```bash
# Check phone column exists on users
docker compose exec db psql -U airflow -d restaurant_test -c "\d restaurant.users"

# Check index exists on orders
docker compose exec db psql -U airflow -d restaurant_test -c "\d restaurant.orders"

# Check restaurant_id is INTEGER in popular_menu_items
docker compose exec db psql -U airflow -d restaurant_test -c "\d analytics.popular_menu_items"
```

### Code formatting

```bash
# Format code locally
black .
isort .

# Check only — same as what CI runs
black --check .
isort --check-only .
```

### Docker commands reference

```bash
docker compose up -d              # start all services detached
docker compose down               # stop containers, keep database volume
docker compose down -v            # stop containers AND delete database volume
docker compose ps                 # check running containers
docker compose logs airflow-init -f  # watch init logs
docker compose up --build         # rebuild Docker image then start
```

---

## Phase 4 — AWS Cloud Deployment

### Prerequisites

- AWS CLI v2 — `aws --version` must show 2.x.x
- Terraform >= 1.6 — `terraform -version`
- AWS credentials from your AWS portal

### Set AWS credentials

```bash
export AWS_ACCESS_KEY_ID="your-access-key"
export AWS_SECRET_ACCESS_KEY="your-secret-key"
export AWS_SESSION_TOKEN="your-session-token"
export AWS_DEFAULT_REGION="eu-central-1"

# Verify credentials work
aws sts get-caller-identity
```

> Credentials expire every session. Re-export them every time you open a new terminal.


```bash
# Create S3 state bucket
aws s3 mb s3://restaurant-analytics-s3-natasa --region eu-central-1

# Enable versioning on state bucket
aws s3api put-bucket-versioning \
  --bucket restaurant-analytics-s3-natasa \
  --versioning-configuration Status=Enabled
```

### Deploy infrastructure

```bash
cd terraform

# Download providers, connect to state bucket
terraform init

# Preview changes — nothing in AWS is modified
terraform plan -var="env=dev"

# Apply changes — creates real AWS resources
terraform apply -var="env=dev"
```

### Upload CSV files to S3

```bash
aws s3 cp data/raw/ s3://restaurant-analytics-dev/raw/ --recursive

# Verify upload
aws s3 ls s3://restaurant-analytics-dev/raw/
```

### Store Neon connection string in Secrets Manager

```bash
export NEON_DB_URL='postgresql://neondb_owner:password@host.neon.tech/neondb?sslmode=require'

aws secretsmanager create-secret \
  --name "natasa/restaurant/dev/neon-db-url" \
  --description "Neon PostgreSQL connection string for natasa restaurant project" \
  --secret-string "{\"url\":\"$NEON_DB_URL\"}" \
  --region eu-central-1

# Verify secret was stored
aws secretsmanager list-secrets --region eu-central-1 --query "SecretList[].Name"
```

### Run migrations against Neon

```bash
export DATABASE_URL='postgresql://neondb_owner:password@host.neon.tech/neondb?sslmode=require'
alembic upgrade head

# Verify schemas exist
psql $DATABASE_URL -c "\dn"

# Verify tables exist
psql $DATABASE_URL -c "\dt restaurant.*"
psql $DATABASE_URL -c "\dt analytics.*"
```

### Verify S3 data lake

```bash
# See all prefixes in data lake bucket
aws s3 ls s3://restaurant-analytics-dev/

# See CSV files in raw prefix
aws s3 ls s3://restaurant-analytics-dev/raw/

# See Terraform state (separate bucket)
aws s3 ls s3://restaurant-analytics-s3-natasa/
```
