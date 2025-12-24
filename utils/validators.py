"""
Business validation rules and validators for CRM application.

This module provides functional validation using Result monads to handle
validation errors explicitly without exceptions.
"""

import re
from typing import Dict, Any, List, Callable
from dataclasses import dataclass

from .monads import Result, Ok, Err


# ============================================================================
# Validation Rule Types
# ============================================================================

@dataclass(frozen=True)
class ValidationError:
    """Represents a validation error with field and message."""
    field: str
    message: str

    def to_dict(self) -> Dict[str, str]:
        """Convert to dictionary format."""
        return {
            'field': self.field,
            'message': self.message
        }


@dataclass(frozen=True)
class ValidationRule:
    """
    A validation rule that can be applied to a value.

    Attributes:
        name: Name of the validation rule
        validator: Function that takes a value and returns Result
        error_message: Error message if validation fails
    """
    name: str
    validator: Callable[[Any], bool]
    error_message: str

    def validate(self, field: str, value: Any) -> Result[Any, ValidationError]:
        """
        Apply validation rule to a value.

        Args:
            field: Name of the field being validated
            value: Value to validate

        Returns:
            Ok(value) if valid, Err(ValidationError) if invalid
        """
        if self.validator(value):
            return Ok(value)
        return Err(ValidationError(field=field, message=self.error_message))


# ============================================================================
# Common Validation Rules
# ============================================================================

def required(value: Any) -> bool:
    """Check if value is not None and not empty."""
    if value is None:
        return False
    if isinstance(value, str):
        return bool(value.strip())
    return True


def min_length(min_len: int) -> Callable[[str], bool]:
    """Create validator for minimum string length."""
    def validator(value: str) -> bool:
        if value is None:
            return False
        return len(value.strip()) >= min_len
    return validator


def max_length(max_len: int) -> Callable[[str], bool]:
    """Create validator for maximum string length."""
    def validator(value: str) -> bool:
        if value is None:
            return True  # Optional fields can be None
        return len(value) <= max_len
    return validator


def email_format(value: str) -> bool:
    """Validate email format using regex."""
    if not value:
        return False
    # RFC 5322 simplified email regex
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return bool(re.match(pattern, value))


def phone_format(value: str) -> bool:
    """Validate phone format (flexible, allows various formats)."""
    if not value:
        return True  # Optional field
    # Remove common separators
    cleaned = re.sub(r'[\s\-\(\)\+]', '', value)
    # Check if remaining characters are digits and length is reasonable
    return cleaned.isdigit() and 7 <= len(cleaned) <= 15


def in_choices(choices: List[str]) -> Callable[[str], bool]:
    """Create validator that checks if value is in allowed choices."""
    def validator(value: str) -> bool:
        return value in choices
    return validator


def unique_in_db(model_class, field: str, exclude_id: int = None) -> Callable[[Any], bool]:
    """
    Create validator that checks uniqueness in database.

    Args:
        model_class: SQLAlchemy model class
        field: Field name to check
        exclude_id: Optional ID to exclude (for updates)

    Returns:
        Validator function
    """
    def validator(value: Any) -> bool:
        query = model_class.query.filter(getattr(model_class, field) == value)
        if exclude_id:
            query = query.filter(model_class.id != exclude_id)
        return query.first() is None
    return validator


# ============================================================================
# Predefined Validation Rules
# ============================================================================

CUSTOMER_NAME_RULES = [
    ValidationRule(
        name="required",
        validator=required,
        error_message="Name is required"
    ),
    ValidationRule(
        name="min_length",
        validator=min_length(2),
        error_message="Name must be at least 2 characters long"
    ),
    ValidationRule(
        name="max_length",
        validator=max_length(100),
        error_message="Name must not exceed 100 characters"
    ),
]

CUSTOMER_EMAIL_RULES = [
    ValidationRule(
        name="required",
        validator=required,
        error_message="Email is required"
    ),
    ValidationRule(
        name="email_format",
        validator=email_format,
        error_message="Invalid email format"
    ),
    ValidationRule(
        name="max_length",
        validator=max_length(120),
        error_message="Email must not exceed 120 characters"
    ),
]

