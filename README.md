# 🤖 Query DB Bot APIs - Conversational SQL Engine

A modern, production-ready FastAPI application that transforms natural language queries into SQL using Large Language Models (LLM). This intelligent system provides conversational database interactions with comprehensive session management, role-based access control, and JWT authentication.

## 🚀 Key Features

### 🧠 AI-Powered Query Generation
- **Natural Language Processing**: Convert plain English to SQL queries using Ollama LLM (Mistral model)
- **Context-Aware**: Maintains conversation history for intelligent query building
- **Smart Table Identification**: Automatically identifies relevant tables from your query
- **SQL Generation**: AI-generated SQL with built-in validation and error handling

### 💬 Conversational Interface
- **Session Management**: Persistent chat sessions with auto-generated AI titles
- **Conversation History**: Complete query/response tracking with timestamps and execution metrics
- **Multi-User Support**: Isolated sessions per user for data privacy
- **Interactive Responses**: Get SQL queries, results, and error messages

### 🗄️ Dual Database Architecture
- **Bot Database**: Manages users, roles, permissions, table metadata, and chat sessions (SQLite)
- **Transactional Database**: Stores business data for query execution (SQLite/PostgreSQL/Oracle)
- **Table Metadata System**: Rich table definitions with column descriptions and sample data
- **CSV Export**: Query result export functionality

### 🔐 Enterprise Security
- **JWT Authentication**: Secure token-based authentication with Bearer token support
- **Role-Based Access Control**: Flexible role and permission management system
- **Password Hashing**: Secure password storage with SHA-256 hashing
- **Global Auth Middleware**: Automatic token validation on all protected endpoints
- **User Management**: Complete CRUD operations with active/inactive status

### 🏗️ Production Architecture
- **Clean Architecture**: Repository pattern with dependency injection
- **Type Safety**: Full Pydantic validation and SQLAlchemy type hints
- **Error Handling**: Centralized exception handlers with custom error responses
- **Structured Logging**: Comprehensive logging with file and console output
- **Scalable Design**: Modular structure for easy maintenance and extension

## 📁 Project Architecture

```
query-db-bot-apis/
├── 📋 config/                      # Configuration Management
│   ├── __init__.py                # Package exports
│   ├── settings.py               # Environment-based settings (JWT, DB URLs)
│   └── database.py               # Dual database connections (bot + transactional)
├── 🗃️ models/                     # SQLAlchemy ORM Models
│   ├── __init__.py               # Model registry
│   ├── user.py                   # User authentication & role model
│   ├── role.py                   # Role master & permissions model
│   ├── table.py                  # Table metadata model
│   └── chat.py                   # Chat sessions & conversation history
├── 📊 schemas/                    # Pydantic API Schemas
│   ├── __init__.py               # Schema exports
│   ├── auth.py                   # Authentication request/response schemas
│   ├── user.py                   # User CRUD schemas
│   ├── role.py                   # Role & permission schemas
│   ├── table.py                  # Table definition schemas
│   ├── chat.py                   # Chat conversation schemas
│   └── error.py                  # Error response schemas
├── 🔄 repositories/               # Data Access Layer
│   ├── __init__.py               
│   ├── user_repository.py        # User CRUD operations
│   ├── role_repository.py        # Role & permission operations
│   ├── table_repository.py       # Table metadata operations
│   ├── chat_repository.py        # Chat session & history management
│   └── query_repository.py       # SQL query execution
├── 🧠 services/                   # Business Logic Layer
│   ├── __init__.py               
│   ├── auth_service.py           # Authentication & JWT token management
│   ├── user_service.py           # User management logic
│   ├── role_service.py           # Role & permission logic
│   ├── table_service.py          # Table operations logic
│   ├── chat_service.py           # Conversational query processing
│   ├── llm_service.py            # Ollama LLM integration (Mistral)
│   ├── prompt_service.py         # AI prompt template management
│   └── masters_service.py        # Master data service
├── 🌐 routers/                    # API Endpoints
│   ├── __init__.py               
│   ├── auth_router.py            # Authentication APIs (/apis/auth)
│   ├── user_router.py            # User management APIs (/apis/users)
│   ├── role_router.py            # Role management APIs (/apis/roles)
│   ├── table_router.py           # Table management APIs (/apis/tabledef)
│   ├── chat_router.py            # Conversational query APIs (/apis/chat)
│   └── masters_router.py         # Master data APIs (/apis/masters)
├── 🔒 middleware/                 # HTTP Middleware
│   ├── __init__.py               
│   └── auth_middleware.py        # Global JWT authentication middleware
├── 🛠️ utils/                      # Utility Modules
│   ├── __init__.py               
│   ├── dependencies.py           # FastAPI dependency injection
│   ├── security.py               # JWT encoding/decoding & password hashing
│   ├── logger.py                 # Structured logging configuration
│   ├── file_utils.py             # File operations
│   └── role_checker.py           # Role-based authorization helpers
├── 🎨 decorators/                 # Custom Decorators
│   ├── auth_decorators.py        # Authentication decorators
│   └── transaction.py            # Database transaction decorators
├── 🧩 mappers/                    # Data Mappers
│   ├── __init__.py               
│   ├── auth_mapper.py            # Authentication data mapping
│   ├── user_mapper.py            # User data mapping
│   ├── role_mapper.py            # Role data mapping
│   └── table_mapper.py           # Table data mapping
├── ⚠️ exceptions/                 # Exception Handling
│   ├── exceptions.py             # Custom exception classes
│   └── error_handlers.py         # Global error handlers
├── 📝 templates/                  # AI Prompt Templates
│   ├── sql_generation.txt        # SQL generation prompts
│   ├── table_identification.txt  # Table selection prompts
│   ├── session_title.txt         # Auto-title generation
│   └── context_help_message.txt  # User guidance prompts
├── 💬 messages/                   # Internationalization
│   ├── message_source.py         # Message source loader
│   └── messages.properties       # Message templates
├── 📊 csv/                        # CSV Export
│   └── csv_exporter.py           # Query result CSV export
├── 📄 logs/                       # Application Logs
│   └── app.log                   # Rotating log file
├── 🚀 main.py                     # FastAPI application entry point
├── 📦 requirements.txt            # Python dependencies
└── 📖 README.md                  # Project documentation
```

