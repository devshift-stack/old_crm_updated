"""
Functional programming monads for better error handling and null safety.

This module provides Result, Maybe, and Either monads commonly used in functional programming
to handle errors, optional values, and computations that can fail gracefully.
"""

from typing import TypeVar, Generic, Callable, Optional, Union
from dataclasses import dataclass

T = TypeVar('T')
E = TypeVar('E')
U = TypeVar('U')


# ============================================================================
# Result Monad - For operations that can succeed or fail
# ============================================================================

@dataclass(frozen=True)
class Result(Generic[T, E]):
    """
    Result monad representing either a success (Ok) or failure (Err).

    Use this for operations that can fail and you want to handle errors explicitly
    without using exceptions.

    Examples:
        >>> result = Ok(42)
        >>> result.is_ok()
        True
        >>> result.unwrap()
        42

        >>> error = Err("Something went wrong")
        >>> error.is_err()
        True
        >>> error.unwrap_err()
        'Something went wrong'
    """

    def is_ok(self) -> bool:
        """Check if result is Ok."""
        return isinstance(self, Ok)

    def is_err(self) -> bool:
        """Check if result is Err."""
        return isinstance(self, Err)

    def map(self, fn: Callable[[T], U]) -> 'Result[U, E]':
        """
        Apply a function to the Ok value, leaving Err unchanged.

        Args:
            fn: Function to apply to Ok value

        Returns:
            New Result with transformed value or original Err
        """
        if self.is_ok():
            return Ok(fn(self.unwrap()))
        return self

    def map_err(self, fn: Callable[[E], U]) -> 'Result[T, U]':
        """
        Apply a function to the Err value, leaving Ok unchanged.

        Args:
            fn: Function to apply to Err value

        Returns:
            New Result with original Ok or transformed Err
        """
        if self.is_err():
            return Err(fn(self.unwrap_err()))
        return self

    def and_then(self, fn: Callable[[T], 'Result[U, E]']) -> 'Result[U, E]':
        """
        Chain operations that return Result (flatMap).

        Args:
            fn: Function that takes Ok value and returns a new Result

        Returns:
            Result of applying fn to Ok value, or original Err
        """
        if self.is_ok():
            return fn(self.unwrap())
        return self

    def unwrap(self) -> T:
        """
        Extract the Ok value or raise ValueError if Err.

        Returns:
            The Ok value

        Raises:
            ValueError: If Result is Err
        """
        if isinstance(self, Ok):
            return self.value
        raise ValueError(f"Called unwrap on Err: {self.error}")

    def unwrap_err(self) -> E:
        """
        Extract the Err value or raise ValueError if Ok.

        Returns:
            The Err value

        Raises:
            ValueError: If Result is Ok
        """
        if isinstance(self, Err):
            return self.error
        raise ValueError(f"Called unwrap_err on Ok: {self.value}")

    def unwrap_or(self, default: T) -> T:
        """
        Extract Ok value or return default if Err.

        Args:
            default: Default value to return if Err

        Returns:
            Ok value or default
        """
        if self.is_ok():
            return self.unwrap()
        return default

    def unwrap_or_else(self, fn: Callable[[E], T]) -> T:
        """
        Extract Ok value or compute from Err using fn.

        Args:
            fn: Function to compute default from Err value

        Returns:
            Ok value or result of fn(err)
        """
        if self.is_ok():
            return self.unwrap()
        return fn(self.unwrap_err())


@dataclass(frozen=True)
class Ok(Result[T, E]):
    """Represents a successful result."""
    value: T


@dataclass(frozen=True)
class Err(Result[T, E]):
    """Represents a failed result."""
    error: E


# ============================================================================
# Maybe Monad - For optional values (null safety)
# ============================================================================

@dataclass(frozen=True)
class Maybe(Generic[T]):
    """
    Maybe monad representing an optional value (Some or Nothing).

    Use this instead of None to make null handling explicit and type-safe.

    Examples:
        >>> maybe = Some(42)
        >>> maybe.is_some()
        True
        >>> maybe.unwrap()
        42

        >>> nothing = Nothing()
        >>> nothing.is_none()
        True
        >>> nothing.unwrap_or(0)
        0
    """

    def is_some(self) -> bool:
        """Check if value is present."""
        return isinstance(self, Some)

    def is_none(self) -> bool:
        """Check if value is absent."""
        return isinstance(self, Nothing)

    def map(self, fn: Callable[[T], U]) -> 'Maybe[U]':
        """
        Apply function to value if present.

        Args:
            fn: Function to apply to value

        Returns:
            New Maybe with transformed value or Nothing
        """
        if self.is_some():
            return Some(fn(self.unwrap()))
        return Nothing()

    def and_then(self, fn: Callable[[T], 'Maybe[U]']) -> 'Maybe[U]':
        """
        Chain operations that return Maybe (flatMap).

        Args:
            fn: Function that takes value and returns a new Maybe

        Returns:
            Result of applying fn to value, or Nothing
        """
        if self.is_some():
            return fn(self.unwrap())
        return Nothing()

    def unwrap(self) -> T:
        """
        Extract value or raise ValueError if Nothing.

        Returns:
            The contained value

        Raises:
            ValueError: If Maybe is Nothing
        """
        if isinstance(self, Some):
            return self.value
        raise ValueError("Called unwrap on Nothing")

    def unwrap_or(self, default: T) -> T:
        """
        Extract value or return default if Nothing.

        Args:
            default: Default value to return if Nothing

        Returns:
            Contained value or default
        """
        if self.is_some():
            return self.unwrap()
        return default

    def unwrap_or_else(self, fn: Callable[[], T]) -> T:
        """
        Extract value or compute default if Nothing.

        Args:
            fn: Function to compute default value

        Returns:
            Contained value or result of fn()
        """
        if self.is_some():
            return self.unwrap()
        return fn()

    def to_result(self, error: E) -> Result[T, E]:
        """
        Convert Maybe to Result, using provided error for Nothing.

        Args:
            error: Error value to use if Nothing

        Returns:
            Ok(value) if Some, Err(error) if Nothing
        """
        if self.is_some():
            return Ok(self.unwrap())
        return Err(error)


