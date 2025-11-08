# SQL Style Guide

## Table of Contents
- [Naming Conventions](#naming-conventions)
- [Schema Design](#schema-design)
- [Query Writing](#query-writing)
- [Performance](#performance)
- [Security](#security)

## Naming Conventions

### Tables and Columns

✅ **Good:**
```sql
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    email VARCHAR(255) NOT NULL UNIQUE,
    first_name VARCHAR(100) NOT NULL,
    last_name VARCHAR(100) NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE order_items (
    id SERIAL PRIMARY KEY,
    order_id INTEGER NOT NULL,
    product_id INTEGER NOT NULL,
    quantity INTEGER NOT NULL CHECK (quantity > 0),
    unit_price DECIMAL(10, 2) NOT NULL,
    CONSTRAINT fk_order_items_order_id FOREIGN KEY (order_id) REFERENCES orders(id),
    CONSTRAINT fk_order_items_product_id FOREIGN KEY (product_id) REFERENCES products(id)
);
```

❌ **Bad:**
```sql
CREATE TABLE User (  -- Should be lowercase and plural
    ID INT PRIMARY KEY,  -- Should be lowercase
    Email VARCHAR(255),  -- Should be lowercase with underscore
    FirstName VARCHAR(100),
    CreatedDate TIMESTAMP
);
```

### Indexes and Constraints

✅ **Good:**
```sql
CREATE INDEX idx_users_email ON users(email);
CREATE INDEX idx_orders_user_id_created_at ON orders(user_id, created_at);

ALTER TABLE orders
    ADD CONSTRAINT pk_orders_id PRIMARY KEY (id),
    ADD CONSTRAINT fk_orders_user_id FOREIGN KEY (user_id) REFERENCES users(id),
    ADD CONSTRAINT ck_orders_total_positive CHECK (total_amount > 0);
```

## Schema Design

### Table Structure

✅ **Good:**
```sql
-- Well-normalized user and address tables
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    email VARCHAR(255) NOT NULL UNIQUE,
    password_hash VARCHAR(255) NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE user_addresses (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL,
    address_line1 VARCHAR(255) NOT NULL,
    address_line2 VARCHAR(255),
    city VARCHAR(100) NOT NULL,
    state VARCHAR(50) NOT NULL,
    postal_code VARCHAR(20) NOT NULL,
    country VARCHAR(100) NOT NULL,
    is_primary BOOLEAN DEFAULT FALSE,
    CONSTRAINT fk_user_addresses_user_id FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);

-- Audit columns for tracking changes
CREATE TABLE products (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    description TEXT,
    price DECIMAL(10, 2) NOT NULL,
    stock_quantity INTEGER NOT NULL DEFAULT 0,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    created_by INTEGER,
    updated_by INTEGER
);
```

### Data Types

✅ **Good:**
```sql
CREATE TABLE financial_transactions (
    id SERIAL PRIMARY KEY,
    amount DECIMAL(19, 4) NOT NULL,  -- Use DECIMAL for money
    transaction_date TIMESTAMP WITH TIME ZONE NOT NULL,  -- Include timezone
    description TEXT,
    is_processed BOOLEAN DEFAULT FALSE,  -- Use BOOLEAN, not TINYINT
    metadata JSONB  -- Use JSONB for flexible data
);
```

## Query Writing

### SELECT Statements

✅ **Good:**
```sql
-- Explicit column selection
SELECT 
    u.id,
    u.email,
    u.first_name,
    u.last_name,
    COUNT(o.id) AS order_count
FROM users u
LEFT JOIN orders o ON u.id = o.user_id
WHERE u.is_active = TRUE
    AND u.created_at >= '2024-01-01'
GROUP BY u.id, u.email, u.first_name, u.last_name
HAVING COUNT(o.id) > 0
ORDER BY order_count DESC
LIMIT 100;

-- Using CTEs for complex queries
WITH active_users AS (
    SELECT id, email, first_name, last_name
    FROM users
    WHERE is_active = TRUE
),
user_orders AS (
    SELECT 
        user_id,
        COUNT(*) AS order_count,
        SUM(total_amount) AS total_spent
    FROM orders
    WHERE created_at >= '2024-01-01'
    GROUP BY user_id
)
SELECT 
    au.email,
    au.first_name,
    au.last_name,
    uo.order_count,
    uo.total_spent
FROM active_users au
INNER JOIN user_orders uo ON au.id = uo.user_id
ORDER BY uo.total_spent DESC;
```

❌ **Bad:**
```sql
-- Avoid SELECT *
SELECT * FROM users;

-- Don't use subqueries when JOIN is clearer
SELECT u.email,
    (SELECT COUNT(*) FROM orders WHERE user_id = u.id) AS order_count
FROM users u;

-- Don't put multiple conditions on one line
SELECT * FROM users WHERE is_active = TRUE AND created_at >= '2024-01-01' AND email LIKE '%@example.com%';
```

### INSERT, UPDATE, DELETE

✅ **Good:**
```sql
-- Explicit column names in INSERT
INSERT INTO users (email, first_name, last_name, password_hash)
VALUES ('john@example.com', 'John', 'Doe', 'hashed_password');

-- Multiple row insert
INSERT INTO products (name, price, stock_quantity)
VALUES 
    ('Product A', 19.99, 100),
    ('Product B', 29.99, 50),
    ('Product C', 39.99, 75);

-- Safe UPDATE with WHERE clause
UPDATE users
SET 
    last_login_at = CURRENT_TIMESTAMP,
    login_count = login_count + 1
WHERE id = 123;

-- DELETE with explicit WHERE
DELETE FROM user_sessions
WHERE expires_at < CURRENT_TIMESTAMP;
```

### JOIN Operations

✅ **Good:**
```sql
-- Clear join types and conditions
SELECT 
    o.id AS order_id,
    o.order_number,
    u.email AS customer_email,
    p.name AS product_name,
    oi.quantity,
    oi.unit_price
FROM orders o
INNER JOIN users u ON o.user_id = u.id
INNER JOIN order_items oi ON o.id = oi.order_id
INNER JOIN products p ON oi.product_id = p.id
WHERE o.status = 'completed'
    AND o.created_at >= CURRENT_DATE - INTERVAL '30 days'
ORDER BY o.created_at DESC;
```

## Performance

### Indexes

✅ **Good:**
```sql
-- Index on frequently queried columns
CREATE INDEX idx_users_email ON users(email);
CREATE INDEX idx_orders_user_id ON orders(user_id);
CREATE INDEX idx_orders_created_at ON orders(created_at);

-- Composite index for multi-column queries
CREATE INDEX idx_orders_user_id_status_created_at 
ON orders(user_id, status, created_at);

-- Partial index for specific queries
CREATE INDEX idx_active_users_email 
ON users(email) 
WHERE is_active = TRUE;

-- Index on foreign keys
CREATE INDEX idx_order_items_order_id ON order_items(order_id);
CREATE INDEX idx_order_items_product_id ON order_items(product_id);
```

### Query Optimization

✅ **Good:**
```sql
-- Use EXPLAIN ANALYZE to understand query performance
EXPLAIN ANALYZE
SELECT u.email, COUNT(o.id) AS order_count
FROM users u
LEFT JOIN orders o ON u.id = o.user_id
WHERE u.created_at >= '2024-01-01'
GROUP BY u.id, u.email;

-- Use appropriate WHERE conditions
SELECT id, email, first_name, last_name
FROM users
WHERE created_at >= '2024-01-01'  -- Indexed column
    AND is_active = TRUE
LIMIT 100;

-- Use EXISTS instead of IN for large subqueries
SELECT u.id, u.email
FROM users u
WHERE EXISTS (
    SELECT 1 
    FROM orders o 
    WHERE o.user_id = u.id 
        AND o.created_at >= '2024-01-01'
);
```

❌ **Bad:**
```sql
-- Don't use functions on indexed columns
SELECT * FROM users 
WHERE LOWER(email) = 'john@example.com';  -- Index on email won't be used

-- Avoid OR in WHERE clause when possible
SELECT * FROM orders 
WHERE status = 'pending' OR status = 'processing';  -- Use IN instead

-- Better:
SELECT * FROM orders 
WHERE status IN ('pending', 'processing');
```

## Security

### Parameterized Queries

✅ **Good:**
```sql
-- In application code, always use parameterized queries
-- Example with PostgreSQL (psycopg2 in Python)
-- cursor.execute("SELECT * FROM users WHERE email = %s", (user_email,))

-- Prepared statements
PREPARE get_user_by_email (VARCHAR) AS
    SELECT id, email, first_name, last_name
    FROM users
    WHERE email = $1;

EXECUTE get_user_by_email('john@example.com');
```

❌ **Bad:**
```sql
-- NEVER concatenate user input directly (SQL Injection vulnerability!)
-- BAD: query = "SELECT * FROM users WHERE email = '" + user_email + "'"
```

### Permissions

✅ **Good:**
```sql
-- Create roles with minimal privileges
CREATE ROLE app_reader;
GRANT SELECT ON ALL TABLES IN SCHEMA public TO app_reader;

CREATE ROLE app_writer;
GRANT SELECT, INSERT, UPDATE ON ALL TABLES IN SCHEMA public TO app_writer;

-- Create user and assign role
CREATE USER app_user WITH PASSWORD 'secure_password';
GRANT app_writer TO app_user;

-- Revoke unnecessary privileges
REVOKE DELETE ON users FROM app_writer;
```

## Stored Procedures and Functions

✅ **Good:**
```sql
-- PostgreSQL function with proper error handling
CREATE OR REPLACE FUNCTION create_order(
    p_user_id INTEGER,
    p_total_amount DECIMAL(10, 2)
) RETURNS INTEGER AS $$
DECLARE
    v_order_id INTEGER;
BEGIN
    -- Validate input
    IF p_user_id IS NULL OR p_total_amount <= 0 THEN
        RAISE EXCEPTION 'Invalid input parameters';
    END IF;

    -- Insert order
    INSERT INTO orders (user_id, total_amount, status, created_at)
    VALUES (p_user_id, p_total_amount, 'pending', CURRENT_TIMESTAMP)
    RETURNING id INTO v_order_id;

    -- Return order ID
    RETURN v_order_id;
EXCEPTION
    WHEN OTHERS THEN
        RAISE EXCEPTION 'Error creating order: %', SQLERRM;
END;
$$ LANGUAGE plpgsql;

-- Usage
SELECT create_order(123, 99.99);
```

## Transactions

✅ **Good:**
```sql
-- Explicit transaction management
BEGIN TRANSACTION;

    UPDATE accounts 
    SET balance = balance - 100.00 
    WHERE id = 1;

    UPDATE accounts 
    SET balance = balance + 100.00 
    WHERE id = 2;

    INSERT INTO transactions (from_account_id, to_account_id, amount)
    VALUES (1, 2, 100.00);

COMMIT;

-- With error handling
BEGIN TRANSACTION;
    -- SQL operations
    
    IF @@ERROR <> 0
        ROLLBACK TRANSACTION;
    ELSE
        COMMIT TRANSACTION;
```