## 🛠️ Installation

### Prerequisites

- Python 3.8+
- pip or poetry

### Setup

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd query-db-bot-apis
   ```

2. **Create virtual environment**
   ```bash
   # Windows PowerShell
   python -m venv .venv
   .venv\Scripts\Activate.ps1
   
   # macOS/Linux
   python -m venv .venv
   source .venv/bin/activate
   ```

3. **Install dependencies**
   
   **Option A: Activate virtual environment first (Recommended)**
   ```bash
   # On Windows
   .venv\Scripts\Activate.ps1
   pip install -r requirements.txt
   
   # On macOS/Linux
   source .venv/bin/activate
   pip install -r requirements.txt
   ```
   
   **Option B: Use full path to avoid activation**
   ```bash
   # On Windows
   .venv\Scripts\pip.exe install -r requirements.txt
   
   # On macOS/Linux
   .venv/bin/pip install -r requirements.txt
   ```
   
   **Option C: Use python -m pip**
   ```bash
   # On Windows
   .venv\Scripts\python.exe -m pip install -r requirements.txt
   
   # On macOS/Linux
   .venv/bin/python -m pip install -r requirements.txt
   ```

## Generate Bot Database

Create roles, role_permissions, users, table_definitions, chat_sessions and chat history:

```bash
python test_dbs/bot_db/bot_db_creator.py
```
## Generate Transactional Database

Create orders, products, sales and employee:

```bash
python test_dbs/trans_db/trans_db_creator.py
```

4. **Environment configuration**
   ```bash
   # Create .env file with your settings
DATABASE_URL=sqlite:///./test_dbs/bot_db/bot_db.db
TRANS_DATABASE_URL=sqlite:///./test_dbs/trans_db/trans_db.db
JWT_SECRET_KEY=1234567890
JWT_ALGORITHM=HS256
JWT_EXPIRATION_MINUTES=3060
   ```

5. **Run the application**
   ```bash
   uvicorn main:app --reload
   ```

The API will be available at `http://localhost:8000`

**Note:** The application will automatically create database tables on first run.

## 🔧 Configuration

### Environment Variables

Create a `.env` file in the project root:

```env
# Bot Database (Metadata, Users, Roles, Chat Sessions)
DATABASE_URL=sqlite:///./test.db

# Transactional Database (Business Data for Queries)
TRANS_DATABASE_URL=sqlite:///./data.db

# JWT Configuration
JWT_SECRET_KEY=your-secret-key-here
JWT_ALGORITHM=HS256
JWT_EXPIRATION_MINUTES=3060  # 51 hours
```

### Database Configuration

The system uses a **dual database architecture**:

1. **Bot Database (`DATABASE_URL`)**
   - Stores: Users, Roles, Permissions, Table Definitions, Chat Sessions, Conversation History
   - Purpose: Application metadata and user management
   