CUSTOMER_PHONE_RULES = [
    ValidationRule(
        name="phone_format",
        validator=phone_format,
        error_message="Invalid phone format"
    ),
    ValidationRule(
        name="max_length",
        validator=max_length(20),
        error_message="Phone must not exceed 20 characters"
    ),
]

CUSTOMER_STATUS_RULES = [
    ValidationRule(
        name="valid_status",
        validator=in_choices(['active', 'inactive', 'lead']),
        error_message="Status must be one of: active, inactive, lead"
    ),
]

INTERACTION_TYPE_RULES = [
    ValidationRule(
        name="valid_type",
        validator=in_choices(['call', 'email', 'meeting', 'note']),
        error_message="Type must be one of: call, email, meeting, note"
    ),
]


# ============================================================================
# Validation Functions
# ============================================================================

def validate_field(
    field_name: str,
    value: Any,
    rules: List[ValidationRule]
) -> Result[Any, List[ValidationError]]:
    """
    Validate a single field against multiple rules.

    Args:
        field_name: Name of the field
        value: Value to validate
        rules: List of validation rules to apply

    Returns:
        Ok(value) if all rules pass, Err([ValidationError]) if any fail
    """
    errors = []

    for rule in rules:
        result = rule.validate(field_name, value)
        if result.is_err():
            errors.append(result.unwrap_err())

    if errors:
        return Err(errors)
    return Ok(value)


def validate_customer_data(data: Dict[str, Any], exclude_id: int = None) -> Result[Dict[str, Any], List[ValidationError]]:
    """
    Validate customer data against all business rules.

    Args:
        data: Dictionary with customer data
        exclude_id: Optional customer ID to exclude from uniqueness check

    Returns:
        Ok(data) if valid, Err([ValidationError]) if invalid

    Example:
        >>> data = {'name': 'John Doe', 'email': 'john@example.com'}
        >>> result = validate_customer_data(data)
        >>> if result.is_ok():
        ...     customer_data = result.unwrap()
    """
    all_errors = []

    # Validate name
    name_result = validate_field('name', data.get('name'), CUSTOMER_NAME_RULES)
    if name_result.is_err():
        all_errors.extend(name_result.unwrap_err())

    # Validate email
    email_result = validate_field('email', data.get('email'), CUSTOMER_EMAIL_RULES)
    if email_result.is_err():
        all_errors.extend(email_result.unwrap_err())

    # Validate email uniqueness (requires database check)
    email = data.get('email')
    if email:
        # This would need to be called with actual database check
        # For now, just format validation
        pass

    # Validate phone (optional)
    phone = data.get('phone')
    if phone:
        phone_result = validate_field('phone', phone, CUSTOMER_PHONE_RULES)
        if phone_result.is_err():
            all_errors.extend(phone_result.unwrap_err())

    # Validate status
    status = data.get('status', 'active')
    status_result = validate_field('status', status, CUSTOMER_STATUS_RULES)
    if status_result.is_err():
        all_errors.extend(status_result.unwrap_err())

    # Validate company (optional, just length)
    company = data.get('company')
    if company:
        company_result = validate_field(
            'company',
            company,
            [ValidationRule(
                name="max_length",
                validator=max_length(100),
                error_message="Company must not exceed 100 characters"
            )]
        )
        if company_result.is_err():
            all_errors.extend(company_result.unwrap_err())

    if all_errors:
        return Err(all_errors)
    return Ok(data)


