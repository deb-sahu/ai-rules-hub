# Python Style Guide

This style guide provides concrete examples and best practices for writing clean, Pythonic code.

## Table of Contents
- [Naming Conventions](#naming-conventions)
- [Type Hints](#type-hints)
- [Functions](#functions)
- [Classes](#classes)
- [Error Handling](#error-handling)
- [Data Structures](#data-structures)
- [Async Programming](#async-programming)
- [Testing](#testing)

## Naming Conventions

### ✅ Good
```python
# Variables and functions use snake_case
user_name = "John Doe"
user_age = 30

def get_user_data(user_id: int) -> dict:
    """Fetch user data from database."""
    return {"id": user_id, "name": user_name}

def calculate_total_price(items: list, discount: float = 0.0) -> float:
    """Calculate total price with optional discount."""
    subtotal = sum(item['price'] for item in items)
    return subtotal * (1 - discount)

# Classes use PascalCase
class UserProfile:
    """Represents a user profile."""
    
    def __init__(self, user_id: int, name: str):
        self.user_id = user_id
        self.name = name
        self._email = None  # Private attribute
    
    def get_full_name(self) -> str:
        """Return the user's full name."""
        return self.name

# Constants use UPPER_SNAKE_CASE
MAX_CONNECTIONS = 100
API_BASE_URL = "https://api.example.com"
DEFAULT_TIMEOUT = 30

# Private methods with single underscore
class DataProcessor:
    def process_data(self, data: list) -> list:
        """Public method to process data."""
        cleaned = self._clean_data(data)
        return self._transform_data(cleaned)
    
    def _clean_data(self, data: list) -> list:
        """Private method to clean data."""
        return [item for item in data if item is not None]
    
    def _transform_data(self, data: list) -> list:
        """Private method to transform data."""
        return [item.upper() for item in data]
```

### ❌ Bad
```python
# Bad naming conventions
userName = "John"  # Should be snake_case
UserAge = 30  # Should be snake_case
MAX_retry_count = 3  # Should be all caps

def GetUserData(UserID):  # Should be snake_case
    return {}

class userProfile:  # Should be PascalCase
    pass
```

## Type Hints

### ✅ Good
```python
from typing import List, Dict, Optional, Union, Tuple, Any, Callable
from dataclasses import dataclass

# Basic type hints
def greet(name: str) -> str:
    return f"Hello, {name}!"

def add_numbers(a: int, b: int) -> int:
    return a + b

# Optional types
def find_user(user_id: int) -> Optional[dict]:
    """Return user dict or None if not found."""
    users = get_all_users()
    return next((u for u in users if u['id'] == user_id), None)

# Collection types
def process_items(items: List[str]) -> Dict[str, int]:
    """Count occurrences of each item."""
    return {item: items.count(item) for item in set(items)}

def get_user_info(user_id: int) -> Tuple[str, int, str]:
    """Return name, age, and email."""
    return ("John Doe", 30, "john@example.com")

# Union types
def process_input(value: Union[str, int, float]) -> str:
    """Process different input types."""
    return str(value)

# Modern union syntax (Python 3.10+)
def find_item(item_id: int) -> dict | None:
    """Return item or None."""
    return None

# Callable types
def execute_callback(callback: Callable[[int, str], bool]) -> bool:
    """Execute a callback function."""
    return callback(1, "test")

# Generic types
from typing import TypeVar, Generic

T = TypeVar('T')

def get_first_element(items: List[T]) -> T | None:
    """Return first element or None."""
    return items[0] if items else None

# Class with type hints
@dataclass
class User:
    """User data class with type hints."""
    user_id: int
    name: str
    email: str
    age: Optional[int] = None
    is_active: bool = True
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            'user_id': self.user_id,
            'name': self.name,
            'email': self.email,
            'age': self.age,
            'is_active': self.is_active
        }
```

### ❌ Bad
```python
# Missing type hints
def process_data(data):  # No type hints
    return data

def get_user(user_id):  # No type hints
    return {"id": user_id}
```

## Functions

### ✅ Good
```python
# Clean function with docstring
def calculate_discount(price: float, discount_percent: float) -> float:
    """
    Calculate discounted price.
    
    Args:
        price: Original price
        discount_percent: Discount percentage (0-100)
    
    Returns:
        Discounted price
    
    Raises:
        ValueError: If discount_percent is not between 0 and 100
    """
    if not 0 <= discount_percent <= 100:
        raise ValueError("Discount must be between 0 and 100")
    
    return price * (1 - discount_percent / 100)

# Using default arguments
def fetch_users(limit: int = 10, offset: int = 0) -> List[dict]:
    """Fetch users with pagination."""
    return []

# Using *args and **kwargs
def log_message(level: str, *args: Any, **kwargs: Any) -> None:
    """Log a message with arbitrary arguments."""
    message = ' '.join(str(arg) for arg in args)
    metadata = ', '.join(f'{k}={v}' for k, v in kwargs.items())
    print(f"[{level}] {message} ({metadata})")

# Example usage
log_message("INFO", "User logged in", user_id=123, ip="192.168.1.1")

# List comprehensions
numbers = [1, 2, 3, 4, 5]
squared = [x**2 for x in numbers]
evens = [x for x in numbers if x % 2 == 0]

# Dictionary comprehensions
items = [('a', 1), ('b', 2), ('c', 3)]
item_dict = {key: value for key, value in items}

# Generator expressions for memory efficiency
def read_large_file(file_path: str):
    """Read large file line by line."""
    with open(file_path, 'r') as f:
        for line in f:
            yield line.strip()

# Using enumerate
names = ['Alice', 'Bob', 'Charlie']
for index, name in enumerate(names):
    print(f"{index}: {name}")

# Using zip
first_names = ['John', 'Jane', 'Bob']
last_names = ['Doe', 'Smith', 'Johnson']
for first, last in zip(first_names, last_names):
    print(f"{first} {last}")
```

### ❌ Bad
```python
# Bad: No docstring, unclear purpose
def calc(x, y):
    return x * y * 0.9

# Bad: Too complex, should be broken down
def process_everything(data):
    # 50 lines of complex logic
    pass

# Bad: Using loops instead of comprehensions
squared = []
for x in numbers:
    squared.append(x**2)
```

## Classes

### ✅ Good
```python
from dataclasses import dataclass
from typing import ClassVar
from abc import ABC, abstractmethod

# Using dataclass for simple data containers
@dataclass
class Point:
    """Represents a 2D point."""
    x: float
    y: float
    
    def distance_from_origin(self) -> float:
        """Calculate distance from origin."""
        return (self.x**2 + self.y**2)**0.5

# Regular class with proper structure
class UserService:
    """Service for managing users."""
    
    # Class variable
    MAX_RETRY_ATTEMPTS: ClassVar[int] = 3
    
    def __init__(self, database_url: str):
        """Initialize the service."""
        self.database_url = database_url
        self._connection = None
    
    def __enter__(self):
        """Context manager entry."""
        self._connection = self._connect()
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit."""
        if self._connection:
            self._connection.close()
    
    def _connect(self):
        """Private method to establish connection."""
        # Connection logic
        pass
    
    def get_user(self, user_id: int) -> Optional[dict]:
        """Public method to get user."""
        # Implementation
        return None
    
    def __repr__(self) -> str:
        """String representation."""
        return f"UserService(database_url='{self.database_url}')"

# Abstract base class
class Repository(ABC):
    """Abstract repository interface."""
    
    @abstractmethod
    def get_by_id(self, item_id: int) -> Optional[dict]:
        """Get item by ID."""
        pass
    
    @abstractmethod
    def save(self, item: dict) -> int:
        """Save item and return ID."""
        pass

# Concrete implementation
class UserRepository(Repository):
    """Concrete user repository."""
    
    def __init__(self, db_connection):
        self.db = db_connection
    
    def get_by_id(self, item_id: int) -> Optional[dict]:
        """Get user by ID."""
        # Implementation
        return None
    
    def save(self, item: dict) -> int:
        """Save user."""
        # Implementation
        return 0

# Property decorator
class Temperature:
    """Temperature with unit conversion."""
    
    def __init__(self, celsius: float):
        self._celsius = celsius
    
    @property
    def celsius(self) -> float:
        """Get temperature in Celsius."""
        return self._celsius
    
    @celsius.setter
    def celsius(self, value: float) -> None:
        """Set temperature in Celsius."""
        self._celsius = value
    
    @property
    def fahrenheit(self) -> float:
        """Get temperature in Fahrenheit."""
        return self._celsius * 9/5 + 32
```

### ❌ Bad
```python
# Bad: Not using dataclass for simple data
class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        
# Bad: Public attributes that should be private
class User:
    def __init__(self, password):
        self.password = password  # Should be private
```

## Error Handling

### ✅ Good
```python
# Custom exceptions
class ValidationError(Exception):
    """Raised when validation fails."""
    pass

class UserNotFoundError(Exception):
    """Raised when user is not found."""
    
    def __init__(self, user_id: int):
        self.user_id = user_id
        super().__init__(f"User with ID {user_id} not found")

# Proper exception handling
def get_user(user_id: int) -> dict:
    """
    Get user by ID.
    
    Raises:
        ValueError: If user_id is invalid
        UserNotFoundError: If user doesn't exist
        ConnectionError: If database connection fails
    """
    if user_id <= 0:
        raise ValueError("User ID must be positive")
    
    try:
        user = fetch_from_database(user_id)
        if user is None:
            raise UserNotFoundError(user_id)
        return user
    except ConnectionError as e:
        logger.error(f"Database connection failed: {e}")
        raise
    except Exception as e:
        logger.exception(f"Unexpected error fetching user {user_id}")
        raise

# Context manager for resource management
from contextlib import contextmanager

@contextmanager
def database_connection(connection_string: str):
    """Context manager for database connections."""
    connection = connect(connection_string)
    try:
        yield connection
    except Exception as e:
        connection.rollback()
        logger.error(f"Transaction failed: {e}")
        raise
    else:
        connection.commit()
    finally:
        connection.close()

# Usage
with database_connection("postgresql://localhost/mydb") as conn:
    result = conn.execute("SELECT * FROM users")

# Multiple exception types
def process_file(file_path: str) -> str:
    """Process a file with proper error handling."""
    try:
        with open(file_path, 'r') as f:
            content = f.read()
        return content.upper()
    except FileNotFoundError:
        logger.error(f"File not found: {file_path}")
        return ""
    except PermissionError:
        logger.error(f"Permission denied: {file_path}")
        return ""
    except Exception as e:
        logger.exception(f"Unexpected error processing {file_path}")
        raise
```

### ❌ Bad
```python
# Bad: Bare except
try:
    risky_operation()
except:  # Never do this
    pass

# Bad: Catching Exception without re-raising
try:
    important_operation()
except Exception:
    print("Something went wrong")
    # Lost the exception!

# Bad: Using exceptions for flow control
try:
    value = my_dict['key']
except KeyError:
    value = None
# Better: value = my_dict.get('key')
```

## Data Structures

### ✅ Good
```python
from dataclasses import dataclass, field
from typing import NamedTuple
from enum import Enum, auto
from collections import defaultdict, Counter, deque

# Using dataclasses
@dataclass
class User:
    """User data with default values."""
    user_id: int
    name: str
    email: str
    tags: List[str] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)

# Using NamedTuple for immutable data
class Point(NamedTuple):
    """Immutable 2D point."""
    x: float
    y: float

# Using Enum for constants
class Status(Enum):
    """Order status enum."""
    PENDING = auto()
    PROCESSING = auto()
    COMPLETED = auto()
    CANCELLED = auto()

# Using collections
# defaultdict for grouping
users_by_city = defaultdict(list)
for user in users:
    users_by_city[user['city']].append(user)

# Counter for counting
words = ['apple', 'banana', 'apple', 'cherry', 'banana', 'apple']
word_counts = Counter(words)
most_common = word_counts.most_common(2)  # [('apple', 3), ('banana', 2)]

# deque for efficient append/pop from both ends
queue = deque([1, 2, 3])
queue.append(4)  # Right side
queue.appendleft(0)  # Left side
queue.pop()  # Right side
queue.popleft()  # Left side

# Set operations
set1 = {1, 2, 3, 4}
set2 = {3, 4, 5, 6}
intersection = set1 & set2  # {3, 4}
union = set1 | set2  # {1, 2, 3, 4, 5, 6}
difference = set1 - set2  # {1, 2}
```

## Async Programming

### ✅ Good
```python
import asyncio
import aiohttp
from typing import List

# Async function
async def fetch_user(user_id: int) -> dict:
    """Fetch user data asynchronously."""
    async with aiohttp.ClientSession() as session:
        async with session.get(f'https://api.example.com/users/{user_id}') as response:
            return await response.json()

# Parallel async operations
async def fetch_all_users(user_ids: List[int]) -> List[dict]:
    """Fetch multiple users concurrently."""
    tasks = [fetch_user(user_id) for user_id in user_ids]
    return await asyncio.gather(*tasks)

# Async context manager
class AsyncDatabaseConnection:
    """Async database connection."""
    
    async def __aenter__(self):
        """Async enter."""
        self.connection = await connect_async()
        return self.connection
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Async exit."""
        await self.connection.close()

# Usage
async def query_database():
    """Query database asynchronously."""
    async with AsyncDatabaseConnection() as conn:
        result = await conn.execute("SELECT * FROM users")
        return result

# Async generator
async def fetch_paginated_data(page_size: int = 100):
    """Fetch data in pages asynchronously."""
    page = 1
    while True:
        data = await fetch_page(page, page_size)
        if not data:
            break
        for item in data:
            yield item
        page += 1

# Usage
async def process_all_data():
    """Process all paginated data."""
    async for item in fetch_paginated_data():
        await process_item(item)

# Running async code
if __name__ == "__main__":
    # Python 3.7+
    asyncio.run(fetch_all_users([1, 2, 3]))
```

## Testing

### ✅ Good
```python
import pytest
from unittest.mock import Mock, patch, MagicMock
from typing import Generator

# Test fixtures
@pytest.fixture
def user() -> dict:
    """Create a test user."""
    return {
        'user_id': 1,
        'name': 'John Doe',
        'email': 'john@example.com'
    }

@pytest.fixture
def user_service() -> Generator:
    """Create a user service for testing."""
    service = UserService('test_db')
    yield service
    # Cleanup
    service.close()

# Basic test
def test_calculate_discount():
    """Test discount calculation."""
    result = calculate_discount(100, 10)
    assert result == 90

# Parametrized tests
@pytest.mark.parametrize("price,discount,expected", [
    (100, 10, 90),
    (200, 20, 160),
    (50, 0, 50),
])
def test_calculate_discount_parametrized(price, discount, expected):
    """Test discount calculation with multiple inputs."""
    assert calculate_discount(price, discount) == expected

# Testing exceptions
def test_invalid_discount():
    """Test that invalid discount raises error."""
    with pytest.raises(ValueError, match="Discount must be between"):
        calculate_discount(100, 150)

# Using mocks
def test_fetch_user_with_mock():
    """Test fetching user with mocked API."""
    with patch('myapp.api.requests.get') as mock_get:
        mock_response = Mock()
        mock_response.json.return_value = {'user_id': 1, 'name': 'John'}
        mock_get.return_value = mock_response
        
        result = fetch_user(1)
        
        assert result['name'] == 'John'
        mock_get.assert_called_once_with('https://api.example.com/users/1')

# Testing async functions
@pytest.mark.asyncio
async def test_fetch_user_async():
    """Test async user fetch."""
    user = await fetch_user(1)
    assert user['user_id'] == 1

# Using fixtures
def test_user_service(user_service, user):
    """Test user service with fixtures."""
    result = user_service.save(user)
    assert result > 0

# Testing with fixtures and cleanup
@pytest.fixture
def temp_file(tmp_path):
    """Create a temporary file for testing."""
    file_path = tmp_path / "test_file.txt"
    file_path.write_text("test content")
    yield file_path
    # Cleanup happens automatically with tmp_path

def test_read_file(temp_file):
    """Test reading from file."""
    content = temp_file.read_text()
    assert content == "test content"
```

### ❌ Bad
```python
# Bad: No assertion
def test_something():
    result = calculate(5)
    # Forgot assertion!

# Bad: Testing implementation details
def test_internal_method():
    obj = MyClass()
    obj._private_method()  # Don't test private methods
```

## Context Managers and File I/O

### ✅ Good
```python
from pathlib import Path

# Using context manager
with open('file.txt', 'r') as f:
    content = f.read()

# Using pathlib
file_path = Path('data') / 'users.json'
if file_path.exists():
    content = file_path.read_text()

# Writing files
data = {'key': 'value'}
file_path.write_text(json.dumps(data, indent=2))

# Multiple context managers
with open('input.txt', 'r') as infile, open('output.txt', 'w') as outfile:
    for line in infile:
        outfile.write(line.upper())
```

## Summary

- Use snake_case for variables and functions, PascalCase for classes
- Always use type hints for function parameters and returns
- Write comprehensive docstrings
- Use dataclasses for simple data containers
- Handle exceptions specifically, avoid bare except
- Use context managers for resource management
- Prefer comprehensions over loops
- Use async/await for I/O-bound operations
- Write thorough tests with pytest
- Follow PEP 8 style guidelines
