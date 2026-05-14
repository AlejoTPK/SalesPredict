from pydantic import ValidationError
import pytest

from app.schemas.auth import UserCreate, UserResponse
from app.schemas.sale import SaleCreate, SaleResponse


class TestUserSchemas:
    def test_user_create_valid(self, sample_user_data):
        user = UserCreate(**sample_user_data)
        assert user.email == sample_user_data["email"]
        assert user.full_name == sample_user_data["full_name"]

    def test_user_create_invalid_email(self):
        with pytest.raises(ValidationError):
            UserCreate(email="not-an-email", password="Test123!", full_name="Test User")

    def test_user_create_short_password(self):
        with pytest.raises(ValidationError):
            UserCreate(email="test@test.com", password="Ab1", full_name="Test User")

    def test_user_create_no_uppercase(self):
        with pytest.raises(ValidationError):
            UserCreate(email="test@test.com", password="test1234", full_name="Test User")

    def test_user_create_no_digit(self):
        with pytest.raises(ValidationError):
            UserCreate(email="test@test.com", password="TestTest", full_name="Test User")


class TestSaleSchemas:
    def test_sale_create_valid(self, sample_sale_data):
        sale = SaleCreate(**sample_sale_data)
        assert sale.amount == 15000.0
        assert sale.product_name == "Enterprise Suite"

    def test_sale_create_negative_amount(self):
        with pytest.raises(ValidationError):
            SaleCreate(
                amount=-100,
                quantity=1,
                product_id="p1",
                product_name="Test",
            )

    def test_sale_create_zero_quantity(self):
        with pytest.raises(ValidationError):
            SaleCreate(
                amount=100,
                quantity=0,
                product_id="p1",
                product_name="Test",
            )

    def test_sale_create_missing_required(self):
        with pytest.raises(ValidationError):
            SaleCreate(amount=100, quantity=1)  # missing product_id, product_name
