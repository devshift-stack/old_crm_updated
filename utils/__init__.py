"""Utility modules for functional programming patterns and helpers."""

from .monads import Result, Maybe, Either, Ok, Err, Some, Nothing, Left, Right
from .validators import ValidationRule, validate_customer_data, validate_email_format

__all__ = [
    'Result',
    'Maybe',
    'Either',
    'Ok',
    'Err',
    'Some',
    'Nothing',
    'Left',
    'Right',
    'ValidationRule',
    'validate_customer_data',
    'validate_email_format',
]
