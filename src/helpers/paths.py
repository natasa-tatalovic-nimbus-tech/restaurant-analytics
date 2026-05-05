import os

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

RAW_DATA_DIR = os.path.join(ROOT, "data", "raw")
USERS_CSV = os.path.join(RAW_DATA_DIR, "users.csv")
RESTAURANTS_CSV = os.path.join(RAW_DATA_DIR, "restaurants.csv")
MENU_ITEMS_CSV = os.path.join(RAW_DATA_DIR, "menu_items.csv")
ORDERS_CSV = os.path.join(RAW_DATA_DIR, "orders.csv")
ORDER_ITEMS_CSV = os.path.join(RAW_DATA_DIR, "order_items.csv")

SQL_CREATE_DIR = os.path.join(ROOT, "sql", "create")
SQL_ANALYTICS_DIR = os.path.join(ROOT, "sql", "analytics")

print(ROOT)
print(SQL_CREATE_DIR)
