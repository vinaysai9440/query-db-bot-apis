import sys
import os
from datetime import datetime, timedelta
import random
import json
import uuid

# Add project root to Python path first
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.abspath(os.path.join(current_dir, "..", ".."))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

# Import SQLAlchemy before models
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Now import models
from models.user import UserMaster
from models.role import RoleMaster, RolePermission
from models.table import TableDef
from models.chat import ChatSession, ChatConversation
from config.database import Base


class BotDBCreator:

    def __init__(self, database_url: str):
        self.engine = create_engine(
            database_url, connect_args={"check_same_thread": False}
        )
        Base.metadata.create_all(bind=self.engine)
        SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=self.engine)
        self.session = SessionLocal()

        self.user_names = [
            "Alice Johnson", "Bob Smith", "Carol Williams", "David Brown",
            "Emma Davis", "Frank Wilson", "Grace Miller", "Henry Taylor",
            "Isabella Anderson", "Jack Thomas", "Kate Jackson", "Liam White",
            "Mia Harris", "Noah Martin", "Olivia Thompson", "Paul Garcia"
        ]

        self.company_emails = [
            "techcorp.com", "datainsights.com", "analytics.pro", "businesstech.io",
            "enterprise.com", "solutions.net", "systems.org"
        ]

        self.role_definitions = [
            {
                "name": "admin",
                "description": "Full system access with all administrative privileges",
                "permissions": ["*.*"]
            },
            {
                "name": "analyst",
                "description": "Analytical role with access to data analysis module and tables",
                "permissions": ["tables.*", "modules.analytics"]
            },
            {
                "name": "user",
                "description": "Standard user with access to all tables and basic modules",
                "permissions": ["tables.*"]
            }
        ]

        self.table_definitions = [
            {
                "name": "customers",
                "description": "Customer master data including contact information and demographics",
                "notes": "Main customer table. Updated nightly from CRM system.",
                "columns": [
                    {"name": "customer_id", "type": "INTEGER", "primary_key": True, "description": "Unique customer identifier"},
                    {"name": "first_name", "type": "VARCHAR(50)", "nullable": False, "description": "Customer first name"},
                    {"name": "last_name", "type": "VARCHAR(50)", "nullable": False, "description": "Customer last name"},
                    {"name": "email", "type": "VARCHAR(100)", "unique": True, "description": "Customer email address"},
                    {"name": "phone", "type": "VARCHAR(20)", "description": "Customer phone number"},
                    {"name": "registration_date", "type": "DATE", "description": "Date customer registered"},
                    {"name": "country", "type": "VARCHAR(50)", "description": "Customer country"},
                    {"name": "city", "type": "VARCHAR(50)", "description": "Customer city"},
                    {"name": "is_active", "type": "BOOLEAN", "default": True, "description": "Whether customer is active"}
                ],
                "sample_rows": [
                    {"customer_id": 1001, "first_name": "John", "last_name": "Doe", "email": "john.doe@email.com", "phone": "+1-555-0123", "registration_date": "2023-01-15", "country": "USA", "city": "New York", "is_active": True},
                    {"customer_id": 1002, "first_name": "Jane", "last_name": "Smith", "email": "jane.smith@email.com", "phone": "+1-555-0124", "registration_date": "2023-02-20", "country": "USA", "city": "Los Angeles", "is_active": True},
                    {"customer_id": 1003, "first_name": "Carlos", "last_name": "Rodriguez", "email": "carlos.r@email.com", "phone": "+1-555-0125", "registration_date": "2023-03-10", "country": "Mexico", "city": "Mexico City", "is_active": True}
                ]
            },
            {
                "name": "orders",
                "description": "Customer order transactions and purchase history",
                "notes": "Order data synced from e-commerce platform. Includes both completed and pending orders.",
                "columns": [
                    {"name": "order_id", "type": "INTEGER", "primary_key": True, "description": "Unique order identifier"},
                    {"name": "customer_id", "type": "INTEGER", "foreign_key": "customers.customer_id", "description": "Reference to customer"},
                    {"name": "order_date", "type": "DATETIME", "description": "When order was placed"},
                    {"name": "total_amount", "type": "DECIMAL(10,2)", "description": "Total order amount in USD"},
                    {"name": "status", "type": "VARCHAR(20)", "description": "Order status (pending, completed, cancelled)"},
                    {"name": "payment_method", "type": "VARCHAR(30)", "description": "Payment method used"},
                    {"name": "shipping_address", "type": "TEXT", "description": "Shipping address"}
                ],
                "sample_rows": [
                    {"order_id": 2001, "customer_id": 1001, "order_date": "2023-11-01 10:30:00", "total_amount": 299.99, "status": "completed", "payment_method": "credit_card", "shipping_address": "123 Main St, New York, NY 10001"},
                    {"order_id": 2002, "customer_id": 1002, "order_date": "2023-11-02 14:15:00", "total_amount": 149.50, "status": "completed", "payment_method": "paypal", "shipping_address": "456 Oak Ave, Los Angeles, CA 90210"},
                    {"order_id": 2003, "customer_id": 1001, "order_date": "2023-11-03 09:45:00", "total_amount": 75.25, "status": "pending", "payment_method": "credit_card", "shipping_address": "123 Main St, New York, NY 10001"}
                ]
            },
            {
                "name": "products",
                "description": "Product catalog with pricing and inventory information",
                "notes": "Product master data. Inventory levels updated in real-time.",
                "columns": [
                    {"name": "product_id", "type": "INTEGER", "primary_key": True, "description": "Unique product identifier"},
                    {"name": "product_name", "type": "VARCHAR(100)", "description": "Product name"},
                    {"name": "category", "type": "VARCHAR(50)", "description": "Product category"},
                    {"name": "price", "type": "DECIMAL(8,2)", "description": "Current product price"},
                    {"name": "stock_quantity", "type": "INTEGER", "description": "Available inventory"},
                    {"name": "supplier", "type": "VARCHAR(100)", "description": "Product supplier"},
                    {"name": "is_active", "type": "BOOLEAN", "description": "Whether product is available for sale"}
                ],
                "sample_rows": [
                    {"product_id": 3001, "product_name": "Wireless Bluetooth Headphones", "category": "Electronics", "price": 79.99, "stock_quantity": 150, "supplier": "TechSupplier Inc", "is_active": True},
                    {"product_id": 3002, "product_name": "Ergonomic Office Chair", "category": "Furniture", "price": 299.99, "stock_quantity": 45, "supplier": "OfficeMax Pro", "is_active": True},
                    {"product_id": 3003, "product_name": "Stainless Steel Water Bottle", "category": "Home & Garden", "price": 24.99, "stock_quantity": 200, "supplier": "EcoProducts Ltd", "is_active": True}
                ]
            },
            {
                "name": "sales_summary",
                "description": "Aggregated sales data by date, region, and product category",
                "notes": "Daily aggregated sales metrics. Updated by ETL job every morning at 6 AM.",
                "columns": [
                    {"name": "summary_date", "type": "DATE", "description": "Date of sales summary"},
                    {"name": "region", "type": "VARCHAR(50)", "description": "Sales region"},
                    {"name": "category", "type": "VARCHAR(50)", "description": "Product category"},
                    {"name": "total_sales", "type": "DECIMAL(12,2)", "description": "Total sales amount"},
                    {"name": "order_count", "type": "INTEGER", "description": "Number of orders"},
                    {"name": "avg_order_value", "type": "DECIMAL(8,2)", "description": "Average order value"}
                ],
                "sample_rows": [
                    {"summary_date": "2023-11-01", "region": "North America", "category": "Electronics", "total_sales": 15750.50, "order_count": 42, "avg_order_value": 375.01},
                    {"summary_date": "2023-11-01", "region": "Europe", "category": "Furniture", "total_sales": 8920.25, "order_count": 18, "avg_order_value": 495.57},
                    {"summary_date": "2023-11-02", "region": "Asia Pacific", "category": "Home & Garden", "total_sales": 3240.75, "order_count": 67, "avg_order_value": 48.37}
                ]
            },
            {
                "name": "employee_performance",
                "description": "Employee performance metrics and KPI tracking",
                "notes": "HR and performance data. Contains sensitive information - access restricted.",
                "columns": [
                    {"name": "employee_id", "type": "INTEGER", "primary_key": True, "description": "Unique employee identifier"},
                    {"name": "full_name", "type": "VARCHAR(100)", "description": "Employee full name"},
                    {"name": "department", "type": "VARCHAR(50)", "description": "Employee department"},
                    {"name": "position", "type": "VARCHAR(100)", "description": "Job position/title"},
                    {"name": "hire_date", "type": "DATE", "description": "Date of hire"},
                    {"name": "performance_score", "type": "DECIMAL(3,2)", "description": "Performance score (1.00-5.00)"},
                    {"name": "salary", "type": "DECIMAL(10,2)", "description": "Annual salary"},
                    {"name": "manager_id", "type": "INTEGER", "description": "Manager employee ID"}
                ],
                "sample_rows": [
                    {"employee_id": 4001, "full_name": "Sarah Johnson", "department": "Sales", "position": "Senior Sales Manager", "hire_date": "2020-03-15", "performance_score": 4.8, "salary": 85000.00, "manager_id": None},
                    {"employee_id": 4002, "full_name": "Michael Chen", "department": "Engineering", "position": "Software Developer", "hire_date": "2021-07-20", "performance_score": 4.5, "salary": 75000.00, "manager_id": 4003},
                    {"employee_id": 4003, "full_name": "Lisa Rodriguez", "department": "Engineering", "position": "Engineering Manager", "hire_date": "2019-01-10", "performance_score": 4.9, "salary": 95000.00, "manager_id": None}
                ]
            }
        ]

        self.session_titles = [
            "Customer Analysis Query",
            "Monthly Sales Report",
            "Product Performance Review",
            "Employee Metrics Dashboard",
            "Order Trend Analysis",
            "Regional Sales Comparison",
            "Customer Segmentation Study",
            "Inventory Status Check",
            "Revenue Breakdown Analysis",
            "Top Customers Report",
            "Product Category Performance",
            "Quarterly Business Review"
        ]

        self.sample_conversations = [
            {
                "query": "Show me the top 10 customers by total order value",
                "sql": "SELECT c.first_name, c.last_name, SUM(o.total_amount) as total_spent FROM customers c JOIN orders o ON c.customer_id = o.customer_id GROUP BY c.customer_id ORDER BY total_spent DESC LIMIT 10",
                "content": [
                    {"first_name": "John", "last_name": "Doe", "total_spent": 1250.00},
                    {"first_name": "Jane", "last_name": "Smith", "total_spent": 980.50}
                ],
                "content_type": "application/json",
                "time_ms": 245,
                "suggestions": [
                    "What is the average order value for these top customers?",
                    "Show me the order history for the top customer"
                ]
            },
            {
                "query": "What are the sales trends for electronics category last month?",
                "sql": "SELECT summary_date, total_sales FROM sales_summary WHERE category = 'Electronics' AND summary_date >= DATE_SUB(CURDATE(), INTERVAL 1 MONTH) ORDER BY summary_date",
                "content": "summary_date,total_sales\n2023-10-01,15750.50\n2023-10-02,16200.75",
                "content_type": "text/csv",
                "time_ms": 156,
                "suggestions": [
                    "Compare electronics sales with other categories",
                    "Show me the best-selling electronics products"
                ]
            }
        ]

        self.error_queries = [
            {
                "query": "Show me sales for non-existent table",
                "sql": "SELECT * FROM non_existent_table",
                "error": "Table 'non_existent_table' doesn't exist"
            },
            {
                "query": "Calculate average of invalid column",
                "sql": "SELECT AVG(invalid_column) FROM customers",
                "error": "Unknown column 'invalid_column' in field list"
            }
        ]

    def generate_users(self):
        print("Generating users...")
        users = []

        # Admin user
        admin_user = UserMaster(
            id=str(uuid.uuid4()),
            email="admin@techcorp.com",
            password="15e2b0d3c33891ebb0f1ef609ec419420c20e320ce94c65fbc8c3312448eb225",
            name="System Administrator",
            provider="local",
            is_active=True,
            role="admin",
            created_by=None,
            created_date=datetime.utcnow() - timedelta(days=365),
            updated_by=None,
            updated_date=datetime.utcnow() - timedelta(days=30)
        )
        users.append(admin_user)

        # Regular users
        roles = ["admin", "user", "analyst"]
        providers = ["email", "sso"]

        for i, name in enumerate(self.user_names[:12]):
            email_domain = random.choice(self.company_emails)
            first_name = name.split()[0].lower()
            last_name = name.split()[1].lower()

            has_been_updated = random.choice([True, False])
            user = UserMaster(
                id=str(uuid.uuid4()),
                email=f"{first_name}.{last_name}@{email_domain}",
                password="15e2b0d3c33891ebb0f1ef609ec419420c20e320ce94c65fbc8c3312448eb225",
                name=name,
                provider=random.choice(providers),
                is_active=random.choice([True, True, True, False]),
                role=random.choice(roles) if i > 0 else "user",
                created_by=None,
                created_date=datetime.utcnow() - timedelta(days=random.randint(30, 300)),
                updated_by=None,
                updated_date=datetime.utcnow() - timedelta(days=random.randint(1, 30)) if has_been_updated else None
            )
            users.append(user)

        self.session.bulk_save_objects(users)
        self.session.commit()
        print(f"Created {len(users)} users.")
        return users

    def generate_roles(self):
        print("Generating roles...")
        roles = []

        for i, role_def in enumerate(self.role_definitions):
            has_been_updated = i < 2
            role = RoleMaster(
                role_id=str(uuid.uuid4()),
                role_name=role_def["name"],
                description=role_def["description"],
                is_active=True,
                created_by=None,
                created_date=datetime.utcnow() - timedelta(days=random.randint(100, 400)),
                updated_by=None,
                updated_date=datetime.utcnow() - timedelta(days=random.randint(1, 50)) if has_been_updated else None
            )
            roles.append(role)
            role_def["role_id"] = role.role_id

        self.session.bulk_save_objects(roles)
        self.session.commit()
        print(f"Created {len(roles)} roles.")
        return roles

    def generate_role_permissions(self):
        print("Generating role permissions...")
        permissions = []

        for role_def in self.role_definitions:
            for permission_str in role_def["permissions"]:
                perm = RolePermission(
                    id=str(uuid.uuid4()),
                    role_id=role_def["role_id"],
                    ref_id=permission_str,
                    granted=True,
                    created_date=datetime.utcnow() - timedelta(days=random.randint(90, 390))
                )
                permissions.append(perm)

        self.session.bulk_save_objects(permissions)
        self.session.commit()
        print(f"Created {len(permissions)} role permissions.")
        return permissions

    def generate_tables(self):
        print("Generating table definitions...")
        tables = []

        admin_user = self.session.query(UserMaster).filter(UserMaster.role == "admin").first()

        for i, table_def in enumerate(self.table_definitions):
            has_been_updated = i < 2
            table = TableDef(
                id=str(uuid.uuid4()),
                table_name=table_def["name"],
                description=table_def["description"],
                notes=table_def["notes"],
                columns=json.dumps(table_def["columns"]),
                sample_rows=json.dumps(table_def["sample_rows"]),
                is_active=True,
                created_by=admin_user.id if admin_user else None,
                created_date=datetime.utcnow() - timedelta(days=random.randint(50, 200)),
                updated_by=admin_user.id if (admin_user and has_been_updated) else None,
                updated_date=datetime.utcnow() - timedelta(days=random.randint(1, 30)) if has_been_updated else None
            )
            tables.append(table)

        # Inactive table
        inactive_table = TableDef(
            id=str(uuid.uuid4()),
            table_name="legacy_data",
            description="Legacy data table - no longer maintained",
            notes="This table is deprecated and will be removed in next cleanup cycle.",
            columns=json.dumps([
                {"name": "id", "type": "INTEGER", "primary_key": True},
                {"name": "old_data", "type": "TEXT"}
            ]),
            sample_rows=json.dumps([]),
            is_active=False,
            created_by=admin_user.id if admin_user else None,
            created_date=datetime.utcnow() - timedelta(days=800),
            updated_by=admin_user.id if admin_user else None,
            updated_date=datetime.utcnow() - timedelta(days=365)
        )
        tables.append(inactive_table)

        self.session.bulk_save_objects(tables)
        self.session.commit()
        print(f"Created {len(tables)} table definitions.")
        return tables

    def generate_chat_sessions(self):
        print("Generating chat sessions...")
        sessions = []

        active_users = self.session.query(UserMaster).filter(UserMaster.is_active == True).limit(8).all()

        for user in active_users:
            num_sessions = random.randint(1, 3)

            for _ in range(num_sessions):
                session = ChatSession(
                    session_id=str(uuid.uuid4()),
                    user_id=user.id,
                    title=random.choice(self.session_titles),
                    is_active=random.choice([True, True, False]),
                    created_date=datetime.utcnow() - timedelta(days=random.randint(1, 60)),
                    updated_date=datetime.utcnow() - timedelta(hours=random.randint(1, 24))
                )
                sessions.append(session)

        self.session.bulk_save_objects(sessions)
        self.session.commit()
        print(f"Created {len(sessions)} chat sessions.")
        return sessions

    def generate_chat_conversations(self):
        print("Generating chat conversations...")
        conversations = []

        sessions = self.session.query(ChatSession).all()

        for session in sessions:
            num_conversations = random.randint(1, 5)
            session_start = session.created_date

            for i in range(num_conversations):
                conversation_time = session_start + timedelta(minutes=random.randint(1, 30) * i)

                if random.random() < 0.9:
                    sample = random.choice(self.sample_conversations)
                    conversation = ChatConversation(
                        id=str(uuid.uuid4()),
                        session_id=session.session_id,
                        query_text=sample["query"],
                        content=json.dumps(sample["content"]) if isinstance(sample["content"], (list, dict)) else sample["content"],
                        content_type=sample["content_type"],
                        sql_generated=sample["sql"],
                        error_message=None,
                        execution_time_ms=str(sample["time_ms"]),
                        suggestions=json.dumps(sample.get("suggestions", [])),
                        created_date=conversation_time
                    )
                else:
                    error = random.choice(self.error_queries)
                    conversation = ChatConversation(
                        id=str(uuid.uuid4()),
                        session_id=session.session_id,
                        query_text=error["query"],
                        content=None,
                        content_type=None,
                        sql_generated=error["sql"],
                        error_message=error["error"],
                        execution_time_ms=None,
                        suggestions=None,
                        created_date=conversation_time
                    )

                conversations.append(conversation)

        self.session.bulk_save_objects(conversations)
        self.session.commit()
        print(f"Created {len(conversations)} chat conversations.")
        return conversations

    def generate_all_data(self):
        print("Generating all bot database data...")
        print("=" * 50)

        self.generate_users()
        self.generate_roles()
        self.generate_role_permissions()
        self.generate_tables()
        self.generate_chat_sessions()
        self.generate_chat_conversations()

        print("=" * 50)
        print("Bot database generation complete!")
        self.print_summary()

    def print_summary(self):
        print("\nBOT DATABASE SUMMARY:")
        print("-" * 40)

        user_count = self.session.query(UserMaster).count()
        role_count = self.session.query(RoleMaster).count()
        permission_count = self.session.query(RolePermission).count()
        table_count = self.session.query(TableDef).count()
        session_count = self.session.query(ChatSession).count()
        conversation_count = self.session.query(ChatConversation).count()

        print(f"Users: {user_count}")
        print(f"Roles: {role_count}")
        print(f"Role Permissions: {permission_count}")
        print(f"Table Definitions: {table_count}")
        print(f"Chat Sessions: {session_count}")
        print(f"Chat Conversations: {conversation_count}")
        print(f"Total Records: {user_count + role_count + permission_count + table_count + session_count + conversation_count}")

    def cleanup(self):
        self.session.close()
        self.engine.dispose()

def clean_existing_db(bot_db: str):
    if os.path.exists(bot_db):
        try:
            os.remove(bot_db)
            print(f"Deleted existing database: {bot_db}")
        except Exception as e:
            print(f"Warning: Could not delete {bot_db}: {e}")


def main():
    try:
        print("Bot Database Generator")
        print("=" * 50)
        print()

        dbFile = "./test_dbs/bot_db/bot_db.db"
        dbURL = f"sqlite:///{dbFile}"
        #
        clean_existing_db(dbFile)
        dbCreator = BotDBCreator(dbURL)
        dbCreator.generate_all_data()
        dbCreator.cleanup()

        print("\n" + "=" * 50)
        print("SUCCESS!")
        print("=" * 50)
        print("The bot database has been created and populated.")

    except Exception as e:
        print(f"\nError generating bot database: {e}")
        import traceback
        traceback.print_exc()
        return 1

    return 0


if __name__ == "__main__":
    sys.exit(main())
