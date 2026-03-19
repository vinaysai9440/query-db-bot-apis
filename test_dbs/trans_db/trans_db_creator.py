import sys
import os
from datetime import datetime, timedelta
import random

current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir)

from sqlalchemy import (
    create_engine,
    Column,
    Integer,
    String,
    Boolean,
    Date,
    DateTime,
    DECIMAL,
    Text,
    ForeignKey,
)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

TransBase = declarative_base()


class Customer(TransBase):
    __tablename__ = "customers"

    customer_id = Column(Integer, primary_key=True)
    first_name = Column(String(50), nullable=False)
    last_name = Column(String(50), nullable=False)
    email = Column(String(100), unique=True)
    phone = Column(String(20))
    registration_date = Column(Date)
    country = Column(String(50))
    city = Column(String(50))
    is_active = Column(Boolean, default=True)


class Order(TransBase):
    __tablename__ = "orders"

    order_id = Column(Integer, primary_key=True)
    customer_id = Column(Integer, ForeignKey("customers.customer_id"))
    order_date = Column(DateTime)
    total_amount = Column(DECIMAL(10, 2))
    status = Column(String(20))
    payment_method = Column(String(30))
    shipping_address = Column(Text)


class Product(TransBase):
    __tablename__ = "products"

    product_id = Column(Integer, primary_key=True)
    product_name = Column(String(100))
    category = Column(String(50))
    price = Column(DECIMAL(8, 2))
    stock_quantity = Column(Integer)
    supplier = Column(String(100))
    is_active = Column(Boolean)


class SalesSummary(TransBase):
    __tablename__ = "sales_summary"

    id = Column(Integer, primary_key=True, autoincrement=True)
    summary_date = Column(Date)
    region = Column(String(50))
    category = Column(String(50))
    total_sales = Column(DECIMAL(12, 2))
    order_count = Column(Integer)
    avg_order_value = Column(DECIMAL(8, 2))


class EmployeePerformance(TransBase):
    __tablename__ = "employee_performance"

    employee_id = Column(Integer, primary_key=True)
    full_name = Column(String(100))
    department = Column(String(50))
    position = Column(String(100))
    hire_date = Column(Date)
    performance_score = Column(DECIMAL(3, 2))
    salary = Column(DECIMAL(10, 2))
    manager_id = Column(Integer)


