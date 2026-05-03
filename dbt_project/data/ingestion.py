import csv
import psycopg2
from pydantic import BaseModel, Field, ValidationError, EmailStr
from datetime import date
from typing import Optional

class CustomerEvent(BaseModel):
    customer_id: int = Field(gt=0)
    name: str = Field(min_length=2)
    email: EmailStr
    city: Optional[str] = "Unknown"

class ProductEvent(BaseModel):
    product_id: int = Field(gt=0)
    product_name: str
    category: str = "Unknown"
    price: float = Field(gt=0)

class OrderEvent(BaseModel):
    order_id: int = Field(gt=0)
    customer_id: int = Field(gt=0)
    order_date: date
    status: Optional[str] = "PENDING"

class OrderItemEvent(BaseModel):
    order_id: int = Field(gt=0)
    product_id: int = Field(gt=0)
    quantity: int = Field(ge=1)

def run_pipeline():
    conn = psycopg2.connect(host="127.0.0.1", port="5433", user="postgres", password="mypassword", database="analytics_db")
    cursor = conn.cursor()
    
    configs = [
        ("customers.csv", CustomerEvent, "insert into raw_customers (customer_id, name, email, city) values (%s, %s, %s, %s) on conflict (customer_id) do nothing"),
        ("products.csv", ProductEvent, "insert into raw_products (product_id, product_name, category, price) values (%s, %s, %s, %s) on conflict (product_id) do nothing"),
        ("orders.csv", OrderEvent, "insert into raw_orders (order_id, customer_id, order_date, status) values (%s, %s, %s, %s) on conflict (order_id) do nothing"),
        ("order_items.csv", OrderItemEvent, "insert into raw_order_items (order_id, product_id, quantity) values (%s, %s, %s) on conflict (order_id, product_id) do nothing")
    ]
    
    for file_name, model_class, query in configs:
        print(f"processing {file_name}...")
        f = open(file_name, 'r', encoding='utf-8')
        reader = csv.DictReader(f)
        
        for row in reader:
            try:
                data = model_class(**row)
                vals = tuple(data.model_dump().values())
                cursor.execute(query, vals)
            except ValidationError:
                print("bad data skipped")
            except Exception as e:
                print(e)
                
        f.close()
                
    conn.commit()
    cursor.close()
    conn.close()
    print("pipeline done")

if __name__ == "__main__":
    run_pipeline()