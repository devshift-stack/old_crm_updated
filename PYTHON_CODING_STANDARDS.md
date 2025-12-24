# Python Coding Standards - Flask CRM Application

## 📋 Inhaltsverzeichnis

1. [Code Style & Formatting](#code-style--formatting)
2. [Type Hints & Type Safety](#type-hints--type-safety)
3. [Error Handling mit Monads](#error-handling-mit-monads)
4. [Validation & Business Rules](#validation--business-rules)
5. [Database Operations](#database-operations)
6. [API Endpoints](#api-endpoints)
7. [Testing Standards](#testing-standards)
8. [Security Best Practices](#security-best-practices)
9. [Documentation](#documentation)
10. [Project Structure](#project-structure)

---

## Code Style & Formatting

### PEP 8 Compliance

**ALLE** Python-Code muss PEP 8 konform sein:

```python
# ✅ RICHTIG
def calculate_customer_score(
    customer: Customer,
    weight_interactions: float = 0.6,
    weight_recency: float = 0.4
) -> float:
    """Calculate customer engagement score."""
    pass

# ❌ FALSCH
def calculateCustomerScore(customer,weight_interactions=0.6,weight_recency=0.4):
    pass
```

### Naming Conventions

```python
# ✅ Module names: lowercase_with_underscores
# customer_service.py, email_validator.py

# ✅ Class names: PascalCase
class CustomerService:
    pass

class EmailValidator:
    pass

# ✅ Function/Variable names: snake_case
def get_customer_by_id(customer_id: int) -> Optional[Customer]:
    pass

user_name = "John"
is_active = True

# ✅ Constants: SCREAMING_SNAKE_CASE
MAX_RETRIES = 3
DEFAULT_PAGE_SIZE = 10
API_VERSION = "v1"

# ✅ Private attributes: _leading_underscore
class Customer:
    def __init__(self):
        self._internal_state = {}

    def _private_method(self):
        pass

# ❌ FALSCH
class customerService:  # Should be PascalCase
    pass

def GetCustomer():  # Should be snake_case
    pass

maxRetries = 3  # Should be SCREAMING_SNAKE_CASE
```

### Import Organization

```python
# ✅ RICHTIG - Importe in 3 Gruppen, alphabetisch sortiert

# 1. Standard library imports
import os
import sys
from datetime import datetime, timezone
from typing import Dict, List, Optional

# 2. Third-party imports
from flask import Flask, request, jsonify
from sqlalchemy import Column, Integer, String
from wtforms import StringField, validators

# 3. Local application imports
from config import Config
from models import Customer, Interaction
from utils.monads import Result, Ok, Err
from utils.validators import validate_customer_data

# ❌ FALSCH - Durcheinander, nicht sortiert
from models import Customer
import os
from utils.monads import Result
from flask import Flask
import sys
```

---

## Type Hints & Type Safety

### Type Hints sind PFLICHT

**IMMER** Type Hints verwenden für:
- Function arguments
- Return types
- Class attributes
- Module-level variables

```python
# ✅ RICHTIG
from typing import List, Optional, Dict, Any

def get_customers(
    status: Optional[str] = None,
    limit: int = 10
) -> List[Customer]:
    """Get customers filtered by status."""
    query = Customer.query
    if status:
        query = query.filter_by(status=status)
    return query.limit(limit).all()

def create_customer(data: Dict[str, Any]) -> Result[Customer, List[ValidationError]]:
    """Create customer with validation."""
    # Implementation
    pass

# Class attributes
class CustomerService:
    cache: Dict[int, Customer]
    max_cache_size: int = 1000

    def __init__(self) -> None:
        self.cache = {}

# ❌ FALSCH - Keine Type Hints
def get_customers(status=None, limit=10):
    pass

def create_customer(data):
    pass
```

### Using typing Module

```python
from typing import (
    List,
    Dict,
    Optional,
    Union,
    Tuple,
    Callable,
    TypeVar,
    Generic
)

# Generic types
T = TypeVar('T')

def first_or_none(items: List[T]) -> Optional[T]:
    """Get first item or None."""
    return items[0] if items else None

# Union types
def parse_id(value: Union[int, str]) -> int:
    """Parse ID from int or string."""
    if isinstance(value, int):
        return value
    return int(value)

# Callable types
def retry(
    func: Callable[[], T],
    max_attempts: int = 3
) -> T:
    """Retry function until success."""
    pass

# Dict with specific types
customer_stats: Dict[str, int] = {
    'total': 100,
    'active': 80,
    'leads': 20
}
```

---

## Error Handling mit Monads

### Result Monad Pattern (PREFERRED)

**VERWENDE** Result Monad für Operationen die fehlschlagen können:

```python
from utils.monads import Result, Ok, Err

# ✅ RICHTIG - Result Monad
def create_customer(data: Dict[str, Any]) -> Result[Customer, str]:
    """
    Create customer with validation.

    Returns:
        Ok(customer) if successful
        Err(error_message) if validation fails
    """
    # Validate data
    validation_result = validate_customer_data(data)
    if validation_result.is_err():
        errors = validation_result.unwrap_err()
        error_msg = '; '.join([e.message for e in errors])
        return Err(error_msg)

    # Check email uniqueness
    existing = Customer.query.filter_by(email=data['email']).first()
    if existing:
        return Err(f"Customer with email {data['email']} already exists")

    # Create customer
    try:
        customer = Customer(**validation_result.unwrap())
        db.session.add(customer)
        db.session.commit()
        return Ok(customer)
    except Exception as e:
        db.session.rollback()
        return Err(f"Database error: {str(e)}")

# Usage in route
@app.route('/api/customers', methods=['POST'])
def api_create_customer():
    data = request.get_json()
    result = create_customer(data)

    if result.is_ok():
        customer = result.unwrap()
        return jsonify(customer.to_dict()), 201
    else:
        error = result.unwrap_err()
        return jsonify({'error': error}), 400
```

### Maybe Monad für Optional Values

```python
from utils.monads import Maybe, Some, Nothing

# ✅ RICHTIG - Maybe Monad
def find_customer_by_email(email: str) -> Maybe[Customer]:
    """
    Find customer by email.

    Returns:
        Some(customer) if found
        Nothing() if not found
    """
    customer = Customer.query.filter_by(email=email).first()
    if customer:
        return Some(customer)
    return Nothing()

# Usage
maybe_customer = find_customer_by_email("john@example.com")

# Chain operations
score = (maybe_customer
    .map(lambda c: calculate_score(c))
    .unwrap_or(0))

# Convert to Result
result = maybe_customer.to_result("Customer not found")
```

### Exception Handling (when monads aren't suitable)

```python
# ✅ Specific exceptions
try:
    customer = Customer.query.get_or_404(customer_id)
    send_email(customer.email)
except EmailError as e:
    logger.error(f"Failed to send email: {e}")
    flash("Email could not be sent", "error")
except Exception as e:
    logger.exception("Unexpected error")
    raise

# ❌ Bare except - NEVER use
try:
    do_something()
except:  # WRONG
    pass

# ❌ Silencing exceptions - AVOID
try:
    do_something()
except Exception:
    pass  # WRONG - at least log it!
```

---

## Validation & Business Rules

### Use Functional Validation

```python
from utils.validators import (
    validate_customer_data,
    validate_and_sanitize_customer,
    CustomerBusinessRules
)

# ✅ RICHTIG - Validate before database operations
@app.route('/customers/new', methods=['POST'])
def customer_create():
    form = CustomerForm()

    if form.validate_on_submit():
        # Additional business validation
        data = {
            'name': form.name.data,
            'email': form.email.data,
            'phone': form.phone.data,
            'company': form.company.data,
            'status': form.status.data,
            'notes': form.notes.data
        }

        # Functional validation with Result monad
        validation_result = validate_and_sanitize_customer(data)

        if validation_result.is_err():
            errors = validation_result.unwrap_err()
            for error in errors:
                flash(f"{error.field}: {error.message}", "error")
            return render_template('customers/form.html', form=form)

        clean_data = validation_result.unwrap()
        customer = Customer(**clean_data)
        db.session.add(customer)
        db.session.commit()

        return redirect(url_for('customer_detail', id=customer.id))

    return render_template('customers/form.html', form=form)
```

### Business Rules Enforcement

```python
# ✅ RICHTIG - Check business rules before operations
@app.route('/customers/<int:id>/delete', methods=['POST'])
def customer_delete(id):
    customer = Customer.query.get_or_404(id)

    # Check business rules
    can_delete = CustomerBusinessRules.can_delete_customer(customer)

    if can_delete.is_err():
        flash(can_delete.unwrap_err(), "error")
        return redirect(url_for('customer_detail', id=id))

    db.session.delete(customer)
    db.session.commit()
    flash("Customer deleted successfully", "success")
    return redirect(url_for('customer_list'))

# ✅ Status change validation
@app.route('/customers/<int:id>/status', methods=['POST'])
def customer_change_status(id):
    customer = Customer.query.get_or_404(id)
    new_status = request.form.get('status')

    # Validate status change
    can_change = CustomerBusinessRules.can_change_status(customer, new_status)

    if can_change.is_err():
        return jsonify({'error': can_change.unwrap_err()}), 400

    customer.status = new_status
    db.session.commit()
    return jsonify({'success': True})
```

---

## Database Operations

### Transaction Management

```python
# ✅ RICHTIG - Proper transaction handling
def create_customer_with_interaction(
    customer_data: Dict[str, Any],
    interaction_data: Dict[str, Any]
) -> Result[Customer, str]:
    """Create customer and initial interaction in one transaction."""
    try:
        # Validate both
        customer_valid = validate_customer_data(customer_data)
        if customer_valid.is_err():
            return Err("Invalid customer data")

        # Create customer
        customer = Customer(**customer_valid.unwrap())
        db.session.add(customer)
        db.session.flush()  # Get customer.id without committing

        # Create interaction
        interaction_data['customer_id'] = customer.id
        interaction = Interaction(**interaction_data)
        db.session.add(interaction)

        # Commit both together
        db.session.commit()
        return Ok(customer)

    except Exception as e:
        db.session.rollback()
        return Err(f"Transaction failed: {str(e)}")

# ❌ FALSCH - No rollback on error
def bad_create_customer(data):
    customer = Customer(**data)
    db.session.add(customer)
    db.session.commit()  # No try/except, no rollback!
```

### Query Optimization

```python
# ✅ RICHTIG - Eager loading to avoid N+1 queries
from sqlalchemy.orm import joinedload

def get_customers_with_interactions() -> List[Customer]:
    """Get customers with their interactions (optimized)."""
    return (Customer.query
        .options(joinedload(Customer.interactions))
        .all())

# ✅ Pagination for large datasets
def get_paginated_customers(
    page: int = 1,
    per_page: int = 20
) -> Dict[str, Any]:
    """Get paginated customers."""
    pagination = Customer.query.paginate(
        page=page,
        per_page=per_page,
        error_out=False
    )

    return {
        'items': [c.to_dict() for c in pagination.items],
        'total': pagination.total,
        'page': pagination.page,
        'pages': pagination.pages,
        'has_next': pagination.has_next,
        'has_prev': pagination.has_prev
    }

# ❌ FALSCH - N+1 query problem
def bad_get_customers():
    customers = Customer.query.all()
    for customer in customers:
        # This triggers a separate query for EACH customer!
        interactions = customer.interactions.all()
```

### Model Best Practices

```python
from datetime import datetime, timezone
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

# ✅ RICHTIG
class Customer(db.Model):
    """Customer model with proper practices."""

    __tablename__ = 'customers'

    # Type hints for IDE support
    id: int
    name: str
    email: str

    # Column definitions
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, index=True)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)

    # Always use timezone-aware datetimes
    created_at = db.Column(
        db.DateTime,
        default=lambda: datetime.now(timezone.utc),
        nullable=False
    )
    updated_at = db.Column(
        db.DateTime,
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
        nullable=False
    )

    # Proper relationship with cascade
    interactions = db.relationship(
        'Interaction',
        backref='customer',
        lazy='dynamic',
        cascade='all, delete-orphan'
    )

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for JSON serialization."""
        return {
            'id': self.id,
            'name': self.name,
            'email': self.email,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }

    def __repr__(self) -> str:
        """String representation for debugging."""
        return f"<Customer {self.id}: {self.name}>"
```

---

## API Endpoints

### RESTful API Standards

```python
# ✅ RICHTIG - Proper REST API design

@app.route('/api/customers', methods=['GET'])
def api_list_customers():
    """
    List customers with filtering and pagination.

    Query params:
        - status: Filter by status
        - search: Search in name/email
        - page: Page number (default 1)
        - per_page: Items per page (default 20)

    Returns:
        200: List of customers
    """
    status = request.args.get('status')
    search = request.args.get('search')
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 20, type=int)

    query = Customer.query

    if status:
        query = query.filter_by(status=status)

    if search:
        search_filter = f'%{search}%'
        query = query.filter(
            db.or_(
                Customer.name.ilike(search_filter),
                Customer.email.ilike(search_filter)
            )
        )

    pagination = query.paginate(
        page=page,
        per_page=per_page,
        error_out=False
    )

    return jsonify({
        'data': [c.to_dict() for c in pagination.items],
        'meta': {
            'total': pagination.total,
            'page': pagination.page,
            'per_page': per_page,
            'pages': pagination.pages
        }
    }), 200

@app.route('/api/customers/<int:id>', methods=['GET'])
def api_get_customer(id: int):
    """
    Get customer by ID.

    Returns:
        200: Customer data
        404: Customer not found
    """
    customer = Customer.query.get_or_404(id)
    return jsonify(customer.to_dict()), 200

@app.route('/api/customers', methods=['POST'])
def api_create_customer():
    """
    Create new customer.

    Request body:
        {
            "name": "John Doe",
            "email": "john@example.com",
            "phone": "+1234567890",  // optional
            "company": "Acme Inc",   // optional
            "status": "active"       // optional
        }

    Returns:
        201: Customer created
        400: Validation error
        409: Email already exists
    """
    data = request.get_json()

    if not data:
        return jsonify({'error': 'No data provided'}), 400

    # Use Result monad for creation
    result = create_customer(data)

    if result.is_ok():
        customer = result.unwrap()
        return jsonify(customer.to_dict()), 201
    else:
        error = result.unwrap_err()
        status_code = 409 if 'already exists' in error else 400
        return jsonify({'error': error}), status_code

@app.route('/api/customers/<int:id>', methods=['PUT'])
def api_update_customer(id: int):
    """
    Update customer.

    Returns:
        200: Customer updated
        400: Validation error
        404: Customer not found
    """
    customer = Customer.query.get_or_404(id)
    data = request.get_json()

    result = update_customer(customer, data)

    if result.is_ok():
        updated = result.unwrap()
        return jsonify(updated.to_dict()), 200
    else:
        return jsonify({'error': result.unwrap_err()}), 400

@app.route('/api/customers/<int:id>', methods=['DELETE'])
def api_delete_customer(id: int):
    """
    Delete customer.

    Returns:
        204: Customer deleted
        400: Cannot delete (business rule violation)
        404: Customer not found
    """
    customer = Customer.query.get_or_404(id)

    can_delete = CustomerBusinessRules.can_delete_customer(customer)
    if can_delete.is_err():
        return jsonify({'error': can_delete.unwrap_err()}), 400

    db.session.delete(customer)
    db.session.commit()

    return '', 204
```

### Error Response Format

```python
# ✅ Standard error response format
def error_response(message: str, status_code: int = 400, **kwargs) -> tuple:
    """Create standard error response."""
    response = {
        'error': message,
        'status_code': status_code
    }
    response.update(kwargs)
    return jsonify(response), status_code

# Usage
@app.route('/api/customers/<int:id>')
def api_get_customer(id):
    maybe_customer = find_customer_by_id(id)

    if maybe_customer.is_none():
        return error_response(
            f"Customer {id} not found",
            status_code=404
        )

    customer = maybe_customer.unwrap()
    return jsonify(customer.to_dict()), 200
```

---

## Testing Standards

### Pytest Structure

```python
# tests/test_validators.py

from utils.validators import (
    validate_customer_data,
    validate_email_format,
    ValidationError
)
from utils.monads import Ok, Err

# ✅ RICHTIG - Clear test structure
class TestEmailValidation:
    """Tests for email validation."""

    def test_valid_email_returns_ok(self):
        """Should return Ok for valid email."""
        result = validate_email_format("john@example.com")
        assert result.is_ok()
        assert result.unwrap() == "john@example.com"

    def test_invalid_email_returns_err(self):
        """Should return Err for invalid email."""
        result = validate_email_format("not-an-email")
        assert result.is_err()
        assert "Invalid email" in result.unwrap_err()

    def test_empty_email_returns_err(self):
        """Should return Err for empty email."""
        result = validate_email_format("")
        assert result.is_err()

class TestCustomerDataValidation:
    """Tests for customer data validation."""

    def test_valid_customer_data_returns_ok(self):
        """Should return Ok for valid customer data."""
        data = {
            'name': 'John Doe',
            'email': 'john@example.com',
            'phone': '+1234567890',
            'status': 'active'
        }

        result = validate_customer_data(data)
        assert result.is_ok()
        validated_data = result.unwrap()
        assert validated_data['name'] == 'John Doe'

    def test_missing_name_returns_validation_errors(self):
        """Should return validation errors for missing name."""
        data = {
            'email': 'john@example.com'
        }

        result = validate_customer_data(data)
        assert result.is_err()
        errors = result.unwrap_err()
        assert any(e.field == 'name' for e in errors)

    def test_invalid_status_returns_error(self):
        """Should return error for invalid status."""
        data = {
            'name': 'John Doe',
            'email': 'john@example.com',
            'status': 'invalid_status'
        }

        result = validate_customer_data(data)
        assert result.is_err()

# Fixtures for testing
import pytest

@pytest.fixture
def app():
    """Create app instance for testing."""
    from app import create_app
    from config import TestConfig

    app = create_app(TestConfig)

    with app.app_context():
        db.create_all()
        yield app
        db.drop_all()

@pytest.fixture
def client(app):
    """Create test client."""
    return app.test_client()

@pytest.fixture
def sample_customer(app):
    """Create sample customer for testing."""
    customer = Customer(
        name="Test User",
        email="test@example.com",
        status="active"
    )
    db.session.add(customer)
    db.session.commit()
    return customer
```

---

## Security Best Practices

### Input Validation

```python
# ✅ ALWAYS validate and sanitize input
@app.route('/api/customers', methods=['POST'])
def api_create_customer():
    data = request.get_json()

    # 1. Validate data exists
    if not data:
        return jsonify({'error': 'No data provided'}), 400

    # 2. Validate and sanitize
    result = validate_and_sanitize_customer(data)

    if result.is_err():
        return jsonify({'error': 'Validation failed'}), 400

    # 3. Use sanitized data
    clean_data = result.unwrap()
    customer = Customer(**clean_data)
    # ...

# ❌ NEVER trust user input directly
@app.route('/bad-endpoint', methods=['POST'])
def bad_endpoint():
    data = request.get_json()
    # WRONG - direct usage without validation
    customer = Customer(**data)
```

### SQL Injection Prevention

```python
# ✅ RICHTIG - Use ORM parameter binding
def search_customers(search_term: str) -> List[Customer]:
    """Search customers safely."""
    search_filter = f'%{search_term}%'
    return Customer.query.filter(
        db.or_(
            Customer.name.ilike(search_filter),
            Customer.email.ilike(search_filter)
        )
    ).all()

# ❌ FALSCH - String concatenation (SQL injection risk!)
def bad_search(search_term):
    # NEVER DO THIS
    query = f"SELECT * FROM customers WHERE name LIKE '%{search_term}%'"
    db.session.execute(query)
```

### Environment Variables for Secrets

```python
# config.py

import os
from pathlib import Path

# ✅ RICHTIG - Use environment variables
class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or os.urandom(32)
    DATABASE_URL = os.environ.get('DATABASE_URL', 'sqlite:///dev.db')
    API_KEY = os.environ.get('API_KEY')

    # Validate critical secrets
    @staticmethod
    def validate():
        if not os.environ.get('SECRET_KEY'):
            raise ValueError("SECRET_KEY must be set in production")

# ❌ FALSCH - Hardcoded secrets
class BadConfig:
    SECRET_KEY = "my-secret-key-123"  # NEVER DO THIS
    API_KEY = "sk-1234567890"         # NEVER DO THIS
```

---

## Documentation

### Docstring Standards (Google Style)

```python
# ✅ RICHTIG - Complete docstrings
def create_customer(
    data: Dict[str, Any],
    send_welcome_email: bool = True
) -> Result[Customer, str]:
    """
    Create a new customer with validation.

    This function validates customer data, checks for duplicate emails,
    creates the customer record, and optionally sends a welcome email.

    Args:
        data: Dictionary containing customer data with keys:
            - name (str): Customer's full name (required)
            - email (str): Customer's email address (required)
            - phone (str, optional): Customer's phone number
            - company (str, optional): Customer's company name
            - status (str, optional): Customer status (default: 'active')
        send_welcome_email: Whether to send welcome email after creation

    Returns:
        Result[Customer, str]: Ok(customer) if successful, Err(message) if failed

    Raises:
        ValueError: If data is None or empty

    Examples:
        >>> data = {'name': 'John Doe', 'email': 'john@example.com'}
        >>> result = create_customer(data)
        >>> if result.is_ok():
        ...     customer = result.unwrap()
        ...     print(f"Created customer: {customer.name}")

    Note:
        Email uniqueness is checked before creation. If a customer with
        the same email exists, an Err is returned.
    """
    # Implementation
    pass

# Class docstrings
class CustomerService:
    """
    Service class for customer operations.

    This class provides high-level business logic for customer management,
    including creation, updates, validation, and business rule enforcement.

    Attributes:
        cache: In-memory cache of recently accessed customers
        max_cache_size: Maximum number of customers to cache

    Example:
        >>> service = CustomerService()
        >>> result = service.create_customer(data)
        >>> if result.is_ok():
        ...     customer = result.unwrap()
    """

    def __init__(self, max_cache_size: int = 1000) -> None:
        """
        Initialize customer service.

        Args:
            max_cache_size: Maximum number of customers to cache (default: 1000)
        """
        self.cache: Dict[int, Customer] = {}
        self.max_cache_size = max_cache_size
```

---

## Project Structure

```
old_crm_updated/
├── app.py                      # Application factory and routes
├── models.py                   # SQLAlchemy models
├── config.py                   # Configuration classes
├── requirements.txt            # Python dependencies
│
├── utils/                      # Utility modules
│   ├── __init__.py
│   ├── monads.py              # Result, Maybe, Either monads
│   └── validators.py          # Validation rules and business logic
│
├── services/                   # Business logic services (optional)
│   ├── __init__.py
│   ├── customer_service.py    # Customer operations
│   └── email_service.py       # Email operations
│
├── api/                        # API routes (optional, if separating)
│   ├── __init__.py
│   ├── customers.py           # Customer API endpoints
│   └── interactions.py        # Interaction API endpoints
│
├── templates/                  # Jinja2 templates
│   ├── base.html
│   ├── index.html
│   ├── customers/
│   │   ├── list.html
│   │   ├── detail.html
│   │   └── form.html
│   └── errors/
│       ├── 404.html
│       └── 500.html
│
├── static/                     # Static files
│   ├── css/
│   ├── js/
│   └── images/
│
├── tests/                      # Test files
│   ├── __init__.py
│   ├── conftest.py            # Pytest fixtures
│   ├── test_models.py
│   ├── test_validators.py
│   ├── test_api.py
│   └── test_services.py
│
├── migrations/                 # Database migrations (Alembic)
│   └── versions/
│
├── .env                        # Environment variables (not in git!)
├── .gitignore
├── README.md
└── PYTHON_CODING_STANDARDS.md  # This file
```

---

## Summary - Quick Checklist

Before committing code, verify:

### ✅ Code Style
- [ ] PEP 8 compliant
- [ ] Proper naming conventions (snake_case, PascalCase, SCREAMING_SNAKE_CASE)
- [ ] Imports organized (stdlib, third-party, local)

### ✅ Type Safety
- [ ] All functions have type hints
- [ ] Return types specified
- [ ] Complex types use typing module

### ✅ Error Handling
- [ ] Database operations use try/except with rollback
- [ ] API operations use Result monad
- [ ] No bare except clauses
- [ ] Errors are logged

### ✅ Validation
- [ ] Input validated before database operations
- [ ] Business rules checked
- [ ] Data sanitized

### ✅ Security
- [ ] No SQL injection (using ORM)
- [ ] No hardcoded secrets
- [ ] Input validation on all endpoints
- [ ] CSRF protection enabled

### ✅ Documentation
- [ ] All public functions have docstrings
- [ ] Complex logic has inline comments
- [ ] API endpoints documented with params and returns

### ✅ Testing
- [ ] Unit tests for validators
- [ ] Integration tests for API endpoints
- [ ] Test fixtures used properly

---

**Quality > Speed. Nimm dir Zeit es richtig zu machen!**