2. **Transactional Database (`TRANS_DATABASE_URL`)**
   - Stores: Business data (customers, orders, products, etc.)
   - Purpose: SQL query execution target

### Database URL Formats

- **SQLite** (Development): `sqlite:///./database.db`
- **PostgreSQL** (Production): `postgresql://user:password@host:port/database`
- **Oracle** (Enterprise): `oracle://user:password@host:port/service_name`

## 🎯 Quick Start Example

```python
import requests

# Base URL
BASE_URL = "http://localhost:8000"

# 1. Authenticate and get JWT token
login_response = requests.post(f"{BASE_URL}/apis/auth/login", json={
    "email": "user@example.com",
    "password": "yourpassword"
})
auth_data = login_response.json()
token = auth_data["token"]

# Setup headers with Bearer token
headers = {"Authorization": f"Bearer {token}"}

# 2. Create a new chat session with first query
session_response = requests.post(
    f"{BASE_URL}/apis/chat/session",
    headers=headers,
    json={
        "user_id": auth_data["id"],
        "query_text": "Show me all customers from New York"
    }
)
session = session_response.json()
session_id = session["session_id"]
print(f"Session created: {session_id}")
print(f"First query SQL: {session['conversations'][0]['sql_generated']}")

# 3. Continue the conversation with follow-up questions
query_response = requests.post(
    f"{BASE_URL}/apis/chat/session/{session_id}/query",
    headers=headers,
    json={
        "query_text": "Now show their recent orders"
    }
)
result = query_response.json()
print(f"Generated SQL: {result['sql_generated']}")
print(f"Content: {result['content']}")
```

## 📚 API Documentation

### Interactive Documentation
Once the application is running, explore the full API:

- **📖 Swagger UI**: `http://localhost:8000/docs`
- **📝 ReDoc**: `http://localhost:8000/redoc`

### 🔐 Authentication API

#### Login
```http
POST /apis/auth/login
```

**Request:**
```json
{
  "email": "user@example.com",
  "password": "userpassword"
}
```

**Success Response (200):**
```json
{
  "id": "user_12345",
  "name": "John Doe",
  "email": "user@example.com",
  "provider": "local",
  "role": "admin",
  "permissions": [
    {"ref_id": "table1", "granted": true},
    {"ref_id": "table2", "granted": false}
  ],
  "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
}
```

**Note:** All subsequent API calls require the `Authorization: Bearer <token>` header.

### 👤 User Management API

#### Create User
```http
POST /apis/users/
Authorization: Bearer <token>
```

**Request:**
```json
{
  "email": "newuser@example.com",
  "password": "securepassword",
  "name": "Jane Doe",
  "provider": "local",
  "role": "user",
  "is_active": true
}
```

#### List Users (Paginated)
```http
GET /apis/users/?skip=0&limit=10
Authorization: Bearer <token>
```

#### Get User by ID
```http
GET /apis/users/{user_id}
Authorization: Bearer <token>
```

#### Update User
```http
PUT /apis/users/{user_id}
Authorization: Bearer <token>
```

#### Delete User
```http
DELETE /apis/users/{user_id}
Authorization: Bearer <token>
```

### 🔑 Role Management API

#### Create Role
```http
POST /apis/roles/
Authorization: Bearer <token>
```

**Request:**
```json
{
  "role_name": "analyst",
  "description": "Data analyst role with read access",
  "is_active": true,
  "created_by": "admin",
  "permissions": [
    {"ref_id": "customers_table", "granted": true},
    {"ref_id": "orders_table", "granted": true}
  ]
}
```

#### List Roles
```http
GET /apis/roles/
Authorization: Bearer <token>
```

#### Update Role
```http
PUT /apis/roles/{role_id}
Authorization: Bearer <token>
```

#### Delete Role
```http
DELETE /apis/roles/{role_id}
Authorization: Bearer <token>
```

### 💬 Chat Session API

#### Create Chat Session
```http
POST /apis/chat/session
Authorization: Bearer <token>
```

**Request:**
```json
{
  "user_id": "user_12345",
  "query_text": "Show me all customers from New York"
}
```

**Response:**
```json
{
  "session_id": "sess_abc123",
  "user_id": "user_12345",
  "title": "Customers from New York",
  "is_active": true,
  "created_date": "2025-11-13T10:30:00Z",
  "conversations": [
    {
      "id": "conv_xyz789",
      "session_id": "sess_abc123",
      "query_text": "Show me all customers from New York",
      "sql_generated": "SELECT * FROM customers WHERE state = 'NY'",
      "content": "[{...}]",
      "content_type": "application/json",
      "execution_time_ms": "156.78",
      "created_date": "2025-11-13T10:30:00Z"
    }
  ]
}
```