class TransactionalDBCreator:

    def __init__(self, database_url: str):
        self.engine = create_engine(
            database_url, connect_args={"check_same_thread": False}
        )
        TransBase.metadata.create_all(bind=self.engine)
        SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=self.engine)
        self.session = SessionLocal()

        self.first_names = [
            "John",
            "Jane",
            "Michael",
            "Emily",
            "David",
            "Sarah",
            "Chris",
            "Lisa",
            "James",
            "Anna",
            "Robert",
            "Maria",
            "William",
            "Jennifer",
            "Richard",
            "Linda",
            "Joseph",
            "Patricia",
            "Thomas",
            "Elizabeth",
            "Charles",
            "Susan",
            "Daniel",
            "Jessica",
            "Matthew",
            "Karen",
            "Anthony",
            "Nancy",
            "Mark",
            "Betty",
            "Donald",
            "Helen",
            "Steven",
            "Dorothy",
            "Paul",
            "Sandra",
            "Andrew",
            "Ashley",
            "Joshua",
            "Kimberly",
            "Kenneth",
            "Donna",
            "Kevin",
            "Emily",
            "Brian",
            "Carol",
            "George",
            "Michelle",
            "Edward",
            "Amanda",
        ]

        self.last_names = [
            "Smith",
            "Johnson",
            "Williams",
            "Brown",
            "Jones",
            "Garcia",
            "Miller",
            "Davis",
            "Rodriguez",
            "Martinez",
            "Hernandez",
            "Lopez",
            "Gonzalez",
            "Wilson",
            "Anderson",
            "Thomas",
            "Taylor",
            "Moore",
            "Jackson",
            "Martin",
            "Lee",
            "Perez",
            "Thompson",
            "White",
            "Harris",
            "Sanchez",
            "Clark",
            "Ramirez",
            "Lewis",
            "Robinson",
            "Walker",
            "Young",
            "Allen",
            "King",
            "Wright",
            "Scott",
            "Torres",
            "Nguyen",
            "Hill",
            "Flores",
            "Green",
            "Adams",
            "Nelson",
            "Baker",
            "Hall",
            "Rivera",
            "Campbell",
            "Mitchell",
            "Carter",
            "Roberts",
        ]

        self.cities = {
            "USA": [
                "New York",
                "Los Angeles",
                "Chicago",
                "Houston",
                "Phoenix",
                "Philadelphia",
                "San Antonio",
                "San Diego",
                "Dallas",
                "San Jose",
                "Austin",
                "Jacksonville",
                "Fort Worth",
                "Columbus",
                "Charlotte",
                "Seattle",
                "Denver",
                "Boston",
            ],
            "Canada": [
                "Toronto",
                "Montreal",
                "Vancouver",
                "Calgary",
                "Edmonton",
                "Ottawa",
            ],
            "UK": [
                "London",
                "Manchester",
                "Birmingham",
                "Leeds",
                "Glasgow",
                "Liverpool",
            ],
            "Germany": [
                "Berlin",
                "Munich",
                "Hamburg",
                "Frankfurt",
                "Cologne",
                "Stuttgart",
            ],
            "France": ["Paris", "Marseille", "Lyon", "Toulouse", "Nice", "Nantes"],
            "Mexico": ["Mexico City", "Guadalajara", "Monterrey", "Puebla", "Tijuana"],
            "Australia": ["Sydney", "Melbourne", "Brisbane", "Perth", "Adelaide"],
            "Japan": ["Tokyo", "Osaka", "Yokohama", "Nagoya", "Sapporo"],
            "Brazil": [
                "Sao Paulo",
                "Rio de Janeiro",
                "Brasilia",
                "Salvador",
                "Fortaleza",
            ],
            "India": [
                "Mumbai",
                "Delhi",
                "Bangalore",
                "Hyderabad",
                "Chennai",
                "Kolkata",
            ],
        }

        self.product_categories = {
            "Electronics": [
                ("Wireless Bluetooth Headphones", 79.99, "TechSupplier Inc"),
                ("Wireless Mouse", 29.99, "TechSupplier Inc"),
                ("USB-C Cable 6ft", 12.99, "Cable Pro Ltd"),
                ("Laptop Stand", 45.50, "ErgoTech Solutions"),
                ("Webcam HD 1080p", 89.99, "Vision Systems"),
                ("Mechanical Keyboard", 129.99, "KeyMaster Corp"),
                ("Portable SSD 1TB", 159.99, "Storage Plus"),
                ("USB Hub 7-Port", 34.99, "TechSupplier Inc"),
                ("Phone Charger Fast", 24.99, "PowerTech Ltd"),
                ("HDMI Cable 10ft", 15.99, "Cable Pro Ltd"),
                ("Laptop Cooling Pad", 39.99, "ErgoTech Solutions"),
                ("Wireless Earbuds", 99.99, "Audio Pro Inc"),
                ("USB Microphone", 79.99, "Audio Pro Inc"),
                ("Monitor Stand", 54.99, "ErgoTech Solutions"),
                ("External HDD 2TB", 89.99, "Storage Plus"),
            ],
            "Furniture": [
                ("Ergonomic Office Chair", 299.99, "OfficeMax Pro"),
                ("Standing Desk", 449.99, "OfficeMax Pro"),
                ("Bookshelf 5-Tier", 89.99, "Furniture World"),
                ("Computer Desk", 189.99, "OfficeMax Pro"),
                ("Filing Cabinet", 129.99, "Office Solutions"),
                ("Desk Lamp LED", 39.99, "Lighting Plus"),
                ("Office Chair Mat", 49.99, "OfficeMax Pro"),
                ("Monitor Arm Mount", 79.99, "ErgoTech Solutions"),
                ("Drawer Organizer", 24.99, "Office Solutions"),
                ("Footrest Ergonomic", 34.99, "ErgoTech Solutions"),
            ],
            "Home & Garden": [
                ("Stainless Steel Water Bottle", 24.99, "EcoProducts Ltd"),
                ("Coffee Maker 12-Cup", 79.99, "Kitchen Essentials"),
                ("Indoor Plant Pot Set", 34.99, "Garden Plus"),
                ("LED Light Bulbs 4-Pack", 19.99, "Lighting Plus"),
                ("Vacuum Cleaner Robot", 299.99, "Home Tech"),
                ("Air Purifier", 149.99, "Home Tech"),
                ("Bedding Set Queen", 89.99, "Sleep Comfort"),
                ("Bath Towel Set", 39.99, "Linens & More"),
                ("Kitchen Knife Set", 69.99, "Kitchen Essentials"),
                ("Blender High-Speed", 99.99, "Kitchen Essentials"),
                ("Garden Tool Set", 54.99, "Garden Plus"),
                ("Outdoor String Lights", 29.99, "Lighting Plus"),
                ("Throw Pillow Set", 44.99, "Home Decor Co"),
                ("Area Rug 5x7", 129.99, "Home Decor Co"),
                ("Wall Clock Modern", 34.99, "Home Decor Co"),
            ],
            "Sports & Outdoors": [
                ("Yoga Mat Premium", 39.99, "Fitness First"),
                ("Resistance Bands Set", 24.99, "Fitness First"),
                ("Water Bottle Insulated", 29.99, "Outdoor Gear Co"),
                ("Camping Tent 4-Person", 199.99, "Outdoor Gear Co"),
                ("Hiking Backpack", 79.99, "Outdoor Gear Co"),
                ("Bicycle Helmet", 49.99, "Sports Central"),
                ("Running Shoes", 89.99, "Athletic Wear Inc"),
                ("Dumbbell Set", 149.99, "Fitness First"),
                ("Jump Rope", 14.99, "Fitness First"),
                ("Camping Sleeping Bag", 69.99, "Outdoor Gear Co"),
            ],
            "Clothing": [
                ("Cotton T-Shirt", 19.99, "Fashion Basics"),
                ("Denim Jeans", 59.99, "Fashion Basics"),
                ("Hoodie Pullover", 44.99, "Casual Wear Co"),
                ("Running Jacket", 79.99, "Athletic Wear Inc"),
                ("Sneakers Casual", 69.99, "Footwear Plus"),
                ("Baseball Cap", 24.99, "Accessories Hub"),
                ("Winter Coat", 149.99, "Outerwear Pro"),
                ("Dress Shirt", 49.99, "Fashion Basics"),
                ("Sweatpants", 34.99, "Casual Wear Co"),
                ("Socks 6-Pack", 14.99, "Fashion Basics"),
            ],
        }

        self.departments = [
            "Sales",
            "Engineering",
            "Marketing",
            "HR",
            "Operations",
            "Finance",
            "Customer Service",
            "Product Management",
        ]

        self.positions = {
            "Sales": [
                "Sales Manager",
                "Senior Sales Representative",
                "Sales Representative",
                "Sales Coordinator",
            ],
            "Engineering": [
                "Engineering Manager",
                "Senior Software Engineer",
                "Software Engineer",
                "QA Engineer",
                "DevOps Engineer",
            ],
            "Marketing": [
                "Marketing Manager",
                "Marketing Specialist",
                "Content Creator",
                "SEO Specialist",
            ],
            "HR": ["HR Manager", "HR Specialist", "Recruiter", "HR Coordinator"],
            "Operations": [
                "Operations Manager",
                "Operations Coordinator",
                "Logistics Specialist",
            ],
            "Finance": [
                "Finance Manager",
                "Financial Analyst",
                "Accountant",
                "Accounts Payable Specialist",
            ],
            "Customer Service": [
                "Customer Service Manager",
                "Customer Service Representative",
                "Support Specialist",
            ],
            "Product Management": [
                "Product Manager",
                "Senior Product Manager",
                "Product Owner",
            ],
        }

        self.payment_methods = [
            "credit_card",
            "debit_card",
            "paypal",
            "apple_pay",
            "google_pay",
            "bank_transfer",
        ]
        self.order_statuses = [
            "completed",
            "pending",
            "processing",
            "shipped",
            "cancelled",
        ]
        self.regions = [
            "North America",
            "Europe",
            "Asia Pacific",
            "Latin America",
            "Middle East",
        ]

    def generate_customers(self, count=100):
        print(f"Generating {count} customers...")
        customers = []

        for i in range(count):
            first_name = random.choice(self.first_names)
            last_name = random.choice(self.last_names)
            country = random.choice(list(self.cities.keys()))

            customer = Customer(
                customer_id=1000 + i,
                first_name=first_name,
                last_name=last_name,
                email=f"{first_name.lower()}.{last_name.lower()}{i}@email.com",
                phone=f"+1-555-{random.randint(1000, 9999)}",
                registration_date=datetime.now().date()
                - timedelta(days=random.randint(30, 730)),
                country=country,
                city=random.choice(self.cities[country]),
                is_active=random.choice([True, True, True, False]),  # 75% active
            )
            customers.append(customer)

        self.session.bulk_save_objects(customers)
        self.session.commit()
        print(f"Created {count} customers.")
        return customers

    def generate_products(self):
        print("Generating products...")
        products = []
        product_id = 3000

        for category, items in self.product_categories.items():
            for product_name, price, supplier in items:
                product = Product(
                    product_id=product_id,
                    product_name=product_name,
                    category=category,
                    price=price,
                    stock_quantity=random.randint(10, 300),
                    supplier=supplier,
                    is_active=random.choice(
                        [True, True, True, True, False]
                    ),  # 80% active
                )
                products.append(product)
                product_id += 1

        self.session.bulk_save_objects(products)
        self.session.commit()
        print(f"Created {len(products)} products.")
        return products

    def generate_orders(self, customer_count=100, orders_per_customer_range=(1, 5)):
        print("Generating orders...")
        orders = []
        order_id = 2000

        customers = self.session.query(Customer).all()
        products = self.session.query(Product).filter(Product.is_active == True).all()

        for customer in customers[:customer_count]:
            num_orders = random.randint(*orders_per_customer_range)

            for _ in range(num_orders):
                order_products = random.sample(products, random.randint(1, 5))
                total_amount = sum(
                    float(p.price) * random.randint(1, 3) for p in order_products
                )

                order = Order(
                    order_id=order_id,
                    customer_id=customer.customer_id,
                    order_date=datetime.now() - timedelta(days=random.randint(1, 365)),
                    total_amount=round(total_amount, 2),
                    status=random.choice(self.order_statuses),
                    payment_method=random.choice(self.payment_methods),
                    shipping_address=f"{random.randint(100, 9999)} {random.choice(['Main', 'Oak', 'Maple', 'Pine', 'Cedar'])} {random.choice(['St', 'Ave', 'Blvd', 'Rd'])}, {customer.city}, {customer.country}",
                )
                orders.append(order)
                order_id += 1

        self.session.bulk_save_objects(orders)
        self.session.commit()
        print(f"Created {len(orders)} orders.")
        return orders

    def generate_sales_summary(self, days=90):
        print(f"Generating sales summary for {days} days...")
        summaries = []

        categories = list(self.product_categories.keys())

        for day_offset in range(days):
            summary_date = datetime.now().date() - timedelta(days=day_offset)

            for region in self.regions:
                for category in random.sample(
                    categories, random.randint(2, len(categories))
                ):
                    order_count = random.randint(10, 100)
                    avg_order_value = round(random.uniform(50, 500), 2)
                    total_sales = round(order_count * avg_order_value, 2)

                    summary = SalesSummary(
                        summary_date=summary_date,
                        region=region,
                        category=category,
                        total_sales=total_sales,
                        order_count=order_count,
                        avg_order_value=avg_order_value,
                    )
                    summaries.append(summary)

        self.session.bulk_save_objects(summaries)
        self.session.commit()
        print(f"Created {len(summaries)} sales summary records.")
        return summaries

    def generate_employees(self, count=50):
        print(f"Generating {count} employees...")
        employees = []

        manager_ids = []
        for i in range(count // 10):  # 10% are managers
            department = random.choice(self.departments)
            full_name = (
                f"{random.choice(self.first_names)} {random.choice(self.last_names)}"
            )

            employee = EmployeePerformance(
                employee_id=4000 + i,
                full_name=full_name,
                department=department,
                position=f"{department} Manager",
                hire_date=datetime.now().date()
                - timedelta(days=random.randint(730, 2920)),  # 2-8 years
                performance_score=round(random.uniform(3.5, 5.0), 2),
                salary=round(random.uniform(80000, 120000), 2),
                manager_id=None,
            )
            employees.append(employee)
            manager_ids.append(employee.employee_id)

        # Create regular employees (with manager_id)
        for i in range(len(manager_ids), count):
            department = random.choice(self.departments)
            full_name = (
                f"{random.choice(self.first_names)} {random.choice(self.last_names)}"
            )
            position = random.choice(self.positions.get(department, ["Staff Member"]))

            employee = EmployeePerformance(
                employee_id=4000 + i,
                full_name=full_name,
                department=department,
                position=position,
                hire_date=datetime.now().date()
                - timedelta(days=random.randint(30, 1825)),  # 1 month to 5 years
                performance_score=round(random.uniform(2.5, 5.0), 2),
                salary=round(random.uniform(40000, 90000), 2),
                manager_id=random.choice(manager_ids),
            )
            employees.append(employee)

        self.session.bulk_save_objects(employees)
        self.session.commit()
        print(f"Created {count} employee records.")
        return employees

    def generate_all_data(self):
        print("Generating all transactional database data...")
        print("=" * 50)

        self.generate_customers(100)
        self.generate_products()
        self.generate_orders(100, (2, 8))
        self.generate_sales_summary(90)
        self.generate_employees(50)

        print("=" * 50)
        print("Transactional database generation complete!")
        self.print_summary()

    def print_summary(self):
        print("\nTRANSACTIONAL DATABASE SUMMARY:")
        print("-" * 40)

        customer_count = self.session.query(Customer).count()
        order_count = self.session.query(Order).count()
        product_count = self.session.query(Product).count()
        sales_summary_count = self.session.query(SalesSummary).count()
        employee_count = self.session.query(EmployeePerformance).count()

        print(f"Customers: {customer_count}")
        print(f"Orders: {order_count}")
        print(f"Products: {product_count}")
        print(f"Sales Summary: {sales_summary_count}")
        print(f"Employees: {employee_count}")

    def cleanup(self):
        self.session.close()

def clean_existing_db(trans_db: str):
    if os.path.exists(trans_db):
        try:
            os.remove(trans_db)
            print(f"Deleted existing database: {trans_db}")
        except Exception as e:
            print(f"Warning: Could not delete {trans_db}: {e}")


def main():
    try:

        print("Transactional Database Generator")
        print("=" * 50)
        print()
        dbFile = "./test_dbs/trans_db/trans_db.db"
        dbURL = f"sqlite:///{dbFile}"
        clean_existing_db(dbFile)
        dbCreator = TransactionalDBCreator(dbURL)
        dbCreator.generate_all_data()
        dbCreator.cleanup()

        print("\n" + "=" * 50)
        print("SUCCESS!")
        print("=" * 50)
        print("The transactional database has been created and populated.")

    except Exception as e:
        print(f"\nError generating transactional database: {e}")
        import traceback

        traceback.print_exc()
        return 1

    return 0


if __name__ == "__main__":
    sys.exit(main())