def validate_interaction_data(data: Dict[str, Any]) -> Result[Dict[str, Any], List[ValidationError]]:
    """
    Validate interaction data against all business rules.

    Args:
        data: Dictionary with interaction data

    Returns:
        Ok(data) if valid, Err([ValidationError]) if invalid
    """
    all_errors = []

    # Validate type
    type_result = validate_field('type', data.get('type'), INTERACTION_TYPE_RULES)
    if type_result.is_err():
        all_errors.extend(type_result.unwrap_err())

    # Validate subject
    subject_rules = [
        ValidationRule(
            name="required",
            validator=required,
            error_message="Subject is required"
        ),
        ValidationRule(
            name="max_length",
            validator=max_length(200),
            error_message="Subject must not exceed 200 characters"
        ),
    ]
    subject_result = validate_field('subject', data.get('subject'), subject_rules)
    if subject_result.is_err():
        all_errors.extend(subject_result.unwrap_err())

    # Validate customer_id
    customer_id = data.get('customer_id')
    if not customer_id or not isinstance(customer_id, int):
        all_errors.append(ValidationError(
            field='customer_id',
            message='Valid customer ID is required'
        ))

    if all_errors:
        return Err(all_errors)
    return Ok(data)


def validate_email_format(email: str) -> Result[str, str]:
    """
    Simple email format validator that returns Result.

    Args:
        email: Email address to validate

    Returns:
        Ok(email) if valid, Err(message) if invalid

    Example:
        >>> validate_email_format("john@example.com")
        Ok(value='john@example.com')
        >>> validate_email_format("invalid")
        Err(error='Invalid email format')
    """
    if email_format(email):
        return Ok(email)
    return Err("Invalid email format")


# ============================================================================
# Composite Validators
# ============================================================================

def validate_and_sanitize_customer(data: Dict[str, Any]) -> Result[Dict[str, Any], List[ValidationError]]:
    """
    Validate and sanitize customer data in one operation.

    This function:
    1. Validates all fields
    2. Sanitizes string inputs (trim whitespace)
    3. Applies default values
    4. Returns clean data ready for database

    Args:
        data: Raw customer data

    Returns:
        Ok(sanitized_data) if valid, Err([ValidationError]) if invalid
    """
    # First validate
    validation_result = validate_customer_data(data)

    if validation_result.is_err():
        return validation_result

    # Sanitize and apply defaults
    sanitized = {
        'name': data.get('name', '').strip(),
        'email': data.get('email', '').strip().lower(),
        'phone': data.get('phone', '').strip() if data.get('phone') else None,
        'company': data.get('company', '').strip() if data.get('company') else None,
        'status': data.get('status', 'active'),
        'notes': data.get('notes', '').strip() if data.get('notes') else None,
    }

    return Ok(sanitized)


# ============================================================================
# Business Rules
# ============================================================================

class CustomerBusinessRules:
    """
    Business rules for customer operations.

    These go beyond simple validation and encode business logic.
    """

    @staticmethod
    def can_delete_customer(customer) -> Result[bool, str]:
        """
        Check if customer can be deleted according to business rules.

        Args:
            customer: Customer model instance

        Returns:
            Ok(True) if can delete, Err(reason) if cannot
        """
        # Business rule: Can only delete customers with no interactions
        # Or inactive customers
        if customer.interactions.count() > 0 and customer.status != 'inactive':
            return Err(
                "Cannot delete active customer with interactions. "
                "Set to inactive first or remove interactions."
            )

        return Ok(True)

    @staticmethod
    def can_change_status(customer, new_status: str) -> Result[bool, str]:
        """
        Check if customer status can be changed.

        Args:
            customer: Customer model instance
            new_status: New status to apply

        Returns:
            Ok(True) if can change, Err(reason) if cannot
        """
        # Business rule: Cannot change from lead to active without email verification
        if customer.status == 'lead' and new_status == 'active':
            if not customer.email or not email_format(customer.email):
                return Err("Cannot activate lead without valid email address")

        # Business rule: Cannot set to inactive if there are recent interactions
        if new_status == 'inactive' and customer.interactions.count() > 0:
            # Could add date check here for "recent"
            pass

        return Ok(True)

    @staticmethod
    def requires_interaction_follow_up(interaction) -> bool:
        """
        Check if interaction requires follow-up.

        Args:
            interaction: Interaction model instance

        Returns:
            True if follow-up is needed
        """
        # Business rule: Calls and meetings require follow-up
        return interaction.type in ['call', 'meeting']