#### Process Chat Query
```http
POST /apis/chat/session/{session_id}/query
Authorization: Bearer <token>
```

**Request:**
```json
{
  "query_text": "Show me all customers from New York with orders over $100"
}
```

**Response:**
```json
{
  "id": "conv_xyz789",
  "session_id": "sess_abc123",
  "query_text": "Show me all customers from New York with orders over $100",
  "sql_generated": "SELECT c.* FROM customers c JOIN orders o ON c.customer_id = o.customer_id WHERE c.state = 'NY' AND o.total_amount > 100",
  "content": "[{\"customer_id\": 1, \"name\": \"John Doe\", ...}, ...]",
  "content_type": "application/json",
  "execution_time_ms": "234.56",
  "error_message": null,
  "created_date": "2025-11-13T10:35:00Z"
}
```

#### Get Session Information
```http
GET /apis/chat/session/{session_id}
Authorization: Bearer <token>
```

#### Get User's Chat Sessions
```http
GET /apis/chat/sessions/{user_id}
Authorization: Bearer <token>
```

#### Delete Chat Session
```http
DELETE /apis/chat/session/{session_id}
Authorization: Bearer <token>
```

### 🗄️ Table Definition API

#### Create Table Definition
```http
POST /apis/tabledef/
Authorization: Bearer <token>
```

**Request:**
```json
{
  "table_name": "customers",
  "description": "Customer information with contact details",
  "notes": "Primary table for customer data",
  "columns": [
    {
      "name": "customer_id",
      "type": "INTEGER",
      "nullable": false,
      "description": "Unique customer identifier"
    },
    {
      "name": "first_name",
      "type": "VARCHAR(50)",
      "nullable": false,
      "description": "Customer first name"
    },
    {
      "name": "email",
      "type": "VARCHAR(100)",
      "nullable": false,
      "description": "Customer email address"
    }
  ],
  "sample_rows": [
    {"customer_id": 1, "first_name": "John", "email": "john@example.com"},
    {"customer_id": 2, "first_name": "Jane", "email": "jane@example.com"}
  ]
}
```

#### List Table Definitions
```http
GET /apis/tabledef/?skip=0&limit=50
Authorization: Bearer <token>
```

#### Get Table Definition by ID
```http
GET /apis/tabledef/{td_id}
Authorization: Bearer <token>
```

#### Update Table Definition
```http
PUT /apis/tabledef/{td_id}
Authorization: Bearer <token>
```

#### Delete Table Definition
```http
DELETE /apis/tabledef/{td_id}
Authorization: Bearer <token>
```

### 📋 Masters API

#### Get Available Permissions
```http
GET /apis/masters/permissions
Authorization: Bearer <token>
```

**Response:**
```json
[
  "customers_table",
  "orders_table",
  "products_table",
  "inventory_table"
]
```

## 🏗️ System Architecture

### 🧠 AI-Powered Query Processing Flow

```mermaid
graph TD
    A[User Login] --> B[JWT Token Generation]
    B --> C[Authenticated Request with Bearer Token]
    C --> D[Auth Middleware Validation]
    D --> E[Natural Language Query]
    E --> F[Chat Service]
    F --> G[LLM Service - Table Identification]
    G --> H[Permission Check]
    H --> I[LLM Service - SQL Generation]
    I --> J[Query Repository - SQL Execution]
    J --> K[Result Processing & CSV Export]
    K --> L[Save Conversation History]
    L --> M[Return Response with SQL + Data]

    N[Table Repository] --> G
    O[Conversation History] --> I
    P[Prompt Templates] --> G
    P --> I
    Q[Role & Permission Repository] --> H
```

### 🔐 JWT Authentication Flow

```mermaid
sequenceDiagram
    participant User
    participant AuthRouter
    participant AuthService
    participant JWTMiddleware
    participant ProtectedEndpoint

    User->>AuthRouter: POST /apis/auth/login
    AuthRouter->>AuthService: Validate credentials
    AuthService-->>AuthRouter: User data + JWT token
    AuthRouter-->>User: Return token
    
    User->>ProtectedEndpoint: Request with Bearer token
    ProtectedEndpoint->>JWTMiddleware: Validate token
    JWTMiddleware->>JWTMiddleware: Decode & verify JWT
    JWTMiddleware->>JWTMiddleware: Check user exists & active
    JWTMiddleware-->>ProtectedEndpoint: Attach user to request
    ProtectedEndpoint-->>User: Process request
```

### 🏛️ Clean Architecture Principles

