# Sample DB Generation

This directory contains scripts to generate sample data for both databases:
- **Bot Database**: User accounts, roles, permissions, chat sessions, and table definitions
- **Transactional Database**: Customer orders, products, sales data, and employee records

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

# Usage
Make sure you have configured your `.env` file with database URLs:
```
DATABASE_URL=sqlite:///./test_dbs/bot_db/bot_db.db
TRANS_DATABASE_URL=sqlite:///./test_dbs/trans_db/trans_db.db
```