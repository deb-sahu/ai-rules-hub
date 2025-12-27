# SQL Style Guide

This style guide provides concrete examples and best practices for writing clean, efficient, and maintainable SQL code.

## Table of Contents
- [Naming Conventions](#naming-conventions)
- [Query Structure](#query-structure)
- [Joins](#joins)
- [Indexing](#indexing)
- [Performance](#performance)
- [Stored Procedures](#stored-procedures)
- [Security](#security)

## Naming Conventions

### ✅ Good
```sql
-- Tables use singular names with snake_case
CREATE TABLE user (
    user_id INT PRIMARY KEY,
    first_name VARCHAR(50) NOT NULL,
    last_name VARCHAR(50) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

CREATE TABLE order (
    order_id INT PRIMARY KEY,
    user_id INT NOT NULL,
    order_date DATE NOT NULL,
    total_amount DECIMAL(10, 2) NOT NULL,
    status VARCHAR(20) NOT NULL,
    FOREIGN KEY (user_id) REFERENCES user(user_id)
);

CREATE TABLE order_item (
    order_item_id INT PRIMARY KEY,
    order_id INT NOT NULL,
    product_id INT NOT NULL,
    quantity INT NOT NULL,
    unit_price DECIMAL(10, 2) NOT NULL,
    FOREIGN KEY (order_id) REFERENCES order(order_id),
    FOREIGN KEY (product_id) REFERENCES product(product_id)
);

-- Indexes with descriptive names
CREATE INDEX idx_user_email ON user(email);
CREATE INDEX idx_order_user_date ON order(user_id, order_date);
CREATE INDEX idx_order_item_order ON order_item(order_id);
```

### ❌ Bad
```sql
-- Bad: Plural table names, mixed case, unclear naming
CREATE TABLE Users (
    ID INT PRIMARY KEY,
    FName VARCHAR(50),  -- Bad: abbreviation
    LName VARCHAR(50),
    EmailAddress VARCHAR(100)
);

CREATE TABLE Orders (
    OrderID INT,
    UserID INT,
    dt DATE,  -- Bad: unclear abbreviation
    amt DECIMAL(10, 2)
);
```

## Query Structure

### ✅ Good
```sql
-- Clear SELECT with explicit columns
SELECT 
    u.user_id,
    u.first_name,
    u.last_name,
    u.email,
    COUNT(o.order_id) AS order_count,
    SUM(o.total_amount) AS total_spent
FROM 
    user u
    LEFT JOIN order o ON u.user_id = o.user_id
WHERE 
    u.created_at >= '2024-01-01'
    AND u.status = 'active'
GROUP BY 
    u.user_id,
    u.first_name,
    u.last_name,
    u.email
HAVING 
    COUNT(o.order_id) > 0
ORDER BY 
    total_spent DESC,
    u.last_name ASC
LIMIT 100;

-- Complex query with CTEs for readability
WITH active_users AS (
    SELECT 
        user_id,
        first_name,
        last_name,
        email
    FROM 
        user
    WHERE 
        status = 'active'
        AND created_at >= DATE_SUB(CURRENT_DATE, INTERVAL 1 YEAR)
),
user_orders AS (
    SELECT 
        u.user_id,
        COUNT(o.order_id) AS order_count,
        SUM(o.total_amount) AS total_amount
    FROM 
        active_users u
        INNER JOIN order o ON u.user_id = o.user_id
    WHERE 
        o.status = 'completed'
    GROUP BY 
        u.user_id
)
SELECT 
    au.user_id,
    au.first_name,
    au.last_name,
    au.email,
    COALESCE(uo.order_count, 0) AS order_count,
    COALESCE(uo.total_amount, 0) AS total_amount
FROM 
    active_users au
    LEFT JOIN user_orders uo ON au.user_id = uo.user_id
ORDER BY 
    uo.total_amount DESC NULLS LAST;
```

### ❌ Bad
```sql
-- Bad: SELECT *, no formatting, unclear logic
SELECT * FROM user u, order o WHERE u.user_id=o.user_id AND u.status='active' AND o.status='completed';

-- Bad: No table aliases, hard to read
SELECT user.first_name, user.last_name, order.order_id FROM user INNER JOIN order WHERE user.user_id = order.user_id;
```

## Joins

### ✅ Good
```sql
-- INNER JOIN: Get users with orders
SELECT 
    u.user_id,
    u.first_name,
    u.last_name,
    o.order_id,
    o.order_date,
    o.total_amount
FROM 
    user u
    INNER JOIN order o ON u.user_id = o.user_id
WHERE 
    o.status = 'completed';

-- LEFT JOIN: Get all users and their orders (if any)
SELECT 
    u.user_id,
    u.first_name,
    u.last_name,
    COUNT(o.order_id) AS order_count
FROM 
    user u
    LEFT JOIN order o ON u.user_id = o.user_id
GROUP BY 
    u.user_id,
    u.first_name,
    u.last_name;

-- Multiple joins with clear relationships
SELECT 
    o.order_id,
    u.first_name || ' ' || u.last_name AS customer_name,
    p.product_name,
    oi.quantity,
    oi.unit_price,
    oi.quantity * oi.unit_price AS line_total
FROM 
    order o
    INNER JOIN user u ON o.user_id = u.user_id
    INNER JOIN order_item oi ON o.order_id = oi.order_id
    INNER JOIN product p ON oi.product_id = p.product_id
WHERE 
    o.order_date >= '2024-01-01'
ORDER BY 
    o.order_id,
    p.product_name;

-- Self-join example: Employee hierarchy
SELECT 
    e.employee_id,
    e.first_name AS employee_name,
    m.first_name AS manager_name
FROM 
    employee e
    LEFT JOIN employee m ON e.manager_id = m.employee_id;
```

### ❌ Bad
```sql
-- Bad: Implicit join (comma-separated)
SELECT u.first_name, o.order_id
FROM user u, order o
WHERE u.user_id = o.user_id;

-- Bad: Mixing join conditions with filters
SELECT u.first_name, o.order_id
FROM user u
LEFT JOIN order o ON u.user_id = o.user_id AND u.status = 'active';
-- Should use WHERE for filters
```

## Indexing

### ✅ Good
```sql
-- Single column index for frequent lookups
CREATE INDEX idx_user_email ON user(email);

-- Composite index for common query patterns
CREATE INDEX idx_order_user_date ON order(user_id, order_date);

-- Covering index includes all columns needed by a query
CREATE INDEX idx_order_covering ON order(user_id, order_date, total_amount);

-- Partial/filtered index for specific subsets
CREATE INDEX idx_active_user_email ON user(email) WHERE status = 'active';

-- Unique index to enforce uniqueness
CREATE UNIQUE INDEX idx_user_email_unique ON user(email);

-- Full-text index for search
CREATE FULLTEXT INDEX idx_product_search ON product(product_name, description);

-- Check index usage
EXPLAIN SELECT * FROM user WHERE email = 'john@example.com';
```

### ❌ Bad
```sql
-- Bad: Index on low-cardinality column
CREATE INDEX idx_user_status ON user(status);  -- Only a few distinct values

-- Bad: Too many indexes on one table (slows down writes)
CREATE INDEX idx1 ON user(first_name);
CREATE INDEX idx2 ON user(last_name);
CREATE INDEX idx3 ON user(email);
CREATE INDEX idx4 ON user(phone);
CREATE INDEX idx5 ON user(city);
-- Consider composite indexes based on actual query patterns
```

## Performance

### ✅ Good
```sql
-- Use EXISTS instead of COUNT for existence checks
SELECT u.user_id, u.first_name
FROM user u
WHERE EXISTS (
    SELECT 1
    FROM order o
    WHERE o.user_id = u.user_id
    AND o.status = 'completed'
);

-- Avoid functions on indexed columns
-- Good: Date range without function
SELECT * FROM order
WHERE order_date >= '2024-01-01' AND order_date < '2025-01-01';

-- Use UNION ALL when duplicates don't matter
SELECT user_id, 'customer' AS user_type FROM customer
UNION ALL
SELECT user_id, 'vendor' AS user_type FROM vendor;

-- Efficient pagination with LIMIT and OFFSET
SELECT 
    user_id,
    first_name,
    last_name
FROM 
    user
ORDER BY 
    user_id
LIMIT 20 OFFSET 0;

-- Better pagination with keyset (cursor-based)
SELECT 
    user_id,
    first_name,
    last_name
FROM 
    user
WHERE 
    user_id > 100  -- Last seen ID from previous page
ORDER BY 
    user_id
LIMIT 20;

-- Aggregate with proper indexes
SELECT 
    DATE_TRUNC('month', order_date) AS month,
    COUNT(*) AS order_count,
    SUM(total_amount) AS total_revenue
FROM 
    order
WHERE 
    order_date >= '2024-01-01'
GROUP BY 
    DATE_TRUNC('month', order_date)
ORDER BY 
    month;
```

### ❌ Bad
```sql
-- Bad: Using COUNT(*) > 0 for existence check
SELECT u.user_id
FROM user u
WHERE (SELECT COUNT(*) FROM order o WHERE o.user_id = u.user_id) > 0;

-- Bad: Function on indexed column prevents index usage
SELECT * FROM order
WHERE YEAR(order_date) = 2024;

-- Bad: Using UNION when UNION ALL would work
SELECT user_id FROM customer
UNION  -- Removes duplicates unnecessarily
SELECT user_id FROM vendor;

-- Bad: SELECT * in production code
SELECT * FROM user;  -- Returns all columns even if not needed
```

## Stored Procedures

### ✅ Good
```sql
-- Well-structured stored procedure with error handling
DELIMITER //

CREATE PROCEDURE usp_CreateOrder(
    IN p_user_id INT,
    IN p_items JSON,
    OUT p_order_id INT,
    OUT p_error_message VARCHAR(255)
)
BEGIN
    DECLARE v_total_amount DECIMAL(10, 2) DEFAULT 0;
    DECLARE EXIT HANDLER FOR SQLEXCEPTION
    BEGIN
        -- Rollback transaction on error
        ROLLBACK;
        SET p_error_message = 'Error creating order';
        SET p_order_id = NULL;
    END;
    
    -- Input validation
    IF p_user_id IS NULL OR p_user_id <= 0 THEN
        SET p_error_message = 'Invalid user ID';
        SET p_order_id = NULL;
    ELSE
        START TRANSACTION;
        
        -- Calculate total
        SELECT SUM(JSON_UNQUOTE(JSON_EXTRACT(value, '$.price')) * 
                   JSON_UNQUOTE(JSON_EXTRACT(value, '$.quantity')))
        INTO v_total_amount
        FROM JSON_TABLE(p_items, '$[*]' COLUMNS(
            value JSON PATH '$'
        )) AS items;
        
        -- Create order
        INSERT INTO order (user_id, order_date, total_amount, status)
        VALUES (p_user_id, CURRENT_DATE, v_total_amount, 'pending');
        
        SET p_order_id = LAST_INSERT_ID();
        
        -- Insert order items
        INSERT INTO order_item (order_id, product_id, quantity, unit_price)
        SELECT 
            p_order_id,
            JSON_UNQUOTE(JSON_EXTRACT(value, '$.product_id')),
            JSON_UNQUOTE(JSON_EXTRACT(value, '$.quantity')),
            JSON_UNQUOTE(JSON_EXTRACT(value, '$.price'))
        FROM JSON_TABLE(p_items, '$[*]' COLUMNS(
            value JSON PATH '$'
        )) AS items;
        
        COMMIT;
        SET p_error_message = NULL;
    END IF;
END //

DELIMITER ;

-- Using the procedure
CALL usp_CreateOrder(
    1,
    '[{"product_id": 1, "quantity": 2, "price": 29.99}, {"product_id": 2, "quantity": 1, "price": 49.99}]',
    @order_id,
    @error_message
);

SELECT @order_id, @error_message;
```

### ❌ Bad
```sql
-- Bad: No error handling, no validation
CREATE PROCEDURE CreateOrder(user_id INT, product_id INT)
BEGIN
    INSERT INTO order (user_id, product_id) VALUES (user_id, product_id);
END;
```

## Security

### ✅ Good
```sql
-- Use parameterized queries (in application code)
-- Python example:
-- cursor.execute("SELECT * FROM user WHERE email = %s", (email,))

-- Grant minimal permissions
GRANT SELECT, INSERT, UPDATE ON mydb.order TO 'app_user'@'localhost';
GRANT SELECT ON mydb.product TO 'app_user'@'localhost';

-- Revoke unnecessary permissions
REVOKE DELETE ON mydb.* FROM 'app_user'@'localhost';

-- Create read-only user
CREATE USER 'readonly_user'@'localhost' IDENTIFIED BY 'secure_password';
GRANT SELECT ON mydb.* TO 'readonly_user'@'localhost';

-- Encrypt sensitive data
CREATE TABLE user_sensitive (
    user_id INT PRIMARY KEY,
    ssn_encrypted VARBINARY(256),
    FOREIGN KEY (user_id) REFERENCES user(user_id)
);

-- Views to restrict data access
CREATE VIEW vw_public_user AS
SELECT 
    user_id,
    first_name,
    last_name,
    email
FROM 
    user
WHERE 
    status = 'active';

GRANT SELECT ON mydb.vw_public_user TO 'public_user'@'localhost';
```

### ❌ Bad
```sql
-- Bad: Dynamic SQL vulnerable to injection
SET @sql = CONCAT('SELECT * FROM user WHERE email = ''', email, '''');
PREPARE stmt FROM @sql;
EXECUTE stmt;

-- Bad: Granting excessive permissions
GRANT ALL PRIVILEGES ON *.* TO 'app_user'@'%';

-- Bad: Storing sensitive data in plain text
CREATE TABLE user (
    user_id INT PRIMARY KEY,
    password VARCHAR(100),  -- Should be hashed
    credit_card VARCHAR(16)  -- Should be encrypted
);
```

## Transactions

### ✅ Good
```sql
-- Proper transaction handling
START TRANSACTION;

UPDATE account SET balance = balance - 100 WHERE account_id = 1;
UPDATE account SET balance = balance + 100 WHERE account_id = 2;

-- Check if both updates succeeded
IF (SELECT balance FROM account WHERE account_id = 1) >= 0 THEN
    COMMIT;
ELSE
    ROLLBACK;
END IF;

-- Using savepoints
START TRANSACTION;

INSERT INTO order (user_id, order_date) VALUES (1, CURRENT_DATE);
SAVEPOINT order_created;

INSERT INTO order_item (order_id, product_id) VALUES (LAST_INSERT_ID(), 1);
-- If this fails, can rollback to savepoint
SAVEPOINT items_added;

UPDATE inventory SET quantity = quantity - 1 WHERE product_id = 1;

COMMIT;
```

## Views

### ✅ Good
```sql
-- Materialized view for expensive queries
CREATE MATERIALIZED VIEW mv_user_order_summary AS
SELECT 
    u.user_id,
    u.first_name,
    u.last_name,
    COUNT(o.order_id) AS order_count,
    SUM(o.total_amount) AS lifetime_value,
    MAX(o.order_date) AS last_order_date
FROM 
    user u
    LEFT JOIN order o ON u.user_id = o.user_id
GROUP BY 
    u.user_id,
    u.first_name,
    u.last_name;

-- Refresh materialized view
REFRESH MATERIALIZED VIEW mv_user_order_summary;

-- Regular view for data abstraction
CREATE VIEW vw_order_details AS
SELECT 
    o.order_id,
    o.order_date,
    u.first_name || ' ' || u.last_name AS customer_name,
    u.email,
    o.total_amount,
    o.status
FROM 
    order o
    INNER JOIN user u ON o.user_id = u.user_id;

-- Query the view
SELECT * FROM vw_order_details WHERE status = 'completed';
```

## Summary

- Use lowercase snake_case for table and column names
- Always use explicit column names instead of SELECT *
- Use table aliases for clarity in joins
- Place JOIN conditions in ON clause, filters in WHERE clause
- Create indexes based on actual query patterns
- Use parameterized queries to prevent SQL injection
- Implement proper transaction handling with error recovery
- Grant minimal necessary permissions
- Document complex queries and business logic
- Avoid functions on indexed columns in WHERE clauses
- Use CTEs for complex queries to improve readability