#### **🔄 Repository Pattern**
- **Data Access Abstraction**: Clean separation between business logic and database operations
- **Dual Database Support**: Bot database (metadata) + Transactional database (queries)
- **Testability**: Easy mocking for unit tests
- **Database Agnostic**: Switch between SQLite, PostgreSQL, Oracle seamlessly

#### **🧠 Service Layer Architecture**
- **Business Logic Isolation**: Core functionality separated from API concerns  
- **Dependency Injection**: Loose coupling for maintainability and testing
- **Single Responsibility**: Each service handles one domain area
- **LLM Integration**: Centralized AI service for table identification and SQL generation

#### **🔒 Security Architecture**
- **Global Middleware**: Automatic JWT validation on all protected endpoints
- **Role-Based Access**: Flexible permission system with grant/deny support
- **Password Security**: SHA-256 hashing with secure storage
- **Token Management**: Configurable expiration with refresh capability

#### **🛡️ Type Safety & Validation**
- **Pydantic Schemas**: Request/response validation with clear error messages
- **SQLAlchemy Types**: Database-level type enforcement
- **Runtime Validation**: Input sanitization and format checking

### 🎯 Key Design Components

| Layer | Component | Responsibility |
|-------|-----------|----------------|
| **🌐 API** | FastAPI Routers | HTTP request handling, validation, response formatting |
| **🔒 Middleware** | JWTAuthMiddleware | Token validation, user verification, request enrichment |
| **🧠 Business** | Service Classes | Business logic, orchestration, AI integration |
| **🔄 Data** | Repository Classes | Database operations, query execution, transaction management |
| **🗃️ Models** | SQLAlchemy Models | Database schema definition, relationships, constraints |
| **📊 Schemas** | Pydantic Models | API contract definition, validation rules, serialization |
| **⚙️ Config** | Settings Management | Environment configuration, dual database connections, JWT settings |
| **🛠️ Utils** | Helper Functions | Cross-cutting concerns, utilities, decorators |
| **🧩 Mappers** | Data Mappers | Model-to-schema transformation, data mapping |
| **⚠️ Exceptions** | Error Handlers | Centralized exception handling, error response formatting |

## � LLM Integration (Ollama)

### 🔧 Setup Ollama

