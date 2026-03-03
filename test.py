"""
Simple tests for the API
Run with: pytest test_simple.py -v
"""

import pytest
from pydantic import ValidationError
from app.schemas import UserCreate, UserResponse


def test_user_create_valid():
    user = UserCreate(name="John Doe", email="john@example.com")
    assert user.name == "John Doe"
    assert user.email == "john@example.com"
    
    print("✓ Valid user creation passed")


def test_user_create_empty_name():
    with pytest.raises(ValidationError):
        UserCreate(name="", email="john@example.com")
    print("✓ Empty name validation passed")


def test_user_create_empty_email():
    with pytest.raises(ValidationError):
        UserCreate(name="John", email="   ")
    print("✓ Empty email validation passed")


def test_user_response_valid_id():
    user = UserResponse(id=1, name="John", email="john@example.com")
    assert user.id == 1
    print("✓ Valid user response ID passed")


def test_user_response_negative_id():
    with pytest.raises(ValidationError):
        UserResponse(id=0, name="John", email="john@example.com")
    
    with pytest.raises(ValidationError):
        UserResponse(id=-1, name="John", email="john@example.com")
    print("✓ Negative ID validation passed")


def test_user_create_whitespace_trimming():
    user = UserCreate(name="  John  ", email="  john@example.com  ")
    assert user.name == "John"
    assert user.email == "john@example.com"
    print("✓ Whitespace trimming passed")


if __name__ == "__main__":
    print("\n=== Running Simple Tests ===\n")
    test_user_create_valid()
    test_user_create_empty_name()
    test_user_create_empty_email()
    test_user_response_valid_id()
    test_user_response_negative_id()
    test_user_create_whitespace_trimming()
    print("\n=== All Tests Passed ===\n")
