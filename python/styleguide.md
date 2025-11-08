# Python Style Guide

## Table of Contents
- [Naming Conventions](#naming-conventions)
- [Code Organization](#code-organization)
- [Type Hints](#type-hints)
- [Functions and Classes](#functions-and-classes)
- [Error Handling](#error-handling)
- [Testing](#testing)

## Naming Conventions

✅ **Good:**
```python
# Modules - lowercase with underscores
# user_service.py, data_utils.py

# Classes - PascalCase
class UserService:
    pass

class DataProcessor:
    pass

# Functions and variables - lowercase with underscores
def get_user_by_id(user_id: int) -> User:
    pass

user_name = "John Doe"
total_count = 100

# Constants - uppercase with underscores
MAX_RETRIES = 3
API_ENDPOINT = "https://api.example.com"
DEFAULT_TIMEOUT = 30

# Private attributes - leading underscore
class User:
    def __init__(self, name: str):
        self._name = name  # Private attribute
    
    def _internal_method(self):  # Private method
        pass
```

❌ **Bad:**
```python
# Bad naming
class user_service:  # Should be PascalCase
    pass

def GetUserById(userId):  # Should be snake_case
    pass

maxRetries = 3  # Constants should be UPPER_CASE
```

## Code Organization

### Import Organization

✅ **Good:**
```python
"""Module docstring describing the module."""

# Standard library imports
import os
import sys
from datetime import datetime
from typing import List, Optional, Dict

# Third-party imports
import requests
from flask import Flask, request
from sqlalchemy import create_engine

# Local application imports
from myapp.models import User
from myapp.utils import validate_email
from myapp.services.user_service import UserService
```

### Module Structure

✅ **Good:**
```python
"""User service module for managing user operations."""

from typing import Optional, List
import logging

# Constants
MAX_LOGIN_ATTEMPTS = 3
SESSION_TIMEOUT = 3600

# Configure logging
logger = logging.getLogger(__name__)

# Exception classes
class UserNotFoundError(Exception):
    """Raised when a user is not found."""
    pass

# Main classes
class UserService:
    """Service for managing user operations."""
    
    def __init__(self, database_url: str):
        self.database_url = database_url
        self._connection = None
    
    def get_user(self, user_id: int) -> Optional[User]:
        """Retrieve a user by ID."""
        pass

# Utility functions
def validate_email(email: str) -> bool:
    """Validate email format."""
    pass

# Main execution
if __name__ == "__main__":
    service = UserService("postgresql://localhost/mydb")
    user = service.get_user(1)
    print(user)
```

## Type Hints

✅ **Good:**
```python
from typing import List, Dict, Optional, Union, Tuple, Any, TypedDict

# Basic type hints
def greet(name: str) -> str:
    return f"Hello, {name}!"

def calculate_total(prices: List[float]) -> float:
    return sum(prices)

# Optional types
def find_user(user_id: int) -> Optional[User]:
    """Returns User or None if not found."""
    pass

# Union types
def process_data(data: Union[str, int, float]) -> str:
    return str(data)

# Dictionary types
def get_user_data(user_id: int) -> Dict[str, Any]:
    return {"id": user_id, "name": "John"}

# Tuple types
def get_coordinates() -> Tuple[float, float]:
    return (40.7128, -74.0060)

# TypedDict for structured dictionaries
class UserData(TypedDict):
    id: int
    name: str
    email: str
    is_active: bool

def create_user_data() -> UserData:
    return {
        "id": 1,
        "name": "John Doe",
        "email": "john@example.com",
        "is_active": True
    }

# Generic types
from typing import TypeVar, Generic

T = TypeVar('T')

class Repository(Generic[T]):
    def get_by_id(self, id: int) -> Optional[T]:
        pass
    
    def get_all(self) -> List[T]:
        pass
```

## Functions and Classes

### Function Design

✅ **Good:**
```python
def calculate_discount(
    price: float,
    discount_percent: float = 0.0,
    min_price: float = 0.0
) -> float:
    """
    Calculate the discounted price.
    
    Args:
        price: Original price of the item
        discount_percent: Discount percentage (0-100)
        min_price: Minimum price after discount
    
    Returns:
        Discounted price
    
    Raises:
        ValueError: If price is negative or discount is invalid
    
    Examples:
        >>> calculate_discount(100, 10)
        90.0
        >>> calculate_discount(50, 20, min_price=45)
        45.0
    """
    if price < 0:
        raise ValueError("Price cannot be negative")
    
    if not 0 <= discount_percent <= 100:
        raise ValueError("Discount must be between 0 and 100")
    
    discounted_price = price * (1 - discount_percent / 100)
    return max(discounted_price, min_price)

# Using *args and **kwargs
def log_message(level: str, *messages: str, **context: Any) -> None:
    """Log a message with optional context."""
    combined_message = " ".join(messages)
    print(f"[{level}] {combined_message}")
    if context:
        print(f"Context: {context}")

# Keyword-only arguments
def create_user(
    name: str,
    email: str,
    *,  # Everything after this must be keyword-only
    age: Optional[int] = None,
    is_active: bool = True
) -> User:
    """Create a new user."""
    pass
```

### Class Design

✅ **Good:**
```python
from dataclasses import dataclass
from abc import ABC, abstractmethod

# Using dataclasses for data containers
@dataclass
class User:
    """User data model."""
    id: int
    name: str
    email: str
    is_active: bool = True
    
    def __post_init__(self):
        """Validate data after initialization."""
        if not self.email:
            raise ValueError("Email is required")

# Abstract base class
class Repository(ABC):
    """Abstract repository interface."""
    
    @abstractmethod
    def get_by_id(self, id: int) -> Optional[Any]:
        """Retrieve entity by ID."""
        pass
    
    @abstractmethod
    def save(self, entity: Any) -> None:
        """Save entity."""
        pass

# Concrete implementation
class UserRepository(Repository):
    """User repository implementation."""
    
    def __init__(self, database_url: str):
        self._database_url = database_url
        self._connection = None
    
    def get_by_id(self, id: int) -> Optional[User]:
        """Retrieve user by ID."""
        # Implementation
        pass
    
    def save(self, user: User) -> None:
        """Save user."""
        # Implementation
        pass
    
    def __enter__(self):
        """Context manager entry."""
        self._connection = self._connect()
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit."""
        if self._connection:
            self._connection.close()
```

### Pythonic Patterns

✅ **Good:**
```python
# List comprehensions
squares = [x**2 for x in range(10)]
evens = [x for x in range(20) if x % 2 == 0]

# Dictionary comprehensions
user_ages = {user.name: user.age for user in users}

# Set comprehensions
unique_names = {user.name for user in users}

# Generator expressions for memory efficiency
total = sum(x**2 for x in range(1000000))

# enumerate instead of range(len())
for index, item in enumerate(items):
    print(f"{index}: {item}")

# zip for parallel iteration
names = ["Alice", "Bob", "Charlie"]
ages = [25, 30, 35]
for name, age in zip(names, ages):
    print(f"{name} is {age} years old")

# Dictionary methods
user_data = {"name": "John", "age": 30}
name = user_data.get("name", "Unknown")  # Use get with default
email = user_data.get("email")  # Returns None if not found

# Context managers
with open("file.txt", "r") as f:
    content = f.read()

# Multiple context managers
with open("input.txt", "r") as infile, open("output.txt", "w") as outfile:
    content = infile.read()
    outfile.write(content.upper())

# F-strings for formatting
name = "John"
age = 30
message = f"My name is {name} and I am {age} years old"
```

## Error Handling

✅ **Good:**
```python
# Custom exceptions
class ValidationError(Exception):
    """Raised when validation fails."""
    pass

class UserNotFoundError(Exception):
    """Raised when a user is not found."""
    def __init__(self, user_id: int):
        self.user_id = user_id
        super().__init__(f"User with ID {user_id} not found")

# Proper exception handling
def get_user(user_id: int) -> User:
    """Get user by ID."""
    try:
        if user_id <= 0:
            raise ValidationError("User ID must be positive")
        
        user = database.query(User).filter_by(id=user_id).first()
        
        if not user:
            raise UserNotFoundError(user_id)
        
        return user
    
    except ValidationError as e:
        logger.error(f"Validation error: {e}")
        raise
    
    except UserNotFoundError as e:
        logger.warning(f"User not found: {e.user_id}")
        raise
    
    except Exception as e:
        logger.exception(f"Unexpected error getting user {user_id}")
        raise RuntimeError("Failed to retrieve user") from e
    
    finally:
        # Cleanup code
        database.close()

# Context manager for exception handling
from contextlib import contextmanager

@contextmanager
def database_transaction():
    """Database transaction context manager."""
    try:
        begin_transaction()
        yield
        commit_transaction()
    except Exception:
        rollback_transaction()
        raise
```

## Async Programming

✅ **Good:**
```python
import asyncio
import aiohttp
from typing import List

async def fetch_user(session: aiohttp.ClientSession, user_id: int) -> dict:
    """Fetch user data asynchronously."""
    url = f"https://api.example.com/users/{user_id}"
    async with session.get(url) as response:
        return await response.json()

async def fetch_multiple_users(user_ids: List[int]) -> List[dict]:
    """Fetch multiple users concurrently."""
    async with aiohttp.ClientSession() as session:
        tasks = [fetch_user(session, user_id) for user_id in user_ids]
        return await asyncio.gather(*tasks)

# Run async function
async def main():
    user_ids = [1, 2, 3, 4, 5]
    users = await fetch_multiple_users(user_ids)
    print(f"Fetched {len(users)} users")

if __name__ == "__main__":
    asyncio.run(main())
```

## Testing

✅ **Good:**
```python
import pytest
from unittest.mock import Mock, patch, MagicMock

# Test class organization
class TestUserService:
    """Tests for UserService."""
    
    @pytest.fixture
    def user_service(self):
        """Create UserService instance for testing."""
        return UserService(database_url="sqlite:///:memory:")
    
    @pytest.fixture
    def sample_user(self):
        """Create sample user for testing."""
        return User(id=1, name="Test User", email="test@example.com")
    
    def test_get_user_success(self, user_service, sample_user):
        """Test getting user successfully."""
        # Arrange
        user_id = 1
        
        # Act
        user = user_service.get_user(user_id)
        
        # Assert
        assert user is not None
        assert user.id == user_id
        assert user.name == "Test User"
    
    def test_get_user_not_found(self, user_service):
        """Test getting non-existent user."""
        # Arrange
        user_id = 999
        
        # Act & Assert
        with pytest.raises(UserNotFoundError) as exc_info:
            user_service.get_user(user_id)
        
        assert exc_info.value.user_id == user_id
    
    @pytest.mark.parametrize("user_id,expected", [
        (1, "John"),
        (2, "Jane"),
        (3, "Bob"),
    ])
    def test_get_user_name(self, user_service, user_id, expected):
        """Test getting user name for multiple users."""
        user = user_service.get_user(user_id)
        assert user.name == expected
    
    @patch('myapp.services.database')
    def test_get_user_with_mock(self, mock_database, user_service, sample_user):
        """Test getting user with mocked database."""
        # Arrange
        mock_database.query.return_value.filter_by.return_value.first.return_value = sample_user
        
        # Act
        user = user_service.get_user(1)
        
        # Assert
        assert user == sample_user
        mock_database.query.assert_called_once()

# Async test
@pytest.mark.asyncio
async def test_fetch_user_async():
    """Test async user fetching."""
    user_id = 1
    user = await fetch_user_async(user_id)
    assert user["id"] == user_id
```

## Documentation

✅ **Good:**
```python
def calculate_statistics(data: List[float]) -> Dict[str, float]:
    """
    Calculate statistical measures for a dataset.
    
    This function computes mean, median, and standard deviation
    for the provided numerical data.
    
    Args:
        data: List of numerical values to analyze.
              Must contain at least one value.
    
    Returns:
        Dictionary containing:
            - mean: Arithmetic mean of the data
            - median: Middle value of sorted data
            - std_dev: Standard deviation
    
    Raises:
        ValueError: If data is empty or contains non-numeric values
    
    Examples:
        >>> calculate_statistics([1, 2, 3, 4, 5])
        {'mean': 3.0, 'median': 3.0, 'std_dev': 1.414}
        
        >>> calculate_statistics([10, 20, 30])
        {'mean': 20.0, 'median': 20.0, 'std_dev': 8.165}
    
    Note:
        For datasets with even number of elements, median is
        calculated as the average of the two middle values.
    """
    if not data:
        raise ValueError("Data cannot be empty")
    
    # Implementation
    pass
```