1. **Install Ollama**: Visit [ollama.ai](https://ollama.ai) and download for your OS
2. **Pull a model**:
   ```bash
   ollama pull llama2  # or codellama, mistral, etc.
   ```
3. **Verify installation**:
   ```bash
   ollama list
   ```

### 🧠 How AI Works in the System

#### **Phase 1: Smart Table Identification**
- Analyzes your natural language query
- Identifies relevant tables from your database schema
- Provides context-aware suggestions if no tables match

#### **Phase 2: SQL Generation**
- Uses conversation history for context
- Generates Oracle-compatible SQL
- Applies safety validations before execution

#### **Phase 3: Response Enhancement**
- Auto-generates session titles based on query content
- Provides helpful guidance for unclear queries
- Maintains conversation context for follow-up questions

### 📝 Prompt Engineering

The system uses carefully crafted prompt templates in `/templates/`:

- `sql_generation.txt` - Core SQL generation logic
- `table_identification.txt` - Smart table selection
- `session_title.txt` - Automatic session naming
- `context_help_message.txt` - User guidance system

## �🧪 Testing & Development

### 🚀 Quick Test Setup

```bash
# 1. Start the development server
uvicorn main:app --reload --port 8000

# 2. Access interactive API documentation
# Visit http://localhost:8000/docs

# 3. Test authentication endpoint
# Use the Swagger UI to login and get a JWT token
```

### 🔧 Development Testing

```bash
# Test authentication
curl -X POST http://localhost:8000/apis/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"user@example.com","password":"password"}'

# Test protected endpoint (requires token)
curl -X GET http://localhost:8000/apis/users/ \
  -H "Authorization: Bearer YOUR_TOKEN_HERE"

# View application logs
cat logs/app.log
```

### 📊 Sample Queries to Test

Once your server is running, try these conversational queries:

```bash
# Basic queries
"Show me all customers from New York"
"List products in Electronics category"
"What are the recent orders?"

# Complex analytical queries  
"Show customers with orders over $100"
"Which products have low inventory?"
"What's the average order value by state?"

# Follow-up conversations
"Now show their email addresses"
"Filter those to only active customers"
"Export the top 10 results"
```

## 🚀 Production Deployment

### 🐳 Docker Deployment (Recommended)

#### **Single Container Setup**

1. **Create Dockerfile** (if not exists):
   ```dockerfile
   FROM python:3.11-slim
   
   WORKDIR /app
   
   COPY requirements.txt .
   RUN pip install --no-cache-dir -r requirements.txt
   
   COPY . .
   
   EXPOSE 8000
   
   CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
   ```

2. **Build and run**:
   ```bash
   # Build image
   docker build -t query-db-bot-apis .
   
   # Run container
   docker run -p 8000:8000 \
     -e DATABASE_URL=postgresql://user:pass@host:port/db \
     -e OLLAMA_URL=http://host.docker.internal:11434 \
     query-db-bot-apis
   ```

#### **Docker Compose Setup**

Create `docker-compose.yml`:
```yaml
version: '3.8'
services:
  query-bot-api:
    build: .
    ports:
      - "8000:8000"
    environment:
      - DATABASE_URL=postgresql://postgres:password@db:5432/querybot
      - OLLAMA_URL=http://ollama:11434
    depends_on:
      - db
      - ollama
    
  db:
    image: postgres:15
    environment:
      POSTGRES_DB: querybot
      POSTGRES_USER: postgres
      POSTGRES_PASSWORD: password
    volumes:
      - postgres_data:/var/lib/postgresql/data
    
  ollama:
    image: ollama/ollama
    ports:
      - "11434:11434"
    volumes:
      - ollama_data:/root/.ollama

volumes:
  postgres_data:
  ollama_data:
```

**Deploy with**:
```bash
docker-compose up -d
```

### ⚡ High-Performance Production Setup

#### **🚀 Gunicorn + Uvicorn Workers**
```bash
# Install production server
pip install gunicorn

# Run with multiple workers
gunicorn main:app \
  -w 4 \
  -k uvicorn.workers.UvicornWorker \
  --bind 0.0.0.0:8000 \
  --access-logfile - \
  --error-logfile - \
  --log-level info
```

#### **🔄 Load Balancer Configuration**

**Nginx Configuration**:
```nginx
upstream query_bot_api {
    server 127.0.0.1:8001;
    server 127.0.0.1:8002;
    server 127.0.0.1:8003;
    server 127.0.0.1:8004;
}

server {
    listen 80;
    server_name your-domain.com;
    
    location / {
        proxy_pass http://query_bot_api;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    }
}
```

### 📊 Production Environment Variables

```bash
# Bot Database (Metadata, Users, Roles, Sessions)
DATABASE_URL=postgresql://user:pass@host:port/bot_database

# Transactional Database (Business Data for Queries)
TRANS_DATABASE_URL=postgresql://user:pass@host:port/trans_database

# JWT Configuration
JWT_SECRET_KEY=your-strong-secret-key-here
JWT_ALGORITHM=HS256
JWT_EXPIRATION_MINUTES=3060

# AI/LLM Configuration (Ollama runs locally or containerized)
# Mistral model is used by default in LLMService

# Performance
WORKERS=4
MAX_CONNECTIONS=100
TIMEOUT=30

# Logging
LOG_LEVEL=INFO
# Logs are stored in logs/app.log
```

### 🔍 Production Monitoring

#### **Health Check Endpoint**
```python
# Add to main.py
@app.get("/health")
def health_check():
    return {
        "status": "healthy",
        "timestamp": datetime.utcnow(),
        "version": "1.0.0"
    }
```

#### **Monitoring Stack**
- **📊 Prometheus**: Metrics collection
- **📈 Grafana**: Dashboard visualization  
- **🚨 AlertManager**: Error alerting
- **📝 ELK Stack**: Centralized logging

## 🔒 Security & Best Practices

### 🛡️ Multi-Layer Security

#### **🔐 Authentication & Authorization**
- **JWT Authentication**: Bearer token-based authentication with HS256 algorithm
- **Global Middleware**: Automatic token validation on all protected endpoints
- **Password Hashing**: Secure SHA-256 hashing for password storage
- **Role-Based Access**: Flexible role and permission management system
- **Token Expiration**: Configurable token expiration (default: 51 hours)
- **User Status Check**: Active/inactive user status validation

#### **🔒 Protected Endpoints**
- **Exempt Paths**: `/apis/auth/login`, `/docs`, `/openapi.json`, `/redoc`
- **Authorization Header**: Required format: `Authorization: Bearer <token>`
- **Token Validation**: Decodes JWT, validates signature, checks user existence
- **Request Enrichment**: Attaches user info to request state for endpoints

#### **🚫 SQL Injection Prevention**
- **Query Validation**: LLM-generated SQL validation and sanitization
- **Parameterized Queries**: SQLAlchemy ORM protection
- **Repository Pattern**: Abstracted database access layer
- **LLM Output Sanitization**: Cleans and validates AI-generated SQL

#### **🔒 Data Protection**
- **User Isolation**: Complete session and data segregation per user
- **Transaction Safety**: Database transaction management with decorators
- **Dual Database Architecture**: Separated metadata and transactional data
- **Environment Secrets**: Sensitive configuration via environment variables
- **CORS Configuration**: Configurable CORS with error response headers

### ⚡ Performance Optimization

#### **🚀 Query Performance**
- **Connection Pooling**: Efficient database connections
- **Lazy Loading**: On-demand data fetching
- **Result Caching**: Configurable query result caching (Redis ready)
- **Pagination**: Built-in result set pagination

#### **🧠 AI Performance**
- **Context Management**: Conversation history used for SQL generation context
- **Table Filtering**: Smart table identification reduces LLM context size
- **Prompt Optimization**: Efficient prompt templates in `/templates/`
- **Timeout Configuration**: Configurable timeouts for each LLM operation (200s default)
- **Subprocess Execution**: Ollama runs as subprocess with timeout management
- **Fallback Mechanisms**: Graceful degradation when LLM is unavailable

#### **📊 Monitoring & Observability**
```python
# Built-in structured logging throughout the application
from utils.logger import get_logger

logger = get_logger(__name__)

# Request tracking
logger.info(f"Login request received for email: {email}")

# Performance monitoring  
logger.info(f"Query processed successfully in {execution_time_ms}ms")

# Error tracking
logger.error(f"Query processing failed: {error_message}")

# Logs are written to: logs/app.log (rotating file handler)
```

### 🔧 Configuration Management

#### **Environment-Based Settings**
```python
# config/settings.py - Production-ready configuration
class Settings(BaseSettings):
    DATABASE_URL: str = "sqlite:///./test.db"
    TRANS_DATABASE_URL: str = "sqlite:///./data.db"
    JWT_SECRET_KEY: str = "your-secret-key-here"
    JWT_ALGORITHM: str = "HS256"
    JWT_EXPIRATION_MINUTES: int = 3060
    
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra='ignore'
    )
```

### 🚨 Error Handling & Resilience

#### **Graceful Degradation**
- **LLM Service Failures**: Fallback to basic query patterns
- **Database Connectivity**: Connection retry logic with exponential backoff  
- **File System Issues**: Alternative storage mechanisms
- **Invalid Queries**: User-friendly error messages with suggestions

#### **Comprehensive Exception Management**
```python
# Centralized error handling with custom exception handlers
# exceptions/error_handlers.py - Global exception handlers registered in main.py

# Custom exceptions defined in exceptions/exceptions.py
# Error responses follow ErrorResponse schema

# Example in routers:
@router.post("/apis/auth/login", responses={401: {"model": ErrorResponse}})
def authenticate_user(login_data: AuthRequest, db: Session = Depends(get_db)):
    try:
        response = auth_service.authenticate_user(db, login_data)
        return response
    except ValueError as e:
        # Handled by global exception handler
        raise HTTPException(status_code=401, detail=str(e))
```

### 📋 Production Checklist

- [ ] **🔒 Security Audit**: Review all endpoints for security vulnerabilities
- [ ] **🚀 Performance Testing**: Load testing with expected traffic patterns
- [ ] **📊 Monitoring Setup**: Implement health checks and alerting
- [ ] **🔄 Backup Strategy**: Database backup and recovery procedures  
- [ ] **🌍 Scaling Plan**: Horizontal scaling strategy for increased load
- [ ] **📝 Documentation**: API documentation and operational runbooks
- [ ] **🧪 Testing Suite**: Comprehensive unit and integration tests
- [ ] **🔐 Secrets Management**: Secure handling of API keys and passwords

## 🛠️ Development

### Code Quality

```bash
# Format code
black .

# Sort imports
isort .

# Lint code
flake8 .

# Type checking
mypy .
```

### Pre-commit Hooks

```bash
# Install pre-commit
pip install pre-commit

# Install hooks
pre-commit install

# Run hooks manually
pre-commit run --all-files
```

## 🛠️ Development & Contributing

### 🔧 Development Setup

```bash
# 1. Clone and setup
git clone <repository-url>
cd query-db-bot-apis

# 2. Create development environment  
python -m venv .venv
.venv\Scripts\Activate.ps1  # Windows
# source .venv/bin/activate  # macOS/Linux

# 3. Install development dependencies
pip install -r requirements.txt
pip install -r requirements-dev.txt  # If exists

# 4. Setup pre-commit hooks (if available)
pre-commit install

# 5. Start development server
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### 🧪 Code Quality & Testing

```bash
# Code formatting
black .                          # Format Python code
isort .                         # Sort imports

# Code linting  
flake8 .                        # Style guide enforcement
pylint **/*.py                  # Advanced code analysis
mypy .                          # Type checking

# Security scanning
bandit -r .                     # Security vulnerability scanning
safety check                    # Check dependencies for vulnerabilities
```

### 🚀 Contributing Guidelines

#### **🔀 Pull Request Process**

1. **Fork & Branch**
   ```bash
   git checkout -b feature/your-feature-name
   # or
   git checkout -b bugfix/issue-description  
   # or
   git checkout -b docs/documentation-update
   ```

2. **Development Standards**
   - Follow PEP 8 style guidelines
   - Add type hints to all functions
   - Write docstrings for all public methods
   - Include unit tests for new functionality
   - Update API documentation if needed

3. **Commit Guidelines**
   ```bash
   # Use conventional commit format
   git commit -m "feat: add new chat session endpoint"
   git commit -m "fix: resolve SQL injection vulnerability"  
   git commit -m "docs: update API documentation"
   git commit -m "test: add integration tests for chat service"
   ```

4. **Pull Request Template**
   - Clear description of changes
   - Screenshots/examples for UI changes
   - Test coverage information
   - Breaking change notifications
   - Link to related issues

#### **🐛 Issue Reporting**

**Bug Report Template:**
```markdown
## Bug Description
Brief description of the issue

## Steps to Reproduce
1. Step one
2. Step two  
3. Step three

## Expected Behavior
What should happen

## Actual Behavior  
What actually happens

## Environment
- OS: [Windows/macOS/Linux]
- Python version: [3.11]
- FastAPI version: [0.104.1]
- Database: [SQLite/PostgreSQL/Oracle]
```

**Feature Request Template:**
```markdown
## Feature Description
Clear description of the proposed feature

## Use Case
Why this feature would be valuable

## Proposed Implementation
Technical approach (if you have ideas)

## Additional Context
Screenshots, mockups, or related issues
```

### 📚 Development Resources

#### **🏗️ Architecture Patterns**
- **Repository Pattern**: `repositories/` - Data access layer
- **Service Layer**: `services/` - Business logic layer  
- **Dependency Injection**: `utils/dependencies.py` - IoC container
- **Transaction Management**: `utils/transaction.py` - Database transactions

#### **🧪 Testing Patterns**
```python
# Example test structure
def test_chat_query_processing(test_db, sample_user):
    # Arrange
    chat_service = ChatService(chat_repo, table_repo, llm_service)
    request = ChatQueryRequest(user_id=sample_user.id, query_text="test query")
    
    # Act  
    response = chat_service.process_chat_query(test_db, request)
    
    # Assert
    assert response.session_id is not None
    assert response.sql_generated is not None
    assert len(response.data_preview) <= 50
```

#### **🔌 Adding New Features**

**Example: Adding a new API endpoint**

1. **Create Schema** (`schemas/new_feature.py`)
2. **Update Model** (`models/new_feature.py`) 
3. **Add Repository Methods** (`repositories/new_feature_repository.py`)
4. **Implement Service Logic** (`services/new_feature_service.py`)
5. **Create API Router** (`routers/new_feature_router.py`)
6. **Register Router** (`main.py`)
7. **Add Tests** (`tests/test_new_feature.py`)
8. **Update Documentation** (API docs, README)



### 🚀 Core Technologies
- **[FastAPI](https://fastapi.tiangolo.com/)** v0.104.1 - Modern, fast Python web framework
- **[SQLAlchemy](https://www.sqlalchemy.org/)** >=2.0.30 - Powerful Python SQL toolkit and ORM
- **[Pydantic](https://pydantic.dev/)** v2.5.0 - Data validation using Python type hints
- **[Uvicorn](https://www.uvicorn.org/)** v0.24.0 - Lightning-fast ASGI server
- **[Ollama](https://ollama.ai/)** - Local LLM inference engine
- **[PyJWT](https://pyjwt.readthedocs.io/)** v2.8.0 - JSON Web Token implementation
- **[httpx](https://www.python-httpx.org/)** v0.25.2 - Async HTTP client
- **[oracledb](https://python-oracledb.readthedocs.io/)** v2.0.1 - Oracle Database driver

### 🧠 AI & Machine Learning
- **Mistral** - Default LLM model for SQL generation and table identification
- **Ollama** - Local LLM inference platform for privacy and performance
- **Custom Prompt Engineering** - Optimized templates for SQL generation

### 🏗️ Architecture Inspiration  
- **Clean Architecture** by Robert C. Martin
- **Domain-Driven Design** principles
- **FastAPI** best practices and patterns
