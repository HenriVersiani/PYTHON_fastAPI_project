import pytest
from unittest.mock import MagicMock
from pydantic import ValidationError
from app.schemas import UserCreate, UserResponse
from app.repository import UserRepository
from app.models import User


# ========== FIXTURE 1: Mock Session ==========
@pytest.fixture
def mock_db():
    """
    Creates a fake database session using MagicMock.
    This lets us test without a real database!
    """
    return MagicMock()


# ========== FIXTURE 2: Sample User Data ==========
@pytest.fixture
def sample_user_data():
    return {"name": "John Doe", "email": "john@example.com"}


# ========== FIXTURE 3: Sample User Model ==========
@pytest.fixture
def sample_user_model(sample_user_data):
    user = MagicMock()
    user.id = 1
    user.name = sample_user_data["name"]
    user.email = sample_user_data["email"]
    return user

def test_create_user_with_mock(mock_db, sample_user_data): #testar criar um usuario com mock
    user_create = UserCreate(**sample_user_data)

    user_obj = User(name=user_create.name, email=user_create.email)

    mock_db.add(user_obj)
    mock_db.commit()

    user_obj.id = 1 #resposta, colocando um id
    mock_db.refresh(user_obj)

    assert mock_db.add.called
    assert mock_db.commit.called #verificar se foi chamado
    assert mock_db.refresh.called 
    
    assert user_obj.name == "John Doe"
    assert user_obj.email == "john@example.com" #ver se retornou tudo certinho
    assert user_obj.id == 1
    
    print("✓ Create user with mock passed")


def test_mock_session_calls(mock_db, sample_user_model): #ver se o mock funciona
    mock_db.add(sample_user_model)
    mock_db.commit()
    mock_db.refresh(sample_user_model)
    
    assert mock_db.add.called
    assert mock_db.commit.called
    assert mock_db.refresh.called
    print("✓ Mock session calls verified")

def test_fixture_isolation(mock_db):
    """Each test gets its own fresh mock_db (no data leaks between tests)"""
    mock_db.query.return_value.all.return_value = []
    result = mock_db.query().all()
    
    assert result == []
    print("✓ Fixture isolation passed")


# testes das validacoes dos schemas

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
    print("\n=== Running All Tests ===\n")
    
    # Schema validation tests
    test_user_create_valid()
    test_user_create_empty_name()
    test_user_create_empty_email()
    test_user_response_valid_id()
    test_user_response_negative_id()
    test_user_create_whitespace_trimming()
    
    # Mock/Fixture tests (need mocks)
    from unittest.mock import MagicMock
    mock_db = MagicMock()
    test_fixture_isolation(mock_db)
    test_create_user_with_mock(mock_db, {"name": "John Doe", "email": "john@example.com"})
    
    # Create sample user model for test_mock_session_calls
    sample_user_model = MagicMock()
    sample_user_model.id = 1
    sample_user_model.name = "John Doe"
    sample_user_model.email = "john@example.com"
    test_mock_session_calls(mock_db, sample_user_model)
    
    print("\n=== All Tests Passed ===\n")
    test_user_create_empty_name()
    test_user_create_empty_email()
    test_user_response_valid_id()
    test_user_response_negative_id()
    test_user_create_whitespace_trimming()
    print("\n=== All Tests Passed ===\n")