@dataclass(frozen=True)
class Some(Maybe[T]):
    """Represents a present value."""
    value: T


@dataclass(frozen=True)
class Nothing(Maybe[T]):
    """Represents an absent value."""
    pass


# ============================================================================
# Either Monad - For computations with two possible types
# ============================================================================

@dataclass(frozen=True)
class Either(Generic[T, E]):
    """
    Either monad representing a value that can be one of two types (Left or Right).

    By convention, Right is used for success/correct values and Left for errors/alternative values.

    Examples:
        >>> right = Right(42)
        >>> right.is_right()
        True
        >>> right.unwrap_right()
        42

        >>> left = Left("error")
        >>> left.is_left()
        True
        >>> left.unwrap_left()
        'error'
    """

    def is_left(self) -> bool:
        """Check if this is a Left value."""
        return isinstance(self, Left)

    def is_right(self) -> bool:
        """Check if this is a Right value."""
        return isinstance(self, Right)

    def map_right(self, fn: Callable[[E], U]) -> 'Either[T, U]':
        """
        Apply function to Right value, leaving Left unchanged.

        Args:
            fn: Function to apply to Right value

        Returns:
            New Either with transformed Right or original Left
        """
        if self.is_right():
            return Right(fn(self.unwrap_right()))
        return self

    def map_left(self, fn: Callable[[T], U]) -> 'Either[U, E]':
        """
        Apply function to Left value, leaving Right unchanged.

        Args:
            fn: Function to apply to Left value

        Returns:
            New Either with transformed Left or original Right
        """
        if self.is_left():
            return Left(fn(self.unwrap_left()))
        return self

    def unwrap_left(self) -> T:
        """
        Extract Left value or raise ValueError if Right.

        Returns:
            The Left value

        Raises:
            ValueError: If Either is Right
        """
        if isinstance(self, Left):
            return self.value
        raise ValueError(f"Called unwrap_left on Right: {self.value}")

    def unwrap_right(self) -> E:
        """
        Extract Right value or raise ValueError if Left.

        Returns:
            The Right value

        Raises:
            ValueError: If Either is Left
        """
        if isinstance(self, Right):
            return self.value
        raise ValueError(f"Called unwrap_right on Left: {self.value}")

    def to_result(self) -> Result[E, T]:
        """
        Convert Either to Result (Right becomes Ok, Left becomes Err).

        Returns:
            Ok(right) if Right, Err(left) if Left
        """
        if self.is_right():
            return Ok(self.unwrap_right())
        return Err(self.unwrap_left())


@dataclass(frozen=True)
class Left(Either[T, E]):
    """Represents the left alternative (typically error/alternative case)."""
    value: T


@dataclass(frozen=True)
class Right(Either[T, E]):
    """Represents the right alternative (typically success/correct case)."""
    value: E


# ============================================================================
# Helper functions
# ============================================================================

def safe_divide(a: float, b: float) -> Result[float, str]:
    """
    Safely divide two numbers, returning Result.

    Args:
        a: Numerator
        b: Denominator

    Returns:
        Ok(result) if successful, Err(message) if division by zero

    Example:
        >>> safe_divide(10, 2)
        Ok(value=5.0)
        >>> safe_divide(10, 0)
        Err(error='Division by zero')
    """
    if b == 0:
        return Err("Division by zero")
    return Ok(a / b)


def safe_get(dictionary: dict, key: str) -> Maybe[any]:
    """
    Safely get value from dictionary, returning Maybe.

    Args:
        dictionary: Dictionary to get value from
        key: Key to look up

    Returns:
        Some(value) if key exists, Nothing() otherwise

    Example:
        >>> safe_get({'a': 1}, 'a')
        Some(value=1)
        >>> safe_get({'a': 1}, 'b')
        Nothing()
    """
    value = dictionary.get(key)
    if value is not None:
        return Some(value)
    return Nothing()


def try_parse_int(value: str) -> Result[int, str]:
    """
    Try to parse string to int, returning Result.

    Args:
        value: String to parse

    Returns:
        Ok(int) if successful, Err(message) if parsing fails

    Example:
        >>> try_parse_int("42")
        Ok(value=42)
        >>> try_parse_int("not a number")
        Err(error='Invalid integer: not a number')
    """
    try:
        return Ok(int(value))
    except ValueError:
        return Err(f"Invalid integer: {value}")
