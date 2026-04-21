import pandas as pd
from sqlalchemy import create_engine
from pydantic import BaseModel

# Database connection
DATABASE_URL = "postgresql://postgres:mypassword@127.0.0.1:5433/analytics_db"
engine = create_engine(DATABASE_URL)

# Models for validation
class Cust(BaseModel):
    customer_id: int
    name: str
    email: str
    city: str

class Prod(BaseModel):
    product_id: int
    product_name: str
    category: str
    price: float

class Order(BaseModel):
    order_id: int
    customer_id: int
    order_date: str
    status: str

class OrderItem(BaseModel):
    order_id: int
    product_id: int
    quantity: int

def ingest_all():
    # Saari files ki list yahan hai
    files = {
        'customers.csv': ('raw_customers', Cust),
        'products.csv': ('raw_products', Prod),
        'orders.csv': ('raw_orders', Order),
        'order_items.csv': ('raw_order_items', OrderItem)
    }

    for file_name, (table_name, model) in files.items():
        try:
            df = pd.read_csv(f'data/{file_name}')
            # Validation logic
            valid_data = [model(**row).model_dump() for _, row in df.iterrows()]
            
            # Save to db
            pd.DataFrame(valid_data).to_sql(table_name, engine, if_exists='replace', index=False)
            print("Success: " + file_name + " save ho gyi")
            
        except Exception as e:
            print("Error in " + file_name + " : " + str(e))

if __name__ == "__main__":
    ingest_all()